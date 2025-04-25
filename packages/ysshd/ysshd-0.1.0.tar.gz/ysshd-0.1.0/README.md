# ysshd

yet another ssh daemon

## Features

*   Supports SSH remote forwarding (`ssh -R`).
*   Supports SSH local forwarding (`ssh -L`).
*   Authentication via standard `~/.ssh/authorized_keys`.
*   Optional password authentication using bcrypt hashes (via environment variables).
*   Configurable host, port, key paths via command-line arguments.
*   Basic interactive prompt after connection.

## Installation

```bash
# Ensure you have uv (https://github.com/astral-sh/uv)
# Install the package and its dependencies using uv
uv tool install ysshd
```

## Usage

### Running the Server

Once installed, you can run the server using the `ysshd` command:

```bash
# Run with default settings (listens on 0.0.0.0:8022)
ysshd

# Run on a different port
ysshd --port 8023

# Specify a different host key path
ysshd --server-host-key /path/to/your/host_key

# Specify a different authorized_keys file
ysshd --authorized-keys /path/to/other/authorized_keys

# Enable password authentication (requires environment variables set, see Prerequisites)
export YSSHD_ADMIN_USER="admin"
export YSSHD_ADMIN_PASSWORD="your_password_or_hash"
ysshd --enable-password-auth

# Combine options
ysshd --port 9022 --enable-password-auth
```

### Command-Line Arguments

*   `--host <ip>`: IP address to listen on (default: `0.0.0.0`).
*   `--port <number>`: Port to listen on (default: `8022`).
*   `--server-host-key <path>`: Path to the server's private host key (default: `~/.ssh/ysshd_ed25519_key`, generated if not found).
*   `--authorized-keys <path>`: Path to the authorized public keys file (default: `~/.ssh/authorized_keys`).
*   `--enable-password-auth`: Boolean flag to enable password authentication (default: `False`). Requires `YSSHD_ADMIN_USER` and `YSSHD_ADMIN_PASSWORD` environment variables to be set (see Prerequisites).
*   `--help`: Display help message and exit.

### Prerequisites

These steps are required *before* clients can connect successfully using certain authentication methods.

1.  **Public Key Authentication:**
    *   Ensure the client user has an SSH key pair (e.g., `~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub` on their machine).
    *   Add the client's **public key** (the content of `~/.ssh/id_ed25519.pub` or similar) to the `~/.ssh/authorized_keys` file on the **server** machine (the one running `ysshd`). Create the file if it doesn't exist. The default path used by `ysshd` is `~/.ssh/authorized_keys` unless overridden by `--authorized-keys`.
    *   Ensure permissions are correct on the server:
        ```bash
        chmod 700 ~/.ssh
        chmod 600 ~/.ssh/authorized_keys
        ```

2.  **Password Authentication (Optional):**
    *   To enable password authentication (which requires the `--enable-password-auth` flag when running the server), you must set the following environment variables **before** starting `ysshd`:
        *   `YSSHD_ADMIN_USER`: The username allowed to log in with a password.
        *   `YSSHD_ADMIN_PASSWORD`: This variable should contain **either**:
            *   A pre-generated bcrypt hash string (recommended for security). You can generate one using Python's `bcrypt` library or tools like `htpasswd` (ensure it outputs bcrypt format).
            *   A plain-text password. If you provide plain text, `ysshd` will hash it on startup using `bcrypt` and log the generated hash (which you should then use directly in the environment variable in the future).
        
        **Warning:** Password authentication is less secure than public key authentication and is primarily intended for development or testing purposes. It is **not recommended** for production deployments. Always prefer public key authentication for better security.

        ```bash
        # Example: Setting environment variables before running ysshd
        export YSSHD_ADMIN_USER="admin"
        export YSSHD_ADMIN_PASSWORD='$2b$12$YourPreGeneratedBcryptHashHere' # Or use plain text initially
        # Now run: ysshd --enable-password-auth ...
        ```

### Connecting with an SSH Client

Make sure the prerequisites for your chosen authentication method have been met on the server.

```bash
# Connect using public key (replace user, host, port if needed)
ssh your@server_ip -p 8022

# Connect using password (if enabled on server)
ssh admin@server_ip -p 8022
# (You will be prompted for the password)

# Set up remote forwarding (forward local port 8080 to remote port 80)
# Traffic to server_ip:8080 will be sent to localhost:80 on the client machine.
ssh your@server_ip -p 8022 -R 8080:localhost:80

# Set up local forwarding (forward local port 9000 to remote service)
# Traffic sent to localhost:9000 on the client machine will be sent
# through the SSH server to internal_service_host:80 on the server's network.
ssh your@server_ip -p 8022 -L 9000:internal_service_host:80
```