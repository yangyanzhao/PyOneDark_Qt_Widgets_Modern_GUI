# -*- mode: python ; coding: utf-8 -*-
import os
import site
# 找到第三方依赖的路径
site_packages_dirs = site.getsitepackages()
dayu_widgets_path = None
for site_packages_dir in site_packages_dirs:
    potential_path = os.path.join(site_packages_dir, 'dayu_widgets')
    if os.path.exists(potential_path):
        dayu_widgets_path = potential_path
        break
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[("./settings.json","."),("./gui","./gui"),("./modules","./modules"),(dayu_widgets_path, "dayu_widgets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,# 是否显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
