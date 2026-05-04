"""
╔══════════════════════════════════════════════════════════════╗
║         VIDYALAYA PRO — LICENSE MANAGEMENT SYSTEM           ║
║         Sirf Saadat (Developer) ke paas rahega ye file      ║
╚══════════════════════════════════════════════════════════════╝

KAISE KAAM KARTA HAI:
- Har school ko alag license key milti hai (machine-locked)
- Master key se kisi bhi machine pe chalega
- License key machine ID se bind hoti hai (copy nahi ho sakti)
- Expire date set kar sakte ho
- Saadat ka Master Code: VIDYA-MASTER-2025-SAADAT (kabhi mat batana)
"""

import hashlib
import base64
import json
import os
import sys
import platform
import uuid
from datetime import datetime, date, timedelta
from cryptography.fernet import Fernet

# ══════════════════════════════════════════════
# MASTER SECRET — KABHI KISI KO MAT BATANA
# ══════════════════════════════════════════════
MASTER_PASSWORD  = "SAADAT@VidyalayaPro#2025$Developer"
MASTER_KEY_CODE  = "VIDYA-MASTER-2025-SAADAT"
APP_SALT         = "VidyalayaProSchoolERP_Salt_v1"

def get_machine_id():
    """
    Is computer ki unique ID nikalte hain.
    Ye ID change nahi hoti jab tak OS reinstall na ho.
    """
    try:
        # Windows
        if platform.system() == "Windows":
            import subprocess
            result = subprocess.run(
                ['wmic', 'csproduct', 'get', 'uuid'],
                capture_output=True, text=True
            )
            lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
            if len(lines) >= 2:
                return lines[1]
        # Linux/Mac
        mid = str(uuid.getnode())  # MAC address based
        return mid
    except:
        return str(uuid.getnode())

def generate_fernet_key(password: str, salt: str) -> bytes:
    """Password se consistent Fernet key banate hain"""
    key_material = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000
    )
    return base64.urlsafe_b64encode(key_material)

def generate_license(school_name: str, school_city: str,
                      days_valid: int = 365,
                      machine_id: str = None) -> dict:
    """
    Naya license generate karo kisi school ke liye.

    Args:
        school_name: School ka naam
        school_city: School ka sheher
        days_valid: Kitne din valid rahega (default 1 saal)
        machine_id: Agar specific machine ke liye chahiye to daalo,
                    warna None rakho (any machine pe chalega — sirf master key se)

    Returns:
        dict with license_key and details
    """
    issue_date  = date.today().strftime('%Y-%m-%d')
    expiry_date = (date.today() + timedelta(days=days_valid)).strftime('%Y-%m-%d')

    # License data
    data = {
        "school_name":  school_name,
        "school_city":  school_city,
        "issue_date":   issue_date,
        "expiry_date":  expiry_date,
        "machine_id":   machine_id or "ANY",
        "version":      "1.0",
        "developer":    "Saadat"
    }

    # Encrypt karke license key banao
    key    = generate_fernet_key(MASTER_PASSWORD, APP_SALT)
    f      = Fernet(key)
    token  = f.encrypt(json.dumps(data).encode()).decode()

    # Short readable key banao
    short_hash = hashlib.md5(token.encode()).hexdigest()[:8].upper()
    license_key = f"VIDYA-{short_hash[:4]}-{short_hash[4:]}-{days_valid}"

    return {
        "license_key":  license_key,
        "full_token":   token,
        "school_name":  school_name,
        "school_city":  school_city,
        "issue_date":   issue_date,
        "expiry_date":  expiry_date,
        "machine_id":   machine_id or "ANY",
        "days_valid":   days_valid
    }

