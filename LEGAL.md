# Legal Defence — Dreams to Reality

**Project:** Dreams to Reality (Photogrammetry Pipeline for PlayStation Dreams)
**Author:** Jonathan Hobson
**Last Updated:** 2026-02-16

---

## Executive Summary

Dreams to Reality is a **photogrammetry tool** that reconstructs 3D models from standard video recordings of PlayStation Dreams creations. It uses only publicly available computer vision algorithms (COLMAP, Structure-from-Motion) applied to videos that users themselves export via PlayStation 5's built-in capture feature.

This document establishes the legal basis for the project's legitimacy under UK, EU, and US law.

---

## 1. No Reverse Engineering

Dreams to Reality does **not** reverse engineer any Sony or Media Molecule software.

| What we do | What we don't do |
|------------|-----------------|
| Apply standard photogrammetry to exported video | Decompile, disassemble, or probe Dreams engine code |
| Use publicly available CV algorithms (COLMAP, OpenCV) | Access Dreams' internal APIs, save files, or data formats |
| Process MP4 files exported via PS5's built-in capture | Intercept, modify, or inject data into the Dreams application |
| Reconstruct 3D geometry from visual data | Extract or read Dreams' proprietary SDF representation |

The project treats Dreams output identically to any other video source — the same pipeline could reconstruct 3D models from video of physical objects, other games, or any visual media.

**Legal basis:**
- UK Computer Misuse Act 1990 — no unauthorised access to computer material occurs
- No circumvention of technical protection measures (no DRM bypass)

---

## 2. No DRM Circumvention

The project does **not** circumvent any copy protection, digital rights management, or technological protection measures.

- Videos are exported using **PS5's built-in capture feature**, which Sony explicitly provides to all users
- No HDMI capture devices or signal interception is required
- No encryption is bypassed
- No access controls are defeated

**Legal basis:**
- UK Copyright, Designs and Patents Act 1988, s.296ZA — no circumvention of effective technological measures
- US Digital Millennium Copyright Act (DMCA) §1201 — no circumvention of access controls
- EU Copyright Directive 2001/29/EC, Art. 6 — no circumvention of technological measures

---

## 3. User Ownership of Creative Content

Dreams users **create original works** within Dreams using its sculpting, painting, and design tools. These creations are the intellectual property of their creators.

**Key arguments:**

### 3.1 Dreams' Own Positioning
Media Molecule markets Dreams as a "creation" tool — the entire value proposition is that users make their own content. The game's tagline is "Made in Dreams" and it encourages sharing and showcasing creations.

### 3.2 User-Generated Content Rights
Under UK copyright law (CDPA 1988), the author of an original work is the first owner of copyright. When a user sculpts an original 3D creation in Dreams, they hold copyright in the artistic work, even though it's expressed through Dreams' tools.

**Analogy:** A painter who uses Photoshop owns the copyright in their painting, not Adobe. A musician who uses GarageBand owns their composition, not Apple.

### 3.3 Right to Export One's Own Work
Users have a legitimate interest in accessing their own creative works in portable formats. Dreams to Reality enables this — it helps creators liberate their own work from a platform-locked format.

---

## 4. Interoperability Defence

### 4.1 UK Law
The Copyright, Designs and Patents Act 1988, s.50B permits decompilation for interoperability purposes. While this project doesn't decompile anything, the broader principle supports tools that enable data portability between systems.

### 4.2 EU Law
- **Computer Programs Directive 2009/24/EC, Art. 6** — permits acts necessary for interoperability
- **Digital Markets Act (DMA) 2022** — establishes rights to data portability (though primarily aimed at gatekeepers)
- **GDPR Art. 20** — right to data portability for personal data

