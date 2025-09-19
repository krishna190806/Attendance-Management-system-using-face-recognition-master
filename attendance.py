import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import takeImage
import trainImage
import automaticAttedance


def text_to_speech(user_text):
    try:
        engine = pyttsx3.init()
        engine.say(user_text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./TrainingImageLabel/Trainner.yml"
)
trainimage_path = "/TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "./StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"

# Customized Theme Colors for Better UI
PRIMARY_COLOR = "#2563eb"  # Professional Blue
SECONDARY_COLOR = "#7c3aed"  # Modern Purple
ACCENT_COLOR = "#0ea5e9"  # Fresh Light Blue
BG_COLOR = "#e2e8f0"  # Soft Gray Background
CARD_COLOR = "#e2e8f0"  # Consistent with Background
CARD_HOVER = "#d1d5db"  # Subtle darkening on hover
TEXT_COLOR = "#1e293b"  # Dark Text
TEXT_SECONDARY = "#475569"  # Muted Darker Text
SUCCESS_COLOR = "#16a34a"  # Clean Green
WARNING_COLOR = "#f59e0b"  # Bright Orange
ERROR_COLOR = "#ef4444"  # Vivid Red
SHADOW_COLOR = "rgba(0, 0, 0, 0.05)"  # Very Soft Shadow
GRADIENT_START = "#cfd8e3"  # Soft Blue Gradient
GRADIENT_END = "#93c5fd"    # Light Blue to Blue Gradient
BORDER_COLOR = "#cbd5e1"    # Subtle Border

# Modern UI Setup
window = Tk()
window.title("CLASS VISION - Smart Attendance System")
window.geometry("1400x800")
window.state('zoomed')  # Start maximized
window.configure(bg=BG_COLOR)  # Premium dark background
window.resizable(True, True)

dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",  # Dark background for the error window
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",  # Darker button color
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


# Create modern header with gradient effect
header_frame = Frame(window, bg=BG_COLOR, height=120)
header_frame.pack(fill=X, padx=0, pady=0)
header_frame.pack_propagate(False)

# Logo and title section
title_frame = Frame(header_frame, bg=BG_COLOR)
title_frame.pack(expand=True, fill=BOTH, pady=20)

# Load and resize logo
logo = Image.open("UI_Image/0001.png")
logo = logo.resize((80, 76), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)

# Create modern title with logo
logo_label = tk.Label(title_frame, image=logo1, bg=BG_COLOR)
logo_label.pack(side=LEFT, padx=(50, 20))

title_label = tk.Label(
    title_frame, 
    text="CLASS VISION", 
    bg=BG_COLOR, 
    fg=TEXT_COLOR, 
    font=("Inter", 36, "bold")
)
title_label.pack(side=LEFT, pady=10)

subtitle_label = tk.Label(
    title_frame,
    text="Smart Face Recognition Attendance System",
    bg=BG_COLOR,
    fg=TEXT_SECONDARY,
    font=("Inter", 14)
)
subtitle_label.pack(side=LEFT, padx=(20, 0), pady=10)

# Main content area
main_frame = Frame(window, bg=BG_COLOR)
main_frame.pack(expand=True, fill=BOTH, padx=40, pady=20)

# Enhanced Welcome section with better design
welcome_frame = Frame(main_frame, bg=BG_COLOR, relief=FLAT, bd=0)
welcome_frame.pack(fill=X, pady=(0, 50))

welcome_label = tk.Label(
    welcome_frame,
    text="Welcome to CLASS VISION",
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=("Inter", 32, "bold"),
    pady=15
)
welcome_label.pack()

desc_label = tk.Label(
    welcome_frame,
    text="Experience seamless, AI-powered attendance tracking with real-time face recognition technology",
    bg=BG_COLOR,
    fg=TEXT_SECONDARY,
    font=("Inter", 16),
    wraplength=800
)
desc_label.pack(pady=(5, 20))

