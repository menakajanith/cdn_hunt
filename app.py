from flask import Flask, request, render_template, jsonify
import requests
import dns.resolver
import ipaddress
import socket
from urllib.parse import urlparse
from ipwhois import IPWhois
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import json
import os

app = Flask(__name__)

init(autoreset=True)

CDN_INDICATORS = {
    "Cloudflare": {
        "headers": ["Server: cloudflare", "cf-ray", "CF-Cache-Status"],
        "cname_patterns": [".cloudflare.com", ".cloudflarestorage.com"],
        "asn": ["AS13335"]
    },
    "Amazon CloudFront": {
        "headers": ["X-Amz-Cf-Id", "X-Cache: Hit from cloudfront"],
        "cname_patterns": [".cloudfront.net"],
        "asn": ["AS16509"]
    },
    "Azure Front Door": {
        "headers": ["X-Azure-FD"],
        "cname_patterns": [".azurefd.net"],
        "asn": ["AS8075"]
    },
    "Akamai": {
        "headers": ["X-Akamai-Request-ID", "Edge-Control"],
        "cname_patterns": [".edgekey.net", ".akamai.net"],
        "asn": ["AS16625", "AS20940"]
    },
    "Fastly": {
        "headers": ["X-Fastly-Request-ID", "Vary: Fastly-SSL"],
        "cname_patterns": [".fastly.net", ".fastlylb.net"],
        "asn": ["AS54113"]
    },
    "Incapsula": {
        "headers": ["X-CDN: Incapsula"],
        "cname_patterns": [".incapdns.net"],
        "asn": ["AS19551"]
    },
    "Sucuri": {
        "headers": ["X-Sucuri-ID"],
        "cname_patterns": [".sucuri.net"],
        "asn": ["AS30148"]
    },
    "Facebook": {
        "headers": ["X-FB-Debug", "X-FB-Content"],
        "cname_patterns": [".fbcdn.net"],
        "asn": ["AS32934"]
    },
    "Google": {
        "headers": ["Server: gws", "X-GFE-SSL"],
        "cname_patterns": [".google.com", ".googletagmanager.com", ".gstatic.com"],
        "asn": ["AS15169"]
    }
}

COMMON_SUBDOMAINS = ["www", "m", "media", "cdn", "api", "st1", "marketplace", "marketplacefront"]

