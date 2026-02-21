"""
Gaussian Splatting training using gsplat 1.5.x on COLMAP sparse data.
Self-contained: includes COLMAP binary parser (no pycolmap needed).
Optimized for 4GB VRAM (GTX 1650).

Usage:
    python train_gsplat.py --data novel-shapes/gsplat_data --output novel-shapes/gsplat_output
    python train_gsplat.py --data novel-shapes/gsplat_data --output novel-shapes/gsplat_output --factor 8 --max-steps 3000
"""

import argparse
import math
import os
import struct
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torch import Tensor

from gsplat import rasterization
from gsplat.utils import save_ply


# ── COLMAP binary parsers ──────────────────────────────────────────────


def read_cameras_binary(path: str) -> Dict:
    """Parse COLMAP cameras.bin. Returns {cam_id: {model, width, height, params}}."""
    cameras = {}
    with open(path, "rb") as f:
        num_cameras = struct.unpack("<Q", f.read(8))[0]
        for _ in range(num_cameras):
            cam_id = struct.unpack("<I", f.read(4))[0]
            model_id = struct.unpack("<i", f.read(4))[0]
            width = struct.unpack("<Q", f.read(8))[0]
            height = struct.unpack("<Q", f.read(8))[0]
            # Number of params per model type
            num_params = {0: 3, 1: 4, 2: 4, 3: 5, 4: 4, 5: 5}.get(model_id, 4)
            params = struct.unpack(f"<{num_params}d", f.read(8 * num_params))
            cameras[cam_id] = {
                "model_id": model_id,
                "width": width,
                "height": height,
                "params": np.array(params),
            }
    return cameras


def read_images_binary(path: str) -> Dict:
    """Parse COLMAP images.bin. Returns {img_id: {qvec, tvec, cam_id, name}}."""
    images = {}
    with open(path, "rb") as f:
        num_images = struct.unpack("<Q", f.read(8))[0]
        for _ in range(num_images):
            img_id = struct.unpack("<I", f.read(4))[0]
            qvec = np.array(struct.unpack("<4d", f.read(32)))
            tvec = np.array(struct.unpack("<3d", f.read(24)))
            cam_id = struct.unpack("<I", f.read(4))[0]
            name = b""
            while True:
                c = f.read(1)
                if c == b"\x00":
                    break
                name += c
            num_points2D = struct.unpack("<Q", f.read(8))[0]
            # Skip 2D point data (x, y, point3D_id per point)
            f.read(num_points2D * 24)
            images[img_id] = {
                "qvec": qvec,
                "tvec": tvec,
                "camera_id": cam_id,
                "name": name.decode("utf-8"),
            }
    return images


