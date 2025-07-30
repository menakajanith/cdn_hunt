CDN HUNT
CDN HUNT is a web-based tool to detect Content Delivery Networks (CDNs) used by websites. It checks for CDN indicators in HTTP headers, CNAME records, IP ranges, and ASNs. The tool supports three modes: Hostname, Website, and Subdomain check.
Features

Detects popular CDNs like Cloudflare, Amazon CloudFront, Akamai, Fastly, etc.
Supports checking single hostnames, entire websites, or common subdomains.
User-friendly web interface with loading spinner for better UX.
Displays results with IP, IP range, and CDN information.

Installation
One-Command Installation
Run the following command to automatically set up and start CDN HUNT:
curl -sL https://raw.githubusercontent.com/menakajanith/cdn_hunt/main/setup_and_run.sh | bash

This command will:

Download the necessary files.
Set up a Python virtual environment.
Install all required dependencies.
Start the Flask web server at http://localhost:5000.

Manual Installation

Clone the repository:git clone https://github.com/menakajanith/cdn_hunt.git
cd cdn_hunt


Create and activate a virtual environment:python3 -m venv venv
source venv/bin/activate


Install dependencies:pip install flask requests dnspython ipwhois beautifulsoup4 colorama tqdm


Run the application:python app.py



Usage

Open http://localhost:5000 in your browser.
Enter a domain (e.g., www.example.com).
Select a check type (Hostname, Website, or Subdomain).
Click "Detect CDN" to view results.

Dependencies

Python 3.6+
Flask
Requests
dnspython
ipwhois
beautifulsoup4
colorama
tqdm

License
MIT License
