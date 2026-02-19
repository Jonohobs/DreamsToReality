@echo off
set COLMAP_DIR=C:\Users\jonat\dreams-to-reality\COLMAP\COLMAP-3.9.1-windows-cuda
set PATH=%COLMAP_DIR%\lib;%PATH%
set QT_PLUGIN_PATH=%COLMAP_DIR%\lib\plugins

"%COLMAP_DIR%\bin\colmap.exe" patch_match_stereo --workspace_path "C:\Users\jonat\dreams-to-reality\novel-shapes\reconstruction\dense" --workspace_format COLMAP --PatchMatchStereo.max_image_size 1000 --PatchMatchStereo.gpu_index 0

echo.
echo patch_match_stereo complete! Now run stereo fusion:
echo "%COLMAP_DIR%\bin\colmap.exe" stereo_fusion --workspace_path "C:\Users\jonat\dreams-to-reality\novel-shapes\reconstruction\dense" --workspace_format COLMAP --output_path "C:\Users\jonat\dreams-to-reality\novel-shapes\reconstruction\dense\fused.ply" --output_type PLY
pause
