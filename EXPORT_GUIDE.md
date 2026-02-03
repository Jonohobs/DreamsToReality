# Dreams Model Export Guide

## Your Model Location
**Path**: `C:\Users\jonat\OneDrive\Desktop\DesktopFiles\Reality scan attempt 1\`

## Quick Export Options

### Option 1: RealityScan App (Easiest)
1. Open RealityScan on your phone/tablet
2. Load the scan project
3. Tap **Export** → **Model & Point Cloud**
4. Select format:
   - **OBJ** - Universal (Blender, Maya, Unity)
   - **FBX** - Industry standard (animations/materials)
   - **USDZ** - Apple AR format
5. Save to iCloud/OneDrive to access on PC

### Option 2: Online Converter
If you can get the model as OBJ first:
- **OBJ → FBX**: https://anyconv.com/obj-to-fbx-converter/
- **OBJ → USDZ**: https://products.aspose.app/3d/conversion/obj-to-usdz

### Option 3: Meshroom Pipeline (Advanced)
Install Meshroom and run:
```bash
python export_models.py data_v1/clean_frames models/output
```

## Model Files Found
Your RealityScan export contains:
- 4 textured models (~25MB each)
- Multiple model iterations
- SfM (Structure from Motion) data
- Metadata files

**Largest/Best Quality Models**:
- `model326D822CB4AD4BBA94EA9ED244116F90_tex0_1.dat` (25.7 MB)
- `modelCCAEEC006C094898AA01E54EFBA00803_tex0_1.dat` (25.8 MB)
