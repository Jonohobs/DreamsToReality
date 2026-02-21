import struct
import numpy as np
import cv2
from pathlib import Path

def visualize_ply(ply_path, output_path):
    print(f"Loading {ply_path}...")
    
    with open(ply_path, 'rb') as f:
        # Read header to find end_header and vertex count
        header = ""
        has_normals = False
        while "end_header" not in header:
            line = f.readline().decode('ascii')
            header += line
            if "element vertex" in line:
                num_vertices = int(line.split()[-1])
            if "property float nx" in line:
                has_normals = True
        
        print(f"Found {num_vertices} vertices. Normals: {has_normals}")
        
        stride = 27 if has_normals else 15
        unpack_fmt = '<ffffffBBB' if has_normals else '<fffBBB'
        
        data = f.read(num_vertices * stride)
        
    vertices = []
    colors = []
    
    for i in range(num_vertices):
        offset = i * stride
        v = struct.unpack(unpack_fmt, data[offset:offset+stride])
        vertices.append(v[:3])  # x, y, z
        if has_normals:
            colors.append(v[6:9])   # r, g, b (after normals)
        else:
            colors.append(v[3:6])   # r, g, b (immediately after xyz)
        
    pts = np.array(vertices)
    cols = np.array(colors)

    # 1. Centering and Outlier Removal
    centroid = np.mean(pts, axis=0)
    pts -= centroid
    
    # Simple outlier removal: only keep points within 1.5 std devs of the mean
    # This filters out stray points that make the object look small/fuzzy
    dists = np.linalg.norm(pts, axis=1)
    mean_dist = np.mean(dists)
    std_dist = np.std(dists)
    mask = dists < (mean_dist + 1.5 * std_dist)
    pts = pts[mask]
    cols = cols[mask]
    
    # Recenter after outlier removal
    centroid = np.mean(pts, axis=0)
    pts -= centroid

    # 2. Add some rotation (y-up to z-up or whatever matches the scene better)
    angle_y = np.radians(45)
    angle_x = np.radians(-15)
    
    Ry = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    
    pts = pts @ Ry @ Rx

    # 3. Project to 2D
    img_size = 1024
    margin = 80
    
    # Zoom to fit the filtered points
    # We use a robust max to avoid being clipped by single outliers
    max_val = np.percentile(np.abs(pts[:, :2]), 99) 
    scale = (img_size - 2 * margin) / (2 * max_val)
    
    x_2d = (pts[:, 0] * scale + img_size / 2).astype(int)
    y_2d = (pts[:, 1] * scale + img_size / 2).astype(int)
    
    # 4. Create Image
    canvas = np.zeros((img_size, img_size, 3), dtype=np.uint8)
    
    # Sort by Z for simple occlusion
    z_indices = np.argsort(pts[:, 2])
    
    for idx in z_indices:
        px, py = x_2d[idx], y_2d[idx]
        if 0 <= px < img_size and 0 <= py < img_size:
            # OpenCV uses BGR
            color = (int(cols[idx, 2]), int(cols[idx, 1]), int(cols[idx, 0]))
            # Larger point radius to make it feel more solid like the Dreams source
            cv2.circle(canvas, (px, py), 3, color, -1)

    # Dilate and blur to bridge the gaps in the "soft" Dreams shapes
    kernel = np.ones((3,3), np.uint8)
    canvas = cv2.dilate(canvas, kernel, iterations=1)
    canvas = cv2.GaussianBlur(canvas, (3,3), 0)

    cv2.imwrite(output_path, canvas)
    print(f"Saved enhanced visualization to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_ply', help="Path to input .ply file")
    parser.add_argument('output_png', help="Path to output .png file")
    args = parser.parse_args()
    
    ply_f = Path(args.input_ply)
    if ply_f.exists():
        visualize_ply(ply_f, args.output_png)
    else:
        print(f"Error: {ply_f} not found.")
