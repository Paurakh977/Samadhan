# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/pande/OneDrive/Desktop/PyQt/Samadhan-App/Scripts/main_file.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/pande/OneDrive/Desktop/PyQt/Samadhan-App/UI', 'UI')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main_file',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
