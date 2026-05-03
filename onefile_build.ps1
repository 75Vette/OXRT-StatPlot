$ErrorActionPreference = "Stop"

Write-Host "Building OXRT-StatPlot 1.0.2 with Nuitka..."

py -3.12 -m nuitka `
  --onefile `
  --enable-plugin=pyside6 `
  --include-qt-plugins=sensible `
  --lto=yes `
  --clang `
  --assume-yes-for-downloads `
  --remove-output `
  --nofollow-import-to=tkinter `
  --nofollow-import-to=matplotlib.backends.tkagg `
  --include-data-dir=src/assets=assets `
  --noinclude-pytest-mode=nofollow `
  --noinclude-setuptools-mode=nofollow `
  --noinclude-unittest-mode=nofollow `
  --python-flag=no_docstrings `
  --python-flag=no_asserts `
  --windows-console-mode=disable `
  --windows-icon-from-ico=src/assets/statplotfav.ico `
  --windows-company-name="75Vette" `
  --windows-product-name="OXRT-StatPlot" `
  --windows-file-version="1.0.2" `
  --windows-product-version="1.0.2" `
  --windows-file-description="OXRT-StatPlot 1.0.2" `
  --output-filename=OXRT-StatPlot-1.0.2.exe `
  src/statplot_gui.py

Write-Host "Build complete."