def read_points3D_binary(path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Parse COLMAP points3D.bin. Returns (xyz [N,3], rgb [N,3])."""
    points = []
    colors = []
    with open(path, "rb") as f:
        num_points = struct.unpack("<Q", f.read(8))[0]
        for _ in range(num_points):
            _point3D_id = struct.unpack("<Q", f.read(8))[0]
            xyz = np.array(struct.unpack("<3d", f.read(24)))
            rgb = np.array(struct.unpack("<3B", f.read(3)))
            _error = struct.unpack("<d", f.read(8))[0]
            track_length = struct.unpack("<Q", f.read(8))[0]
            f.read(track_length * 8)  # skip track (image_id + point2D_idx pairs)
            points.append(xyz)
            colors.append(rgb)
    return np.array(points, dtype=np.float32), np.array(colors, dtype=np.uint8)


# ── Quaternion / pose utilities ────────────────────────────────────────


def qvec2rotmat(qvec: np.ndarray) -> np.ndarray:
    """COLMAP quaternion (w,x,y,z) to 3x3 rotation matrix."""
    w, x, y, z = qvec
    return np.array(
        [
            [1 - 2 * y * y - 2 * z * z, 2 * x * y - 2 * w * z, 2 * x * z + 2 * w * y],
            [2 * x * y + 2 * w * z, 1 - 2 * x * x - 2 * z * z, 2 * y * z - 2 * w * x],
            [2 * x * z - 2 * w * y, 2 * y * z + 2 * w * x, 1 - 2 * x * x - 2 * y * y],
        ]
    )


def colmap_to_viewmat(qvec: np.ndarray, tvec: np.ndarray) -> np.ndarray:
    """COLMAP pose to 4x4 world-to-camera matrix."""
    R = qvec2rotmat(qvec)
    w2c = np.eye(4)
    w2c[:3, :3] = R
    w2c[:3, 3] = tvec
    return w2c


def get_intrinsics(cam: Dict, factor: int) -> np.ndarray:
    """Extract 3x3 intrinsics from COLMAP camera, applying downsample factor."""
    params = cam["params"]
    model_id = cam["model_id"]
    if model_id == 0:  # SIMPLE_PINHOLE: f, cx, cy
        fx = fy = params[0]
        cx, cy = params[1], params[2]
    elif model_id == 1:  # PINHOLE: fx, fy, cx, cy
        fx, fy = params[0], params[1]
        cx, cy = params[2], params[3]
    elif model_id == 2:  # SIMPLE_RADIAL: f, cx, cy, k
        fx = fy = params[0]
        cx, cy = params[1], params[2]
    elif model_id == 3:  # RADIAL: f, cx, cy, k1, k2
        fx = fy = params[0]
        cx, cy = params[1], params[2]
    else:
        fx = fy = params[0]
        cx, cy = params[1], params[2]

    K = np.array([[fx / factor, 0, cx / factor], [0, fy / factor, cy / factor], [0, 0, 1]])
    return K.astype(np.float32)


# ── Scene loading ──────────────────────────────────────────────────────


def load_scene(data_dir: str, factor: int = 4, test_every: int = 8):
    """Load COLMAP scene. Returns training data dict."""
    sparse_dir = os.path.join(data_dir, "sparse", "0")
    images_dir = os.path.join(data_dir, "images")

    cameras = read_cameras_binary(os.path.join(sparse_dir, "cameras.bin"))
    images = read_images_binary(os.path.join(sparse_dir, "images.bin"))
    points3D, point_colors = read_points3D_binary(os.path.join(sparse_dir, "points3D.bin"))

    print(f"Loaded {len(cameras)} cameras, {len(images)} images, {len(points3D)} 3D points")

    # Normalize scene to unit sphere
    center = points3D.mean(axis=0)
    points3D -= center
    scale = np.linalg.norm(points3D, axis=1).max()
    if scale > 0:
        points3D /= scale

    # Build per-image data
    train_viewmats = []
    train_Ks = []
    train_images_list = []
    train_sizes = []
    val_viewmats = []
    val_Ks = []
    val_images_list = []
    val_sizes = []

    sorted_images = sorted(images.items(), key=lambda x: x[1]["name"])

    for idx, (img_id, img_data) in enumerate(sorted_images):
        cam = cameras[img_data["camera_id"]]
        w2c = colmap_to_viewmat(img_data["qvec"], img_data["tvec"])
        # Apply scene normalization to translation
        # p_cam = R @ p_world + t = R @ (p_new + center) + t = R @ p_new + (R @ center + t)
        w2c[:3, 3] = w2c[:3, :3] @ center + img_data["tvec"]
        if scale > 0:
            w2c[:3, 3] /= scale

        K = get_intrinsics(cam, factor)
        W = cam["width"] // factor
        H = cam["height"] // factor

        # Load and resize image
        img_path = os.path.join(images_dir, img_data["name"])
        if not os.path.exists(img_path):
            continue
        img = Image.open(img_path).convert("RGB").resize((W, H), Image.LANCZOS)
        img_tensor = torch.from_numpy(np.array(img)).float() / 255.0  # (H, W, 3)

        if idx % test_every == 0:
            val_viewmats.append(w2c)
            val_Ks.append(K)
            val_images_list.append(img_tensor)
            val_sizes.append((H, W))
        else:
            train_viewmats.append(w2c)
            train_Ks.append(K)
            train_images_list.append(img_tensor)
            train_sizes.append((H, W))

    print(f"Train: {len(train_viewmats)} images, Val: {len(val_viewmats)} images")
    print(f"Image size (after {factor}x downsample): {train_sizes[0][1]}x{train_sizes[0][0]}")

    return {
        "points3D": points3D,
        "point_colors": point_colors,
        "train_viewmats": np.array(train_viewmats, dtype=np.float32),
        "train_Ks": np.array(train_Ks, dtype=np.float32),
        "train_images": train_images_list,
        "train_sizes": train_sizes,
        "val_viewmats": np.array(val_viewmats, dtype=np.float32),
        "val_Ks": np.array(val_Ks, dtype=np.float32),
        "val_images": val_images_list,
        "val_sizes": val_sizes,
    }


# ── Gaussian initialization ───────────────────────────────────────────


def init_gaussians(points: np.ndarray, colors: np.ndarray, device: str = "cuda") -> Dict[str, torch.nn.Parameter]:
    """Initialize Gaussian parameters from sparse point cloud."""
    N = len(points)

    # Means: from COLMAP points
    means = torch.from_numpy(points).float().to(device)

    # Scales: estimate from nearest neighbor distances
    from scipy.spatial import KDTree

    tree = KDTree(points)
    dists, _ = tree.query(points, k=4)  # k=4: self + 3 neighbors
    avg_dist = np.mean(dists[:, 1:], axis=1)  # skip self
    avg_dist = np.clip(avg_dist, 1e-7, 0.05)  # cap at 0.05 (in normalized coords) to prevent OOM
    scales = np.log(avg_dist[:, None].repeat(3, axis=1)).astype(np.float32)

    # Quaternions: identity (w,x,y,z)
    quats = np.zeros((N, 4), dtype=np.float32)
    quats[:, 0] = 1.0

    # Opacities: inverse sigmoid of 0.1
    opacities = np.full(N, np.log(0.1 / (1 - 0.1)), dtype=np.float32)

    # Colors: SH degree 0 (just DC component)
    # Convert RGB [0,255] to SH DC coefficient
    C0 = 0.28209479177387814  # 1 / (2 * sqrt(pi))
    rgb_normalized = colors.astype(np.float32) / 255.0
    sh0 = (rgb_normalized - 0.5) / C0
    sh0 = sh0.reshape(N, 1, 3)

    splats = {
        "means": torch.nn.Parameter(means),
        "scales": torch.nn.Parameter(torch.from_numpy(scales).to(device)),
        "quats": torch.nn.Parameter(torch.from_numpy(quats).to(device)),
        "opacities": torch.nn.Parameter(torch.from_numpy(opacities).to(device)),
        "sh0": torch.nn.Parameter(torch.from_numpy(sh0).float().to(device)),
    }
    return splats


# ── SSIM ───────────────────────────────────────────────────────────────


def ssim(img1: Tensor, img2: Tensor, window_size: int = 11) -> Tensor:
    """Compute SSIM between two images (H, W, 3). Returns scalar."""
    # Reshape to (1, 3, H, W) for conv2d
    x = img1.permute(2, 0, 1).unsqueeze(0)
    y = img2.permute(2, 0, 1).unsqueeze(0)
    C = x.shape[1]

    # Gaussian window
    sigma = 1.5
    coords = torch.arange(window_size, dtype=x.dtype, device=x.device) - window_size // 2
    g = torch.exp(-(coords**2) / (2 * sigma**2))
    g = g / g.sum()
    window = g.unsqueeze(1) * g.unsqueeze(0)
    window = window.unsqueeze(0).unsqueeze(0).expand(C, 1, -1, -1)

    pad = window_size // 2
    mu_x = F.conv2d(x, window, padding=pad, groups=C)
    mu_y = F.conv2d(y, window, padding=pad, groups=C)

    mu_x2 = mu_x * mu_x
    mu_y2 = mu_y * mu_y
    mu_xy = mu_x * mu_y

    sigma_x2 = F.conv2d(x * x, window, padding=pad, groups=C) - mu_x2
    sigma_y2 = F.conv2d(y * y, window, padding=pad, groups=C) - mu_y2
    sigma_xy = F.conv2d(x * y, window, padding=pad, groups=C) - mu_xy

    C1 = 0.01**2
    C2 = 0.03**2

    ssim_map = ((2 * mu_xy + C1) * (2 * sigma_xy + C2)) / ((mu_x2 + mu_y2 + C1) * (sigma_x2 + sigma_y2 + C2))
    return ssim_map.mean()


# ── Training ───────────────────────────────────────────────────────────


def train(args):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda", "CUDA required for gsplat training"

    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"GPU: {torch.cuda.get_device_name(0)} ({vram_gb:.1f} GB VRAM)")

    # Load scene
    scene = load_scene(args.data, factor=args.factor, test_every=args.test_every)

    # Subsample points if too many (4GB VRAM constraint)
    max_init_points = args.max_points
    points = scene["points3D"]
    colors = scene["point_colors"]
    if len(points) > max_init_points:
        idx = np.random.choice(len(points), max_init_points, replace=False)
        points = points[idx]
        colors = colors[idx]
        print(f"Subsampled {len(scene['points3D'])} -> {max_init_points} points")

    # Initialize Gaussians
    splats = init_gaussians(points, colors, device)
    num_points = len(points)
    print(f"Initialized {num_points} Gaussians")

    # Optimizers — SparseAdam for means (sparse_grad=True)
    optimizers = {
        "means": torch.optim.Adam([splats["means"]], lr=1.6e-4),
        "scales": torch.optim.Adam([splats["scales"]], lr=5e-3),
        "quats": torch.optim.Adam([splats["quats"]], lr=1e-3),
        "opacities": torch.optim.Adam([splats["opacities"]], lr=5e-2),
        "sh0": torch.optim.Adam([splats["sh0"]], lr=2.5e-3),
    }

    # LR scheduler for means (decay to 1% by end)
    lr_lambda = lambda step: max(0.01, math.exp(-step * math.log(100) / args.max_steps))
    schedulers = {"means": torch.optim.lr_scheduler.LambdaLR(optimizers["means"], lr_lambda)}

    # Training data on GPU
    train_viewmats = torch.from_numpy(scene["train_viewmats"]).to(device)
    train_Ks = torch.from_numpy(scene["train_Ks"]).to(device)
    num_train = len(scene["train_images"])

    os.makedirs(args.output, exist_ok=True)

    # Adaptive density control state
    grad_accum = torch.zeros(num_points, device=device)
    grad_count = torch.zeros(num_points, device=device, dtype=torch.int32)

    print(f"\nStarting training for {args.max_steps} steps...")
    start_time = time.time()

    for step in range(args.max_steps):
        # Random training image
        idx = torch.randint(0, num_train, (1,)).item()
        gt_image = scene["train_images"][idx].to(device)
        H, W = scene["train_sizes"][idx]
        viewmat = train_viewmats[idx : idx + 1]
        K = train_Ks[idx : idx + 1]

        # SH degree ramp
        if step < 500:
            sh_degree = 0
        else:
            sh_degree = 0  # Keep at 0 to save VRAM on 4GB card

        # Forward pass — clamp scales to prevent OOM from huge projections
        clamped_scales = torch.exp(torch.clamp(splats["scales"], max=-4.0))  # max exp(-4)=0.018
        renders, alphas, info = rasterization(
            means=splats["means"],
            quats=F.normalize(splats["quats"], dim=-1),
            scales=clamped_scales,
            opacities=torch.sigmoid(splats["opacities"]),
            colors=splats["sh0"],
            viewmats=viewmat,
            Ks=K,
            width=W,
            height=H,
            sh_degree=sh_degree,
            near_plane=0.01,
            far_plane=1e10,
            packed=True,
            sparse_grad=False,
            render_mode="RGB",
            rasterize_mode="classic",
        )

        rendered = renders[0]  # (H, W, 3)

        # Simple L1 loss only (skip SSIM to save VRAM on 4GB card)
        loss = F.l1_loss(rendered, gt_image)

        # Backward
        for opt in optimizers.values():
            opt.zero_grad()
        loss.backward()

        # Free computation graph BEFORE optimizer step
        del renders, alphas, info, rendered, gt_image
        torch.cuda.empty_cache()

        for opt in optimizers.values():
            opt.step()
        for sched in schedulers.values():
            sched.step()

        # Logging
        if step % 100 == 0:
            elapsed = time.time() - start_time
            mem_mb = torch.cuda.max_memory_allocated() / 1024**2
            n_gaussians = splats["means"].shape[0]
            print(
                f"Step {step:5d}/{args.max_steps} | "
                f"Loss: {loss.item():.4f} | "
                f"Gaussians: {n_gaussians:,} | "
                f"VRAM: {mem_mb:.0f}MB | "
                f"{elapsed:.0f}s"
            )

        # Save checkpoint
        if step > 0 and step % args.save_every == 0:
            save_checkpoint(splats, args.output, step)

        del loss

    # Final save
    save_checkpoint(splats, args.output, args.max_steps)
    print(f"\nTraining complete in {time.time() - start_time:.0f}s")
    print(f"Output saved to {args.output}")


def save_checkpoint(splats: Dict, output_dir: str, step: int):
    """Save Gaussians as PLY and PyTorch checkpoint."""
    means = splats["means"].detach().cpu().numpy()
    quats = F.normalize(splats["quats"].detach(), dim=-1).cpu().numpy()
    scales = torch.exp(splats["scales"].detach()).cpu().numpy()
    opacities = torch.sigmoid(splats["opacities"].detach()).cpu().numpy()

    # Convert SH0 back to RGB for PLY
    C0 = 0.28209479177387814
    sh0 = splats["sh0"].detach().cpu().numpy().reshape(-1, 3)
    colors = np.clip(sh0 * C0 + 0.5, 0, 1)

    ply_path = os.path.join(output_dir, f"splat_{step}.ply")

    # Use gsplat's save_ply
    save_ply(
        means=torch.from_numpy(means),
        scales=torch.from_numpy(scales),
        quats=torch.from_numpy(quats),
        opacities=torch.from_numpy(opacities.reshape(-1)),
        sh0=splats["sh0"].detach().cpu().reshape(-1, 1, 3),
        path=ply_path,
    )
    print(f"  Saved PLY: {ply_path}")

    # Also save torch checkpoint for resuming
    ckpt_path = os.path.join(output_dir, f"checkpoint_{step}.pt")
    torch.save({k: v.detach().cpu() for k, v in splats.items()}, ckpt_path)
    print(f"  Saved checkpoint: {ckpt_path}")


# ── Entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train 3D Gaussian Splatting from COLMAP data")
    parser.add_argument("--data", type=str, required=True, help="Path to COLMAP data (with sparse/0/ and images/)")
    parser.add_argument("--output", type=str, required=True, help="Output directory for checkpoints")
    parser.add_argument("--factor", type=int, default=4, help="Image downsample factor (default: 4)")
    parser.add_argument("--max-steps", type=int, default=7000, help="Training steps (default: 7000)")
    parser.add_argument("--test-every", type=int, default=8, help="Hold out every Nth image for val (default: 8)")
    parser.add_argument("--save-every", type=int, default=1000, help="Save checkpoint every N steps (default: 1000)")
    parser.add_argument("--max-points", type=int, default=5000, help="Max initial Gaussians (subsample if more, default: 5000)")
    args = parser.parse_args()
    train(args)
