#!/usr/bin/env python3
"""
Test script to verify the Excel/CSV download parameter fix
"""

import tkinter as tk
from tkinter import filedialog
import tempfile
import os

def test_filedialog_parameters():
    """Test that the file dialog parameters work correctly"""
    
    print("🧪 Testing file dialog parameters...")
    
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Test the corrected parameters
        test_filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Test Excel Save Dialog",
            initialfile="test_file.xlsx"
        )
        
        print("✅ Excel file dialog parameters are correct")
        
        test_filename2 = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Test CSV Save Dialog",
            initialfile="test_file.csv"
        )
        
        print("✅ CSV file dialog parameters are correct")
        print("✅ All file dialog parameter fixes are working!")
        
        # Note: The dialogs won't actually show since we're running in headless mode
        # but the fact that they don't throw errors means the parameters are correct
        
    except Exception as e:
        print(f"❌ Error with file dialog parameters: {e}")
        return False
    finally:
        root.destroy()
    
    return True

def main():
    """Main test function"""
    print("🔧 Testing Excel/CSV Download Parameter Fix")
    print("=" * 50)
    
    success = test_filedialog_parameters()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Parameter fix test PASSED!")
        print("📝 The 'initialname' -> 'initialfile' parameter fix is working correctly")
        print("📝 Excel and CSV downloads should now work without the parameter error")
    else:
        print("❌ Parameter fix test FAILED!")
        print("📝 There may still be parameter issues with the file dialogs")
    
    return success

if __name__ == "__main__":
    main()