def validate_license(license_key: str, full_token: str) -> dict:
    """
    License validate karo — app start hone pe call hoti hai ye function.

    Returns:
        {"valid": True/False, "message": "...", "school_name": "...", ...}
    """
    # Master key check
    if license_key.strip() == MASTER_KEY_CODE:
        return {
            "valid":       True,
            "message":     "Master License Active",
            "school_name": "Developer Mode",
            "expiry_date": "9999-12-31",
            "is_master":   True
        }

    try:
        key  = generate_fernet_key(MASTER_PASSWORD, APP_SALT)
        f    = Fernet(key)
        data = json.loads(f.decrypt(full_token.encode()).decode())

        # Expiry check
        expiry = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
        if date.today() > expiry:
            days_ago = (date.today() - expiry).days
            return {
                "valid":   False,
                "message": f"License expired {days_ago} days ago. Please renew.",
                "expired": True
            }

        # Machine ID check (agar locked hai)
        if data.get('machine_id') != 'ANY':
            current_machine = get_machine_id()
            if data['machine_id'] != current_machine:
                return {
                    "valid":   False,
                    "message": "License is not valid for this computer.",
                    "machine_mismatch": True
                }

        days_left = (expiry - date.today()).days
        return {
            "valid":        True,
            "message":      f"License valid. {days_left} days remaining.",
            "school_name":  data['school_name'],
            "school_city":  data['school_city'],
            "expiry_date":  data['expiry_date'],
            "days_left":    days_left,
            "is_master":    False
        }

    except Exception as e:
        return {
            "valid":   False,
            "message": "Invalid or corrupted license key."
        }

def save_license_to_file(license_info: dict, filename: str = None):
    """License file school ke folder mein save karo"""
    if not filename:
        school_safe = license_info['school_name'].replace(' ', '_')[:20]
        filename    = f"license_{school_safe}.json"

    with open(filename, 'w') as f:
        json.dump({
            "license_key": license_info['license_key'],
            "full_token":  license_info['full_token'],
            "school_name": license_info['school_name'],
            "expiry_date": license_info['expiry_date']
        }, f, indent=2)

    print(f"✅ License saved: {filename}")
    return filename

# ══════════════════════════════════════════════
# GENERATOR TOOL — Saadat ke liye
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   VIDYALAYA PRO — LICENSE GENERATOR (Developer Tool)")
    print("=" * 60)
    print()

    while True:
        print("\nOptions:")
        print("  1. Generate new license for a school")
        print("  2. Validate existing license")
        print("  3. Show my machine ID")
        print("  4. Generate machine-locked license")
        print("  5. Exit")
        print()

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            print("\n--- Generate New License ---")
            school_name = input("School Name: ").strip()
            school_city = input("School City: ").strip()
            days_str    = input("Valid for days (default 365): ").strip()
            days        = int(days_str) if days_str.isdigit() else 365

            info = generate_license(school_name, school_city, days)

            print("\n" + "="*50)
            print(f"  School:      {info['school_name']}, {info['school_city']}")
            print(f"  Issue Date:  {info['issue_date']}")
            print(f"  Expiry:      {info['expiry_date']} ({info['days_valid']} days)")
            print(f"  Machine:     {info['machine_id']}")
            print()
            print(f"  LICENSE KEY: {info['license_key']}")
            print()
            print(f"  FULL TOKEN (copy this too):")
            print(f"  {info['full_token'][:80]}...")
            print("="*50)

            save = input("\nSave to file? (y/n): ").strip().lower()
            if save == 'y':
                fname = save_license_to_file(info)
                print(f"Saved as: {fname}")

        elif choice == "2":
            print("\n--- Validate License ---")
            lk    = input("License Key: ").strip()
            token = input("Full Token: ").strip()
            result = validate_license(lk, token)
            print()
            if result['valid']:
                print(f"  ✅ VALID: {result['message']}")
                print(f"  School: {result.get('school_name','')}")
                print(f"  Expiry: {result.get('expiry_date','')}")
            else:
                print(f"  ❌ INVALID: {result['message']}")

        elif choice == "3":
            mid = get_machine_id()
            print(f"\n  This Machine ID: {mid}")
            print("  (Share this ID with Saadat to get machine-locked license)")

        elif choice == "4":
            print("\n--- Machine-Locked License ---")
            school_name = input("School Name: ").strip()
            school_city = input("School City: ").strip()
            machine_id  = input("Machine ID (from school computer): ").strip()
            days_str    = input("Valid for days (default 365): ").strip()
            days        = int(days_str) if days_str.isdigit() else 365

            info = generate_license(school_name, school_city, days, machine_id)

            print("\n" + "="*50)
            print(f"  School:    {info['school_name']}")
            print(f"  Machine:   {info['machine_id']}")
            print(f"  Expiry:    {info['expiry_date']}")
            print(f"\n  LICENSE KEY: {info['license_key']}")
            print(f"\n  FULL TOKEN:")
            print(f"  {info['full_token']}")
            print("="*50)

            save = input("\nSave to file? (y/n): ").strip().lower()
            if save == 'y':
                save_license_to_file(info)

        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try again.")
