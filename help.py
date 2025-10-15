from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import PIL


class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Help Desk")

        title_lb1 = Label(self.root, text="HELP DESK", font=("time new roman", 35, "bold"),
                          bg="white", fg="dark blue")
        title_lb1.place(x=0, y=0, width=1530, height=45)

        # Background with error handling
        try:
            img_top = Image.open("Images/help.jpg")
            img_top = img_top.resize((1530, 740), PIL.Image.Resampling.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            bg_label = Label(self.root, image=self.photoimg_top)
        except:
            bg_label = Label(self.root, bg="lightblue")

        bg_label.place(x=0, y=55, width=1530, height=740)

        # Main help frame
        main_frame = Frame(bg_label, bg="black", bd=3, relief=RAISED)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=400)

        # Title
        title_label = Label(main_frame, text="Development Team",
                            font=("time new roman", 20, "bold"),
                            fg="white", bg="black", pady=10)
        title_label.pack()

        # Contact information - Ensure this list only contains valid pairs
        contact_info = [
            ("Nandhini Sri", "Nandy@gmail.com"),
            ("Sruthi", "Sruthi@gmail.com"),
            ("Kanishka", "Kanishka@gmail.com"),
            ("Shubhakarini", "Shubha@gmail.com"),
            ("Arul Jothi", "ArulJothi@gmail.com"),
            ("Boovana Nathan", "BoovanaNathan@gmail.com"),
            ("Singa Adithya", "SingaAdithya@gmail.com"),
            ("Nithesh Kumar", "Nithesh@gmail.com")
        ]

        # Filter out any invalid entries (just in case)
        contact_info = [(name, email) for name, email in contact_info
                       if name and email and not name.lower().startswith('se') and not email.lower().startswith('se')]

        # Create frames for two columns
        left_frame = Frame(main_frame, bg="black")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        right_frame = Frame(main_frame, bg="black")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10)

        # Split contacts into two columns
        mid_point = len(contact_info) // 2
        left_contacts = contact_info[:mid_point]
        right_contacts = contact_info[mid_point:]

        # Left column
        for name, email in left_contacts:
            contact_label = Label(left_frame,
                                  text=f"{name}\n{email}",
                                  font=("time new roman", 12, "bold"),
                                  fg="white", bg="black",
                                  justify=LEFT)
            contact_label.pack(pady=8, anchor=W)

        # Right column
        for name, email in right_contacts:
            contact_label = Label(right_frame,
                                  text=f"{name}\n{email}",
                                  font=("time new roman", 12, "bold"),
                                  fg="white", bg="black",
                                  justify=LEFT)
            contact_label.pack(pady=8, anchor=W)





if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()