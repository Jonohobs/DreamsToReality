@echo off
echo === Setting up MSVC + CUDA environment ===
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" amd64

set PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.1\bin;%PATH%
set PATH=C:\Users\jonat\dreams-to-reality\nerfstudio-env\Scripts;%PATH%
set TORCH_CUDA_ARCH_LIST=7.5
set CCCL_IGNORE_MSVC_TRADITIONAL_PREPROCESSOR_WARNING=1

echo === Starting Gaussian Splatting training ===
cd /d C:\Users\jonat\dreams-to-reality
nerfstudio-env\Scripts\python.exe train_gsplat.py --data novel-shapes/gsplat_data --output novel-shapes/gsplat_output --factor 8 --max-steps 7000 --save-every 1000

echo === Done ===
pause
