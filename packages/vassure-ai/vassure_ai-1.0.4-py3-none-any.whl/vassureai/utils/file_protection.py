"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""

import os
import sys
import stat
from pathlib import Path
from typing import List

PROTECTED_HEADER = '''"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""'''

def set_file_permissions(file_path: str, make_readonly: bool = True) -> None:
    """Set file permissions"""
    try:
        # Get current permissions
        current = stat.S_IMODE(os.lstat(file_path).st_mode)
        if make_readonly:
            # Remove write permissions for all users
            new_mode = current & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        else:
            # Add write permission for owner
            new_mode = current | stat.S_IWUSR
        os.chmod(file_path, new_mode)
    except Exception as e:
        print(f"Error setting permissions for {file_path}: {str(e)}")

def toggle_protection(files: List[str], protect: bool = True) -> None:
    """Toggle protection for specific files"""
    for file_path in files:
        if os.path.exists(file_path):
            set_file_permissions(file_path, make_readonly=protect)
            action = "Protected" if protect else "Made writable"
            print(f"{action}: {file_path}")
        else:
            print(f"File not found: {file_path}")

def verify_protection() -> List[str]:
    """Verify that all Python files are protected and have the correct header"""
    unprotected_files = []
    project_root = Path(__file__).parent.parent
    
    for py_file in project_root.rglob("*.py"):
        if "venv" not in str(py_file):  # Skip virtual environment files
            try:
                # Check if file is writable
                if os.access(str(py_file), os.W_OK):
                    unprotected_files.append(f"{py_file} (writable)")
                
                # Check for protected header
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.startswith(PROTECTED_HEADER.strip()):
                        unprotected_files.append(f"{py_file} (missing/invalid header)")
            except Exception as e:
                print(f"Error verifying {py_file}: {str(e)}")
    
    return unprotected_files

if __name__ == "__main__":
    # Get project root directory
    project_root = str(Path(__file__).parent.parent)
    
    if len(sys.argv) > 1:
        # If files are specified as arguments, toggle their protection
        args = sys.argv[1:]
        unprotect = "--unprotect" in args
        if unprotect:
            args.remove("--unprotect")
        
        # Convert relative paths to absolute paths
        files = [os.path.join(project_root, f) if not os.path.isabs(f) else f 
                for f in args]
        
        toggle_protection(files, not unprotect)
    else:
        print("Usage: python file_protection.py [--unprotect] file1 file2 ...")
        print("Examples:")
        print("  Make files readonly: python file_protection.py file1.py file2.py")
        print("  Make files writable: python file_protection.py --unprotect file1.py file2.py")