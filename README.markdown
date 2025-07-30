# CDN HUNT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

CDN HUNT is a web-based tool to detect Content Delivery Networks (CDNs) used by websites. It checks for CDN indicators in HTTP headers, CNAME records, IP ranges, and ASNs. The tool supports three modes: Hostname, Website, and Subdomain check.

## Features

- Detects popular CDNs like Cloudflare, Amazon CloudFront, Akamai, Fastly, etc.
- Supports checking single hostnames, entire websites, or common subdomains.
- User-friendly web interface with loading spinner for better UX.
- Mobile-responsive design for seamless use on smartphones and tablets.
- Displays results with IP, IP range, and CDN information.

## Installation

### One-Command Installation (Linux/macOS/Termux)

Run the following command to automatically set up and start CDN HUNT:

```bash
curl -sL https://raw.githubusercontent.com/menakajanith/cdn_hunt/main/setup_and_run.sh | bash
```

**Security Note**: Before running, review the `setup_and_run.sh` script at [https://github.com/menakajanith/cdn_hunt/blob/main/setup_and_run.sh](https://github.com/menakajanith/cdn_hunt/blob/main/setup_and_run.sh) to ensure it is safe.

This command will:
- Download the necessary files.
- Set up a Python virtual environment.
- Install all required dependencies.
- Start the Flask web server at `http://localhost:5000`.

### Termux-Specific Notes

- Ensure Python and pip are installed:
  ```bash
  pkg update && pkg upgrade
  pkg install python
  pip install --upgrade pip
  ```
- Access the web interface at `http://<your-device-ip>:5000` (use `ifconfig` to find your IP).
- If `xdg-open` is unavailable, install `termux-api` to open the browser:
  ```bash
  pkg install termux-api
  termux-open-url http://<your-device-ip>:5000
  ```
- The interface is optimized for mobile browsers, ensuring results are readable and navigable on small screens.

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/menakajanith/cdn_hunt.git
   cd cdn_hunt
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install flask requests dnspython ipwhois beautifulsoup4 colorama tqdm
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open `http://localhost:5000` (or `http://<your-device-ip>:5000` on Termux) in your browser.
2. Enter a domain (e.g., `www.example.com`).
3. Select a check type (Hostname, Website, or Subdomain).
4. Click "Detect CDN" to view results.
5. On mobile devices, the results table is scrollable, and text/buttons are optimized for touch navigation.

## Screenshots

![CDN HUNT Web Interface](https://via.placeholder.com/600x400.png?text=CDN+HUNT+Interface)
*Web interface on desktop and mobile devices*

> **Note**: Replace the placeholder image above with an actual screenshot of the tool by uploading it to the repository (e.g., `screenshots/interface.png`) and updating the URL.

## Dependencies

- Python 3.6+
- Flask
- Requests
- dnspython
- ipwhois
- beautifulsoup4
- colorama
- tqdm

## License

MIT License