def load_ip_ranges():
    ip_ranges_file = "ip_ranges.json"
    ip_ranges = {}
    if os.path.exists(ip_ranges_file):
        try:
            with open(ip_ranges_file, 'r') as f:
                ip_ranges = json.load(f)
                print(f"{Fore.CYAN}Loaded IP ranges from local file: {ip_ranges_file}{Style.RESET_ALL}")
                return ip_ranges
        except Exception as e:
            print(f"{Fore.RED}Error loading IP ranges from local file: {e}{Style.RESET_ALL}")

    try:
        response_v4 = requests.get("https://www.cloudflare.com/ips-v4", timeout=5)
        response_v6 = requests.get("https://www.cloudflare.com/ips-v6", timeout=5)
        ip_ranges["Cloudflare"] = response_v4.text.strip().split("\n") + response_v6.text.strip().split("\n")
    except:
        ip_ranges["Cloudflare"] = [
            "104.16.0.0/12", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
            "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
            "173.245.48.0/20", "162.158.0.0/15", "172.64.0.0/13", "131.0.72.0/22",
            "2400:cb00::/32", "2606:4700::/32", "2803:f800::/32", "2405:b500::/32",
            "2405:8100::/32", "2a06:98c0::/29", "2c0f:f248::/32"
        ]
        print(f"{Fore.YELLOW}Using fallback Cloudflare IP ranges{Style.RESET_ALL}")

    try:
        response = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json", timeout=5)
        data = response.json()
        ip_ranges["Amazon CloudFront"] = [prefix["ip_prefix"] for prefix in data["prefixes"] if prefix["service"] == "CLOUDFRONT"]
        ip_ranges["Amazon CloudFront"] += [prefix["ipv6_prefix"] for prefix in data["ipv6_prefixes"] if prefix["service"] == "CLOUDFRONT"]
    except:
        ip_ranges["Amazon CloudFront"] = ["52.84.0.0/15", "13.32.0.0/15"]
        print(f"{Fore.YELLOW}Using fallback Amazon CloudFront IP ranges{Style.RESET_ALL}")

    try:
        response = requests.get("https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20250722.json", timeout=5)
        data = response.json()
        azure_ranges = []
        for service in data["values"]:
            if "AzureFrontDoor" in service["name"]:
                azure_ranges.extend(service["properties"]["addressPrefixes"])
        ip_ranges["Azure Front Door"] = azure_ranges if azure_ranges else ["20.0.0.0/8"]
    except:
        ip_ranges["Azure Front Door"] = ["20.0.0.0/8"]
        print(f"{Fore.YELLOW}Using fallback Azure Front Door IP ranges{Style.RESET_ALL}")

    try:
        response = requests.get("https://www.gstatic.com/ipranges/goog.json", timeout=5)
        data = response.json()
        ip_ranges["Google"] = [prefix["ipv4Prefix"] for prefix in data["prefixes"] if "ipv4Prefix" in prefix]
        ip_ranges["Google"] += [prefix["ipv6Prefix"] for prefix in data["prefixes"] if "ipv6Prefix" in prefix]
    except:
        ip_ranges["Google"] = ["172.217.0.0/16", "142.250.0.0/15", "64.233.160.0/19"]
        print(f"{Fore.YELLOW}Using fallback Google IP ranges{Style.RESET_ALL}")

    try:
        response = requests.get("https://api.fastly.com/public-ip-list", timeout=5)
        data = response.json()
        ip_ranges["Fastly"] = data["addresses"] + data["ipv6_addresses"]
    except:
        ip_ranges["Fastly"] = ["151.101.0.0/16", "2a04:4e42::/32"]
        print(f"{Fore.YELLOW}Using fallback Fastly IP ranges{Style.RESET_ALL}")

    ip_ranges["Akamai"] = [
        "23.32.0.0/11", "23.64.0.0/14", "23.192.0.0/11", "2a02:26f0::/29",
        "104.64.0.0/10", "184.24.0.0/13", "184.50.0.0/15", "184.84.0.0/14"
    ]

    try:
        with open(ip_ranges_file, 'w') as f:
            json.dump(ip_ranges, f)
        print(f"{Fore.CYAN}Saved IP ranges to local file: {ip_ranges_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving IP ranges to local file: {e}{Style.RESET_ALL}")

    return ip_ranges

IP_RANGES = load_ip_ranges()

