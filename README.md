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
4. Install dependencies: `pip install flask spleeter librosa pedalboard`

---

## ⚖️ License
Internal Development - QI-Labs