# Enhanced Dashboard Design - Clean and Focused

# Cards container
cards_frame = Frame(main_frame, bg=BG_COLOR)
cards_frame.pack(expand=True, fill=BOTH)


def TakeImageUI():
    # Use a child window instead of creating a second root
    ImageUI = Toplevel(window)
    ImageUI.title("👤 Student Registration")
    ImageUI.geometry("900x650")
    ImageUI.configure(bg=BG_COLOR)
    ImageUI.resizable(True, True)
    ImageUI.minsize(700, 500)

    # Main container
    main_frame = Frame(ImageUI, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH, padx=40, pady=30)

    # Header Section
    title_label = Label(main_frame, text="👤 Student Registration", bg=BG_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 28, "bold"))
    title_label.pack(pady=(0, 10))

    subtitle = Label(main_frame, text="Register new student with face recognition", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 16))
    subtitle.pack(pady=(0, 30))

    # Input Section in Card
    input_card = Frame(main_frame, bg=CARD_COLOR, relief=FLAT, bd=0)
    input_card.pack(fill=X, pady=(0, 20))

    # Form fields
    form_frame = Frame(input_card, bg=CARD_COLOR)
    form_frame.pack(pady=30, padx=30, fill=X)

    # Enrollment Number
    lbl1 = Label(form_frame, text="Enrollment Number:", bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 14, "bold"))
    lbl1.pack(pady=(0, 10), anchor=W)

    txt1 = Entry(form_frame, width=30, bg="#f1f5f9", fg=TEXT_COLOR, font=("Segoe UI", 16),
                relief=SOLID, bd=1, insertbackground=TEXT_COLOR, validate="key",
                highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_COLOR, highlightthickness=1)
    txt1.pack(pady=(0, 20), ipady=10, fill=X)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Student Name
    lbl2 = Label(form_frame, text="Student Name:", bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 14, "bold"))
    lbl2.pack(pady=(0, 10), anchor=W)

    txt2 = Entry(form_frame, width=30, bg="#f1f5f9", fg=TEXT_COLOR, font=("Segoe UI", 16),
                relief=SOLID, bd=1, insertbackground=TEXT_COLOR,
                highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_COLOR, highlightthickness=1)
    txt2.pack(pady=(0, 20), ipady=10, fill=X)

    # Notification area
    message = Label(main_frame, text="", bg=BG_COLOR, fg=SUCCESS_COLOR, font=("Segoe UI", 12), wraplength=600)
    message.pack(pady=(10, 20))

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        message.configure(text="📸 Starting camera for image capture...", fg=WARNING_COLOR)
        ImageUI.update()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    def train_image():
        message.configure(text="🤖 Training AI model with captured images...", fg=WARNING_COLOR)
        ImageUI.update()
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Modern Button Styles
    def modern_button_local(parent, text, command, color, emoji=""):
        btn = Button(parent, text=f"{emoji} {text}", command=command, bg=color, fg="white",
                    font=("Segoe UI", 14, "bold"), relief=FLAT, bd=0, padx=30, pady=15,
                    cursor="hand2", activebackground=color)
        # Hover effects
        def on_enter(e):
            btn.configure(relief=RAISED, bd=2)
        def on_leave(e):
            btn.configure(relief=FLAT, bd=0)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # Buttons Section - use grid for reliable horizontal layout
    buttons_frame = Frame(main_frame, bg=BG_COLOR)
    buttons_frame.pack(fill=X, pady=(20, 0))
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)

    takeImg = modern_button_local(buttons_frame, "Take Images", take_image, PRIMARY_COLOR, "📸")
    trainImg = modern_button_local(buttons_frame, "Train Model", train_image, SUCCESS_COLOR, "🤖")

    takeImg.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    trainImg.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


