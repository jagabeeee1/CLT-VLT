import streamlit as st
import pandas as pd
import io
import re

def process_name(name: str) -> tuple:
    """
    Process a single name string and split it into First Name and Second Name based on rules.
    """
    if pd.isna(name):
        return None, None
        
    name_str = str(name).strip()
    if not name_str:
        return None, None

    # Remove dots to cleanly handle initials and salutations
    name_no_dots = name_str.replace('.', ' ')
    
    # Split combined format into meaningful parts (e.g. Yokeshkumar -> Yokesh kumar)
    name_spaced = re.sub(r'(?i)([A-Za-z]{2,})(kumar)\b', r'\1 \2', name_no_dots)
    
    # Maintain proper capitalization
    name_title = name_spaced.title()
    
    # Split into words
    words = " ".join(name_title.split()).split()
    
    if not words:
        return None, None
        
    if len(words) == 1:
        return words[0], ""
        
    last_word = words[-1]
    
    # Check if the last part is a single letter (initial)
    if len(last_word) == 1 and last_word.isalpha():
        second_name = last_word.upper()
        first_name = " ".join(words[:-1])
    else:
        second_name = last_word
        first_name = " ".join(words[:-1])
        
    return first_name, second_name

def process_dataframe(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Process the dataframe to extract First Name and Second Name.
    """
    # Clean up column names in the dataframe (strip spaces)
    df.columns = [str(c).strip() for c in df.columns]
    clean_target_col = column_name.strip()
    
    # Try an exact match first after stripping spaces
    if clean_target_col not in df.columns:
        # Try case-insensitive match
        lower_cols = [str(c).lower() for c in df.columns]
        lower_target = clean_target_col.lower()
        if lower_target in lower_cols:
            idx = lower_cols.index(lower_target)
            clean_target_col = df.columns[idx]
        else:
            available_cols = ", ".join([str(c) for c in df.columns])
            raise ValueError(f"Column '{clean_target_col}' not found. Available columns in your file are: {available_cols}")
        
    # Create new columns using the process_name function
    processed_names = df[clean_target_col].apply(process_name)
    
    # Create a new dataframe with the required output structure
    result_df = pd.DataFrame()
    result_df['Full Name'] = df[clean_target_col]
    result_df['First Name'] = processed_names.apply(lambda x: x[0] if x else None)
    result_df['Second Name'] = processed_names.apply(lambda x: x[1] if x else None)
    
    return result_df

def to_excel(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to an Excel bytes object for download.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed_Names')
    processed_data = output.getvalue()
    return processed_data

def main():
    st.set_page_config(page_title="Faculty Name Splitter Tool", page_icon="📝", layout="centered")
    
    st.title("📝 Faculty Name Splitter Tool")
    st.markdown("Upload an Excel file containing faculty names to split them into **First Name** and **Second Name** based on predefined rules.")
    
    # Optional: allow user to specify the column name
    column_name = st.text_input("Name Column Header (Default is 'Name')", value="Name")
    
    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=['xlsx'])
    
    if uploaded_file is not None:
        try:
            # Read the excel file
            df = pd.read_excel(uploaded_file)
            
            with st.spinner("Processing names..."):
                # Process the data
                processed_df = process_dataframe(df, column_name)
                
            st.success("✅ File processed successfully!")
            
            # Show preview
            st.subheader("Preview")
            st.dataframe(processed_df.head(10), use_container_width=True)
            
            st.info(f"Total records processed: {len(processed_df)}")
            
            # Download button
            excel_data = to_excel(processed_df)
            st.download_button(
                label="📥 Download Processed Excel File",
                data=excel_data,
                file_name="processed_faculty_names.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        except ValueError as ve:
            st.error(f"⚠️ Validation Error: {ve}")
            st.info("Please ensure your Excel file has the correct column name. You can modify the target column name above.")
        except Exception as e:
            st.error(f"❌ An error occurred while processing the file: {str(e)}")

if __name__ == "__main__":
    main()
