import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Awaitable, Coroutine, Dict, Optional, Tuple, Union

import asyncssh
import bcrypt
import fire
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

# Define standard SSH directory path using pathlib
HOME_DIR: Path = Path.home()
SSH_DIR: Path = HOME_DIR / ".ssh"

# Use standard authorized_keys file
AUTHORIZED_KEYS_PATH: Path = SSH_DIR / "authorized_keys"
# Use a dedicated server host key within the .ssh directory
SERVER_HOST_KEY_PATH: Path = SSH_DIR / "ysshd_ed25519_key"


class YSSHServer(asyncssh.SSHServer):
    _listeners: Dict[Tuple[str, int], asyncssh.SSHForwarder]
    _enable_password_auth: bool
    _admin_user: Optional[str]
    _admin_password_hash: Optional[str]  # Store hash instead of plain password

    def __init__(
        self,
        authorized_keys_path: Path,
        enable_password_auth: bool = False,
        admin_user: Optional[str] = None,
        admin_password_hash: Optional[str] = None,  # Expect hash
    ) -> None:
        self._listeners = {}
        self.authorized_keys_path = str(authorized_keys_path)
        self._enable_password_auth = enable_password_auth
        self._admin_user = admin_user
        self._admin_password_hash = admin_password_hash  # Store the hash

    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        self._conn = conn
        peername: Any = conn.get_extra_info("peername")  # type: ignore[attr-defined]
        # Perform runtime check for safety, although get_extra_info is typed as Any
        if (
            isinstance(peername, tuple)
            and len(peername) > 0
            and isinstance(peername[0], str)
        ):
            logger.info(f"SSH connection received from {peername}")
        else:
            logger.info("SSH connection received from unknown peer")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        logger.info(f'SSH connection lost: {exc if exc else "disconnect"}')

    def public_key_auth_supported(self) -> bool:
        return True  # We want to support public key auth

    def begin_auth(self, username: str) -> bool | Awaitable[bool]:
        logger.info(f"Begin auth for user '{username}'")
        try:
            self._conn.set_authorized_keys(self.authorized_keys_path)
        except Exception as e:
            logger.error(f"Error setting authorized keys: {e}")
        return True

    # Enable/Disable password auth based on flag
    def password_auth_supported(self) -> bool:
        # Only support password auth if explicitly enabled AND credentials (user and hash) are set
        is_enabled: bool = self._enable_password_auth
        has_creds: bool = bool(self._admin_user and self._admin_password_hash)
        supported: bool = is_enabled and has_creds
        logger.debug(
            f"Password auth supported check: enabled={is_enabled}, has_creds={has_creds}, supported={supported}"
        )
        return supported

    def validate_password(
        self, username: str, password: str
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """Handle password authentication attempts using bcrypt."""
        logger.info(f"Password authentication attempt for user '{username}'")

        # Ensure we have credentials configured for comparison
        if not self._admin_user or not self._admin_password_hash:
            logger.error(
                "Password auth attempted, but admin user or password hash is not configured on the server."
            )
            return False

        if username == self._admin_user:
            try:
                # Encode provided password and stored hash to bytes for bcrypt
                password_bytes = password.encode("utf-8")
                logger.debug(f"Password bytes: {password_bytes}")
                hash_bytes = self._admin_password_hash.encode("utf-8")
                logger.debug(f"Hash bytes: {hash_bytes}")

                # Check password against stored hash
                if bcrypt.checkpw(password_bytes, hash_bytes):
                    logger.info(
                        f"Password authentication successful for user '{username}'"
                    )
                    return True
                else:
                    logger.warning(
                        f"Password authentication failed for user '{username}' (incorrect password)"
                    )
                    return False
            except ValueError:
                logger.warning(
                    f"Password check failed for user '{username}' due to invalid hash format stored on server."
                )
                return False
            except Exception as e:
                # Log unexpected errors during bcrypt check
                logger.error(f"Error during password check for user '{username}': {e}")
                return False
        else:
            logger.warning(
                f"Password authentication failed for user '{username}' (incorrect username)"
            )
            return False

    def server_requested(
        self, listen_host: str, listen_port: int
    ) -> Union[bool, Awaitable[bool]]:
        """Handle remote forwarding listener requests (ssh -R)."""
        # Note: The actual forwarding channel handling happens later when a
        # connection comes *to* the listener.
        # This method just approves setting up the listener.
        logger.info(
            f"Remote forward listener requested on server at {listen_host}:{listen_port}"
        )
        # Returning True allows asyncssh to set up the listener.
        # We don't need to manage the listener object here directly.
        return True

    def connection_requested(
        self, dest_host: str, dest_port: int, orig_host: str, orig_port: int
    ) -> Union[bool, Awaitable[bool]]:
        """Handle direct TCP/IP connection requests (local forwarding - ssh -L)."""
        logger.info(
            f"Local forward connection requested to {dest_host}:{dest_port} from client {orig_host}:{orig_port}"
        )
        # Returning True allows asyncssh to establish the connection.
        return True


async def handle_client(process: asyncssh.SSHServerProcess) -> None:
    """Handle client connection after authentication for a 'session'."""
    logger.info(
        f"Client session started for user {process.get_extra_info('username', 'unknown')}"
    )

    process.stdout.write("Welcome! This is a limited interaction point.\n")
    process.stdout.write('Type "exit" or press Ctrl+D to disconnect.\n')

    try:
        while True:
            process.stdout.write("> ")
            try:
                # Read a line of input, waiting if necessary
                # Use readline() for interactive input and EOF detection
                logger.debug("Waiting for stdin.readline()...")
                line = await process.stdin.readline()
                logger.debug(
                    f"stdin.readline() returned: {line!r}"
                )  # Log the raw return value

                is_eof = process.stdin.at_eof()
                logger.debug(f"stdin.at_eof() returned: {is_eof}")

                # Check for EOF flag OR empty string from readline (indicates Ctrl+D)
                if is_eof or line == "":
                    # Make sure we log the actual reason
                    reason = (
                        "EOF flag set" if is_eof else "empty line received (Ctrl+D)"
                    )
                    logger.info(f"Disconnecting client because: {reason}.")
                    process.stdout.write("\nDisconnecting due to EOF.\n")
                    break  # Exit loop on EOF or empty line

                # Strip whitespace and convert to lowercase for comparison
                command = line.strip().lower()
                logger.debug(f"Received command: '{command}'")

                if command == "exit":
                    logger.info("Client typed 'exit'.")
                    process.stdout.write("Disconnecting as requested.\n")
                    break  # Exit loop on "exit" command
                else:
                    # Handle other commands (optional - currently does nothing)
                    if command:
                        process.stdout.write(f"Command not recognized: {command}\n")

            except asyncssh.misc.TerminalSizeChanged:
                # Handle terminal resize events if necessary (optional)
                pass
            except asyncssh.misc.BreakReceived:
                # Handle break signal (Ctrl+C) if necessary (optional)
                process.stdout.write(
                    '\nCtrl+C received. Type "exit" or Ctrl+D to disconnect.\n'
                )
            except Exception as exc:
                logger.error(f"Error reading from client stdin: {exc}")
                process.stderr.write(f"Server error: {exc}\n")
                break  # Exit loop on other errors

    except Exception as exc:
        logger.error(f"Error in handle_client session loop: {exc}")
    finally:
        logger.info(
            f"Client session ended for user {process.get_extra_info('username', 'unknown')}"
        )
        process.exit(0)  # Ensure the process exits cleanly


async def start_server(
    host: str = "0.0.0.0",
    port: int = 8022,
    # Use Path type hint for paths
    server_host_key: Path = SERVER_HOST_KEY_PATH,
    authorized_keys: Path = AUTHORIZED_KEYS_PATH,
    # Add flag to enable password auth
    enable_password_auth: bool = False,
) -> None:
    """Starts the SSH server."""

    # Read admin credentials from environment variables if password auth is enabled
    admin_user: Optional[str] = None
    admin_password_hash: Optional[str] = None  # Store hash
    if enable_password_auth:
        admin_user = os.environ.get("YSSHD_ADMIN_USER")
        raw_password = os.environ.get("YSSHD_ADMIN_PASSWORD")  # Get raw value

        if not admin_user or not raw_password:
            logger.warning(
                "Password authentication enabled, but YSSHD_ADMIN_USER or YSSHD_ADMIN_PASSWORD environment variables not set. Password auth will fail."
            )
        else:
            logger.info(
                f"Password authentication enabled for admin user: '{admin_user}'"
            )
            # Check if the raw_password looks like a bcrypt hash
            if (
                raw_password.startswith("$2b$")
                or raw_password.startswith("$2a$")
                or raw_password.startswith("$2y$")
            ):
                logger.debug("Using existing bcrypt hash from YSSHD_ADMIN_PASSWORD.")
                admin_password_hash = raw_password
            else:
                # If not a hash, assume it's plain text, hash it, and warn the user
                logger.warning(
                    "YSSHD_ADMIN_PASSWORD environment variable does not contain a bcrypt hash. "
                    "Hashing it now. For production, store the generated hash directly in the environment variable."
                )
                try:
                    # Generate salt and hash the password
                    password_bytes = raw_password.encode("utf-8")
                    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
                    admin_password_hash = hashed_bytes.decode(
                        "utf-8"
                    )  # Store hash as string
                    logger.info(
                        f"Generated bcrypt hash for admin user: {admin_password_hash}"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to hash password from YSSHD_ADMIN_PASSWORD: {e}. Password auth will fail."
                    )
                    admin_password_hash = None  # Ensure it's None if hashing fails

    # Ensure the .ssh directory exists with correct permissions
    try:
        SSH_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
        logger.debug(f"Ensured SSH directory exists: {SSH_DIR}")
    except OSError as e:
        logger.error(f"Could not create SSH directory {SSH_DIR}: {e}")
        sys.exit(1)

    # Generate server key if it doesn't exist
    server_host_key_used: Path = (
        server_host_key  # Use the argument passed (defaults to global)
    )
    if not server_host_key_used.exists():
        logger.info(f"Generating new server host key: {server_host_key_used}")
        try:
            key: asyncssh.SSHKey = asyncssh.generate_private_key("ssh-ed25519")
            # write_private_key accepts Path objects
            key.write_private_key(server_host_key_used)
            logger.info("Server host key generated and saved.")
        except (OSError, asyncssh.Error) as e:
            logger.error(
                f"Failed to generate or write server host key {server_host_key_used}: {e}"
            )
            sys.exit(1)
    else:
        logger.info(f"Loading server host key from: {server_host_key_used}")

    # Use the authorized_keys path passed as argument (defaults to global)
    authorized_keys_used: Path = authorized_keys

    logger.info(f"Starting SSH server on {host}:{port}")
    logger.info(f"Using authorized keys file: {authorized_keys_used}")
    logger.info(f"Using server host key: {server_host_key_used}")

    try:
        server = await asyncssh.create_server(
            # Pass config to server instance
            lambda: YSSHServer(
                authorized_keys_used,
                enable_password_auth=enable_password_auth,
                admin_user=admin_user,
                admin_password_hash=admin_password_hash,  # Pass the hash
            ),
            host,
            port,
            server_host_keys=[server_host_key_used],
            # Define agent forwarding if needed (set to False for now)
            agent_forwarding=False,
            process_factory=handle_client,  # Enable process factory
        )
        logger.info(f"Server started and listening on {server.get_port()}")
    except (OSError, asyncssh.Error) as exc:
        logger.error(f"Error starting server: {exc}")
        sys.exit(1)  # Exit with non-zero status on error

    # Keep the server running forever
    await asyncio.Future()  # Use asyncio.Future() for an indefinitely pending future


def main(
    host: str = "0.0.0.0",
    port: int = 8022,
    # Accept string from fire, convert to Path for start_server
    server_host_key: str = str(SERVER_HOST_KEY_PATH),
    authorized_keys: str = str(AUTHORIZED_KEYS_PATH),
    # Add command line flag for password auth
    enable_password_auth: bool = False,
) -> None:
    """Synchronous wrapper to start the SSH server, designed to be called by Fire."""
    # This function takes the same arguments as start_server
    # Fire will populate these arguments from the command line.
    # Convert string paths from fire back to Path objects for internal use
    server_host_key_path = Path(server_host_key)
    authorized_keys_path = Path(authorized_keys)

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    try:
        # Call the async start_server with the arguments received by main
        loop.run_until_complete(
            start_server(
                host=host,
                port=port,
                server_host_key=server_host_key_path,
                authorized_keys=authorized_keys_path,
                # Pass the flag down
                enable_password_auth=enable_password_auth,
            )
        )
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        if not loop.is_closed():
            loop.close()
        logger.info("Server stopped.")


def cli() -> None:
    """Command Line Interface entry point that uses fire to wrap main."""
    fire.Fire(main)


if __name__ == "__main__":
    # This allows running the script directly for testing
    # Use fire.Fire to map command-line arguments to the main function's parameters
    # main then passes these to start_server
    # fire.Fire(main)
    cli()  # Call the CLI entry point