### 4.3 US Law
- **Fair use** (17 U.S.C. §107) — transformative use for interoperability has been upheld (see *Google LLC v. Oracle America, Inc.*, 2021)
- **Sega v. Accolade (1992)** — reverse engineering for interoperability is fair use (though we don't reverse engineer)

---

## 5. Transformative Use

The output of Dreams to Reality is fundamentally different from the input:

| Input | Output |
|-------|--------|
| 2D video frames (MP4) | 3D point clouds and meshes (OBJ, PLY, GLTF) |
| Flat pixel data | Geometric reconstruction with depth |
| Platform-locked playback | Portable 3D assets for any application |

This is **transformative** — we create new works (3D models) from existing material (2D video), adding substantial new value and changing the nature, purpose, and character of the work.

---

## 6. Research & Education Defence

This project constitutes **legitimate computer vision research**, exploring:
- Photogrammetry applied to non-traditional rendering (SDF/fleck-based)
- Structure-from-Motion performance on stylised (non-photorealistic) content
- Novel capture techniques for volumetric reconstruction

**Legal basis:**
- UK CDPA 1988, s.29 — fair dealing for research and private study
- UK CDPA 1988, s.30 — fair dealing for criticism, review, and quotation
- US fair use factor: educational/research purpose weighs in favour

---

## 7. Open Source Dependencies — Licence Compliance

All dependencies use permissive licences:

| Dependency | Licence | Compliant |
|------------|---------|-----------|
| OpenCV | BSD 3-Clause | Yes |
| NumPy | BSD | Yes |
| Pillow | HPND | Yes |
| rembg | MIT | Yes |
| COLMAP | BSD 3-Clause | Yes |
| FastAPI | MIT | Yes |
| React | MIT | Yes |
| Tailwind CSS | MIT | Yes |

No GPL or copyleft dependencies that would impose distribution requirements.

---

## 8. Potential Risks & Mitigations

### 8.1 Sony EULA / Dreams TOS
**Risk:** Sony's Terms of Service or Dreams' EULA may contain clauses restricting use of exported content.

**Mitigation:**
- Review and document specific TOS clauses
- Note that overly broad TOS restrictions may be unenforceable under UK Consumer Rights Act 2015 (unfair contract terms)
- The PS5 capture feature exists specifically to allow users to export content — restricting what they do with those exports would contradict the feature's purpose

### 8.2 Cease & Desist
**Risk:** Sony or Media Molecule could send a C&D letter.

**Mitigation:**
- This document establishes good-faith legal basis before any dispute
- No Sony trademarks are used in the project name or branding
- The project doesn't distribute any Sony copyrighted material
- Response strategy: engage respectfully, cite interoperability and user rights

### 8.3 "Dreams" in Project Name
**Risk:** Using "Dreams" could imply endorsement or association.

**Mitigation:**
- Project name is "Dreams to Reality" — descriptive, not claiming affiliation
- Add disclaimer: "Not affiliated with, endorsed by, or associated with Sony Interactive Entertainment or Media Molecule"
- Consider renaming if formally requested

---

## 9. Recommended Disclaimers

Add to README and any public-facing material:

```
DISCLAIMER

Dreams to Reality is an independent research project. It is not affiliated with,
endorsed by, or associated with Sony Interactive Entertainment, Media Molecule,
or PlayStation.

"PlayStation" and "Dreams" are trademarks of Sony Interactive Entertainment.
All trademarks are property of their respective owners.

This tool processes video files that users have exported using PlayStation 5's
built-in capture feature. It does not access, modify, or reverse engineer any
Sony software or systems.

Users are responsible for ensuring they have the right to process and export
content created in Dreams, including respecting the rights of other creators
whose work may appear in exported videos.
```

---

## 10. Recommended Next Steps

1. [ ] Add the disclaimer above to README.md
2. [ ] Add a LICENSE file (recommend MIT for open source, or keep proprietary)
3. [ ] Review PlayStation Network Terms of Service for specific export clauses
4. [ ] Review Media Molecule's Dreams community guidelines
5. [ ] Consider trademark search for "Dreams to Reality" name
6. [ ] If publishing: add contributor licence agreement (CLA) if accepting contributions
