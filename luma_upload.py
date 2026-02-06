import os
import argparse
import sys
from pathlib import Path
from lumaai import LumaAI

def upload_to_luma(zip_path: Path, api_key: str, title: str = None):
    """
    Uploads a zip file to Luma AI for processing.
    """
    if not zip_path.exists():
        print(f"Error: Zip file not found at {zip_path}")
        return

    print(f"Initializing Luma AI client...")
    client = LumaAI(auth_token=api_key)

    if title is None:
        title = f"Dreams Export - {zip_path.stem}"

    print(f"Uploading '{title}' to Luma AI...")
    try:
        # Create a capture from the zip file
        capture = client.captures.create(
            video=open(zip_path, "rb"),
            title=title
        )
        
        print(f"\n✅ Upload Successful!")
        print(f"Capture ID: {capture.slug}")
        print(f"Track progress at: https://lumalabs.ai/capture/{capture.slug}")
        
    except Exception as e:
        print(f"\n❌ Upload Failed: {e}")
        print("Please check your API Key and internet connection.")

def main():
    parser = argparse.ArgumentParser(description='Upload Dreams captures to Luma AI')
    parser.add_argument('zip_path', type=Path, help='Path to the .zip file to upload')
    parser.add_argument('--api-key', type=str, help='Luma AI API Key (or set LUMA_API_KEY env var)')
    parser.add_argument('--title', type=str, help='Title for the capture')
    
    args = parser.parse_args()
    
    # Get API key from arg or env
    api_key = args.api_key or os.environ.get("LUMA_API_KEY")
    
    if not api_key:
        print("Error: Luma API Key is required. Pass with --api-key or set LUMA_API_KEY environment variable.")
        print("Get your key at: https://lumalabs.ai/dashboard/api")
        sys.exit(1)
        
    upload_to_luma(args.zip_path, api_key, args.title)

if __name__ == "__main__":
    main()
