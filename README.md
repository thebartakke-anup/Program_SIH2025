# Automated Attendance System — Team Agastya
### Smart India Hackathon 2025 | Problem Statement ID: 25012 | Theme: Smart Education

A facial recognition-based attendance system built for rural schools. A webcam captures student faces, matches them against a trained model, and automatically logs attendance to a CSV file — no manual entry needed.

---

## How It Works

1. **Register** — Capture 50 face samples per student via webcam, stored locally.
2. **Train** — The LBPH (Local Binary Pattern Histograms) model is trained on the captured samples.
3. **Recognize** — The live camera feed detects and identifies faces in real time, marking students present.
4. **Export** — Attendance is saved as a `.csv` file (Excel-compatible) for records and reporting.

---

## Requirements

### Hardware
- Webcam (USB or built-in) **or** Raspberry Pi 4 + ESP32-CAM module
- A PC / laptop to run the system

### Software & Dependencies

```bash
pip install opencv-python opencv-contrib-python numpy pillow
```

> **Note:** `opencv-contrib-python` is required for the LBPH face recognizer. The standard `opencv-python` package alone will not work.

---

## Project Structure

```
attendance-system/
│
├── attendance_system.py     # Main application
├── students.csv             # Student ID → Name mapping (auto-generated)
│
├── dataset/                 # Face image samples (gitignored)
│   └── <student_id>_<n>.jpg
│
├── trainer/                 # Trained model output (gitignored)
│   └── trainer.yml
│
└── attendance_<YYYY-MM-DD>.csv   # Daily attendance logs (auto-generated)
```

---

## Setup & Usage

### Step 1 — Clone the repo

```bash
git clone https://github.com/your-username/attendance-system.git
cd attendance-system
pip install opencv-python opencv-contrib-python numpy pillow
```

### Step 2 — Register a student

Run the script and select **Option 1**:

```bash
python attendance_system.py
```

```
===== Facial Recognition Attendance System =====
1. Register Student (Capture Faces)
2. Train Model
3. Take Attendance (Recognize Faces)
4. Exit

Enter choice: 1
Enter Student ID: 101
Enter Student Name: Rahul Sharma
```

The webcam will open and capture **50 face samples** automatically. Press `ESC` to stop early if needed. Repeat this for every student.

### Step 3 — Train the model

Select **Option 2**. This reads all images from the `dataset/` folder and trains the LBPH model. The output is saved to `trainer/trainer.yml`.

```
Enter choice: 2
[INFO] Training model. This may take a while...
[INFO] Training complete. Model saved!
```

> Re-train whenever new students are registered.

### Step 4 — Take attendance

Select **Option 3**. The webcam feed opens and begins recognizing faces in real time.

- A **green label** shows the matched student's ID, name, and confidence score.
- A **red label** marks unrecognized faces as "Unknown".
- Each student is logged **once per session** to avoid duplicates.
- The window title shows a live count of students present.
- Press `ESC` to stop.

Attendance is saved to `attendance_YYYY-MM-DD.csv` in the project directory.

---

## Attendance Log Format

Each daily file contains:

| Student_ID | Name | Date | Time |
|---|---|---|---|
| 101 | Rahul Sharma | 2025-03-15 | 09:02:34 |
| 102 | Priya Patel | 2025-03-15 | 09:03:11 |

---

## Configuration

| Parameter | Location | Default | Description |
|---|---|---|---|
| Confidence threshold | `recognize_faces()` | `70` | Lower = stricter matching. Tune based on lighting. |
| Face samples per student | `capture_faces()` | `50` | More samples = better accuracy |
| LBPH radius | `trainer.yml` | `1` | LBP pixel radius |
| LBPH neighbors | `trainer.yml` | `8` | Sampling points per pixel |
| LBPH grid | `trainer.yml` | `8×8` | Face subdivision grid |

---

## .gitignore

Add this to your `.gitignore` before pushing:

```
# Auto-generated model and face data — regenerate locally
dataset/
trainer/
students.csv
attendance_*.csv
```

To regenerate after cloning: register students (Step 2), then train (Step 3).

---

## Hardware Deployment (Raspberry Pi)

For deployment in schools without a PC, the system can run on a **Raspberry Pi 4** with an ESP32-CAM module.

- RPi 4 handles model inference and CSV logging
- ESP32-CAM streams the video feed
- Attendance CSV is transmitted to a central PC or stored on an SD card as a fallback
- Estimated cost per classroom: ~₹900 INR

---

## Tech Stack

| Component | Technology |
|---|---|
| Face detection | OpenCV Haar Cascades |
| Face recognition | LBPH (opencv-contrib) |
| Data storage | CSV (Excel-compatible) |
| Edge hardware | Raspberry Pi 4 / ESP32-CAM |
| Language | Python 3 |

---

## Team

**Team Agastya** — Smart India Hackathon 2025 Internal Round  
Problem Statement: Automated Attendance System for Rural Schools (ID: 25012)  
Category: Software | Theme: Smart Education
