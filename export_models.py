"""
Export Dreams models to multiple 3D formats (OBJ, FBX, USDZ)
Uses Meshroom for photogrammetry processing
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional

class ModelExporter:
    def __init__(self, frames_dir: str, output_dir: str):
        self.frames_dir = Path(frames_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Meshroom paths (adjust based on installation)
        self.meshroom_batch = self._find_meshroom()
        
    def _find_meshroom(self) -> Optional[Path]:
        """Locate Meshroom installation"""
        common_paths = [
            Path(r"C:\Program Files\Meshroom-2023.3.0\meshroom_batch.exe"),
            Path(r"C:\Program Files\Meshroom\meshroom_batch.exe"),
            Path.home() / "Meshroom" / "meshroom_batch.exe",
        ]
        
        for path in common_paths:
            if path.exists():
                return path
        
        # Check if meshroom_batch is in PATH
        try:
            result = subprocess.run(
                ["where", "meshroom_batch"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip().split('\n')[0])
        except subprocess.CalledProcessError:
            return None
    
    def run_meshroom(self, output_name: str = "dreams_model") -> bool:
        """Run Meshroom photogrammetry pipeline"""
        if not self.meshroom_batch:
            print("❌ Meshroom not found. Please install from:")
            print("   https://github.com/alicevision/Meshroom/releases")
            return False
        
        # Get all frame files
        frames = sorted(self.frames_dir.glob("*.png"))
        if not frames:
            print(f"❌ No frames found in {self.frames_dir}")
            return False
        
        print(f"📸 Processing {len(frames)} frames...")
        
        # Create Meshroom project
        project_dir = self.output_dir / "meshroom_project"
        project_dir.mkdir(exist_ok=True)
        
        # Build command
        cmd = [
            str(self.meshroom_batch),
            "--input", str(self.frames_dir),
            "--output", str(project_dir),
        ]
        
        print(f"🔄 Running Meshroom...")
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode == 0:
                print("✅ Meshroom processing complete!")
                return True
            else:
                print(f"❌ Meshroom failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Meshroom processing timed out (>1 hour)")
            return False
        except Exception as e:
            print(f"❌ Error running Meshroom: {e}")
            return False
    
    def convert_to_fbx(self, obj_file: Path) -> Optional[Path]:
        """Convert OBJ to FBX using Blender"""
        fbx_file = obj_file.with_suffix('.fbx')
        
        # Check if Blender is available
        blender_paths = [
            Path(r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"),
            Path(r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"),
            Path(r"C:\Program Files\Blender Foundation\Blender\blender.exe"),
        ]
        
        blender = None
        for path in blender_paths:
            if path.exists():
                blender = path
                break
        
        if not blender:
            print("⚠️  Blender not found - skipping FBX conversion")
            print("   Install Blender to enable FBX export")
            return None
        
        # Blender Python script for conversion
        script = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.obj(filepath=r"{obj_file}")
bpy.ops.export_scene.fbx(filepath=r"{fbx_file}")
"""
        
        script_file = self.output_dir / "convert_to_fbx.py"
        script_file.write_text(script)
        
        print(f"🔄 Converting to FBX...")
        try:
            subprocess.run(
                [str(blender), "--background", "--python", str(script_file)],
                capture_output=True,
                timeout=300
            )
            if fbx_file.exists():
                print(f"✅ FBX created: {fbx_file}")
                return fbx_file
        except Exception as e:
            print(f"⚠️  FBX conversion failed: {e}")
        
        return None
    
    def convert_to_usdz(self, obj_file: Path) -> Optional[Path]:
        """Convert OBJ to USDZ (requires macOS or usd-core)"""
        usdz_file = obj_file.with_suffix('.usdz')
        
        print("⚠️  USDZ conversion requires macOS or USD tools")
        print("   Skipping USDZ export on Windows")
        print("   You can convert the OBJ file online at:")
        print("   https://products.aspose.app/3d/conversion/obj-to-usdz")
        
        return None
    
    def export_all_formats(self):
        """Main export pipeline"""
        print("=" * 60)
        print("🎮 Dreams to Reality - Model Exporter")
        print("=" * 60)
        
        # Step 1: Run Meshroom
        if not self.run_meshroom():
            print("\n❌ Meshroom processing failed. Cannot proceed.")
            return
        
        # Step 2: Find generated OBJ file
        meshroom_output = self.output_dir / "meshroom_project" / "MeshroomCache" / "Texturing"
        obj_files = list(meshroom_output.rglob("*.obj"))
        
        if not obj_files:
            print("\n❌ No OBJ file generated by Meshroom")
            return
        
        obj_file = obj_files[0]
        print(f"\n✅ OBJ file: {obj_file}")
        
        # Copy OBJ to output directory
        final_obj = self.output_dir / "dreams_model.obj"
        import shutil
        shutil.copy(obj_file, final_obj)
        print(f"📦 Copied to: {final_obj}")
        
        # Step 3: Convert to FBX
        fbx_file = self.convert_to_fbx(final_obj)
        
        # Step 4: Convert to USDZ (informational only on Windows)
        usdz_file = self.convert_to_usdz(final_obj)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Export Summary")
        print("=" * 60)
        print(f"✅ OBJ: {final_obj}")
        if fbx_file:
            print(f"✅ FBX: {fbx_file}")
        else:
            print(f"⚠️  FBX: Not created (Blender required)")
        if usdz_file:
            print(f"✅ USDZ: {usdz_file}")
        else:
            print(f"⚠️  USDZ: Not created (macOS/USD tools required)")
        print("=" * 60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Export Dreams models to OBJ, FBX, and USDZ formats"
    )
    parser.add_argument(
        "frames_dir",
        help="Directory containing preprocessed frames"
    )
    parser.add_argument(
        "output_dir",
        help="Output directory for exported models"
    )
    
    args = parser.parse_args()
    
    exporter = ModelExporter(args.frames_dir, args.output_dir)
    exporter.export_all_formats()


if __name__ == "__main__":
    main()
