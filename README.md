# VibeShift 🎧
> **"Your Music, Reimagined"**

VibeShift is an AI-powered audio transformation platform that allows users to unmix original tracks and generate "Unplugged," "Lo-Fi," or "Dance" reprises automatically. Developed by **QI-Labs**.

---

## 🚀 Project Vision
VibeShift leverages state-of-the-art Source Separation (Spleeter/Demucs) and Digital Signal Processing (DSP) to give users creative control over their favorite songs. Whether it's stripping a track to its acoustic core or building a high-energy dance remix, VibeShift handles the logic via AI.

## 🛠 Tech Stack (Phase 1)
- **Backend:** Python / Flask
- **Audio AI:** Spleeter (Deezer) or Demucs (Meta)
- **DSP:** Librosa, Pydub, Pedalboard
- **Frontend (MVP):** Simple Web Dashboard
- **Future Mobile:** Android (Kotlin, Jetpack Compose, Coroutines/Flow)

---

## 🗺 Roadmap

### Phase 1: The Core Engine (MVP) - *Current*
- [ ] Setup Flask environment and secure file upload handling.
- [ ] Integrate **Source Separation** (Extracting Vocals vs. Accompaniment).
- [ ] Implement **Lo-Fi Logic**:
    - Tempo reduction.
    - Low-pass filtering (Warmth).
    - Vinyl/Rain texture overlay.
- [ ] Implement **Dance Logic**:
    - BPM Analysis and Speed-up.
    - Bass boost and compression.

### Phase 2: Refinement & "Cover" Intelligence
- [ ] **Voice Swap:** Experiment with RVC (Retrieval-based Voice Conversion).
- [ ] **Smart Mashups:** Automated key matching and beat-syncing between two tracks.
- [ ] UI/UX overhaul using Material 3 guidelines.

### Phase 3: Mobile Expansion
- [ ] Development of the **VibeShift Android App**.
- [ ] Integration of WorkManager for long-running audio processing tasks.
- [ ] Real-time audio visualization using Jetpack Compose.

---

## 🛠 Installation & Setup (Local)
1. Clone the repo: `git clone https://github.com/your-username/VibeShift.git`
2. Create virtual env: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. pip install -r requirements.txt
5. System Prerequisite: Ensure you have FFmpeg installed on your computer. Spleeter uses it to decode the MP3s. If you don't have it, the app will throw an error when it tries to separate the stem
   ffmpeg -version
    • If installed: You’ll see a wall of text showing the version number and configuration details.
    • If NOT installed: You’ll see an error like "ffmpeg" is not recognized... or command not found.
    Installation Steps (By OS)
    If it’s missing, here is the fastest way to get it for VibeShift:
    Windows
    1. Download: Go to gyan.dev and download the ffmpeg-git-full.7z (or .zip) from the "release builds" section.
    2. Extract: Unzip it and move the folder to C:\ffmpeg.
    3. Add to Path (Crucial):
        • Search for "Edit the system environment variables" in Windows Start.
        • Click Environment Variables.
        • Under "System variables," find Path, select it, and click Edit.
        • Click New and paste: C:\ffmpeg\bin.
        • Click OK on all windows.
    4. Restart your Terminal for the changes to take effect.

    macOS
    The easiest way is using Homebrew:
        brew install ffmpeg
    Linux
        sudo apt update
        sudo apt install ffmpeg
    

6. Launch the App
    python app.py

---

## ⚖️ License
Internal Development - QI-Labs