# Create modern action cards with hover and dynamic effects
def create_action_card(parent, title, description, icon_path, command, color):
    card = Frame(parent, bg=CARD_COLOR, relief=FLAT, bd=0, padx=30, pady=20)
    card.pack(side=LEFT, fill=BOTH, expand=True, padx=15)
    card.bind("<Enter>", lambda e: card.configure(bg=CARD_HOVER))
    card.bind("<Leave>", lambda e: card.configure(bg=CARD_COLOR))
    
    # Card header with icon
    header_frame = Frame(card, bg=CARD_COLOR)
    header_frame.pack(fill=X, pady=(10, 10))
    
    try:
        icon = Image.open(icon_path)
        icon = icon.resize((64, 64), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon)
        icon_label = tk.Label(header_frame, image=icon_photo, bg=CARD_COLOR)
        icon_label.image = icon_photo  # Keep a reference
        icon_label.pack(pady=5)
    except:
        pass

    # Title
    title_label = tk.Label(
        card,
        text=title,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        font=("Lato", 22, "bold"),
        wraplength=250
    )
    title_label.pack(pady=(5, 5))
    
    # Description
    desc_label = tk.Label(
        card,
        text=description,
        bg=CARD_COLOR,
        fg=TEXT_SECONDARY,
        font=("Lato", 12),
        wraplength=250,
        justify=CENTER
    )
    desc_label.pack(pady=(0, 15))
    
    # Modern button
    btn = tk.Button(
        card,
        text=f"🚀 {title}",
        command=command,
        bg=color,
        fg="white",
        font=("Lato", 14, "bold"),
        relief=FLAT,
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        activebackground=color,
        activeforeground="white"
    )
    btn.pack(fill=X, pady=(5, 10))
    
    # Button hover effects
    def on_enter(e):
        btn.configure(bg=ACCENT_COLOR, relief=RAISED, bd=2)
    
    def on_leave(e):
        btn.configure(bg=color, relief=FLAT, bd=0)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    # Shadow effect
    card.configure(relief=SUNKEN)

    return card

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)




def manual_attendance():
    import takemanually
    takemanually.manually_fill()

def view_attendance():
    """Open the attendance viewer with Excel download functionality"""
    import show_attendance
    show_attendance.subjectchoose(text_to_speech)


# Create action cards in original layout (3 in first row, 2 in second row)
create_action_card(
    cards_frame,
    "Register Student",
    "Add new students to the system with face recognition training",
    "UI_Image/register.png",
    TakeImageUI,
    PRIMARY_COLOR
)

create_action_card(
    cards_frame,
    "Take Attendance",
    "Start real-time face recognition attendance for your class",
    "UI_Image/verifyy.png",
    automatic_attedance,
    SUCCESS_COLOR
)

create_action_card(
    cards_frame,
    "View Reports",
    "Generate and download detailed attendance reports in Excel format",
    "UI_Image/attendance.png",
    view_attendance,
    SECONDARY_COLOR
)

# Create a second row for additional options
second_row_frame = Frame(main_frame, bg=BG_COLOR)
second_row_frame.pack(expand=True, fill=BOTH, pady=(20, 0))

