# scientific-ai
New generation AI

## Build pipeline
This repository contains a simple Python package in `scientific_ai/`.
The `cli.py` module runs a short data analysis when executed.

A GitHub Actions workflow located at `.github/workflows/windows-build.yml`
creates a Windows executable using PyInstaller. The resulting `scientific_ai.exe`
file is published as a build artifact.

### Building locally
If you want to build the executable yourself, install PyInstaller and run:

```bash
pip install pyinstaller
pyinstaller --onefile -n scientific_ai scientific_ai/cli.py
```
