# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/backend/cli.py'],
    pathex=[],
    binaries=[],
    datas=[('config.env', '.'), ('src/migrations', 'migrations'),('src/alembic.ini', '.')],
    hiddenimports=["asyncpg.pgproto.pgproto", "fastapi_filter.ext.sqlalchemy", "fastapi_pagination.contrib.sqlalchemy", "zeroconf._utils.ipaddress", "zeroconf._handlers.answers"],
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
    a.binaries,
    a.datas,
    [],
    name='MedVoice-CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
