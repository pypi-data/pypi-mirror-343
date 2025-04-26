# -------------------------------
# Module Imports
# -------------------------------
import os
import dns.resolver
import json
import requests
import dkim
import re
import ipaddress
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from datetime import timezone, timedelta
from email_auth_checker.reports import generate_html_report, generate_pdf_report, generate_txt_report


# -------------------------------
# Helper Functions
# -------------------------------

# Check Sender Legitimacy
# -------------------------------
def parse_authentication_results(header_value):
    results = {
        "spf": {"status": "missing", "value": None},
        "dkim": {"status": "missing", "value": None},
        "dmarc": {"status": "missing", "value": None}
    }
    if not header_value:
        return results

    # Capture all auth blocks
    auth_blocks = re.findall(r"(spf|dkim|dmarc)=([\w]+)\s*(\([^)]*\))?([^;]*)", header_value, re.IGNORECASE)
    values = {"spf": [], "dkim": [], "dmarc": []}
    for key, status, parens, rest in auth_blocks:
        key = key.lower()
        value = ((parens or "") + (rest or "")).strip()
        if results[key]["status"] == "missing":
            results[key]["status"] = status.lower()
        values[key].append(value)
    for key in results:
        if values[key]:
            results[key]["value"] = ", ".join(values[key])
    return results

