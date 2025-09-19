#!/usr/bin/env python3
"""
Demo script to show the enhanced attendance completion interface
This simulates what happens after taking attendance successfully
"""

import tkinter
from tkinter import *
import datetime

def demo_attendance_completion():
    """Demo the new attendance completion interface"""
    # Simulate the enhanced interface that appears after taking attendance
    Subject = "Math"  # Example subject
    
    # This is the same code that runs after attendance is taken
    options_window = tkinter.Tk()
    options_window.title("CLASS VISION - Attendance Management")
    options_window.geometry("1000x700")
    options_window.configure(bg="#1a1a2e")
    options_window.resizable(True, True)
    
    # Color scheme matching the second image
    DARK_BG = "#1a1a2e"
    CARD_BG = "#16213e"
    ACCENT_COLOR = "#0F3460"
    CYAN_COLOR = "#00d4ff"
    BUTTON_COLOR = "#00a8cc"
    TEXT_COLOR = "#ffffff"
    
    # Header with logo and title
    header_frame = tkinter.Frame(options_window, bg=DARK_BG, height=100)
    header_frame.pack(fill="x", padx=20, pady=(20, 10))
    header_frame.pack_propagate(False)
    
    # Fallback text logo
    logo_label = tkinter.Label(
        header_frame, 
        text="✓", 
        bg=DARK_BG, 
        fg=CYAN_COLOR, 
        font=("Segoe UI", 30, "bold")
    )
    logo_label.pack(side="left", padx=(20, 15))
    
    title_frame = tkinter.Frame(header_frame, bg=DARK_BG)
    title_frame.pack(side="left", fill="both", expand=True)
    
    main_title = tkinter.Label(
        title_frame,
        text="CLASS VISION",
        bg=DARK_BG,
        fg=CYAN_COLOR,
        font=("Segoe UI", 24, "bold")
    )
    main_title.pack(anchor="w")
    
    subtitle = tkinter.Label(
        title_frame,
        text="AI-Powered Face Recognition Attendance System",
        bg=DARK_BG,
        fg="#8892b0",
        font=("Segoe UI", 12)
    )
    subtitle.pack(anchor="w")
    
    # Divider line
    divider = tkinter.Frame(options_window, bg=CYAN_COLOR, height=3)
    divider.pack(fill="x", padx=20, pady=(0, 20))
    
    # Welcome message
    welcome_frame = tkinter.Frame(options_window, bg=CARD_BG, relief="solid", bd=1)
    welcome_frame.pack(fill="x", padx=50, pady=(10, 30))
    
    welcome_title = tkinter.Label(
        welcome_frame,
        text=f"Attendance Recorded Successfully for {Subject}!",
        bg=CARD_BG,
        fg=CYAN_COLOR,
        font=("Segoe UI", 20, "bold")
    )
    welcome_title.pack(pady=20)
    
    # Main content area with cards
    content_frame = tkinter.Frame(options_window, bg=DARK_BG)
    content_frame.pack(expand=True, fill="both", padx=50, pady=20)
    
    def create_action_card(parent, title, description, command, icon=""):
        # Card container
        card_frame = tkinter.Frame(parent, bg=CARD_BG, relief="solid", bd=1)
        card_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        # Card content
        card_content = tkinter.Frame(card_frame, bg=CARD_BG)
        card_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon
        icon_label = tkinter.Label(
            card_content,
            text=icon,
            bg=CARD_BG,
            fg=TEXT_COLOR,
            font=("Segoe UI", 40)
        )
        icon_label.pack(pady=(10, 20))
        
        # Title
        title_label = tkinter.Label(
            card_content,
            text=title,
            bg=CARD_BG,
            fg=TEXT_COLOR,
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = tkinter.Label(
            card_content,
            text=description,
            bg=CARD_BG,
            fg="#8892b0",
            font=("Segoe UI", 11),
            wraplength=250,
            justify="center"
        )
        desc_label.pack(pady=(0, 20))
        
        # Action button
        action_btn = tkinter.Button(
            card_content,
            text=f"Open {title}",
            command=command,
            bg=BUTTON_COLOR,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        action_btn.pack()
        
        # Hover effects
        def on_enter(e):
            action_btn.configure(bg="#0097b8")
            card_frame.configure(bg="#1e2951")
            card_content.configure(bg="#1e2951")
            icon_label.configure(bg="#1e2951")
            title_label.configure(bg="#1e2951")
            desc_label.configure(bg="#1e2951")
        
        def on_leave(e):
            action_btn.configure(bg=BUTTON_COLOR)
            card_frame.configure(bg=CARD_BG)
            card_content.configure(bg=CARD_BG)
            icon_label.configure(bg=CARD_BG)
            title_label.configure(bg=CARD_BG)
            desc_label.configure(bg=CARD_BG)
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        action_btn.bind("<Enter>", on_enter)
        action_btn.bind("<Leave>", on_leave)
        
        return card_frame
    
    def demo_download():
        print("Demo: Download Excel would be executed")
        
    def demo_view():
        print("Demo: View Attendance would be executed")
        
    def demo_all():
        print("Demo: All Subjects would be executed")
    
    # Create action cards
    create_action_card(
        content_frame,
        "Download Excel",
        "Download the attendance data as a formatted Excel spreadsheet with statistics and charts.",
        demo_download,
        "📥"
    )
    
    create_action_card(
        content_frame,
        "View Attendance",
        f"Browse and analyze attendance records for {Subject}, generate reports, and view attendance statistics.",
        demo_view,
        "📊"
    )
    
    create_action_card(
        content_frame,
        "All Subjects",
        "Browse and analyze attendance records for all subjects, generate comprehensive reports.",
        demo_all,
        "📋"
    )
    
    # Bottom section with exit button
    bottom_frame = tkinter.Frame(options_window, bg=DARK_BG, height=80)
    bottom_frame.pack(fill="x", side="bottom", padx=50, pady=20)
    bottom_frame.pack_propagate(False)
    
    def close_window():
        options_window.destroy()
    
    exit_btn = tkinter.Button(
        bottom_frame,
        text="✖️ Close Demo",
        command=close_window,
        bg="#ef4444",
        fg="white",
        font=("Segoe UI", 14, "bold"),
        relief="flat",
        bd=0,
        padx=40,
        pady=15,
        cursor="hand2"
    )
    exit_btn.pack(side="bottom")
    
    # Status bar
    status_label = tkinter.Label(
        bottom_frame,
        text=f"© 2025 CLASS VISION | Demo Mode • System Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        bg=DARK_BG,
        fg=CYAN_COLOR,
        font=("Segoe UI", 10)
    )
    status_label.pack(side="bottom", pady=(10, 0))
    
    print("🎯 DEMO: This is what you'll see AFTER taking attendance successfully!")
    print("📝 To see this in the real application:")
    print("   1. Click 'Take Attendance' from main screen")
    print("   2. Enter a subject name")  
    print("   3. Complete face recognition process")
    print("   4. This interface will appear!")
    
    options_window.mainloop()

if __name__ == "__main__":
    demo_attendance_completion()