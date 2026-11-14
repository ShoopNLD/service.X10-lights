#!/usr/bin/env python3
"""
Build script to package service.X10-lights into a clean, installable Kodi zip file.
Usage:
    python scripts/build_kodi_zip.py
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET

def get_addon_version(addon_xml_path):
    tree = ET.parse(addon_xml_path)
    root = tree.getroot()
    return root.get('version', '2.0.0'), root.get('id', 'service.X10-lights')

def build_zip():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    addon_dir = os.path.join(repo_root, 'service.X10-lights')
    addon_xml = os.path.join(addon_dir, 'addon.xml')

    if not os.path.isfile(addon_xml):
        print(f"Error: Could not find addon.xml at {addon_xml}")
        sys.exit(1)

    version, addon_id = get_addon_version(addon_xml)
    dist_dir = os.path.join(repo_root, 'dist')
    os.makedirs(dist_dir, exist_ok=True)

    zip_filename = f"{addon_id}-{version}.zip"
    zip_path = os.path.join(dist_dir, zip_filename)

    print(f"Packaging {addon_id} v{version}...")
    exclude_extensions = {'.pyc', '.pyo', '.zip'}
    exclude_dirs = {'__pycache__', '.git', '.idea', '.vscode'}

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(addon_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_extensions:
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_root)
                zip_file.write(file_path, rel_path)
                print(f"  + Added: {rel_path}")

    size_kb = os.path.getsize(zip_path) / 1024.0
    print(f"\nSuccessfully created installable Kodi zip:")
    print(f"  -> Path: {zip_path}")
    print(f"  -> Size: {size_kb:.1f} KB")

if __name__ == '__main__':
    build_zip()
