# Dreams Photogrammetry Capture Tool — Build Guide

Step-by-step instructions for building the geometry pattern projector and camera rig inside Dreams on PS5.

---

## PART 1: THE CAPTURE AREA

### Step 1: Create the Platform (Red Cylinder)

1. Open a **blank scene** (Create → New Scene)
2. Open the **Sculpt Tool** (L1 menu → Tools → Sculpt)
3. In the shape picker, select **Cylinder**
4. Stamp a wide, flat cylinder:
   - Scale it wide (use R2 to place, tweak size in the Tweak Menu)
   - Keep it very thin/flat — this is a platform, not a pillar
5. Open Tweak Menu (press the touchpad or L1+X to scope in)
   - Set color to **bright red** (open color wheel)
   - Set finish to **Matte / Plastic** (low shine, low metallic)
   - This is your "record button" platform

### Step 2: Create the Boundary Lines (White Vertical Posts)

1. Still in Sculpt Tool, select **Cylinder** shape
2. Stamp 4-5 tall, thin vertical cylinders around the edge of the red platform
   - Space them evenly around the circumference
   - Make them tall enough to show the capture volume height
3. Color them **white**, finish **matte**
4. These show the user where to place their sculpt and how big it can be

### Step 3: Set Up Visibility Toggling

The platform and boundary lines need to **disappear during recording**.

1. Select all boundary lines + the red platform
2. Group them (L1 menu → Group)
3. Scope into the group (L1+X)
4. Find the **Visible** property in the tweak menu
5. We'll wire this to a logic signal later (Part 4) so it turns off during camera recording

---

## PART 2: THE PATTERN PROJECTOR (Geometry Pass)

The goal: spray colored shape confetti outward from center onto whatever sculpt the user places on the platform.

### Step 4: Create the Pattern Pieces (Tiny Sculpts)

You need to create **5-6 template shapes** that the Emitter will clone and spray:

**Shape 1 — White Triangle**
1. Sculpt Tool → select a small shape
2. Create a tiny triangle (flatten a sphere, pinch 3 corners, or stamp 3 thin cylinders into a triangle)
3. Make it SMALL — maybe 2-3cm across
4. Color: **White**, Finish: **Matte**
5. Name it "pattern-tri-white"

**Shape 2 — White Cross**
1. Create two tiny thin rectangles overlapping at 90 degrees
2. Color: **White**, Finish: **Matte**
3. Name it "pattern-cross-white"

**Shape 3 — Blue Square**
1. Small flat cube/square
2. Color: **Mid-blue**, Finish: **Matte**

**Shape 4 — Green Triangle**
1. Same as Shape 1 but **mid-green**

**Shape 5 — Red/Orange Square**
1. Small flat square, **orange**, Matte

**Shape 6 — White Diamond**
1. Small square rotated 45 degrees
2. **White**, Matte

