#!/usr/bin/env python3
"""
Local test script for the GitHub Actions build process.
Run this to test the build logic before pushing to GitHub.
"""

import os
import requests
import zipfile
import shutil
from datetime import datetime

def test_build():
    """Test the build process locally."""
    print("Testing Pico-Ducky build process...")
    
    # Configuration
    CP_VERSION = "9.2.1"
    VERSION = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # Supported boards (test with just one for speed)
    BOARDS = {
        "raspberry_pi_pico_w": f"https://downloads.circuitpython.org/bin/raspberry_pi_pico_w/en_US/adafruit-circuitpython-raspberry_pi_pico_w-en_US-{CP_VERSION}.uf2"
    }
    
    # Create directories
    os.makedirs("test_dist", exist_ok=True)
    os.makedirs("test_lib", exist_ok=True)
    
    print(f"Testing build {VERSION}")
    
    # Test UF2 download
    print("Testing UF2 download...")
    uf2_files = {}
    for board, url in BOARDS.items():
        filename = f"adafruit-circuitpython-{board}-en_US-{CP_VERSION}.uf2"
        print(f"  Downloading {filename}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(f"test_dist/{filename}", "wb") as f:
                f.write(response.content)
            uf2_files[board] = filename
            print(f"  ✓ Downloaded {filename} ({len(response.content)} bytes)")
        except Exception as e:
            print(f"  ✗ Failed to download {filename}: {e}")
            return False
    
    # Test library download
    print("Testing library download...")
    try:
        # Get latest release (without authentication, like workflow will try first)
        print("  Fetching latest release info...")
        releases_response = requests.get("https://api.github.com/repos/adafruit/Adafruit_CircuitPython_Bundle/releases/latest", timeout=30)
        releases_response.raise_for_status()
        latest_release = releases_response.json()
        
        print(f"  Latest release: {latest_release.get('tag_name', 'unknown')}")
        
        # Find bundle URL
        bundle_url = None
        assets = latest_release.get('assets', [])
        print(f"  Found {len(assets)} assets in release")
        
        for asset in assets:
            asset_name = asset.get('name', '')
            if 'adafruit-circuitpython-bundle-9.x-mpy' in asset_name and asset_name.endswith('.zip'):
                bundle_url = asset['browser_download_url']
                print(f"  Found matching bundle: {asset_name}")
                break
        
        if not bundle_url:
            print("  Available assets:")
            for asset in assets[:5]:  # Show first 5 assets
                print(f"    - {asset.get('name', 'unknown')}")
            print("  ✗ No suitable bundle found")
            return False
        
        print(f"  Downloading bundle from: {bundle_url}")
        response = requests.get(bundle_url, timeout=120)
        response.raise_for_status()
        
        with open("test_bundle.zip", "wb") as f:
            f.write(response.content)
        print(f"  ✓ Downloaded bundle ({len(response.content)} bytes)")
        
        # Extract bundle
        with zipfile.ZipFile("test_bundle.zip", "r") as zip_ref:
            zip_ref.extractall("test_bundle_temp")
        
        # Find bundle directory
        bundle_dirs = [d for d in os.listdir("test_bundle_temp") if d.startswith("adafruit-circuitpython-bundle")]
        if not bundle_dirs:
            print("  ✗ No bundle directory found after extraction")
            return False
            
        bundle_dir = os.path.join("test_bundle_temp", bundle_dirs[0], "lib")
        print(f"  Using bundle directory: {bundle_dirs[0]}")
        
        # Required libraries
        required_libs = [
            "adafruit_hid",
            "adafruit_debouncer.mpy", 
            "adafruit_ticks.mpy",
            "asyncio",
            "adafruit_wsgi"
        ]
        
        # Copy libraries
        for lib in required_libs:
            src = os.path.join(bundle_dir, lib)
            dst = os.path.join("test_lib", lib)
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                print(f"  ✓ Copied {lib}")
            else:
                print(f"  ✗ Missing {lib}")
        
        # Cleanup
        os.remove("test_bundle.zip")
        shutil.rmtree("test_bundle_temp")
        print("  ✓ Libraries downloaded and extracted")
        
    except Exception as e:
        print(f"  ✗ Failed to download libraries: {e}")
        return False
    
    # Test bundle creation
    print("Testing bundle creation...")
    for board in BOARDS.keys():
        bundle_name = f"pico-ducky-{VERSION}-{board}"
        bundle_dir = bundle_name
        
        print(f"  Creating {bundle_name}...")
        
        # Create bundle directory
        if os.path.exists(bundle_dir):
            shutil.rmtree(bundle_dir)
        os.makedirs(bundle_dir)
        
        # Copy Python files
        python_files = [f for f in os.listdir(".") if f.endswith(".py")]
        for file in python_files:
            shutil.copy2(file, bundle_dir)
        
        # Copy lib directory
        if os.path.exists("test_lib"):
            shutil.copytree("test_lib", os.path.join(bundle_dir, "lib"))
        
        # Copy documentation
        md_files = [f for f in os.listdir(".") if f.endswith(".md")]
        for file in md_files:
            shutil.copy2(file, bundle_dir)
        
        # Copy examples if they exist
        if os.path.exists("examples"):
            shutil.copytree("examples", os.path.join(bundle_dir, "examples"))
        
        # Copy UF2 file if available
        if board in uf2_files:
            uf2_src = os.path.join("test_dist", uf2_files[board])
            if os.path.exists(uf2_src):
                shutil.copy2(uf2_src, bundle_dir)
        
        # Create installation instructions
        from create_install import create_install_txt
        create_install_txt(bundle_dir, is_test=True)
        
        # Create ZIP bundle
        zip_path = os.path.join("test_dist", f"{bundle_name}.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(bundle_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arc_path)
        
        zip_size = os.path.getsize(zip_path)
        print(f"  ✓ Created {bundle_name}.zip ({zip_size} bytes)")
        
        # Cleanup bundle directory
        shutil.rmtree(bundle_dir)
    
    # Cleanup
    shutil.rmtree("test_lib")
    
    print("✓ Build test completed successfully!")
    print(f"Test files created in test_dist/:")
    for file in os.listdir("test_dist"):
        size = os.path.getsize(os.path.join("test_dist", file))
        print(f"  - {file} ({size} bytes)")
    
    return True

if __name__ == "__main__":
    try:
        success = test_build()
        if success:
            print("\n✓ All tests passed! The build process should work in GitHub Actions.")
        else:
            print("\n✗ Tests failed. Fix the issues before pushing to GitHub.")
            exit(1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        exit(1)
