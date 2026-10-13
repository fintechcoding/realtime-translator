# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build spec for RealTime Translator (onedir, windowed GUI).

Build:   pyinstaller RealTimeTranslator.spec --noconfirm
Output:  dist/RealTimeTranslator/RealTimeTranslator.exe
"""

from PyInstaller.utils.hooks import collect_all

datas = [
    ("config.yaml", "."),                                   # seeded to %APPDATA% on first run
    ("app/gui/assets/app.ico", "app/gui/assets"),
    ("app/gui/assets/app.png", "app/gui/assets"),
]
binaries = []
hiddenimports = ["qasync", "PyQt6.QtSvg"]

# Packages that ship native binaries / data files and need a full collect.
for pkg in ("azure.cognitiveservices.speech", "sounddevice", "deepgram"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "PySide6", "PyQt5"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RealTimeTranslator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon="app/gui/assets/app.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="RealTimeTranslator",
)