def get_http_headers(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if not response.headers:
            response = requests.get(url, timeout=5, allow_redirects=True)
        return response.headers
    except requests.RequestException:
        return {}

def check_headers_for_cdn(headers):
    for cdn, indicators in CDN_INDICATORS.items():
        for header in indicators["headers"]:
            for key, value in headers.items():
                if header.lower() in key.lower() or header.lower() in str(value).lower():
                    return cdn
    return "unknown"

def get_cname(domain):
    try:
        answers = dns.resolver.resolve(domain, "CNAME")
        return [rdata.target.to_text() for rdata in answers]
    except:
        return []

def check_cname_for_cdn(cnames):
    for cdn, indicators in CDN_INDICATORS.items():
        for cname in cnames:
            for pattern in indicators["cname_patterns"]:
                if pattern in cname:
                    return cdn
    return "unknown"

def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def check_ip_for_cdn(ip):
    if not ip:
        return "unknown", None
    try:
        ip_addr = ipaddress.ip_address(ip)
        for cdn, ip_ranges in IP_RANGES.items():
            for ip_range in ip_ranges:
                try:
                    if ip_addr in ipaddress.ip_network(ip_range):
                        print(f"{Fore.GREEN}IP {ip} matched to {cdn} with range {ip_range}{Style.RESET_ALL}")
                        return cdn, ip_range
                except ValueError:
                    print(f"{Fore.YELLOW}Invalid IP range {ip_range} for {cdn}{Style.RESET_ALL}")
                    continue
        print(f"{Fore.YELLOW}No match for IP {ip}{Style.RESET_ALL}")
        return "unknown", None
    except:
        print(f"{Fore.RED}Error processing IP {ip}{Style.RESET_ALL}")
        return "unknown", None

def check_asn_for_cdn(ip):
    if not ip:
        return "unknown"
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        asn = results.get("asn", "unknown")
        for cdn, indicators in CDN_INDICATORS.items():
            if asn in indicators["asn"]:
                return cdn
        if asn == "AS16509":
            print(f"{Fore.YELLOW}Warning: ASN AS16509 detected for {ip}, likely AWS infrastructure but not necessarily a CDN{Style.RESET_ALL}")
        return "unknown"
    except:
        return "unknown"

def get_dynamic_count(domain):
    count = 0
    for _ in range(20):
        try:
            response = requests.head(f"https://{domain}", timeout=1)
            if response.status_code == 200:
                count += 1
        except:
            continue
    return count if count > 0 else 1

def discover_cdn_domains(url):
    try:
        response = requests.get(url, timeout=5)
        if "text/html" not in response.headers.get("Content-Type", ""):
            print(f"{Fore.YELLOW}Warning: {url} is a non-HTML resource{Style.RESET_ALL}")
            return [urlparse(url).hostname]
        soup = BeautifulSoup(response.text, 'html.parser')
        domains = set()
        for tag in soup.find_all(['script', 'img', 'link', 'iframe', 'source', 'video']):
            for attr in ['src', 'href', 'data-src']:
                resource_url = tag.get(attr)
                if resource_url:
                    parsed = urlparse(resource_url)
                    if parsed.hostname:
                        domains.add(parsed.hostname)
        for script in soup.find_all('script'):
            if script.string:
                for line in script.string.split('\n'):
                    if 'http' in line:
                        try:
                            parsed = urlparse(line.strip())
                            if parsed.hostname:
                                domains.add(parsed.hostname)
                        except:
                            continue
        return list(domains)
    except Exception as e:
        print(f"{Fore.RED}Error discovering CDN domains: {e}{Style.RESET_ALL}")
        return [urlparse(url).hostname]

def detect_cdn(domain, option="Hostname"):
    results = []
    parsed = urlparse(domain)
    base_domain = parsed.hostname or domain

    if option == "Website":
        print(f"{Fore.CYAN}Discovering CDN domains for {base_domain}...{Style.RESET_ALL}")
        domains_to_check = discover_cdn_domains(f"https://{base_domain}")
        print(f"{Fore.CYAN}Discovered domains: {domains_to_check}{Style.RESET_ALL}")
    elif option == "Subdomain":
        print(f"{Fore.CYAN}Checking subdomains for {base_domain}...{Style.RESET_ALL}")
        domains_to_check = [f"{sub}.{base_domain}" for sub in COMMON_SUBDOMAINS]
        print(f"{Fore.CYAN}Subdomains to check: {domains_to_check}{Style.RESET_ALL}")
    else:
        domains_to_check = [base_domain]

    for domain in domains_to_check:
        count = get_dynamic_count(domain)
        headers = get_http_headers(f"https://{domain}")
        cdn_headers = check_headers_for_cdn(headers)
        cnames = get_cname(domain)
        cdn_cname = check_cname_for_cdn(cnames)
        ip = get_ip_address(domain)
        cdn_ip, matched_ip_range = check_ip_for_cdn(ip)
        cdn_asn = check_asn_for_cdn(ip)

        cdn = cdn_ip if cdn_ip != "unknown" else cdn_headers if cdn_headers != "unknown" else cdn_cname if cdn_cname != "unknown" else cdn_asn

        results.append({
            "hostname": domain,
            "cdn": cdn,
            "ip": ip if ip else "N/A",
            "count": count,
            "ip_range": matched_ip_range if matched_ip_range else "N/A"
        })
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    domain = request.form.get('domain')
    option = request.form.get('option', 'Hostname')
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
    results = detect_cdn(domain, option)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
