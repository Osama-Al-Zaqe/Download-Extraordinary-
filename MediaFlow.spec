# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Paths
base_dir = os.path.abspath(SPECPATH)
static_dir = os.path.join(base_dir, "app", "static")

# Locate FFmpeg binary from imageio_ffmpeg
ffmpeg_src = None
try:
    import imageio_ffmpeg
    ffmpeg_src = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    pass

datas = [
    (static_dir, os.path.join("app", "static")),
]

if ffmpeg_src and os.path.exists(ffmpeg_src):
    datas.append((ffmpeg_src, "."))
    datas.append((ffmpeg_src, os.path.join("imageio_ffmpeg", "binaries")))

hiddenimports = [
    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespans",
    "uvicorn.lifespans.on",
    "uvicorn.lifespans.off",
    "fastapi",
    "starlette",
    "starlette.routing",
    "starlette.middleware",
    "starlette.responses",
    "pydantic",
    "pydantic_core",
    "sqlite3",
    "requests",
    "yt_dlp",
    "webview",
]

a = Analysis(
    ['main.py'],
    pathex=[base_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MediaFlow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keeps console visible so users can see startup logs or debug if needed
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
