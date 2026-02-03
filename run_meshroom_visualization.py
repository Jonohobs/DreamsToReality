import os
import subprocess
import sys
from pathlib import Path
import platform

def find_meshroom_executable():
    """Attempts to find the Meshroom executable in common locations."""
    system = platform.system()
    possible_paths = []

    if system == "Windows":
        possible_paths = [
            Path("C:/Program Files/Meshroom/Meshroom.exe"),
            Path("C:/Program Files (x86)/Meshroom/Meshroom.exe"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "Meshroom/Meshroom.exe",
            # Add custom paths here
            Path("C:/Meshroom/Meshroom.exe"),
        ]
    elif system == "Linux":
        possible_paths = [
            Path("/usr/local/bin/meshroom"),
            Path("/opt/meshroom/Meshroom"),
        ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

def main():
    print("Searching for Meshroom executable...")
    meshroom_exe = find_meshroom_executable()

    if not meshroom_exe:
        print("\n❌ Meshroom not found in standard locations.")
        print("Please ensure Meshroom is installed (https://alicevision.org/#meshroom).")
        print("If installed, edit this script to include the correct path in 'possible_paths'.")
        sys.exit(1)

    print(f"✅ Found Meshroom: {meshroom_exe}")

    # Define your project paths here
    # Assuming this script is in dreams-to-reality/
    base_dir = Path(__file__).parent
    images_dir = base_dir / "data_v1" / "clean_frames"
    output_dir = base_dir / "data_v1" / "meshroom_out"

    if not images_dir.exists():
        print(f"\n⚠️  Input directory not found: {images_dir}")
        print("Run 'pipeline.py' first to generate clean frames.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input Images: {images_dir}")
    print(f"Output Directory: {output_dir}")
    print("\nLaunching Meshroom...")

    # Launch Meshroom GUI with the images loaded (if supported by CLI)
    # Meshroom CLI typically creates a .mg file. Opening GUI is usually just `Meshroom.exe`
    # To run a graph headless: meshroom_compute --input ...
    
    # For now, we'll just open the GUI so the user can drag-and-drop or load.
    # To automate fully, we need 'meshroom_batch' or 'meshroom_photogrammetry' executable which is separate.
    
    try:
        subprocess.Popen([str(meshroom_exe)])
        print("\nMeshroom GUI started. Drag and drop the 'clean_frames' folder into the 'Images' pane.")
    except Exception as e:
        print(f"Error launching Meshroom: {e}")

if __name__ == "__main__":
    main()
