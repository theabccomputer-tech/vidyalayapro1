# 📚 VIDYALAYA PRO — Complete Guide
## Developed by: Saadat (AI Tech Channel)

---

## 🚀 NORMAL CHALANE KA TARIKA (Python se)

### Step 1: Python Install
- python.org se Python 3.10+ download karo
- Install karte waqt **"Add Python to PATH"** zaroor tick karo

### Step 2: Libraries Install (Sirf pehli baar)
```
pip install flask flask-sqlalchemy werkzeug cryptography
```

### Step 3: Start karo
```
python launcher.py
```
Ya simply **START_HERE.bat** pe double click karo

### Login:
- Admin: `admin` / `Admin@123`
- Teacher: `teacher1` / `Teacher@123`
- Student: `student1` / `Student@123`

---

## 🔑 LICENSE SYSTEM — AAPKA BUSINESS MODEL

### Kaise kaam karta hai:
1. **Aap developer ho** — Master Key sirf aapke paas hai
2. **Har school** ko alag license milti hai
3. **Machine-locked** license — copy karke doosre computer pe nahi chalega
4. **Expire date** set kar sakte ho — renewal business!

### Naya License Generate Karna (Aapke liye):
```
python license_generator.py
```
Option 1 choose karo → School naam, city, days enter karo → License key milegi

### School Computer ka ID Lena:
School ke computer pe ye command run karo:
```
python license_generator.py
```
Option 3 → Machine ID copy karo → Aapko WhatsApp karo

### Machine-Locked License (Secure):
```
python license_generator.py
```
Option 4 → School naam + Machine ID + Days enter karo

### Master Key (Apne computer pe hamesha chalane ke liye):
```
VIDYA-MASTER-2025-SAADAT
```
⚠️ YE KABHI KISI KO MAT BATANA!

### License Renew Karna:
- Settings → License tab mein naya token paste karo
- Ya school ke `license.json` file update karo

---

## 💻 EXE BANANA (Windows pe .exe file)

### Step 1: PyInstaller Install
```
pip install pyinstaller
```

### Step 2: EXE Build
```
pyinstaller VidyalayaPro.spec
```

### Step 3: EXE ready hoga:
```
dist/VidyalayaPro.exe
```

### School ko dene ke liye folder:
```
dist/
├── VidyalayaPro.exe   ← Ye dena
├── license.json       ← School ka license dena
```

⚠️ EXE ke saath school-specific `license.json` dena zaroori hai!

---

## 💰 PRICING STRATEGY (Aapke business ke liye)

| Package | Price | Duration | Features |
|---------|-------|----------|----------|
| Demo | Free | 30 days | Full features |
| Basic | ₹2,999 | 1 year | 1 computer |
| Standard | ₹4,999 | 1 year | 2 computers |
| Premium | ₹7,999 | Lifetime | Unlimited |
| AMC | ₹1,499 | Annual Renewal | Support + updates |

---

## 📁 FILES STRUCTURE

```
school_erp/
├── app.py                 ← Main application
├── launcher.py            ← EXE entry point
├── license_generator.py   ← Aapka tool (sirf aapke paas)
├── license_checker.py     ← App ke andar validation
├── license.json           ← School ka license (har school alag)
├── VidyalayaPro.spec      ← EXE build config
├── START_HERE.bat         ← Windows me double click
├── requirements.txt       ← Libraries list
├── templates/             ← All HTML pages (32 files)
├── static/                ← CSS, JS, uploaded photos
│   └── uploads/
│       ├── students/      ← Student photos
│       ├── teachers/      ← Teacher photos
│       ├── school/        ← School logo, building photo
│       └── staff/         ← Staff photos
└── instance/
    └── school_erp.db      ← DATABASE (backup karte raho!)
```

---

## 🔧 FEATURES LIST

### Admin / Principal:
- ✅ Dashboard (Dark/Light mode, charts)
- ✅ Student management (photo, 30+ fields)
- ✅ Teacher management (photo, salary slip)
- ✅ Attendance marking + reports
- ✅ Fee collection + receipts
- ✅ Exam scheduling + marks entry
- ✅ Report cards (printable)
- ✅ Library management
- ✅ Transport routes
- ✅ Homework assignment
- ✅ Events calendar
- ✅ Notices & circulars
- ✅ Admission enquiries
- ✅ Reports & analytics
- ✅ User management
- ✅ Audit logs
- ✅ School branding (logo, photo)
- ✅ Database backup

### Teacher Portal:
- ✅ My students
- ✅ Mark attendance
- ✅ Assign homework
- ✅ Enter marks
- ✅ Apply leave

### Student Portal:
- ✅ My attendance
- ✅ My fees
- ✅ My results
- ✅ Homework
- ✅ Library books
- ✅ Notices

---

## ⚠️ IMPORTANT NOTES

1. **Database backup** — `instance/school_erp.db` regularly copy karo
2. **Photos** — `static/uploads/` folder bhi backup lo
3. **License file** — `license.json` school ko dena hai
4. **Master password** — Kabhi share mat karna
5. **Port 5000** — Default port, firewall mein allow karo

---

## 📞 Support
YouTube: AI & Tech Channel (Saadat)
"Basic se AI tak"
