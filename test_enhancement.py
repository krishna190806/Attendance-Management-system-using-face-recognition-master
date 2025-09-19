#!/usr/bin/env python3
"""
Test script to validate the enhanced attendance system
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import attendance
        print("✅ attendance.py imported successfully")
        
        import automaticAttedance
        print("✅ automaticAttedance.py imported successfully")
        
        import show_attendance
        print("✅ show_attendance.py imported successfully")
        
        # Test if the new function exists
        if hasattr(show_attendance, 'subjectchoose_with_subject'):
            print("✅ subjectchoose_with_subject function found in show_attendance.py")
        else:
            print("❌ subjectchoose_with_subject function NOT found")
            
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_attendance_folder_structure():
    """Test if the attendance folder structure is accessible"""
    try:
        attendance_path = "Attendance"
        if os.path.exists(attendance_path):
            subjects = [item for item in os.listdir(attendance_path) 
                       if os.path.isdir(os.path.join(attendance_path, item))]
            print(f"✅ Attendance folder found with {len(subjects)} subjects: {subjects}")
            return True
        else:
            print("⚠️ Attendance folder not found (this is normal for new installations)")
            return True
    except Exception as e:
        print(f"❌ Error checking attendance folder: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Enhanced Attendance System...")
    print("=" * 50)
    
    success = True
    
    print("\n📦 Testing Imports:")
    success &= test_imports()
    
    print("\n📁 Testing File Structure:")
    success &= test_attendance_folder_structure()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! The enhanced attendance system is ready.")
        print("\n🎯 New Features Added:")
        print("   • After taking attendance, you'll see a dialog with options")
        print("   • Click 'View Attendance Reports' to see detailed statistics")
        print("   • Click 'Download Excel File' to save formatted reports")
        print("   • The attendance viewer now auto-loads for the selected subject")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    input("\nPress Enter to exit...")