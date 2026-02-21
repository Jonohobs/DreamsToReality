# Dreams to Reality

Automatically export your PlayStation Dreams creations as portable 3D models.

Dreams to Reality takes a video capture of your Dreams sculpture and reconstructs it into a standard 3D model (OBJ, PLY, GLTF) that you can use in Blender, Unity, Unreal Engine, or any 3D application.

## How It Works

1. **Capture** your Dreams creation as a video using PS5's built-in capture
2. **Run the pipeline** to automatically extract frames, clean them, and reconstruct geometry
3. **Export** your 3D model in the format you need

```bash
python pipeline.py --video my_creation.mp4 --output ./export
```

## Features

- Automatic frame extraction from video
- AI-powered background removal and segmentation
- 3D reconstruction via Structure-from-Motion
- Gaussian Splatting training for high-quality renders
- Export to OBJ, PLY, and GLTF formats
- Web API for remote processing

## Quick Start

### Requirements

- Python 3.10+
- COLMAP (for 3D reconstruction)
- CUDA-compatible GPU recommended

### Installation

```bash
pip install -r requirements.txt
```

### Usage

**Full pipeline** (video to 3D model):
```bash
python pipeline.py --video your_video.mp4 --output ./results
```

**Individual steps:**
```bash
# Preprocess frames
python preprocess.py --input ./frames --output ./clean_frames

# Segment (remove background)
python segment.py --input ./clean_frames --output ./segmented

# Reconstruct 3D model
python reconstruct.py --input ./segmented --output ./model

# Train Gaussian Splatting (optional, for high-quality renders)
python train_gsplat.py --data ./model --output ./splat
```

**API server:**
```bash
uvicorn api.main:app --reload
```

## Capture Tips

See [CAPTURE_GUIDE.md](CAPTURE_GUIDE.md) for best practices on recording your Dreams creations for optimal reconstruction quality.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Disclaimer

Dreams to Reality is an independent project. It is not affiliated with, endorsed by, or associated with Sony Interactive Entertainment, Media Molecule, or PlayStation.

"PlayStation" and "Dreams" are trademarks of Sony Interactive Entertainment. All trademarks are property of their respective owners.

This tool processes video files that users have exported using PlayStation 5's built-in capture feature. It does not access, modify, or reverse engineer any Sony software or systems.

Users are responsible for ensuring they have the right to process and export content created in Dreams, including respecting the rights of other creators whose work may appear in exported videos.
