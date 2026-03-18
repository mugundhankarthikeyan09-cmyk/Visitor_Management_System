# 🛡️ Visitor Management System (VMS)

A mobile-first, Flask-based application designed for seamless guest registration, identity capture, and QR-based checkout. This system provides a digital alternative to physical visitor logbooks.

---

## ✨ Key Features

* **Selfie Identity Capture**: Uses `Webcam.js` to capture visitor photos directly from the browser.
* [cite_start]**Automated QR Pass**: Generates a unique digital pass for every guest upon registration[cite: 1, 6].
* **QR Exit Scanner**: Integrated `jsQR` scanner allows security to check out visitors by scanning their digital pass.
* [cite_start]**Live Dashboard**: Real-time tracking of "In" vs. "Total" visitors for the day[cite: 1, 3].
* [cite_start]**Overstay Detection**: Automatically flags visitors who have stayed longer than 4 hours[cite: 1, 3].
* [cite_start]**Security Blacklist**: Built-in restriction for specific phone numbers to deny access instantly.
* [cite_start]**Data Export**: Searchable history logs with the ability to export all data to a CSV/Excel-compatible format[cite: 1, 4].

---

## 🛠️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | [cite_start]Python / Flask  |
| **Database** | [cite_start]SQLite (SQLAlchemy)  |
| **Frontend** | Bootstrap 5, Chart.js |
| **Utilities** | [cite_start]Pandas (Export), PyQRCode, jsQR [cite: 1, 3] |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python installed, then install the required libraries:
```bash
pip install flask flask-sqlalchemy qrcode pandas