def check_sender_legitimacy(eml_path):
    try:
        # Parse the email
        with open(eml_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        #Extract header and body
        headers = {k: v for k, v in msg.items()}
        if msg.is_multipart():
            parts = [p.get_content() for p in msg.walk() if p.get_content_type()=='text/plain']
            body = "\n".join(parts).strip()
        else:
            body = msg.get_content().strip()
        
        # Extract sender email
        sender_email = msg['From']
        if not sender_email:
            return {"error": "No 'From' field in email"}

        if '<' in sender_email:
            sender_email = sender_email.split('<')[1].split('>')[0]
        domain = sender_email.split('@')[-1]

        # Extract receiver email
        receiver_email = msg['To']
        if not receiver_email:
            return {"error": "No 'To' field in email"}

        # Check if domain has MX records
        try:
            dns.resolver.resolve(domain, 'MX')
            mx_valid = True
        except Exception:
            mx_valid = False

        # Grab Authentication-Results header
        auth_header = msg['Authentication-Results']
        auth_results = parse_authentication_results(auth_header)

        # Extract 'Received' headers
        received_headers = msg.get_all('Received', [])
        received_date = None
        received_time = None

        # Try to extract the datetime from the last (closest to sender) received header
        if received_headers:
            for header in reversed(received_headers):
                # Find the date string at the end of the header
                match = re.search(r';\s*(.+)$', header)
                if match:
                    try:
                        received_datetime = parsedate_to_datetime(match.group(1).strip())
                        # If the datetime is naive or in a different timezone, convert to IST (UTC+5:30)
                        ist_offset = timedelta(hours=5, minutes=30)
                        ist = timezone(ist_offset)
                        received_datetime_ist = received_datetime.astimezone(ist)
                        # Format date and time
                        received_date = received_datetime_ist.strftime("%B %d, %Y")  # e.g., "June 14, 1897"
                        received_time = received_datetime_ist.strftime("%H:%M") + " IST"  # e.g., "14:05 IST"
                        break
                    except Exception:
                        continue  # Try next header if parsing fails

        return {
            "sender_email": sender_email,
            "receiver_email": receiver_email,
            "subject": msg['Subject'],
            "body": body,
            "headers": headers,
            "received_date": received_date if received_date else None,
            "received_time": received_time if received_time else None,
            "received": received_headers,
            "domain": domain,
            "mx_valid": mx_valid,
            "spf_status": auth_results["spf"]["status"],
            "spf_value": auth_results["spf"]["value"],
            "dkim_status": auth_results["dkim"]["status"],
            "dkim_value": auth_results["dkim"]["value"],
            "dmarc_status": auth_results["dmarc"]["status"],
            "dmarc_value": auth_results["dmarc"]["value"],
        }
    except Exception as e:
        return {"error": str(e)}
# -------------------------------

# Checks DKIM validity.
# -------------------------------
def parse_dkim_status(header_value):
    """Extract DKIM result from Authentication-Results."""
    match = re.search(r"dkim=([\w]+)\s*(\([^)]*\))?([^;]*)", header_value or '', re.IGNORECASE)
    if match:
        status = match.group(1).lower()
        detail = ((match.group(2) or '') + (match.group(3) or '')).strip()
        return {
            "auth_results_status": status,
            "auth_results_detail": detail
        }
    return {
        "auth_results_status": "missing",
        "auth_results_detail": None
    }

def evaluate_dkim(path):
    try:
        # Read raw email for DKIM verification
        with open(path, 'rb') as f:
            raw_email = f.read()
            msg = BytesParser(policy=policy.default).parsebytes(raw_email)

        # 1. Receiver-reported DKIM result
        dkim_from_header = parse_dkim_status(msg['Authentication-Results'])

        # 2. Independent DKIM verification
        try:
            independently_verified = dkim.verify(raw_email)
        except Exception as e:
            independently_verified = f"error: {e}"

        # Final result
        return {
            "reported_dkim": dkim_from_header["auth_results_status"],
            "reported_detail": dkim_from_header["auth_results_detail"],
            "independent_dkim_verification": (
                "pass" if independently_verified is True else
                "fail" if independently_verified is False else
                independently_verified  # show the error message
            ),
            "status_match": (
                "match" if (
                    dkim_from_header["auth_results_status"] == "pass"
                    and independently_verified is True
                ) or (
                    dkim_from_header["auth_results_status"] == "fail"
                    and independently_verified is False
                ) else "mismatch"
            )
        }

    except Exception as e:
        return {"error": f"Failed to evaluate DKIM: {e}"}
# -------------------------------


# -------------------------------
# IP Address Extraction
# -------------------------------
# Precompile regexes for IPv4 and IPv6
# Regex patterns
# Stricter regex for IPv4 and IPv6 candidates
_RE_IPv4 = re.compile(r'\b(\d{1,3}(?:\.\d{1,3}){3})\b')
_RE_IPv6 = re.compile(r'\b([A-Fa-f0-9:]{2,39})\b')

# domain IP and geo location
# -------------------------------
def is_public_ip(ip_str):
    """Return True if ip_str (v4 or v6) is a global (public) address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_global
    except ValueError:
        return False

def extract_ip_from_received(received_headers):
    """
    Extract the earliest public IP (v4 or v6) from the Received headers list.
    Returns a string or None.
    """
    for header in reversed(received_headers):
        m4 = _RE_IPv4.search(header)
        if m4 and is_public_ip(m4.group(1)):
            return m4.group(1)

        m6 = _RE_IPv6.search(header)
        if m6 and is_public_ip(m6.group(1)):
            return m6.group(1)
    return None

def get_ipgeolocation(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}"
    except Exception as e:
        return f"Geo-location error: {e}"
# -------------------------------

# All Ip Operations in the mail
# -------------------------------
def get_ip_type(ip_str):
    """Return 'public', 'private', or 'invalid'."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return 'public' if ip.is_global else 'private'
    except ValueError:
        return 'invalid'

def is_valid_ip(ip_str):
    """Return True if string is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def extract_all_ips(received_headers):
    """Extract all valid IPv4 and IPv6 addresses."""
    all_ips = []
    seen = set()

    for header in received_headers:
        for regex in (_RE_IPv4, _RE_IPv6):
            for match in regex.finditer(header):
                ip = match.group(1)
                if ip in seen or not is_valid_ip(ip):
                    continue
                seen.add(ip)
                all_ips.append({
                    'ip': ip,
                    'type': get_ip_type(ip)
                })

    return all_ips

def check_geolocation(ip):
    ip_type = get_ip_type(ip)
    if ip_type != 'public':
        return {
            'hostname': None, 'city': None, 'region': None,
            'country': None, 'loc': None, 'org': None,
            'postal': None, 'note': 'Private/Reserved IP — No geolocation'
        }
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5)
        data = response.json()
        return {
            'hostname': data.get('hostname'),
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'loc': data.get('loc'),
            'org': data.get('org'),
            'postal': data.get('postal'),
            'note': None
        }
    except Exception as e:
        return {
            'hostname': None, 'city': None, 'region': None,
            'country': None, 'loc': None, 'org': None,
            'postal': None, 'note': f"Geo-location error: {e}"
        }

def analyze_ips(received_headers):
    result = []
    all_ips = extract_all_ips(received_headers)
    for entry in all_ips:
        ip = entry['ip']
        ip_type = entry['type']
        geo_info = check_geolocation(ip)
        result.append({
            'ip': ip,
            'type': ip_type,
            **geo_info
        })
    return result
# -------------------------------


# -------------------------------
# Process Report
# -------------------------------
def process_report(data, email_path, output_format):
    # Check SPF, DMARC, DKIM
    spf = data["spf_status"]
    dmarc = data["dmarc_status"]
    mx_valid = data["mx_valid"]
    dkim_res = evaluate_dkim(email_path)
    ip_result = analyze_ips(data["received"])

    ipdomain = extract_ip_from_received(data["received"])
    geo = get_ipgeolocation(ipdomain) if ipdomain else "IP not found"
    # Scoring system
    score = 0
    score += 1 if "pass" in spf else 0
    score += 1 if "pass" in dmarc else 0
    score += 1 if dkim_res["status_match"] == "match" else 0
    score += 1 if mx_valid == True else 0
    score += 1 if "pass" in data["dkim_status"] else 0
    status = "Authentic" if score>=2 else "Suspicious"

    report = {
        "Filename": os.path.basename(email_path),
        "Sender E-mail Address": data["sender_email"],
        "Receiver E-mail Address": data["receiver_email"],
        "Received Date": data["received_date"],
        "Received Time": data["received_time"],
        "Subject": data["subject"],
        "SPF Value": data["spf_value"],
        "SPF Status": spf,
        "DMARC Value": data["dmarc_value"],
        "DMARC Status": dmarc,
        "DKIM Value": data["dkim_value"],
        "DKIM Status": dkim_res,
        "DKIM Verification": dkim_res["status_match"],
        "MX valid": data["mx_valid"],
        "Domain": data["domain"],
        "Domain IP": ipdomain or "—",
        "Domain IP Geo-location": geo,
        "IP Details": ip_result,
        "Authenticity Score": f"{score}/5",
        "Authenticity Status": status,
        "E-mail Body": data["body"],
    }

    # Save to email-reports/<eml-filename>_report.pdf or .txt or .json or .html
    email_dir = os.path.dirname(email_path)
    output_dir = os.path.join(email_dir, "email-reports")
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(email_path))[0]

    # Output formats

    # 1. PDF Format
    if output_format == "pdf":
        report = {
            "file_name": os.path.basename(email_path),
            "sender_email": data["sender_email"],
            "receiver_email": data["receiver_email"],
            "received_date": data["received_date"],
            "received_time": data["received_time"],
            "subject": data["subject"],
            "spf_value": data["spf_value"],
            "spf_status": spf,
            "dkim_value": data["dkim_value"],
            "dkim_status": data["dkim_status"],
            "dkim_verification": dkim_res["status_match"],
            "dmarc_value": data["dmarc_value"],
            "dmarc_status": dmarc,
            "mx_valid": mx_valid,
            "domain": data["domain"],
            "ipdomain": ipdomain or "—",
            "geo": geo,
            "ip_result": ip_result,
            "auth_status": status,
            "score": score,
            "body": data["body"],
        }
        report_path = os.path.join(output_dir, f"{base_name}_report.pdf")
        generate_pdf_report(report_path, report)
        print(f"[+] PDF report saved to {report_path}")

    # 2. TXT Format
    elif output_format == "txt":
        generate_txt_report(report, output_dir, base_name)

    # 3. JSON Format
    elif output_format == "json":
        report_path = os.path.join(output_dir, f"{base_name}_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        print(f"[+] Report saved to {report_path}")

    # 4. HTML Format
    elif output_format == "html":
        generate_html_report(report, output_dir, base_name)
# -------------------------------

# E-mail File Validator
# -------------------------------
def is_valid_email_file(filepath):
    """Check if a file is likely a valid email file based on extension and content."""
    valid_extensions = {'.eml', '.txt', '.msg'}
    _, ext = os.path.splitext(filepath.lower())
    
    if ext not in valid_extensions:
        return False, "Invalid file extension"
    
    try:
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        # Check if any of the standard headers are present
        headers = msg.keys()
        required_headers = ['From', 'To']
        if any(h in headers for h in required_headers):
            return True, "Valid email headers detected"
        else:
            return False, "Invalid E-mail File"
    except Exception as e:
        return False, f"Error reading file: {e}"
# -------------------------------

# Report Generation
# -------------------------------
def generate_report(email_path, output_format="pdf"):
    result, reason = is_valid_email_file(email_path)
    if result == True:
        #check sender info
        data = check_sender_legitimacy(email_path)
        if "error" in data:
            print("Error:", data["error"])
        else:
            process_report(data, email_path, output_format)
    else:
        print(reason)
# -------------------------------

# Process folder containing emails
# -------------------------------
def process_folder(folder, fmt):
    # Supported file extensions
    valid_extensions = ['.eml', '.txt', '.msg']
    
    for fn in os.listdir(folder):
        # Check if file has a valid extension (case insensitive)
        if any(fn.lower().endswith(ext) for ext in valid_extensions):
            generate_report(os.path.join(folder, fn), fmt)
# -------------------------------