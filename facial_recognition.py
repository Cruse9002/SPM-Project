from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
from time import strftime
from datetime import datetime
import numpy as np
import PIL


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # 1st image
        try:
            img_top = Image.open("Images/face_recog1.jpg")
            img_top = img_top.resize((650, 700), PIL.Image.Resampling.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            f_lbl = Label(self.root, image=self.photoimg_top)
            f_lbl.place(x=0, y=55, width=650, height=700)
        except:
            # Fallback if image not found
            f_lbl = Label(self.root, bg="lightblue", text="Face Recognition Image 1")
            f_lbl.place(x=0, y=55, width=650, height=700)

        # 2nd image
        try:
            img_bottom = Image.open("Images/face_recog2.jpg")
            img_bottom = img_bottom.resize((950, 700), PIL.Image.Resampling.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            f_lbl = Label(self.root, image=self.photoimg_bottom)
            f_lbl.place(x=650, y=55, width=950, height=700)
        except:
            # Fallback if image not found
            f_lbl = Label(self.root, bg="lightgreen", text="Face Recognition Image 2")
            f_lbl.place(x=650, y=55, width=950, height=700)

        # button - FIXED: Now using the correct widget reference
        b1_1 = Button(self.root, text="RECOGNIZE", command=self.recognize_attendance, cursor="hand2",
                      font=("times new roman", 18, "bold"), bg="darkgreen", fg="white")
        b1_1.place(x=1000, y=600, width=200, height=40)

    ########################################  attendance  #########################

    def mark_attendance(self, i, n, d):
        try:
            with open("attendance.csv", "r+", newline="\n") as f:
                myDataList = f.readlines()
                name_list = []

                for line in myDataList:
                    if line.strip():  # Skip empty lines
                        entry = line.split(",")
                        name_list.append(entry[0])  # Assuming ID is first column

                # Check if already marked today
                current_date = datetime.now().strftime("%d/%m/%y")
                if i not in name_list:
                    now = datetime.now()
                    dtString = now.strftime("%H:%M:%S")
                    f.writelines(f"\n{i},{n},{d},{dtString},{current_date},Present")
                    print(f"Attendance marked for {n}")

        except FileNotFoundError:
            # Create file if it doesn't exist
            with open("attendance.csv", "w", newline="\n") as f:
                f.write("ID,Name,Department,Time,Date,Status\n")
                now = datetime.now()
                current_date = now.strftime("%d/%m/%y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"{i},{n},{d},{dtString},{current_date},Present")
                print(f"Created attendance file and marked for {n}")

        except Exception as e:
            print(f"Error marking attendance: {e}")

    ########################################  face recognition  #################

    def recognize_attendance(self):  # FIXED: This method is now properly indented INSIDE the class
        try:
            # Load the trained recognizer
            if not os.path.exists("classifier.xml"):
                messagebox.showerror("Error", "Classifier not found. Please train the model first.")
                return

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read('./classifier.xml')

            # Load the Haar cascade for face detection
            harcascadePath = "./cascade/haarcascade_frontalface_default.xml"
            if not os.path.exists(harcascadePath):
                messagebox.showerror("Error", "Haar cascade file not found.")
                return

            faceCascade = cv2.CascadeClassifier(harcascadePath)
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Start realtime video capture
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cam.set(3, 640)  # width
            cam.set(4, 480)  # height

            # Check if camera opened successfully
            if not cam.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                return

            minW = 0.1 * cam.get(3)
            minH = 0.1 * cam.get(4)

            while True:
                ret, im = cam.read()
                if not ret:
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    1.2,
                    5,
                    minSize=(int(minW), int(minH)),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)
                    id, predict = recognizer.predict(gray[y:y + h, x:x + w])
                    confidence = int((100 * (1 - predict / 300)))

                    try:
                        # Connect to database
                        conn = mysql.connector.connect(
                            host='localhost',
                            username='root',
                            password='Nandy#2005',  # Change to your password
                            database='face_recognition'
                        )
                        my_cursor = conn.cursor()

                        # Get student details - FIXED: Using parameterized queries
                        my_cursor.execute("SELECT name FROM student_detail WHERE student_id = %s", (str(id),))
                        n_result = my_cursor.fetchone()
                        n = n_result[0] if n_result else "Unknown"

                        my_cursor.execute("SELECT dep FROM student_detail WHERE student_id = %s", (str(id),))
                        d_result = my_cursor.fetchone()
                        d = d_result[0] if d_result else "Unknown"

                        my_cursor.execute("SELECT eno FROM student_detail WHERE student_id = %s", (str(id),))
                        i_result = my_cursor.fetchone()
                        i = i_result[0] if i_result else "Unknown"

                        my_cursor.close()
                        conn.close()

                        if confidence > 70:  # Adjusted confidence threshold
                            cv2.putText(im, f"ID:{i}", (x, y - 55), font, 0.8, (255, 255, 255), 2)
                            cv2.putText(im, f"Name:{n}", (x, y - 30), font, 0.8, (255, 255, 255), 2)
                            cv2.putText(im, f"Dep:{d}", (x, y - 5), font, 0.8, (255, 255, 255), 2)
                            already_marked = self.mark_attendance(i, n, d)

                            if already_marked:
                                # Show message that attendance was already marked
                                cv2.putText(im, "Already Marked Today", (x, y + h + 25), font, 0.7, (0, 255, 255), 2)
                                print(f"Attendance already marked for {n} today")
                            else:
                                # Show message that attendance was newly marked
                                cv2.putText(im, "Attendance Marked", (x, y + h + 25), font, 0.7, (0, 255, 0), 2)
                                print(f"New attendance marked for {n}")
                        else:
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            cv2.putText(im, "Unknown Face", (x, y - 5), font, 0.8, (255, 255, 255), 3)

                    except mysql.connector.Error as err:
                        print(f"Database error: {err}")
                        cv2.putText(im, "DB Error", (x, y - 5), font, 0.8, (255, 255, 255), 2)
                    except Exception as e:
                        print(f"Error: {e}")
                        cv2.putText(im, "Error", (x, y - 5), font, 0.8, (255, 255, 255), 2)

                cv2.imshow("Face Recognition - Press Q to quit", im)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            print(f"Recognition error: {e}")
            messagebox.showerror("Error", f"Recognition failed: {str(e)}")
        finally:
            if 'cam' in locals():
                cam.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()