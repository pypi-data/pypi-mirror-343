# -------------------------------
# Module Imports
# -------------------------------
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER

# -------------------------------
# REPORT FILE GENERATION
# -------------------------------

# Generate text file
# -------------------------------
def generate_txt_report(report, output_dir, base_name):
    # Prepare IP blocks
    public_ips = []
    private_ips = []

    for ip in report["IP Details"]:
        pblock = f"""
------------------------------------
🌍 IP Address:               {ip["ip"]}
🔐 Hostname:                 {ip.get("hostname", "—") or "—"}
🔐 City:                     {ip.get("city", "—") or "—"}
🔐 Region:                   {ip.get("region", "—") or "—"}
🔐 Country:                  {ip.get("country", "—") or "—"}
🔐 Location:                 {ip.get("loc", "—") or "—"}
🔐 Organization:             {ip.get("org", "—") or "—"}
🔐 Postal Code:              {ip.get("postal", "—") or "—"}
------------------------------------
"""
        sblock = f"""
------------------------------------
🌍 IP Address:               {ip["ip"]}
🔐 Details:                  {ip.get("note", "—") or "—"}\n
------------------------------------
"""
        if ip["type"] == "public":
            public_ips.append(pblock)
        else:
            private_ips.append(sblock)

    ip_report_txt = (
        "\n========== PUBLIC IP & DETAILS ===================="
        + "".join(public_ips)
        + "===================================================\n"
        + "\n========== PRIVATE IP & DETAILS ===================="
        + "".join(private_ips)
        + "===================================================\n"
    )

    # Build full report
    report_text = f"""
======== EMAIL AUTHENTICITY REPORT ========
File Name:                          {report["Filename"]}
------------------------------------
📧 Sender E-Mail Address:           {report["Sender E-mail Address"]}
📤 Receiver E-Mail Address:         {report["Receiver E-mail Address"]}
📅 Received Date:                   {report["Received Date"]}
🕒 Received Time:                   {report["Received Time"]}
📝 Subject:                         {report["Subject"]}
------------------------------------
🔐 SPF:                             {report["SPF Value"]}
🔐 DMARC:                           {report["DMARC Value"]}
🔐 DKIM:                            {report["DKIM Value"]}
------------------------------------
🧾 SPF Status:                      {report["SPF Status"]}
🧾 DMARC Status:                    {report["DMARC Status"]}
🧾 DKIM Status:                     {report["DKIM Status"]["reported_dkim"]}
🧾 DKIM Validation (independent):   {report["DKIM Verification"]}
🧾 MX valid:                        {report["MX valid"]}
------------------------------------
🧠 Authenticity Status:             {report["Authenticity Status"]}
🧮 Authenticity Score:              {report["Authenticity Score"]}
------------------------------------
🌍 Domain:                          {report["Domain"]}
🌍 Domain IP Address:               {report["Domain IP"]}
🌍 Geo-location of IP:              {report["Domain IP Geo-location"]}
{ip_report_txt}
========== EMAIL BODY ====================
{report["E-mail Body"]}
==========================================
"""
    report_path = os.path.join(output_dir, f"{base_name}_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"[+] TXT Report saved to: {report_path}")
# -------------------------------

# Generate HTML File
# -------------------------------
def generate_html_report(report_data, output_dir, base_name):
    public_ips = [ip for ip in report_data["IP Details"] if ip['type'] == 'public']
    private_ips = [ip for ip in report_data["IP Details"] if ip['type'] != 'public']

    def render_kv_section(title, kv_data):
        html = f'<h2>{title}</h2><table>'
        for key, value in kv_data.items():
            html += f'<tr><td><strong>{key}</strong></td><td>{value}</td></tr>'
        html += '</table><br>'
        return html

    def render_public_ips(ips):
        html = '<h2>5. Public IPs and Details</h2>'
        for ip_info in ips:
            html += f"""
            <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
                <strong>IP Address:</strong> {ip_info.get('ip', 'N/A')}<br>
                <ul>
                    <li><strong>Hostname:</strong> {ip_info.get('hostname') or 'N/A'}</li>
                    <li><strong>City:</strong> {ip_info.get('city') or 'N/A'}</li>
                    <li><strong>Region:</strong> {ip_info.get('region') or 'N/A'}</li>
                    <li><strong>Country:</strong> {ip_info.get('country') or 'N/A'}</li>
                    <li><strong>Location:</strong> {ip_info.get('loc') or 'N/A'}</li>
                    <li><strong>Organization:</strong> {ip_info.get('org') or 'N/A'}</li>
                    <li><strong>Postal Code:</strong> {ip_info.get('postal') or 'N/A'}</li>
                </ul>
            </div>
            """
        return html

    def render_private_ips(ips):
        html = '<h2>6. Private IPs and Details</h2><table>'
        html += '<tr><th>IP Address</th><th>Details</th></tr>'
        for ip in ips:
            html += f"<tr><td>{ip['ip']}</td><td>{ip.get('note', 'No Note')}</td></tr>"
        html += '</table><br>'
        return html

    def render_body(body):
        html = '<h2>7. Email Body</h2><div style="white-space: pre-wrap;">'
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("http"):
                html += f'<a href="{line}" target="_blank">{line}</a><br>'
            else:
                html += line + '<br>'
        html += '</div>'
        return html

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Authenticity Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #2C3E50; }}
        h1 {{ text-align: center; color: #1A5276; }}
        h2 {{ color: #2C3E50; border-bottom: 2px solid #ccc; padding-bottom: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        td, th {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; }}
        th {{ background-color: #f4f4f4; text-align: left; }}
    </style>
</head>
<body>
    <h1>Email Authenticity Analysis Report</h1>
    {render_kv_section("1. Email Details", {
        "Filename": report_data["Filename"],
        "Sender E-Mail Address": report_data["Sender E-mail Address"],
        "Receiver E-Mail Address": report_data["Receiver E-mail Address"],
        "Received Date": report_data["Received Date"],
        "Received Time": report_data["Received Time"],
        "Subject": report_data["Subject"]
    })}
    {render_kv_section("2. Authentication Results", {
        "SPF Value": report_data["SPF Value"],
        "SPF Status": report_data["SPF Status"],
        "DKIM Value": report_data["DKIM Value"],
        "DKIM Status": report_data["DKIM Status"],
        "DKIM Verification": report_data["DKIM Verification"],
        "DMARC Value": report_data["DMARC Value"],
        "DMARC Status": report_data["DMARC Status"],
        "MX valid": report_data["MX valid"]
    })}
    {render_kv_section("3. Authenticity Summary", {
        "Authenticity Status": report_data["Authenticity Status"],
        "Authenticity Score": report_data["Authenticity Score"]
    })}
    {render_kv_section("4. Domain, IP Details and Geolocation", {
        "Domain": report_data["Domain"],
        "Domain IP": report_data["Domain IP"],
        "Domain IP Geo-location": report_data["Domain IP Geo-location"]
    })}
    {render_public_ips(public_ips)}
    {render_private_ips(private_ips)}
    {render_body(report_data["E-mail Body"])}
</body>
</html>
    """
    report_path = os.path.join(output_dir, f"{base_name}_report.html")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] HTML report saved to {report_path}")

# -------------------------------

# Generate PDF File
# -------------------------------
def generate_pdf_report(output_path, report_data):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=25 * mm, rightMargin=25 * mm,
                            topMargin=25 * mm, bottomMargin=25 * mm)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('Title', fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.HexColor("#1A5276"), fontName='Helvetica-Bold', spaceAfter=20)
    heading_style = ParagraphStyle('Heading', fontSize=14, leading=18, spaceAfter=10, textColor=colors.HexColor("#2C3E50"), fontName='Helvetica-Bold')
    label_style = ParagraphStyle('Label', fontSize=10, leading=12, fontName='Helvetica-Bold')
    value_style = ParagraphStyle('Value', fontSize=10, leading=12, fontName='Helvetica')

    def add_heading(text):
        story.append(Paragraph(text, heading_style))
        story.append(Spacer(1, 6))

    def add_kv_table(data):
        table_data = [[Paragraph(f"<b>{key}</b>", label_style), Paragraph(str(value), value_style)] for key, value in data.items()]
        table = Table(table_data, colWidths=[120, 350])
        table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                   ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey)]))
        story.append(table)
        story.append(Spacer(1, 12))

    def add_ip_table(ips):
        table_data = [[Paragraph("<b>IP Address</b>", label_style), Paragraph("<b>Details</b>", label_style)]]
        for ip_info in ips:
            ip = ip_info['ip']
            note = ip_info.get('note', 'No Note')
            table_data.append([Paragraph(ip, value_style), Paragraph(note, value_style)])
        table = Table(table_data, colWidths=[200, 300])
        table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                   ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey)]))
        story.append(table)
        story.append(Spacer(1, 12))

    def add_email_body(text):
        story.append(Paragraph("<b>7. Email Body</b>", heading_style))
        for line in text.splitlines():
            if line.strip().startswith("http"):
                link = f'<a href="{line.strip()}" color="blue">{line.strip()}</a>'
                story.append(Paragraph(link, value_style))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(line.strip(), value_style))
        story.append(Spacer(1, 12))

    # === Title ===
    story.append(Paragraph("Email Authenticity Analysis Report", title_style))
    story.append(Spacer(1, 6))

    # === Sections ===
    add_heading("1. Email Details")
    add_kv_table({
        "Filename": report_data["file_name"],
        "Sender E-Mail Address": report_data["sender_email"],
        "Receiver E-Mail Address": report_data["receiver_email"],
        "Received Date": report_data["received_date"],
        "Received Time": report_data["received_time"],
        "Subject": report_data["subject"]
    })
    story.append(Spacer(1, 6))
    add_heading("2. Authentication Results")
    add_kv_table({
        "SPF": report_data["spf_value"],
        "SPF Status": report_data["spf_status"],
        "DKIM": report_data["dkim_value"],
        "DKIM Status": report_data["dkim_status"],
        "DKIM Verification (independent)": report_data["dkim_verification"],
        "DMARC": report_data["dmarc_value"],
        "DMARC Status": report_data["dmarc_status"],
        "MX Valid": report_data["mx_valid"]
    })
    story.append(Spacer(1, 6))
    add_heading("3. Authenticity Summary")
    add_kv_table({
        "Status": report_data["auth_status"],
        "Score": f"{report_data['score']}/5"
    })
    story.append(Spacer(1, 6))

    # === IP Details and Geolocation ===
    add_heading("4. Domain, IP Details and Geolocation")
    add_kv_table({
        "Domain name": report_data["domain"],
        "Domain IP Address": report_data["ipdomain"],
        "Domain IP Geo-location": report_data["geo"]
    })
    story.append(Spacer(1, 6))

    public_ips = [ip for ip in report_data["ip_result"] if ip['type'] == 'public']
    private_ips = [ip for ip in report_data["ip_result"] if ip['type'] != 'public']

    # Public IPs with sub-table for details
    if public_ips:
        # Add heading (will check page availability for this)
        add_heading("5. Public IPs and Details")
        
        # Add some space before the table to ensure it fits properly on the page
        
        # Start the table
        table_data = [[Paragraph("<b>IP Address</b>", label_style),
                    Paragraph("<b>Geolocation Details</b>", label_style)]]

        for ip_info in public_ips:
            sub_data = [
                [Paragraph("<b>Hostname</b>", label_style), Paragraph(ip_info.get('hostname') or 'N/A', value_style)],
                [Paragraph("<b>City</b>", label_style), Paragraph(ip_info.get('city') or 'N/A', value_style)],
                [Paragraph("<b>Region</b>", label_style), Paragraph(ip_info.get('region') or 'N/A', value_style)],
                [Paragraph("<b>Country</b>", label_style), Paragraph(ip_info.get('country') or 'N/A', value_style)],
                [Paragraph("<b>Location</b>", label_style), Paragraph(ip_info.get('loc') or 'N/A', value_style)],
                [Paragraph("<b>Organization</b>", label_style), Paragraph(ip_info.get('org') or 'N/A', value_style)],
                [Paragraph("<b>Postal Code</b>", label_style), Paragraph(ip_info.get('postal') or 'N/A', value_style)]
            ]
            sub_table = Table(sub_data, colWidths=[80, 260])
            sub_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.grey),
            ]))
            table_data.append([Paragraph(ip_info['ip'], value_style), sub_table])

        # Create the main table
        main_table = Table(table_data, colWidths=[120, 400])

        # Base style
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.darkblue),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.darkblue),  # Line below header
        ])

        # Add a line below each data row (excluding the header)
        for i in range(1, len(table_data)):
            style.add('LINEBELOW', (0, i), (-1, i), 0.5, colors.darkblue)

        main_table.setStyle(style)

        # Check for space before adding the table (to avoid a split across pages)
        story.append(main_table)
        story.append(Spacer(1, 18))  # Add some space after the table too

    # Private IPs table
    if private_ips:
        add_heading("6. Private IPs and Details")
        add_ip_table(private_ips)
        story.append(Spacer(1, 6))
    
    add_email_body(report_data["body"])
    doc.build(story)
# -------------------------------