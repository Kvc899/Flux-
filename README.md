# ⚡️ Flux System Monitor
**Version 1.0 | Built by Karsten Cronin**

Flux is a high-performance, minimalist macOS system monitor that lives in your menu bar. Designed for power users and gamers, it provides real-time tracking of CPU, RAM, and Disk usage with custom tiered alerts.

---

## 🚀 Features
- **Always-On Monitoring:** Track system vitals without opening a window.
- **Retina-Ready UI:** Optimized for high-resolution displays (120Hz+).
- **Tiered Alerts:** - 🟢 **Normal:** Silent tracking.
  - 🟡 **Warning:** Visual indicator when resources hit 80%.
  - 🔴 **Red Alert:** Immediate notification when system critical limits (95%+) are reached.
- **Auto-Launch:** Automatically starts when you log in to your Mac.

---

## 🛠 Installation
1. Download the `Flux_Installer.dmg`from releases.
2. Double-click the DMG to open the installer window.
3. **Drag the Flux icon** into the Applications folder.
4. Open **Flux** from your Applications folder.

---

## 💻 Developer Mode
If you want to build Flux from the source:

### Prerequisites
- Python 3.x
- `psutil` (System stats)
- `rumps` (Menu bar framework)
- `py2app` (For building the .app bundle)

### Build Command
```bash
python3 setup.py py2app
```
Source File is linked in the main page of Github Repo
