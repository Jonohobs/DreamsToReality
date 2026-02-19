@echo off
echo === Dreams to Reality - RealityScan v3 (segmented frames, no AI masks) ===
echo.

set RS="C:\Program Files\Epic Games\RealityScan_2.1\RealityScan.exe"
set FRAMES=C:\Users\jonat\dreams-to-reality\novel-shapes\segmented_100
set OUTPUT=C:\Users\jonat\dreams-to-reality\novel-shapes\reconstruction

%RS% ^
  -addFolder "%FRAMES%" ^
  -align ^
  -selectMaximalComponent ^
  -setReconstructionRegionByDensity ^
  -calculateHighModel ^
  -cleanModel ^
  -closeHoles ^
  -smooth ^
  -selectLargeTrianglesRel 10 ^
  -removeSelectedTriangles ^
  -calculateTexture ^
  -save "%OUTPUT%\realityscan_v3.rsproj"

echo.
echo === Done! ===
pause
