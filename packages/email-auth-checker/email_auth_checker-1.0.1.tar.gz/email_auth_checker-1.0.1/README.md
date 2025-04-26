# Email Authenticity Checker

A Python tool to analyze and verify the authenticity of email files (`.eml` or `.txt` or `.msg`). It inspects key headers and metadata, performs SPF, DKIM, and DMARC checks, validates mail servers, and provides IP geolocation data — all summarized in a clean report.

---

## Features

- Parse and validate `.eml` or `.txt` or `.msg` email files
- SPF, DKIM, and DMARC verification
- IP address extraction and geolocation
- Output reports in multiple formats:
  - PDF (styled, modern layout)
  - HTML (interactive report)
  - JSON (for integration)
  - TXT (quick review)
- Supports single files or entire directories
- Intelligent scoring system to flag suspicious emails

---

## Installation

### Install via pip (after packaging or from PyPI):

```bash
pip install email_auth_checker