def download_attendance_excel():
    """Open dialog to download attendance Excel files"""
    def show_download_options():
        """Show download options window"""
        download_window = Toplevel(window)
        download_window.title("📥 Download Attendance Excel")
        download_window.geometry("600x400")
        download_window.configure(bg=BG_COLOR)
        download_window.resizable(True, True)
        
        # Header
        header_label = Label(
            download_window,
            text="📥 Download Attendance Excel",
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
            font=("Segoe UI", 24, "bold")
        )
        header_label.pack(pady=(20, 10))
        
        subtitle_label = Label(
            download_window,
            text="Select a subject to download formatted attendance reports",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 12)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Get available subjects
        subjects = []
        if os.path.exists("Attendance"):
            for item in os.listdir("Attendance"):
                item_path = os.path.join("Attendance", item)
                if os.path.isdir(item_path):
                    subjects.append(item)
        
        if subjects:
            # Subject selection
            subject_frame = Frame(download_window, bg=BG_COLOR)
            subject_frame.pack(fill=X, padx=40, pady=20)
            
            subject_label = Label(
                subject_frame,
                text="Choose Subject:",
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                font=("Segoe UI", 14, "bold")
            )
            subject_label.pack(anchor="w", pady=(0, 10))
            
            subject_var = StringVar(download_window)
            subject_var.set(subjects[0])
            
            subject_combo = ttk.Combobox(
                subject_frame,
                textvariable=subject_var,
                values=list(subjects),
                font=("Segoe UI", 12),
                state="readonly"
            )
            subject_combo.pack(fill=X, pady=(0, 20))
            
            def download_selected():
                selected_subject = subject_var.get()
                download_window.destroy()
                # Import and use the existing download functionality
                import show_attendance
                show_attendance.subjectchoose_with_subject(text_to_speech, selected_subject)
            
            download_btn = Button(
                subject_frame,
                text="📥 Download Excel Report",
                command=download_selected,
                bg=SUCCESS_COLOR,
                fg="white",
                font=("Segoe UI", 14, "bold"),
                relief=FLAT,
                bd=0,
                padx=30,
                pady=15,
                cursor="hand2"
            )
            download_btn.pack(fill=X)
            
        else:
            # No subjects available
            no_data_label = Label(
                download_window,
                text="No attendance data found.\nTake attendance first to generate reports.",
                bg=BG_COLOR,
                fg=ERROR_COLOR,
                font=("Segoe UI", 14),
                justify=CENTER
            )
            no_data_label.pack(expand=True)
        
        download_window.mainloop()
    
    show_download_options()

def open_attendance_folder():
    """Open the attendance folder in file explorer"""
    try:
        import subprocess
        import platform
        
        attendance_folder = os.path.abspath("Attendance")
        if os.path.exists(attendance_folder):
            if platform.system() == "Windows":
                subprocess.Popen(['explorer', attendance_folder])
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', attendance_folder])
            else:  # Linux
                subprocess.Popen(['xdg-open', attendance_folder])
            text_to_speech("Opening attendance folder")
        else:
            messagebox.showinfo("Info", "Attendance folder will be created after taking attendance for the first time.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open folder: {str(e)}")

create_action_card(
    second_row_frame,
    "Manual Entry",
    "Manually enter attendance records for students",
    "UI_Image/0003.png",
    manual_attendance,
    WARNING_COLOR
)

create_action_card(
    second_row_frame,
    "Download Excel",
    "Download formatted Excel reports for any subject with statistics",
    "UI_Image/0004.png",
    download_attendance_excel,
    "#10b981"
)

create_action_card(
    second_row_frame,
    "Open Folder",
    "Browse attendance files and folders on your computer",
    "UI_Image/0002.png",
    open_attendance_folder,
    "#8b5cf6"
)

# Bottom section with exit button
bottom_frame = Frame(window, bg=BG_COLOR, height=80)
bottom_frame.pack(fill=X, side=BOTTOM, padx=40, pady=20)
bottom_frame.pack_propagate(False)

exit_btn = tk.Button(
    bottom_frame,
    text="🚪 Exit Application",
    command=quit,
    bg=ERROR_COLOR,
    fg="white",
    font=("Segoe UI", 14, "bold"),
    relief=FLAT,
    bd=0,
    padx=40,
    pady=15,
    cursor="hand2"
)
exit_btn.pack(side=BOTTOM, pady=10)

# Status bar
status_frame = Frame(bottom_frame, bg=BG_COLOR)
status_frame.pack(fill=X, side=BOTTOM)

status_label = tk.Label(
    status_frame,
    text=f"© 2025 CLASS VISION | Ready • System Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    bg=BG_COLOR,
    fg=ACCENT_COLOR,
    font=("Segoe UI", 10)
)
status_label.pack(side=BOTTOM)


window.mainloop()
