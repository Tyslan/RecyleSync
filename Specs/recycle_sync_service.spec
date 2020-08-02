# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['../Source/recycle_sync_service.py'],
             pathex=['/home/lorenz/Documenten/PythonProjects/RecyleSync'],
             binaries=[],
             datas=[('/home/lorenz/Documenten/PythonProjects/RecyleSync/.venv/lib/python3.8/site-packages/ics/grammar/contentline.ebnf','./ics/grammar/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='recycle_sync_service',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
