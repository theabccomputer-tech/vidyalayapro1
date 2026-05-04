# VidyalayaPro.spec
# EXE banane ke liye: pyinstaller VidyalayaPro.spec

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Saare template aur static files include karo
added_files = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('license_generator.py', '.'),
    ('license_checker.py', '.'),
]

# License file agar exist karti hai
if os.path.exists('license.json'):
    added_files.append(('license.json', '.'))

a = Analysis(
    ['launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'flask', 'flask_sqlalchemy', 'werkzeug', 'werkzeug.security',
        'werkzeug.utils', 'sqlalchemy', 'jinja2', 'cryptography',
        'cryptography.fernet', 'cryptography.hazmat',
        'email_validator', 'click', 'itsdangerous',
        'markupsafe', 'sqlalchemy.dialects.sqlite',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'PIL'],
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
    name='VidyalayaPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,          # Console dikhega — server status ke liye
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,             # Apna icon add kar sakte ho: icon='school.ico'
)
