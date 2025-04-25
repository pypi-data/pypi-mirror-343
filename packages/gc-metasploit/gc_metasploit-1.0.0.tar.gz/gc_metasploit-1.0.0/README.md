# Metasploit MCP Server

A Model Context Protocol (MCP) server for interacting with the Metasploit Framework.

## Features

- List exploits and payloads
- Generate payloads
- Run exploits, post modules, and auxiliary modules
- Manage sessions and listeners
- Send commands to active sessions

## Installation

```bash
pip install gc-metasploit
```

Or install with uvx:

```bash
uvx gc-metasploit
```

## Usage

Ensure Metasploit RPC is running:

```bash
msfrpcd -P your_password -S -a 127.0.0.1
```

Then start the MCP server:

```bash
# As a command-line tool:
gc-metasploit

# Or as a module:
python -m gc_metasploit.server
```

Environment variables:

- `MSF_PASSWORD`: Metasploit RPC password (default: 'yourpassword')
- `MSF_SERVER`: Metasploit RPC server (default: '127.0.0.1')
- `MSF_PORT`: Metasploit RPC port (default: '55553')
- `MSF_SSL`: Use SSL (default: 'false')
- `PAYLOAD_SAVE_DIR`: Directory to save generated payloads (default: '~/payloads')

## License

MIT 