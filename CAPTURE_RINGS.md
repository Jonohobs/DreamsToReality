# 💍 The Capture Ring Setup (Dreams)

The "Capture Ring" is a community-proven method for getting consistent, high-quality 3D scans out of PlayStation Dreams. It provides a reference frame and consistent lighting for the software to track.

## 1. The Environment
- **Start with a Blank Scene**: Use a fresh scene with all effects (Bloom, Sun, Sky) turned off.
- **Studio Lighting**: Use a single "Sun" gadget set to a neutral white, or use the "Studio Lighting" element found in the Dreamiverse. The goal is to avoid moving shadows.

## 2. Setting Up the Rings
- **The Center Piece**: Place your sculpt at the exact center of the scene (Grid Snap: On).
- **The Orbit Rings**: 
  - Create a series of concentric circles around your object at different heights.
  - These rings help you maintain a consistent distance while orbiting with the camera.
  - You can use the "Paint" tool with "Surface Snap" on a large invisible sphere to draw these rings.

## 3. The "Black Background" Trick
- Many creators use a **Solid Black Background** (Black Fog at 100% or a giant black sculpt).
- This forces the photogrammetry software to ignore the background and focus entirely on the subject.
- *Note: For NeRF, a static, unmoving background is actually better than solid black, so use the Black Background for Meshroom only.*

## 4. Capturing the Video
- **The Spiral Method**: Start at the top, looking down at a 45-degree angle. Orbit one full circle. Lower the camera slightly, orbit again. Repeat until you are at eye-level or slightly below.
- **Zoom**: Keep the object filling about 70-80% of the screen.
- **Duration**: Aim for a 60-90 second video for a complex object.
