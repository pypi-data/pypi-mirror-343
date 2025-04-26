# mail_checker/cli.py
import argparse
import os
from email_auth_checker.email_auth import generate_report, process_folder  # Your custom logic

def main():
    parser = argparse.ArgumentParser(
        description=(
            "\t \t Email Authenticity Checker\n\n"
            "Analyze one email file or a directory of emails (.eml or .txt or .msg).\n"
            "Performs SPF, DKIM, DMARC, MX-value checks and generates a report.\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "email_file",
        type=str,
        help="Path to an email file (.eml or .txt) or a folder containing such files"
    )

    parser.add_argument(
        "--format",
        choices=["pdf", "txt", "json", "html"],
        default="pdf",
        help="Output report format (default: pdf)"
    )

    args = parser.parse_args()

    if os.path.isfile(args.email_file):
        generate_report(args.email_file, args.format)

    elif os.path.isdir(args.email_file):
        process_folder(args.email_file, args.format)

    else:
        print("Invalid path. Please provide a valid file or directory.")
        parser.print_help()  # Display the help message

if __name__ == "__main__":
    main()
