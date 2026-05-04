"""
VidyalayaPro EXE Launcher
Double click karo — automatically browser mein khulega
"""
import os
import sys
import time
import threading
import subprocess
import webbrowser
from pathlib import Path

def get_base_dir():
    """EXE aur normal Python dono ke liye base directory"""
    if getattr(sys, 'frozen', False):
        # PyInstaller EXE
        return os.path.dirname(sys.executable)
    else:
        # Normal Python script
        return os.path.dirname(os.path.abspath(__file__))

def open_browser():
    """5 second baad browser kholo"""
    time.sleep(4)
    webbrowser.open('http://localhost:5000')

def check_license_on_start():
    """Startup pe license check"""
    import json
    base = get_base_dir()
    license_file = os.path.join(base, 'license.json')

    if not os.path.exists(license_file):
        # Demo license create karo (30 din)
        try:
            sys.path.insert(0, base)
            from license_generator import generate_license
            import json
            info = generate_license("Demo School", "Demo City", days_valid=30)
            with open(license_file, 'w') as f:
                json.dump({
                    'license_key': info['license_key'],
                    'full_token': info['full_token'],
                    'school_name': 'Demo School',
                    'expiry_date': info['expiry_date']
                }, f, indent=2)
            print(f"Demo license created. Valid till: {info['expiry_date']}")
        except Exception as e:
            print(f"License warning: {e}")

def show_console_header():
    print("=" * 55)
    print("   VIDYALAYA PRO — School Management ERP")
    print("   Developed by: Saadat (AI Tech Channel)")
    print("=" * 55)
    print()
    print("  Starting server...")
    print("  Browser will open automatically in 4 seconds")
    print()
    print("  URL: http://localhost:5000")
    print("  Admin Login: admin / Admin@123")
    print()
    print("  Press Ctrl+C to stop the server")
    print("=" * 55)

if __name__ == '__main__':
    base = get_base_dir()
    os.chdir(base)
    sys.path.insert(0, base)

    show_console_header()
    check_license_on_start()

    # Browser thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Flask app start
    try:
        from app import app, db, seed_database
        with app.app_context():
            db.create_all()
            seed_database()
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except OSError as e:
        if 'Address already in use' in str(e):
            print("\n⚠️  Port 5000 already in use!")
            print("   Koi aur School ERP already chal raha hai.")
            print("   Browser mein http://localhost:5000 kholo.")
            webbrowser.open('http://localhost:5000')
            input("\nPress Enter to exit...")
        else:
            print(f"\nError: {e}")
            input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
