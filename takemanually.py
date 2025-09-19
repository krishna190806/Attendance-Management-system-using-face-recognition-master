import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import os
import csv
import pandas as pd
import datetime
import time
from PIL import Image, ImageTk

# Modern UI Setup and Variables
ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")
d = {}
index = 0

# Enhanced Modern Color Scheme
PRIMARY_COLOR = "#2563eb"  # Professional Blue
SECONDARY_COLOR = "#7c3aed"  # Modern Purple
ACCENT_COLOR = "#06b6d4"  # Vibrant Teal
BG_COLOR = "#0f0f23"  # Enhanced Deep Dark
CARD_COLOR = "#1e1e3f"  # Enhanced Card Background
CARD_HOVER = "#2d2d5f"  # Enhanced Hover State
TEXT_COLOR = "#f8fafc"  # Clean White
TEXT_SECONDARY = "#cbd5e1"  # Muted Text
SUCCESS_COLOR = "#10b981"  # Professional Green
WARNING_COLOR = "#f59e0b"  # Warm Orange
ERROR_COLOR = "#ef4444"  # Clean Red
INPUT_BG = "#2d2d5f"  # Input Background
BUTTON_HOVER = "#1d4ed8"  # Button Hover

####Modern GUI for manually fill attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap("AMS.ico")
    sb.title("📝 Manual Attendance Entry")
    sb.geometry("900x600")
    sb.configure(background=BG_COLOR)

    # Add a logo to the header
    logo_img = Image.open("UI_Image/0001.png")
    logo_img = logo_img.resize((60, 60), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(sb, image=logo_photo, bg=BG_COLOR)
    logo_label.image = logo_photo  # Keep a reference
    logo_label.pack(pady=(10, 0))

    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry("400x150")
        ec.iconbitmap("AMS.ico")
        ec.title("⚠️ Warning")
        ec.configure(background=BG_COLOR)
        ec.resizable(False, False)
        
        # Main frame
        main_frame = Frame(ec, bg=BG_COLOR)
        main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)
        
        warning_label = tk.Label(
            main_frame,
            text="⚠️ Please enter subject name!",
            fg=WARNING_COLOR,
            bg=BG_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        warning_label.pack(pady=(10, 20))
        
        ok_btn = tk.Button(
            main_frame,
            text="OK",
            command=ec_delete,
            fg="white",
            bg=PRIMARY_COLOR,
            width=12,
            height=1,
            relief=FLAT,
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 12, "bold"),
        )
        ok_btn.pack()

    def fill_attendance():

        ##Create table for Attendance
        global subb
        subb = SUB_ENTRY.get()

        if subb == "":
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap("AMS.ico")
            MFW.title(f"📝 Manual Attendance - {str(subb)}")
            MFW.geometry("900x600")
            MFW.configure(background=BG_COLOR)

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry("330x100")
                errsc2.iconbitmap("AMS.ico")
                errsc2.title("Warning!!")
                errsc2.configure(background="snow")
                tk.Label(
                    errsc2,
                    text="Please enter Student & Enrollment!!!",
                    fg="red",
                    bg="white",
                    font=("times", 16, " bold "),
                ).pack()
                tk.Button(
                    errsc2,
                    text="OK",
                    command=del_errsc2,
                    fg="black",
                    bg="lawn green",
                    width=9,
                    height=1,
                    activebackground="Red",
                    font=("times", 15, " bold "),
                ).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == "1":  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(
                MFW,
                text="Enter Enrollment",
                width=15,
                height=2,
                fg="white",
                bg="blue2",
                font=("times", 15, " bold "),
            )
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(
                MFW,
                text="Enter Student name",
                width=15,
                height=2,
                fg="white",
                bg="blue2",
                font=("times", 15, " bold "),
            )
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(
                MFW,
                width=20,
                validate="key",
                bg=INPUT_BG,
                fg=TEXT_COLOR,
                font=("times", 23, " bold "),
            )
            ENR_ENTRY["validatecommand"] = (ENR_ENTRY.register(testVal), "%P", "%d")
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg=INPUT_BG, fg=TEXT_COLOR, font=("times", 23, " bold ")
            )
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            ####get important variable

            def enter_data_DB():
                global index
                global d
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == "":
                    err_screen1()
                elif STUDENT == "":
                    err_screen1()
                else:
                    if index == 0:
                        d = {
                            index: {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        }
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                    else:
                        d[index] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                    # TODO implement CSV code
                print(d)

            def create_csv():
                df = pd.DataFrame(d)
                csv_name = (
                    "Attendance(Manually)/"
                    + subb
                    + "_"
                    + Date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                df.to_csv(csv_name)
                O = "CSV created Successfully"
                Notifi.configure(
                    text=O,
                    bg="Green",
                    fg="white",
                    width=33,
                    font=("times", 19, "bold"),
                )
                Notifi.place(x=180, y=380)
                """import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background="snow")
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root,
                                width=13,
                                height=1,
                                fg="black",
                                font=("times", 13, " bold "),
                                bg="lawn green",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()"""

            Notifi = tk.Label(
                MFW,
                text="CSV created Successfully",
                bg="Green",
                fg="white",
                width=33,
                height=2,
                font=("times", 19, "bold"),
            )

            c1ear_enroll = tk.Button(
                MFW,
                text="Clear",
                command=remove_enr,
                fg="black",
                bg="deep pink",
                width=10,
                height=1,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(
                MFW,
                text="Clear",
                command=remove_student,
                fg="black",
                bg="deep pink",
                width=10,
                height=1,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(
                MFW,
                text="Enter Data",
                command=enter_data_DB,
                fg="white",
                bg=PRIMARY_COLOR,
                activebackground=BUTTON_HOVER,
                width=20,
                height=2,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(
                MFW,
                text="Convert to CSV",
                command=create_csv,
                fg="white",
                bg=SECONDARY_COLOR,
                activebackground=BUTTON_HOVER,
                width=20,
                height=2,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            MAKE_CSV.place(x=570, y=300)
            # TODO remove check sheet
            def attf():
                import subprocess

                subprocess.Popen(
                    r'explorer /select,"C:/Users/patel/OneDrive/Documents/E/FBAS/Attendance(Manually)"'
                )

            attf = tk.Button(
                MFW,
                text="Check Sheets",
                command=attf,
                fg="black",
                bg="lawn green",
                width=12,
                height=1,
                activebackground="Red",
                font=("times", 14, " bold "),
            )
            attf.place(x=730, y=410)

            MFW.mainloop()

    # Main container
    main_frame = Frame(sb, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH, padx=40, pady=30)
    
    # Header Section
    title_label = Label(main_frame, text="📝 Manual Attendance Entry", bg=BG_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 24, "bold"))
    title_label.pack(pady=(0, 10))
    
    subtitle = Label(main_frame, text="Enter subject name to start manual attendance", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 14))
    subtitle.pack(pady=(0, 30))
    
    # Input Section in Card
    input_card = Frame(main_frame, bg=CARD_COLOR, relief=FLAT, bd=0)
    input_card.pack(fill=X, pady=(0, 20))
    
    form_frame = Frame(input_card, bg=CARD_COLOR)
    form_frame.pack(pady=30, padx=30)
    
    # Subject Name
    sub_label = Label(form_frame, text="Subject Name:", bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 14, "bold"))
    sub_label.pack(pady=(0, 10), anchor=W)
    
    global SUB_ENTRY
    SUB_ENTRY = Entry(form_frame, width=30, bg="#2d2d5f", fg=TEXT_COLOR, font=("Segoe UI", 16), 
                     relief=FLAT, bd=0, insertbackground=TEXT_COLOR)
    SUB_ENTRY.pack(pady=(0, 20), ipady=10, fill=X)
    
    # Modern Button
    def modern_button(parent, text, command, color, emoji=""):
        btn = Button(parent, text=f"{emoji} {text}", command=command, bg=color, fg="white", 
                    font=("Segoe UI", 14, "bold"), relief=FLAT, bd=0, padx=30, pady=15, 
                    cursor="hand2", activebackground=color)
        btn.pack(fill=X, pady=10)
        
        # Hover effects
        def on_enter(e):
            btn.configure(relief=RAISED, bd=2)
        def on_leave(e):
            btn.configure(relief=FLAT, bd=0)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    # Button Section
    buttons_frame = Frame(main_frame, bg=BG_COLOR)
    buttons_frame.pack(fill=X, pady=(20, 0))
    
    fill_btn = modern_button(buttons_frame, "Start Manual Entry", fill_attendance, PRIMARY_COLOR, "📝")
    
    sb.mainloop()
