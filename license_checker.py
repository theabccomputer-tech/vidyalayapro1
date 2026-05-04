"""
License checker — app.py mein import hoti hai ye file.
Start pe license validate karta hai.
"""

import os
import json
import sys
from license_generator import validate_license, get_machine_id, MASTER_KEY_CODE

LICENSE_FILE = "license.json"

def check_license():
    """
    App start hone pe ye function call hoti hai.
    Returns: (is_valid: bool, school_info: dict)
    """
    # License file exist karti hai?
    if not os.path.exists(LICENSE_FILE):
        return False, {
            "message": "License file not found. Please contact developer.",
            "school_name": "Unlicensed"
        }

    try:
        with open(LICENSE_FILE, 'r') as f:
            data = json.load(f)

        license_key = data.get('license_key', '')
        full_token  = data.get('full_token', '')

        result = validate_license(license_key, full_token)
        return result['valid'], result

    except Exception as e:
        return False, {"message": f"License error: {str(e)}"}

def create_demo_license():
    """
    Pehli baar chalane ke liye 30-din ka demo license banata hai.
    Sirf development mein use karo.
    """
    from license_generator import generate_license, save_license_to_file
    info = generate_license("Demo School", "Demo City", days_valid=30)
    save_license_to_file(info, LICENSE_FILE)
    return info