For ALL pattern pieces, set these physics properties (Tweak Menu):
- **Moveable**: ON (so emitter can launch them)
- **Collidable**: ON (so they hit the sculpt)
- **Bounciness**: 0% (they stick, don't bounce off)
- **Friction**: 100% / Maximum (grip the surface)
- **Mass**: Very low (they're tiny confetti)

Move all template pieces **off to the side** or **inside a microchip** — they're templates, not placed directly in the scene.

### Step 5: Set Up the Emitter

1. Open Gadgets menu (L1 → Gadgets)
2. Find **Emitter** (under Objects or Create/Destroy section)
3. Place the Emitter at the **exact center** of the red platform, at roughly the middle height of the expected sculpt
4. Scope into the Emitter (L1+X) to configure:
   - **Object to Emit**: Wire the dashed output to one of your pattern pieces
   - **Emit Speed**: Medium-high (pieces need to fly outward and hit the sculpt)
   - **Emit Direction**: Configure to emit in all directions (spherical spread)
     - You may need multiple emitters pointing different directions (up, down, sides) or use the "spread" setting if available
   - **Time Between Emits**: Very short (0.05-0.1s) for rapid coverage
   - **Max Emitted At Once**: High (200-500) — you want dense coverage
   - **Recycle**: OFF for now (we want them to stay)

**For multiple shapes**: You'll need **one emitter per template shape**, or use a **Selector** gadget to cycle which template gets emitted. Simplest approach: use 5-6 emitters at center, each emitting a different shape, all firing simultaneously.

### Step 6: Make Emitters Fire Together

1. Place a **Microchip** (Gadgets → Logic)
2. Put all 5-6 Emitters inside the microchip
3. Add a **Timer** gadget inside the microchip
   - Set duration to ~3-5 seconds (enough time to cover the sculpt)
4. Wire the Timer output → each Emitter's power input
5. When the Timer runs, all emitters fire for 3-5 seconds then stop
6. The confetti sprays outward, hits the sculpt, and settles (high friction, no bounce)

---

## PART 3: THE CAMERA RIG

### Step 7: Create the Camera Boom Arm

1. Sculpt a **thin invisible rod** extending horizontally from the center point outward
   - Length: far enough that the camera has a good view of the full sculpt
   - Make it **non-visible in play mode** (Tweak Menu → Visible toggle, or set to invisible)
2. At the far end of the rod, place a **Camera** gadget:
   - Gadgets menu → Camera
   - Scope into Camera (L1+X) and set:
     - **Depth of Field / Aperture**: 0% (everything in focus — CRITICAL)
     - **FOV**: ~50-60 degrees (keep the sculpt filling 70-80% of frame)
     - **Look At**: Point it toward the center of the platform

### Step 8: Animate the Camera Orbit

We want the camera to spiral around the sculpt at multiple heights. Use **Keyframe Animation**.

**Ring 1 — High angle (looking down ~45 degrees)**

1. Position the camera boom at the **top-right** of the orbit, angled down at ~45 degrees
2. Open the **Keyframe** tool (Gadgets → Keyframes)
3. Create **Keyframe 1** — this is the starting position
4. Rotate the boom arm ~90 degrees around the center
5. Create **Keyframe 2**
6. Rotate another ~90 degrees → **Keyframe 3**
7. Rotate another ~90 degrees → **Keyframe 4**
8. Complete the circle → **Keyframe 5** (same height as KF1 but one full rotation later)

**Ring 2 — Eye level**

9. Lower the camera to eye level with the sculpt
10. Continue adding keyframes every ~90 degrees for another full orbit
11. Keyframes 6-9

**Ring 3 — Low angle (looking up ~30 degrees)**

12. Lower camera further, angle it slightly upward
13. Keyframes 10-13

**Put all keyframes on a Timeline:**
1. Gadgets → Timeline
2. Place all keyframes on the timeline in sequence
3. Space them evenly — aim for ~3-5 seconds per quarter-turn
4. Total orbit time: ~45-60 seconds for all 3 rings
5. Set the Timeline to **play once** (not loop)

### Step 9: Camera Settings Checklist

Scope into the camera and verify:
- [ ] Depth of Field: **OFF** (aperture 0%)
- [ ] FOV: **50-60 degrees** (consistent throughout)
- [ ] Bloom: **OFF** (if available in scene/sun settings)
- [ ] Lens Flare: **OFF**
- [ ] Motion Blur: **OFF** (check scene settings)

Also in Scene Settings (not the camera):
- [ ] Sun/Sky effects: **minimal or off**
- [ ] Use flat, even lighting (single neutral Sun gadget or studio lighting)

---

## PART 4: WIRE THE FULL SEQUENCE

The logic flow should be:

```
User places sculpt on platform
         |
    User presses START (controller input or in-scene button)
         |
    [1] Emitters fire for 3-5 seconds (pattern confetti sprays onto sculpt)
         |
    [2] Short pause — 2 seconds for pieces to settle
         |
    [3] Platform + boundary lines become INVISIBLE
         |
    [4] Camera timeline PLAYS (geometry pass orbit — ~60 seconds)
         |
    [5] Camera timeline ends
         |
    [6] DESTROYER fires — removes all emitted pattern pieces
         |
    [7] Short pause — 1 second
         |
    [8] Camera timeline PLAYS AGAIN (texture pass orbit — same path, clean sculpt)
         |
    [9] Camera timeline ends
         |
    [10] Platform + boundary lines become VISIBLE again
         |
         DONE — user has two recordings
```

### Step 10: Build the Sequence Logic

1. Create a **Microchip** called "Main Sequence"
2. Inside, place these gadgets and wire them in order:

**Trigger:**
- **Controller Sensor** or **Button** gadget → starts the sequence

**Step 1 — Emit patterns:**
- Wire trigger → Timer A (3-5 sec) → powers all Emitters

**Step 2 — Settle pause:**
- Wire Timer A "finished" output → Timer B (2 sec delay)

**Step 3 — Hide UI elements:**
- Wire Timer B "finished" → **NOT gate** → Platform group Visible input
  (NOT gate inverts the signal: when timer fires, visibility turns OFF)

**Step 4 — Start camera:**
- Wire Timer B "finished" → Timeline Play input

**Step 5-6 — Camera finishes, destroy patterns:**
- Wire Timeline "finished" output → Timer C (0.5 sec) → Destroyer gadget
- The Destroyer targets all emitted pattern pieces

**Step 7-8 — Second pass (texture):**
- Wire Destroyer "finished" → Timer D (1 sec) → Timeline Play input (again)

**Step 9-10 — Restore UI:**
- Wire Timeline "finished" (second time) → Platform group Visible input back ON

> **Note:** Triggering the Timeline twice requires either resetting it between plays or using a Counter/Selector to track which pass you're on. You may need a **Counter** set to 2, where count=1 triggers the destroyer and count=2 restores visibility.

---

## PART 5: TESTING & ADJUSTMENT

### Step 11: Test with a Simple Sculpt

1. Create a simple test sculpt (cube or sphere) and place it on the platform
2. Hit play mode and trigger the sequence
3. Watch for:
   - Do pattern pieces reach and cover the sculpt? (Adjust emit speed if not)
   - Do pieces bounce off? (Reduce bounciness to 0)
   - Do pieces slide off? (Increase friction)
   - Is the coverage dense enough? (Increase emit count or duration)
   - Does the camera path look smooth? (Adjust keyframe spacing)
   - Is the full sculpt visible in frame throughout? (Adjust camera distance/FOV)

### Step 12: Test with Different Sculpt Sizes

- Try a tall thin sculpt (like a lamp post)
- Try a wide flat sculpt (like a table)
- Make sure the emitters cover different proportions
- Adjust emit spread angle or add more emitters at different heights if needed

### Tips for User Experience

- The red platform + white lines clearly show "place your sculpt HERE"
- The user just places their sculpt and presses one button
- Both passes happen automatically
- They get two clean video recordings from the PS5's capture
- Those recordings feed into the external pipeline (preprocess → segment → COLMAP)

---

## QUICK REFERENCE — DREAMS CONTROLS

| Action | Button |
|--------|--------|
| Tool Menu | L1 |
| Scope In | L1 + X |
| Scope Out | L1 + Circle |
| Undo | D-Pad Left |
| Redo | D-Pad Right |
| Grab/Move | R2 hold |
| Clone | L1 + R2 |
| Rotate | L2 + motion/stick |
| Color Wheel | Bump controllers (Move) or Tweak Menu |
| Tweak Menu | Touchpad (or scope into object) |
| Play Mode | Start/Options button |

---

*Created 2026-02-14 for the Dreams to Reality project*
*Two-pass capture: Geometry (with patterns) → Texture (clean)*
