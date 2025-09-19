import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time


# Enhanced take Image function with better error handling
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    # Input validation with safe message updates
    def safe_update_message(msg, color=None):
        try:
            if color:
                message.configure(text=msg, fg=color)
            else:
                message.configure(text=msg)
        except:
            print(f"Message: {msg}")
    
    if (l1 == "") and (l2 == ""):
        t = "Please Enter your Enrollment Number and Name."
        text_to_speech(t)
        safe_update_message("⚠️ Both enrollment and name are required!")
        return
    elif l1 == "":
        t = "Please Enter your Enrollment Number."
        text_to_speech(t)
        safe_update_message("⚠️ Enrollment number is required!")
        return
    elif l2 == "":
        t = "Please Enter your Name."
        text_to_speech(t)
        safe_update_message("⚠️ Student name is required!")
        return
    
    try:
        # Initialize camera and detector
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            error_msg = "❌ Camera not found or unable to open!"
            safe_update_message(error_msg)
            text_to_speech("Camera not found or unable to open")
            return
            
        detector = cv2.CascadeClassifier(haarcasecade_path)
        if detector.empty():
            error_msg = "❌ Face detection model not found!"
            safe_update_message(error_msg)
            text_to_speech("Face detection model not found")
            cam.release()
            return
            
        Enrollment = l1
        Name = l2
        sampleNum = 0
        directory = Enrollment + "_" + Name
        path = os.path.join(trainimage_path, directory)
        
        # Check if directory already exists
        if os.path.exists(path):
            error_msg = "⚠️ Student data already exists!"
            safe_update_message(error_msg)
            text_to_speech("Student data already exists")
            cam.release()
            return
            
        os.makedirs(path, exist_ok=True)
        safe_update_message("📸 Camera initialized. Look at the camera...")
        
        while True:
            ret, img = cam.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                sampleNum += 1
                
                # Save face image
                filename = f"{path}/{Name}_{Enrollment}_{sampleNum}.jpg"
                cv2.imwrite(filename, gray[y:y+h, x:x+w])
                
                # Show progress
                cv2.putText(img, f"Samples: {sampleNum}/50", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                           
            cv2.imshow("Taking Images - Press 'q' to quit early", img)
            
            # Break conditions
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif sampleNum >= 50:
                break
                
        # Clean up
        cam.release()
        cv2.destroyAllWindows()
        
        # Save student details to CSV
        if sampleNum > 0:
            os.makedirs("StudentDetails", exist_ok=True)
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+", newline="") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                
            success_msg = f"✅ {sampleNum} images saved for {Name} (ID: {Enrollment})"
            safe_update_message(success_msg)
            text_to_speech(f"Images saved successfully for {Name}")
        else:
            error_msg = "❌ No images captured! Please try again."
            safe_update_message(error_msg)
            text_to_speech("No images captured")
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        safe_update_message(error_msg)
        text_to_speech(f"Error occurred: {str(e)}")
        try:
            cam.release()
            cv2.destroyAllWindows()
        except:
            pass
