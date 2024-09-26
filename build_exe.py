import PyInstaller.__main__

PyInstaller.__main__.run([
    'app_gui.py',
    '--onefile',
    '--windowed',
    '--add-data=app.py:.',
    '--add-data=Chanvre1.png:.',
    '--add-data=Chanvre2.png:.',
    '--add-data=Chanvre3.png:.',
    '--add-data=Chanvre4.png:.',
    '--add-data=Chanvre5.png:.',
    '--add-data=Chanvre6.png:.',
    '--add-data=Chanvre7.png:.',
    '--add-data=Chanvre8.png:.',
    '--add-data=Chanvre9.png:.',
    '--add-data=Chanvre10.png:.',
    '--add-data=Faucher.png:.',
    '--name=Recolteur',
])