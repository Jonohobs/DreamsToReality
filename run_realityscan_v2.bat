@echo off
echo === Dreams to Reality - RealityScan Pipeline v2 ===
echo.

set RS="C:\Program Files\Epic Games\RealityScan_2.1\RealityScan.exe"
set FRAMES=C:\Users\jonat\dreams-to-reality\novel-shapes\subsample_100
set OUTPUT=C:\Users\jonat\dreams-to-reality\novel-shapes\reconstruction

%RS% ^
  -addFolder "%FRAMES%" ^
  -generateAIMasks ^
  -align ^
  -selectMaximalComponent ^
  -setReconstructionRegionAuto ^
  -calculateHighModel ^
  -cleanModel ^
  -closeHoles ^
  -smooth ^
  -calculateTexture ^
  -calculateVertexColors ^
  -selectLargeTrianglesRel 10 ^
  -removeSelectedTriangles ^
  -save "%OUTPUT%\realityscan_project.rsproj"

echo.
echo === Done! Project saved to %OUTPUT%\realityscan_project.rsproj ===
pause
