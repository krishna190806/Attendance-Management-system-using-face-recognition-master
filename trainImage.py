import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image


# Enhanced Train Image function with better error handling
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    # Safe message update function
    def safe_update_message(msg, color=None):
        try:
            if color:
                message.configure(text=msg, fg=color)
            else:
                message.configure(text=msg)
        except:
            print(f"Message: {msg}")
    
    try:
        safe_update_message("🤖 Initializing AI model training...")
        
        # Check if training images exist
        if not os.path.exists(trainimage_path) or not os.listdir(trainimage_path):
            error_msg = "❌ No training images found! Please capture student images first."
            safe_update_message(error_msg)
            text_to_speech("No training images found. Please capture student images first.")
            return
            
        # Initialize recognizer and detector
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        if detector.empty():
            error_msg = "❌ Face detection model not found!"
            safe_update_message(error_msg)
            text_to_speech("Face detection model not found")
            return
            
        safe_update_message("📁 Processing training images...")
        
        # Get images and labels
        faces, Ids = getImagesAndLables(trainimage_path)
        
        if len(faces) == 0:
            error_msg = "❌ No valid training images found!"
            safe_update_message(error_msg)
            text_to_speech("No valid training images found")
            return
            
        safe_update_message(f"🔄 Training model with {len(faces)} images...")
        
        # Train the model
        recognizer.train(faces, np.array(Ids))
        
        # Ensure directory exists for saving model
        os.makedirs(os.path.dirname(trainimagelabel_path), exist_ok=True)
        recognizer.save(trainimagelabel_path)
        
        success_msg = f"✅ AI model trained successfully with {len(faces)} images!"
        safe_update_message(success_msg)
        text_to_speech("AI model trained successfully")
        
    except Exception as e:
        error_msg = f"❌ Training failed: {str(e)}"
        safe_update_message(error_msg)
        text_to_speech(f"Training failed: {str(e)}")


def getImagesAndLables(path):
    """Extract faces and labels from training images"""
    try:
        faces = []
        Ids = []
        
        # Get all subdirectories (student folders)
        if not os.path.exists(path):
            return faces, Ids
            
        student_dirs = [d for d in os.listdir(path) 
                       if os.path.isdir(os.path.join(path, d))]
        
        if not student_dirs:
            return faces, Ids
            
        for student_dir in student_dirs:
            student_path = os.path.join(path, student_dir)
            
            # Get all image files in the student directory
            image_files = [f for f in os.listdir(student_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            for image_file in image_files:
                image_path = os.path.join(student_path, image_file)
                try:
                    # Load and convert image
                    pilImage = Image.open(image_path).convert("L")
                    imageNp = np.array(pilImage, "uint8")
                    
                    # Extract ID from filename (format: Name_ID_number.jpg)
                    parts = image_file.split("_")
                    if len(parts) >= 2:
                        Id = int(parts[1])  # Get the enrollment ID
                        faces.append(imageNp)
                        Ids.append(Id)
                        
                except (ValueError, IndexError, IOError) as e:
                    print(f"Error processing {image_path}: {e}")
                    continue
                    
        return faces, Ids
        
    except Exception as e:
        print(f"Error in getImagesAndLables: {e}")
        return [], []
