import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

import qrcode
from dotenv import load_dotenv
import validators

def configure_logging():
    """Set up logging to display messages on the console."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

def ensure_output_directory(directory: Path):
    """Create the output directory if it does not exist."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory '{directory}' is ready.")
    except Exception as err:
        logging.error(f"Cannot create directory {directory}: {err}")
        sys.exit(1)

def generate_qr_code(url: str, output_file: Path, fill_color: str, back_color: str):
    """Generate and save a QR code image if the URL is valid."""
    if not validators.url(url):
        logging.error(f"Invalid URL: {url}")
        sys.exit(1)

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=2
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(output_file)
        logging.info(f"QR code saved at: {output_file}")
    except Exception as err:
        logging.error(f"Error during QR generation: {err}")
        sys.exit(1)

def main():
    # Load environment variables from a .env file, if present
    load_dotenv()

    # Set up logging
    configure_logging()

    # Command-line arguments for customization
    parser = argparse.ArgumentParser(description="Generate a QR code pointing to your GitHub homepage.")
    parser.add_argument('--url', type=str, default=os.getenv("QR_DATA_URL", "https://github.com/AbhishekDuddupudi"),
                        help="The URL to encode in the QR code")
    parser.add_argument('--dir', type=str, default=os.getenv("QR_CODE_DIR", "output_qr"),
                        help="Directory where the QR code image will be saved")
    parser.add_argument('--filename', type=str, default=os.getenv("QR_CODE_FILENAME", "qr.png"),
                        help="Filename for the QR code image")
    parser.add_argument('--fill', type=str, default=os.getenv("FILL_COLOR", "black"),
                        help="Fill color for the QR code")
    parser.add_argument('--back', type=str, default=os.getenv("BACK_COLOR", "white"),
                        help="Background color for the QR code")
    args = parser.parse_args()

    # Prepare the output directory
    output_directory = Path(args.dir)
    ensure_output_directory(output_directory)

    # If the default filename is used, append a timestamp for uniqueness
    if args.filename == "qr.png":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_{timestamp}.png"
    else:
        filename = args.filename

    output_path = output_directory / filename

    # Generate the QR code
    generate_qr_code(args.url, output_path, args.fill, args.back)

if __name__ == "__main__":
    main()
