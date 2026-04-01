# Moonveil

A Flask-based web application for managing bug bounty reconnaissance targets and attack surface management (ASM). Moonveil helps security researchers organize and track their reconnaissance workflows, including domains, subdomains, ASNs, IP ranges, and discovered assets.

> **Note**: This is version 1 of Moonveil, maintained as a stable release. A complete rewrite (v2) with graph database and LLM-powered analysis is in development.

## Features

- **Target Management**: Organize bug bounty programs with defined scopes
- **Asset Discovery**:
  - Subdomain enumeration (subfinder)
  - DNS resolution (dnsx)
  - HTTP probing (httpx)
  - Subdomain permutations (alterx)
  - DNS bruteforcing (shuffledns)
- **Attack Surface Monitoring**: Track changes in discovered assets over time
- **Archive Collection**: Gather historical data via Wayback Machine
- **Web Interface**: Clean UI for managing targets and viewing results
- **Docker Support**: Containerized deployment with all tools included

## Tech Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.23
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript, Custom CSS
- **External Tools**: subfinder, httpx, dnsx, alterx, shuffledns, waybackurls, massdns

## Prerequisites

- Docker and Docker Compose (recommended)
- **OR** Python 3.9+ and Go 1.24+ (for local installation)

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/r0s4s/moonveil.git
   cd moonveil
   ```

2. **Build and run**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Open your browser to `http://127.0.0.1:8889/`

That's it! The Docker container includes all required tools and dependencies.

## Usage

### Creating a Target
1. Navigate to the home page
2. Click "Add Target"
3. Enter target name and scope (comma-separated domains)
4. Optionally specify the bug bounty program name

### Running Asset Discovery
1. Select a target from the list
2. Click on the target to view the ASM (Attack Surface Management) page
3. Use the available tools:
   - **Enumeration**: Discover subdomains using passive sources
   - **Permutations**: Generate subdomain permutations
   - **Bruteforce**: DNS bruteforce with wordlists
   - **Probing**: Check which subdomains are alive (HTTP/HTTPS)
   - **Archives**: Collect historical URLs from Wayback Machine

### Monitoring Changes
Enable "Monitoring" when running scans to track new assets discovered between scans.

## Project Structure

```
moonveil/
├── core/               # Core application logic
│   ├── app.py         # Flask application factory
│   ├── database.py    # Database operations
│   ├── file.py        # File handling
│   └── shell.py       # External tool execution
├── models/            # SQLAlchemy database models
│   ├── target.py
│   ├── domain.py
│   ├── subdomain.py
│   ├── asn.py
│   ├── range.py
│   └── archive.py
├── routes/            # Flask blueprints
│   ├── target.py
│   ├── asm.py
│   └── search.py
├── static/            # CSS, JS, images
├── templates/         # HTML templates
├── config/            # Configuration files
│   ├── resolvers.txt  # DNS resolvers
│   └── wordlist.txt   # DNS bruteforce wordlist
├── data/              # SQLite database and target data
├── Dockerfile
├── docker-compose.yml
└── run.py             # Application entry point
```

## Configuration

Edit `config.ini` to customize:
- Database location
- Server host/port
- Secret key for sessions
- External tool paths

## CLI Commands

```bash
# Initialize/reset database
flask init-db

# Update external tools (subfinder, httpx, etc.)
flask update-tools
```

## Docker Services

The `docker-compose.yml` includes:
- **App Container**: Flask application with Python environment
- **Go Tools Container**: All Go-based reconnaissance tools pre-installed

## Security and Ethical Use

**IMPORTANT**: This tool is designed for authorized security testing only.

- Only use on targets where you have explicit permission
- Respect bug bounty program scopes
- Follow responsible disclosure practices
- Ensure you have authorization before scanning any target

Unauthorized scanning may be illegal in your jurisdiction.

## Development

### Database Schema
- **Target**: Main entity (name, scope, program)
- **Domain**: Root domains in scope
- **Subdomain**: Discovered subdomains with HTTP metadata
- **ASN**: Autonomous System Numbers
- **Range**: IP address ranges
- **Archive**: Historical URLs from Wayback Machine

All entities cascade delete with their parent Target.

## Troubleshooting

### Docker build fails
- **Go version error**: The Dockerfile uses Go 1.24. If builds fail, ensure you're using the latest Dockerfile.
- **Network issues**: Some tools require internet access to download. Check your network connection.

### Local installation issues
- **Tools not found**: Ensure `$GOPATH/bin` is in your `$PATH`
- **Database errors**: Run `flask init-db` to reset the database

### Performance
- Large scans may take time. Consider adjusting timeout values in `config.ini`
- For better performance, increase thread counts in scan operations

## Status

Stable v1 release. Actively maintained.

## Contributing

This repository contains the stable v1 release. For bug fixes and improvements to v1, feel free to open issues or pull requests.

## License

This project is provided as-is for educational and authorized security testing purposes.

## Acknowledgments

Built with these excellent open-source tools:
- [ProjectDiscovery](https://github.com/projectdiscovery) (subfinder, httpx, dnsx, alterx, shuffledns)
- [tomnomnom](https://github.com/tomnomnom) (waybackurls)
- [blechschmidt](https://github.com/blechschmidt) (massdns)
- [Flask](https://flask.palletsprojects.com/)

---
