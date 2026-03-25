import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import time

# Set page configuration
st.set_page_config(
    page_title="Exercism Submission Checker",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for a clean UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .success-text {
        color: #4CAF50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App Title and Description
st.markdown('<p class="main-header">🎓 Exercism Submission Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload an Excel file containing student details to automatically check their total Exercism submission counts.</p>', unsafe_allow_html=True)

def get_submission_count(profile_url):
    """
    Scrape the Exercism profile page to find the total number of submissions/exercises completed.
    Returns an integer count or 0 if not found/error.
    """
    if not isinstance(profile_url, str) or not profile_url.strip().startswith('http'):
        return 0
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Add a timeout to prevent hanging on invalid domains or slow networks
        response = requests.get(profile_url.strip(), headers=headers, timeout=10)
        
        if response.status_code != 200:
            return 0
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Method 1: Look for the h2 element with class "published-solutions" (Reliable for modern Exercism UI)
        # e.g. <h2 class='published-solutions' data-total-count='75'>Published Solutions</h2>
        h2_published = soup.find('h2', class_='published-solutions')
        if h2_published and h2_published.has_attr('data-total-count'):
            return int(h2_published['data-total-count'])
            
        # Method 2: Look for the React component data which contains the exact metric (Fallback)
        # It's an attribute `data-react-data` holding JSON. E.g., "metric_full":"81 solutions published"
        import re
        react_divs = soup.find_all('div', attrs={'data-react-data': True})
        for div in react_divs:
            data = div['data-react-data']
            # We search for "X solutions published" or "X solutions" in the JSON string
            match = re.search(r'"metric_full":"(\d+)\s+solutions?\s+published"', data)
            if match:
                return int(match.group(1))
            
            # Alternative format
            match2 = re.search(r'"metric_short":"(\d+)\s+solutions?"', data)
            if match2:
                return int(match2.group(1))
                
        # If we couldn't find any typical counter text, return 0
        return 0
        
    except Exception as e:
        # Gracefully handle network issues, timeouts, or parsing errors without crashing the app
        return 0

# Sidebar setup
st.sidebar.header("📁 Upload File")
st.sidebar.markdown(
    """
    Please upload an Excel file **(.xlsx)**.
    
    **Required Columns:**
    - `Student Name`
    - `Register Number`
    - `Exercism Profile Link`
    """
)

uploaded_file = st.sidebar.file_uploader("", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Display loading spinner while reading the file
        with st.spinner("📄 Reading Excel file..."):
            df = pd.read_excel(uploaded_file)
            
        # Standardize column names for flexible detection (case-insensitive, whitespace trimmed)
        cols = [str(c).strip().lower() for c in df.columns]
        df.columns = cols
        
        # Dynamically discover columns to be forgiving with exact names
        name_col = next((c for c in cols if 'name' in c or 'student' in c), None)
        reg_col = next((c for c in cols if 'register' in c or 'reg' in c or 'roll' in c), None)
        link_col = next((c for c in cols if 'link' in c or 'exercism' in c or 'profile' in c or 'url' in c), None)
        
        # Verify if we found the necessary columns
        if not all([name_col, reg_col, link_col]):
            if len(df.columns) >= 3:
                # Fallback to the first 3 columns if names don't match exactly
                name_col, reg_col, link_col = df.columns[0], df.columns[1], df.columns[2]
                st.info(f"💡 Could not auto-detect column names. Assuming: 1. Name (`{name_col}`), 2. Reg No (`{reg_col}`), 3. Link (`{link_col}`)")
            else:
                st.error("❌ The uploaded file does not have enough columns. It must have at least 3 columns.")
                st.stop()
                
        # Data validation and prep
        preview_df = df[[name_col, reg_col, link_col]].copy()
        preview_df.rename(columns={
            name_col: "Student Name", 
            reg_col: "Register Number", 
            link_col: "Exercism Link"
        }, inplace=True)
        preview_df.index = range(1, len(preview_df) + 1)  # 1-based index (Sl.No)
        
        # Show uploaded data
        st.subheader("📋 Uploaded Data Preview")
        st.dataframe(preview_df, use_container_width=True)
        
        st.markdown("---")
        
        # Start processing button
        if st.button("🚀 Start Checking", type="primary"):
            st.subheader("🔍 Checking Submissions...")
            
            # Progress UI
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            total_students = len(preview_df)
            
            for i, (index, row) in enumerate(preview_df.iterrows()):
                link = row['Exercism Link']
                name = row['Student Name']
                reg_no = row['Register Number']
                
                # Update status
                status_text.text(f"Checking {i+1} of {total_students}: {name}...")
                
                # Fetch Exercism submission count
                count = get_submission_count(link)
                
                results.append({
                    "Sl.No": index,
                    "Register Number": reg_no,
                    "Student Name": name,
                    "Exercism Link": link,
                    "Submission Count": count
                })
                
                # Update progress bar
                progress_bar.progress((i + 1) / total_students)
                
                # Polite delay to avoid hammering the Exercism servers (Rate Limiting safe-guard)
                time.sleep(0.5)
                
            status_text.success("✅ Check complete!")
            
            # Show final results
            results_df = pd.DataFrame(results)
            st.subheader("📊 Final Results")
            st.dataframe(results_df, use_container_width=True)
            
            # Generate Excel for download
            output = io.BytesIO()
            # Default to openpyxl for pandas to_excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                results_df.to_excel(writer, index=False, sheet_name='Submissions')
            excel_data = output.getvalue()
            
            st.markdown("### 📥 Download Report")
            st.download_button(
                label="Download Results as Excel (.xlsx)",
                data=excel_data,
                file_name="exercism_submission_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
            
    except Exception as e:
        st.error(f"❌ An error occurred while reading the file: {e}")
        st.write("Please make sure you uploaded a valid Excel file.")
else:
    # Landing page state when no file is uploaded
    st.info("👈 Please upload an Excel file from the sidebar to begin.")
    
    st.markdown("### 💡 Example File Format")
    st.markdown("Your uploaded Excel file should look like this:")
    
    # Mock example data
    example_data = pd.DataFrame({
        "Student Name": ["Alice Johnson", "Bob Smith"],
        "Register Number": ["REG001", "REG002"],
        "Exercism Profile Link": ["https://exercism.org/profiles/alice", "https://exercism.org/profiles/bob"]
    })
    example_data.index = [1, 2]
    st.table(example_data)
