# 🎮 Dreams Capture Best Practices

To get the best results when converting Dreams creations to 3D models, follow these scene-preparation tips before capturing your video.

## 1. Material Properties
Dreams' default "painterly" look can be difficult for photogrammetry. 
- **Use the "Plastic" Finish**: Applying a plastic or matte finish to your sculpts reduces soft "fleck" blending and creates more defined surfaces.
- **Reduce "Shine" & "Metallic"**: Reflections move relative to the camera, which confuses tracking. A matte, non-shiny surface is much easier to reconstruct.
- **Maximize "Fleck Density"**: If you use flecks for detail, ensure they are densely packed so they appear as a solid surface rather than a cloud of particles.

## 2. Lighting & Visuals
- **Flat Lighting**: Avoid high-contrast shadows or dynamic lights that change as you move the camera. Soft, even environmental lighting works best.
- **Disable Depth of Field (DoF)**: In the Show/Hide menu or your camera settings, turn off DoF. Every part of the model should be in sharp focus.
- **Disable Bloom & Lens Flare**: These effects create "floating" artifacts that the reconstruction software might try to turn into geometry.

## 3. Capture Technique
- **Consistent Speed**: Move the camera smoothly. Jerky movements cause motion blur, which we have to filter out.
- **360° Coverage**: Ensure you orbit the object fully at multiple heights (top-down, eye-level, slightly below).
- **Background Contrast**: If possible, capture against a simple, static background (like a solid color gadget or a distant, untextured field).

## 4. UI Preparation
- **Hide the Imp**: Use the "Hide Imp" setting in the preferences or hide it via logic.
- **Clean HUD**: Turn off all on-screen displays and menus.
