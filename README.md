CDN HUNT
CDN HUNT is a web-based tool to detect Content Delivery Networks (CDNs) used by websites. It checks for CDN indicators in HTTP headers, CNAME records, IP ranges, and ASNs. The tool supports three modes: Hostname, Website, and Subdomain check.
Features

Detects popular CDNs like Cloudflare, Amazon CloudFront, Akamai, Fastly, etc.
Supports checking single hostnames, entire websites, or common subdomains.
User-friendly web interface with loading spinner for better UX.
Mobile-responsive design for seamless use on smartphones and tablets.
Displays results with IP, IP range, and CDN information.

Installation
One-Command Installation (Linux/macOS/Termux)
Run the following command to automatically set up and start CDN HUNT:
curl -sL https://raw.githubusercontent.com/menakajanith/cdn_hunt/main/setup_and_run.sh | bash

Security Note: Before running, review the setup_and_run.sh script at https://github.com/menakajanith/cdn_hunt/blob/main/setup_and_run.sh to ensure it is safe.
This command will:

Download the necessary files.
Set up a Python virtual environment.
Install all required dependencies.
Start the Flask web server at http://localhost:5000.

Termux-Specific Notes

Ensure Python and pip are installed:pkg update && pkg upgrade
pkg install python
pip install --upgrade pip


Access the web interface at http://<your-device-ip>:5000 (use ifconfig to find your IP).
If xdg-open is unavailable, install termux-api to open the browser:pkg install termux-api
termux-open-url http://<your-device-ip>:5000


The interface is optimized for mobile browsers, ensuring results are readable and navigable on small screens.

Manual Installation

Clone the repository:git clone https://github.com/menakajanith/cdn_hunt.git
cd cdn_hunt


Create and activate a virtual environment:python3 -m venv venv
source venv/bin/activate


Install dependencies:pip install flask requests dnspython ipwhois beautifulsoup4 colorama tqdm


Run the application:python app.py



Usage

Open http://localhost:5000 (or http://<your-device-ip>:5000 on Termux) in your browser.
Enter a domain (e.g., www.example.com).
Select a check type (Hostname, Website, or Subdomain).
Click "Detect CDN" to view results.
On mobile devices, the results table is scrollable and text/buttons are optimized for touch navigation.

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
