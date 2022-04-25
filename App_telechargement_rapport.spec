# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['App_telechargement_rapport.py'],
             pathex=[],
             binaries=[ ( '/usr/lib/libiodbc.2.dylib', '.' ) ],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('./Images/logo-eronvidal-171x63.jpg', './Images/logo-eronvidal-171x63.jpg', 'DATA')]

exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='App_telechargement_rapport',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True,
            icon=None)

app = BUNDLE(exe,
             name='App_telechargement_rapport.app',
             icon=None,
             version='0.0.3',
             bundle_identifier=None,
             info_plist={
                   'NSPrincipalClass': 'NSApplication',
                   'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'My File Format',
                    'CFBundleTypeIconFile': 'MyFileIcon.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'LSHandlerRank': 'Owner'
                    }
                ]
                })
