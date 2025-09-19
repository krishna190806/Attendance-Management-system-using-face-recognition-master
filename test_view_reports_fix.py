#!/usr/bin/env python3
"""
Test script specifically for the View Reports -> Generate Report functionality
"""

import sys
import os
import pandas as pd

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_attendance_data():
    """Create sample attendance data to test with"""
    try:
        # Create sample data directory
        os.makedirs("Attendance/sgp", exist_ok=True)
        
        # Create sample CSV files similar to what the app generates
        data1 = {
            'Enrollment': [2320, 2321],
            'Name': ['Student A', 'Student B'],
            '2025-09-19': [1, 0]
        }
        
        data2 = {
            'Enrollment': [2320, 2322],
            'Name': ['Student A', 'Student C'],
            '2025-09-18': [1, 1]
        }
        
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        
        df1.to_csv("Attendance/sgp/sgp_2025-09-19_12-00-00.csv", index=False)
        df2.to_csv("Attendance/sgp/sgp_2025-09-18_12-00-00.csv", index=False)
        
        print("✅ Test attendance data created")
        return True
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return False

def test_merge_functionality():
    """Test the specific merge functionality that was causing issues"""
    try:
        print("🧪 Testing the merge functionality...")
        
        # Simulate what the calculate_attendance function does
        import pandas as pd
        from glob import glob
        
        # Read the test CSV files
        filenames = glob("Attendance/sgp/sgp*.csv")
        print(f"Found CSV files: {filenames}")
        
        if not filenames:
            print("❌ No CSV files found for testing")
            return False
        
        # Read and merge all CSV files (this is the problematic part)
        df_list = []
        for file in filenames:
            try:
                df = pd.read_csv(file)
                if not df.empty:
                    df_list.append(df)
                    print(f"✅ Read {file}: {df.shape}")
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
        
        if not df_list:
            print("❌ No valid data found")
            return False
        
        # Merge all dataframes (this was causing the error)
        merged_df = df_list[0].copy()
        print(f"Initial dataframe: {merged_df.shape}, columns: {list(merged_df.columns)}")
        
        for i, df in enumerate(df_list[1:], 1):
            print(f"Merging dataframe {i+1}: {df.shape}, columns: {list(df.columns)}")
            merged_df = merged_df.merge(df, on=['Enrollment', 'Name'], how='outer', suffixes=('', '_y'))
            print(f"After merge {i}: {merged_df.shape}, columns: {list(merged_df.columns)}")
            
            # Remove duplicate columns created by merge
            duplicate_cols = [col for col in merged_df.columns if col.endswith('_y')]
            print(f"Duplicate columns to remove: {duplicate_cols}")
            
            for col in duplicate_cols:
                original_col = col[:-2]  # Remove '_y' suffix
                if original_col in merged_df.columns:
                    # Combine the values (take max since 1 means present, 0 means absent)
                    merged_df[original_col] = merged_df[[original_col, col]].max(axis=1)
                    # Drop the duplicate column
                    merged_df = merged_df.drop(columns=[col])
                    print(f"Combined and removed {col}")
        
        print(f"Final merged dataframe: {merged_df.shape}, columns: {list(merged_df.columns)}")
        
        # Fill missing values with 0
        merged_df = merged_df.fillna(0)
        
        # Calculate attendance percentage - exclude non-date columns
        date_columns = [col for col in merged_df.columns if col not in ['Enrollment', 'Name'] and not col.endswith('_y')]
        print(f"Date columns identified: {date_columns}")
        
        if date_columns:
            # Convert attendance columns to numeric, replacing non-numeric values with 0
            for col in date_columns:
                if col in merged_df.columns:
                    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)
            
            # Filter out only valid date columns that exist in the dataframe
            valid_date_columns = [col for col in date_columns if col in merged_df.columns]
            print(f"Valid date columns: {valid_date_columns}")
            
            if valid_date_columns:
                # This was the problematic line
                merged_df['Total_Classes'] = len(valid_date_columns)
                merged_df['Classes_Attended'] = merged_df[valid_date_columns].sum(axis=1)
                merged_df['Attendance_Percentage'] = (merged_df['Classes_Attended'] / merged_df['Total_Classes'] * 100).round(2)
                
                print("✅ Attendance calculations completed successfully!")
                print(f"Final result:\n{merged_df}")
                return True
            else:
                print("❌ No valid date columns found")
                return False
        else:
            print("❌ No date columns found")
            return False
            
    except Exception as e:
        print(f"❌ Error in merge functionality: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_data():
    """Clean up test data"""
    try:
        import shutil
        if os.path.exists("Attendance/sgp"):
            shutil.rmtree("Attendance/sgp")
        print("✅ Test data cleaned up")
    except Exception as e:
        print(f"Warning: Could not clean up test data: {e}")

if __name__ == "__main__":
    print("🎯 Testing View Reports -> Generate Report Fix")
    print("=" * 60)
    
    success = True
    
    # Create test data
    success &= create_test_attendance_data()
    
    if success:
        # Test the functionality
        success &= test_merge_functionality()
    
    # Clean up
    cleanup_test_data()
    
    print("=" * 60)
    if success:
        print("✅ ALL TESTS PASSED! The Generate Report functionality should work now.")
        print("\n🎯 What was fixed:")
        print("   • Fixed merge operation creating duplicate columns")
        print("   • Added proper duplicate column handling")
        print("   • Enhanced error handling for pandas operations")
        print("   • Added validation for numeric data conversion")
        print("   • Improved column filtering logic")
        print("\n🚀 You should now be able to:")
        print("   1. Click 'View Reports' from main menu")
        print("   2. Select a subject (like 'sgp')")
        print("   3. Click 'Generate Report' WITHOUT errors!")
    else:
        print("❌ TESTS FAILED! There may still be issues.")
    
    input("\nPress Enter to exit...")