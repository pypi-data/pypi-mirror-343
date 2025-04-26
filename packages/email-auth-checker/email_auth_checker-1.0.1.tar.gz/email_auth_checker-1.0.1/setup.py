# setup.py
from setuptools import setup, find_packages
setup(
    name="email_auth_checker",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "dnspython",         # for dns.resolver
        "requests",          # for HTTP requests
        "dkimpy",            # for dkim
        "reportlab",         # for PDF generation
    ],
    entry_points={
        'console_scripts': [
            'email_auth_checker = email_auth_checker.cli:main',
        ],
    },
    python_requires=">=3.7",
    author="VISHAL KUMAR SINHA",
    author_email='v.kr.sinha.99@gmail.com',
    description="A CLI tool for checking email authenticity (SPF, DKIM, DMARC, etc.)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vishal-Kumar-Sinha/email_auth_checker",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
