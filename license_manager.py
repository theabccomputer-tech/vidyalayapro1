"""
╔══════════════════════════════════════════════════════════╗
║         VIDYALAYA PRO - LICENSE MANAGEMENT SYSTEM        ║
║         Developer: Saadat  |  All Rights Reserved        ║
╚══════════════════════════════════════════════════════════╝
"""
import hashlib, base64, json, os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# ⚠️ YE SECRET SIRF AAPKE PAAS RAHE
MASTER_SECRET = b"VidyalayaPro@Saadat2025#SecretMasterKey$Developer"
MASTER_KEY    = "MASTER-VIDYALAYA-SAADAT-2025"

def _fernet():
    h = hashlib.sha256(MASTER_SECRET).digest()
    return Fernet(base64.urlsafe_b64encode(h))

def generate_license(school_name, school_city, days_valid=365, max_students=500):
    payload = {
        "school"  : school_name,
        "city"    : school_city,
        "issued"  : datetime.now().strftime("%Y-%m-%d"),
        "expiry"  : (datetime.now() + timedelta(days=days_valid)).strftime("%Y-%m-%d"),
        "students": max_students,
        "dev"     : "Saadat-AITech"
    }
    enc = _fernet().encrypt(json.dumps(payload).encode())
    return base64.urlsafe_b64encode(enc).decode()

def verify_license(license_key):
    key = license_key.strip()
    # Master key — hamesha valid
    if key.upper() == MASTER_KEY:
        return {"valid": True, "master": True,
                "data": {"school":"Master","expiry":"9999-12-31","students":99999},
                "message": "✅ Master License Active"}
    try:
        enc = base64.urlsafe_b64decode(key + "==")
        payload = json.loads(_fernet().decrypt(enc))
        expiry = datetime.strptime(payload["expiry"], "%Y-%m-%d")
        if datetime.now() > expiry:
            days_ago = (datetime.now() - expiry).days
            return {"valid": False, "data": payload,
                    "message": f"❌ License {days_ago} days pehle expire ho gayi. Developer se sampark karein."}
        days_left = (expiry - datetime.now()).days
        return {"valid": True, "master": False, "data": payload,
                "message": f"✅ Valid | {payload['school']} | {days_left} din baaki"}
    except Exception as e:
        return {"valid": False, "data": {},
                "message": "❌ Invalid license key. Developer se sampark karein."}

def load_license():
    path = os.path.join(os.path.dirname(__file__), "license.key")
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        return f.read().strip()

def save_license(key):
    path = os.path.join(os.path.dirname(__file__), "license.key")
    with open(path, "w") as f:
        f.write(key.strip())

def check_on_startup():
    key = load_license()
    if not key:
        return {"valid": False, "message": "License nahi mili. Settings mein activate karein."}
    return verify_license(key)


# ── COMMAND LINE TOOL ──────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═"*52)
    print("   VIDYALAYA PRO — LICENSE MANAGER")
    print("   Sirf Developer Use (Saadat)")
    print("═"*52)
    print("\n1. Naya License Banao (School ke liye)")
    print("2. License Verify Karo")
    print("3. Master Key Dekho")
    print("4. Saari Generated Licenses dekho")

    ch = input("\nChoice (1/2/3/4): ").strip()

    if ch == "1":
        print("\n── NAYA LICENSE ──────────────────────────────")
        name     = input("School ka Naam        : ").strip()
        city     = input("City / Shahar         : ").strip()
        days_str = input("Kitne din valid (365) : ").strip()
        stu_str  = input("Max Students (500)    : ").strip()
        days     = int(days_str) if days_str.isdigit() else 365
        students = int(stu_str)  if stu_str.isdigit()  else 500

        key    = generate_license(name, city, days, students)
        expiry = (datetime.now() + timedelta(days=days)).strftime("%d %B %Y")

        print("\n" + "─"*52)
        print("✅ LICENSE KEY:")
        print("─"*52)
        print(key)
        print("─"*52)
        print(f"School   : {name}")
        print(f"City     : {city}")
        print(f"Expire   : {expiry}")
        print(f"Students : {students} max")
        print("\n📋 Ye key school ko do.")
        print("   Settings > License mein paste karein.\n")

        # Log karo
        log_path = "licenses_issued.txt"
        with open(log_path, "a") as f:
            f.write(f"\n{'─'*50}\n")
            f.write(f"School  : {name}\n")
            f.write(f"City    : {city}\n")
            f.write(f"Expiry  : {expiry}\n")
            f.write(f"Students: {students}\n")
            f.write(f"Date    : {datetime.now().strftime('%d %b %Y %H:%M')}\n")
            f.write(f"KEY     : {key}\n")
        print(f"✅ Log saved in {log_path}")

    elif ch == "2":
        print("\n── LICENSE VERIFY ────────────────────────────")
        key    = input("License Key paste karo: ").strip()
        result = verify_license(key)
        print("\n" + "─"*52)
        print(result["message"])
        if result.get("data"):
            d = result["data"]
            for k, v in d.items():
                print(f"  {k:10}: {v}")
        print("─"*52)

    elif ch == "3":
        print("\n" + "─"*52)
        print("⚠️  MASTER KEY (kisi ko mat batana!):")
        print(f"   {MASTER_KEY}")
        print("─"*52)

    elif ch == "4":
        log = "licenses_issued.txt"
        if os.path.exists(log):
            with open(log) as f:
                print(f.read())
        else:
            print("Abhi tak koi license nahi banaya.")
