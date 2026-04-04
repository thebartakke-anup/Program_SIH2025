import cv2
import os
import numpy as np
import csv
import datetime
from PIL import Image

# ==============================
# Setup paths
# ==============================
dataset_path = "dataset"
trainer_path = "trainer"
students_file = "students.csv"

os.makedirs(dataset_path, exist_ok=True)
os.makedirs(trainer_path, exist_ok=True)

# ==============================
# Haar Cascade for face detection
# ==============================
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# ==============================
# Helper Functions
# ==============================
def get_today_attendance_file():
    today = datetime.date.today().strftime("%Y-%m-%d")
    return f"attendance_{today}.csv"


def init_attendance_file():
    attendance_file = get_today_attendance_file()
    if not os.path.exists(attendance_file):
        with open(attendance_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Student_ID", "Name", "Date", "Time"])
    return attendance_file


def load_students():
    students = {}
    if os.path.exists(students_file):
        with open(students_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) >= 2:
                    students[int(row[0])] = row[1]
    return students


def register_student():
    student_id = int(input("Enter Student ID: "))
    name = input("Enter Student Name: ")

    exists = os.path.exists(students_file)
    with open(students_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["Student_ID", "Name"])
        writer.writerow([student_id, name])

    print(f"[INFO] Student {name} (ID: {student_id}) registered.")
    return student_id

def capture_faces():
    cam = cv2.VideoCapture(0)
    student_id = register_student()
    count = 0

    print("[INFO] Capturing face samples... Look at the camera.")

    while True:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"{dataset_path}/{student_id}_{count}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Capturing Faces", img)
        if cv2.waitKey(100) & 0xFF == 27:
            break
        elif count >= 50:
            break

    print("[INFO] Face capture complete!")
    cam.release()
    cv2.destroyAllWindows()

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_samples, ids = [], []

        for img_path in image_paths:
            gray_img = Image.open(img_path).convert("L")
            img_np = np.array(gray_img, "uint8")
            id = int(os.path.split(img_path)[-1].split("_")[0])
            faces = face_cascade.detectMultiScale(img_np)
            for (x, y, w, h) in faces:
                face_samples.append(img_np[y:y+h, x:x+w])
                ids.append(id)
        return face_samples, ids

    print("[INFO] Training model. This may take a while...")
    faces, ids = get_images_and_labels(dataset_path)
    recognizer.train(faces, np.array(ids))
    recognizer.write(f"{trainer_path}/trainer.yml")
    print("[INFO] Training complete. Model saved!")

def recognize_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"{trainer_path}/trainer.yml")

    students = load_students()
    attendance_file = init_attendance_file()
    recognized_ids = set()

    cam = cv2.VideoCapture(0)
    print("[INFO] Starting face recognition... Press ESC to exit.")

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 70:
                name = students.get(id_, "Unknown")
                label = f"ID: {id_}, Name: {name}, Conf: {int(conf)}"
                cv2.putText(frame, label, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if id_ not in recognized_ids:
                    now = datetime.datetime.now()
                    with open(attendance_file, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([id_, name, now.date(), now.strftime("%H:%M:%S")])
                    recognized_ids.add(id_)
            else:
                cv2.putText(frame, f"Unknown (Conf: {int(conf)})", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Show live attendance count in window title
        present_count = len(recognized_ids)
        cv2.setWindowTitle("Face Recognition Attendance", f"Present: {present_count}")
        cv2.imshow("Face Recognition Attendance", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

def main():
    while True:
        print("\n===== Facial Recognition Attendance System =====")
        print("1. Register Student (Capture Faces)")
        print("2. Train Model")
        print("3. Take Attendance (Recognize Faces)")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            capture_faces()
        elif choice == "2":
            train_model()
        elif choice == "3":
            recognize_faces()
        elif choice == "4":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
