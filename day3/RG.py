import os
import streamlit as st
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Event Report Generator",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling (Premium Black and Gold/Yellow Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background-color: #050505;
        color: #f3f4f6;
    }
    
    /* Header Container Gradient */
    .header-container {
        background: linear-gradient(135deg, #151515 0%, #000000 100%);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 204, 0, 0.25);
        box-shadow: 0 8px 32px 0 rgba(255, 204, 0, 0.05);
        margin-bottom: 2rem;
    }
    .header-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(to right, #ffe600, #ffb300, #ff8800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        color: #d1d5db;
        font-size: 1.1rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b0b0b !important;
        border-right: 1px solid rgba(255, 204, 0, 0.15);
    }
    
    /* Card Styles */
    .panel-card {
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 204, 0, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .status-active {
        color: #ffcc00;
        font-weight: 600;
    }
    .status-inactive {
        color: #f43f5e;
        font-weight: 600;
    }
    
    /* Custom buttons */
    div.stButton > button {
        background: linear-gradient(to right, #ffcc00, #ff9900);
        color: #000000 !important;
        border: none;
        padding: 0.6rem 1.8rem;
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 204, 0, 0.3);
        background: linear-gradient(to right, #ffe066, #ffaa00);
        color: #000000 !important;
    }
    
    /* Preview Section Custom Styles */
    .preview-doc {
        background-color: #ffffff;
        color: #1a1a1a;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        max-width: 800px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .preview-header {
        border-bottom: 2px solid #ffcc00;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .preview-title {
        color: #000000;
        font-size: 24px;
        font-weight: bold;
    }
    .preview-section-title {
        color: #ff9900;
        font-size: 18px;
        font-weight: bold;
        border-bottom: 1px solid #e2e8f0;
        margin-top: 25px;
        padding-bottom: 5px;
    }
    .preview-sub-title {
        color: #cc9900;
        font-size: 14px;
        font-weight: bold;
        margin-top: 15px;
    }
    .preview-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    .preview-table th, .preview-table td {
        border: 1px solid #cbd5e1;
        padding: 8px;
        text-align: left;
        font-size: 13px;
    }
    .preview-table th {
        background-color: #f8fafc;
        color: #000000;
    }
    .preview-img-container {
        display: inline-block;
        width: 45%;
        margin: 2%;
        text-align: center;
        vertical-align: top;
        border: 1px solid #cbd5e1;
        padding: 5px;
        border-radius: 4px;
        background: #f8fafc;
    }
    .preview-img-caption {
        font-size: 11px;
        color: #64748b;
        font-style: italic;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "event_data" not in st.session_state:
    st.session_state.event_data = {
        "program_name": "National Seminar on Generative Artificial Intelligence",
        "num_days": 3,
        "program_type": "Seminar",
        # Manual entries
        "aim": "To introduce academic researchers and industry professionals to generative AI prompt engineering, large language model design, and multi-agent systems.",
        "objective": "1. Provide insights into Gemini model API integration.\n2. Conduct practical labs for document indexing and custom search systems.\n3. Discuss security controls in cloud-based API architectures.",
        "program_inclusions": "1. Access to practical lab notebooks.\n2. Course participation certificate.\n3. Institutional lunch, tea break refreshments, and resource toolkit.",
        "student_feedback": "Highly positive feedback. Participants valued the hands-on lab sessions and clarity of topic delivery.",
        "target_pages": 4,
        # Generated summaries
        "executive_summary": "",
        "session_highlights": "",
        "learning_outcomes": "",
        "impact_analysis": "",
        "conclusion": "",
        # Document contents parsed
        "documents_text": ""
    }

if "logo_bytes" not in st.session_state:
    st.session_state.logo_bytes = None

if "image_categories" not in st.session_state:
    st.session_state.image_categories = {
        "Attached Event Photos": []
    }

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY") or ""

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/news.png", width=60)
    st.markdown("### 🤖 Report Engine")
    st.write("Automatically draft executive-level event summaries with AI & professional exports.")
    
    st.markdown("---")
    
    # Navigation
    menu = st.radio(
        "Navigation Menu",
        ["🏠 Dashboard", "📝 Event Inputs", "📷 Upload Photos", "✨ AI Refiner & Editor", "🔍 Preview & Export"]
    )
    
    st.markdown("---")
    
    # API Configuration
    st.markdown("#### 🔑 Gemini API Settings")
    if st.session_state.api_key:
        st.markdown('Status: <span class="status-active">🟢 Active</span>', unsafe_allow_html=True)
        if st.button("Change API Key"):
            st.session_state.api_key = ""
            st.rerun()
    else:
        st.markdown('Status: <span class="status-inactive">🔴 Missing</span>', unsafe_allow_html=True)
        key_input = st.text_input("Enter Gemini API Key", type="password")
        if key_input:
            st.session_state.api_key = key_input
            st.success("Key updated!")
            st.rerun()

# Imports for data processes
from report_exporter import extract_text_from_pdf, extract_text_from_docx, generate_pdf, generate_docx
from ai_processor import AIProcessor

processor = AIProcessor(api_key=st.session_state.api_key)

# ---------------------------------------------------------
# Main Page Route: DASHBOARD
# ---------------------------------------------------------
if menu == "🏠 Dashboard":
    st.markdown("""
    <div class="header-container">
        <div class="header-title">AI Event Report Generator</div>
        <div class="header-subtitle">Streamlined completion reporting with automated document summarization, photo captioning, and exports.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Quick Start Guide")
        st.markdown("""
        Follow these simple steps to build your official report:
        1. **Fill Event Inputs**: Provide program name, number of days, type of program, and requirements (Aim, Objective, Inclusions, Target Pages).
        2. **Upload Documents**: Attach files regarding the program to add context for AI summaries.
        3. **Upload Photos**: Upload available photos to be attached to the final report.
        4. **Generate with AI**: Let Gemini read inputs and documents to write structured summaries and captions.
        5. **Refine & Export**: Preview the report and download PDF or Word exports.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Active Report Details")
        st.write(f"**Program Name:** {st.session_state.event_data['program_name']}")
        st.write(f"**Program Type:** {st.session_state.event_data['program_type']}")
        st.write(f"**Duration (Days):** {st.session_state.event_data['num_days']}")
        
        # Check active uploads
        total_photos = len(st.session_state.image_categories["Attached Event Photos"])
        st.write(f"**Uploaded Photos:** {total_photos} items")
        
        has_ai = st.session_state.event_data['executive_summary'] != ""
        st.write(f"**AI Sections Synthesized:** {'🟢 Yes' if has_ai else '🔴 No'}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Page Route: EVENT INPUTS
# ---------------------------------------------------------
elif menu == "📝 Event Inputs":
    st.markdown("## 📝 Program Information & Manual Entries")
    st.write("Provide details and upload files relating to the program.")
    
    tab1, tab2, tab3 = st.tabs(["🏛️ Metadata & Requirements", "📂 Documents Uploader", "✍️ Manual Contents"])
    
    with tab1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.event_data["program_name"] = st.text_input("Program Name", st.session_state.event_data["program_name"])
            st.session_state.event_data["program_type"] = st.selectbox(
                "Type of Program", 
                ["Seminar", "Workshop", "Conference", "FDP", "Webinar", "Symposium", "Guest Lecture", "Field Visit"], 
                index=0
            )
        with col2:
            st.session_state.event_data["num_days"] = st.number_input("No. of Days", min_value=1, value=int(st.session_state.event_data["num_days"]))
            st.session_state.event_data["target_pages"] = st.number_input("No. of Pages (Target Length)", min_value=1, value=int(st.session_state.event_data["target_pages"]))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            logo_file = st.file_uploader("Upload Institution Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
            if logo_file:
                st.session_state.logo_bytes = logo_file.read()
                st.image(st.session_state.logo_bytes, width=120, caption="Uploaded Logo Preview")
                
        with col2:
            uploaded_docs = st.file_uploader("Upload Documents regarding the Program (PDF/DOCX) (Multiple)", type=["pdf", "docx"], accept_multiple_files=True)
            
            if uploaded_docs and st.button("Parse Uploaded Documents"):
                with st.spinner("Extracting contents..."):
                    texts = []
                    for f in uploaded_docs:
                        name = f.name
                        bytes_data = f.read()
                        if name.endswith(".pdf"):
                            texts.append(f"--- DOCUMENT: {name} ---\n" + extract_text_from_pdf(bytes_data))
                        elif name.endswith(".docx"):
                            texts.append(f"--- DOCUMENT: {name} ---\n" + extract_text_from_docx(bytes_data))
                            
                    combined_docs = "\n\n".join(texts)
                    if combined_docs:
                        st.session_state.event_data["documents_text"] = combined_docs
                        st.success("Successfully parsed text from documents! Content added to AI context.")
                    else:
                        st.info("No text files were parsed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.session_state.event_data["aim"] = st.text_area("Aim of the Program", st.session_state.event_data["aim"], height=100)
        st.session_state.event_data["objective"] = st.text_area("Objectives of the Program", st.session_state.event_data["objective"], height=120)
        st.session_state.event_data["program_inclusions"] = st.text_area("Program Inclusions (e.g. materials, certificates, meals)", st.session_state.event_data["program_inclusions"], height=100)
        st.session_state.event_data["student_feedback"] = st.text_area("Student / Participant Feedback Summary", st.session_state.event_data.get("student_feedback", ""), height=100)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Page Route: UPLOAD PHOTOS
# ---------------------------------------------------------
elif menu == "📷 Upload Photos":
    st.markdown("## 📷 Event Photos Upload & Gallery")
    st.write("Upload available photos to attach regarding the program.")
    
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    uploaded_photos = st.file_uploader(
        "Upload Program Photos (Multiple)", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    if uploaded_photos:
        for f in uploaded_photos:
            existing_names = [img["name"] for img in st.session_state.image_categories["Attached Event Photos"]]
            if f.name not in existing_names:
                img_bytes = f.read()
                st.session_state.image_categories["Attached Event Photos"].append({
                    "name": f.name,
                    "bytes": img_bytes,
                    "caption": "Program activities photo."
                })
        st.success(f"Added {len(uploaded_photos)} photos to gallery!")
        
    st.markdown("---")
    
    current_list = st.session_state.image_categories["Attached Event Photos"]
    if current_list:
        cols = st.columns(3)
        for idx, item in enumerate(current_list):
            col_idx = idx % 3
            with cols[col_idx]:
                st.image(item["bytes"], use_container_width=True)
                new_cap = st.text_input(
                    f"Caption #{idx+1}", 
                    value=item["caption"], 
                    key=f"cap_edit_photo_{idx}"
                )
                item["caption"] = new_cap
                if st.button("🗑️ Delete", key=f"del_photo_{idx}"):
                    st.session_state.image_categories["Attached Event Photos"].pop(idx)
                    st.rerun()
    else:
        st.info("No photos uploaded yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Page Route: AI REFINER & EDITOR
# ---------------------------------------------------------
elif menu == "✨ AI Refiner & Editor":
    st.markdown("## ✨ AI Automated Content Refinement")
    st.write("Generate structured summaries and descriptions using Gemini, or use local template heuristics, then edit as required.")
    
    # Render API Key warning if not present, but don't block access
    if not st.session_state.api_key:
        st.info("💡 **Tip**: Enter a Gemini API Key in the sidebar to use advanced AI generation and automatic photo captioning.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Text Report Sections")
        if st.session_state.api_key:
            if st.button("⚡ Generate AI Report (Gemini API)"):
                with st.spinner("Generating report sections..."):
                    try:
                        results = processor.generate_report_sections(
                            st.session_state.event_data,
                            st.session_state.event_data,
                            st.session_state.event_data.get("documents_text", "")
                        )
                        for key in ["executive_summary", "session_highlights", "learning_outcomes", "impact_analysis", "conclusion"]:
                            st.session_state.event_data[key] = results.get(key, "")
                        st.success("Successfully generated report text blocks! Review them below.")
                    except Exception as e:
                        st.error(f"Failed to generate reports: {e}")
        
        # Always provide the local template generation option
        if st.button("📝 Generate Smart Templates (Local Heuristics)"):
            data = st.session_state.event_data
            aim = data.get("aim", "")
            objective = data.get("objective", "")
            inclusions = data.get("program_inclusions", "")
            name = data.get("program_name", "the program")
            type_p = data.get("program_type", "event")
            days = data.get("num_days", 1)
            
            data["executive_summary"] = (
                f"The primary aim of this {type_p} was to address the following: '{aim}'. Over a span of {days} days, the program was "
                f"successfully organized and completed. Key objectives included achieving: \n{objective}\n\nParticipants reported a high "
                f"degree of satisfaction with the learning pace and overall session structure."
            )
            data["session_highlights"] = (
                f"During this {days}-day {type_p}, speakers and coordinators focused on key topics related to: '{aim}'. "
                f"Interactive sessions were conducted to help participants understand practical execution. Notable inclusions "
                f"like '{inclusions}' ensured that attendees had all the resources required for a productive environment."
            )
            data["learning_outcomes"] = (
                f"By the conclusion of the {type_p}, participants achieved the following target competencies:\n"
                f"1. Enhanced understanding of core principles linked to: '{aim}'.\n"
                f"2. Ability to implement practical methodologies to accomplish: \n{objective}\n"
                f"3. Collaborative networking and resource sharing among peers."
            )
            data["impact_analysis"] = (
                f"The program created a strong foundation for future applications. Based on the aim, the participants "
                f"now possess the skills required to address relevant domain challenges. The structured inclusions and "
                f"comprehensive objectives set a benchmark for future iterations of similar educational workshops."
            )
            data["conclusion"] = (
                f"In conclusion, the {days}-day {type_p} on '{name}' successfully met all its defined objectives. We extend our sincere "
                f"gratitude to the resource persons, organizational coordinators, and participants whose dedication made this event a resounding success."
            )
            st.success("Successfully filled sections with local smart templates! Review them below.")
            st.rerun()

    with col2:
        st.markdown("### 📷 Photo Captions")
        if st.session_state.api_key:
            if st.button("📷 Generate AI Captions"):
                with st.spinner("AI describing photos..."):
                    processed_count = 0
                    for img in st.session_state.image_categories["Attached Event Photos"]:
                        try:
                            caption = processor.generate_image_caption(img["bytes"])
                            img["caption"] = caption
                            processed_count += 1
                        except Exception:
                            pass
                    if processed_count > 0:
                        st.success(f"Generated captions for {processed_count} photos!")
                        st.rerun()
                    else:
                        st.info("No photos found or API error occurred.")
        
        # Always provide the local template photo captioning option
        if st.button("📷 Set Default Photo Captions"):
            processed_count = 0
            for idx, img in enumerate(st.session_state.image_categories["Attached Event Photos"]):
                img["caption"] = f"Photograph showing activities during session {idx+1} of the {st.session_state.event_data.get('program_name')}."
                processed_count += 1
            if processed_count > 0:
                st.success(f"Updated default captions for {processed_count} photos!")
                st.rerun()
            else:
                st.info("No photos found.")

    st.markdown("---")
    
    st.subheader("Edit Report Content")
    st.session_state.event_data["executive_summary"] = st.text_area(
        "Executive Summary", st.session_state.event_data["executive_summary"], height=120
    )
    st.session_state.event_data["session_highlights"] = st.text_area(
        "Session Highlights", st.session_state.event_data["session_highlights"], height=120
    )
    st.session_state.event_data["learning_outcomes"] = st.text_area(
        "Learning Outcomes", st.session_state.event_data["learning_outcomes"], height=120
    )
    st.session_state.event_data["impact_analysis"] = st.text_area(
        "Impact Analysis", st.session_state.event_data["impact_analysis"], height=120
    )
    st.session_state.event_data["conclusion"] = st.text_area(
        "Conclusion", st.session_state.event_data["conclusion"], height=120
    )

# ---------------------------------------------------------
# Main Page Route: PREVIEW & EXPORT
# ---------------------------------------------------------
elif menu == "🔍 Preview & Export":
    st.markdown("## 🔍 Report Preview & Document Generation")
    st.write("Preview the layout and download PDF/Word exports.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pdf_bytes = generate_pdf(
            st.session_state.event_data, 
            st.session_state.logo_bytes,
            st.session_state.image_categories
        )
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name="event_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    with col2:
        docx_bytes = generate_docx(
            st.session_state.event_data,
            st.session_state.logo_bytes,
            st.session_state.image_categories
        )
        st.download_button(
            label="📥 Download DOCX Report",
            data=docx_bytes,
            file_name="event_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
    st.markdown("---")
    
    st.subheader("Interactive HTML Preview")
    
    st.markdown(f"""
    <div class="preview-doc">
        <div class="preview-header" style="text-align: center;">
            {"<div style='font-size: 11px; font-weight: bold; color: #1e3a8a;'>INSTITUTION LOGO PLACEHOLDER</div>" if not st.session_state.logo_bytes else ""}
            <div class="preview-title">EVENT COMPLETION REPORT</div>
            <div style="font-size: 16px; font-weight: bold; color: #0d9488; text-transform: uppercase; margin-top: 10px;">
                {st.session_state.event_data['program_name']}
            </div>
        </div>
        
        <table class="preview-table">
            <tr>
                <th width="40%">Field</th>
                <th width="60%">Value</th>
            </tr>
            <tr>
                <td><b>Program Name</b></td>
                <td>{st.session_state.event_data['program_name']}</td>
            </tr>
            <tr>
                <td><b>Program Type</b></td>
                <td>{st.session_state.event_data['program_type']}</td>
            </tr>
            <tr>
                <td><b>Duration (No. of Days)</b></td>
                <td>{st.session_state.event_data['num_days']} Days</td>
            </tr>
            <tr>
                <td><b>Target Page Limit</b></td>
                <td>{st.session_state.event_data['target_pages']} Pages</td>
            </tr>
        </table>
        
        <div class="preview-section-title">1. Aim & Objectives</div>
        <p style="font-size: 13px; line-height: 1.5; color: #475569;">
            <b>Aim:</b><br/>{st.session_state.event_data['aim']}<br/><br/>
            <b>Objectives:</b><br/>{st.session_state.event_data['objective']}
        </p>
        
        <div class="preview-section-title">2. Program Inclusions</div>
        <p style="font-size: 13px; line-height: 1.5; color: #475569; white-space: pre-wrap;">
            {st.session_state.event_data['program_inclusions']}
        </p>
        
        <div class="preview-section-title">3. Executive Summary (AI Generated)</div>
        <p style="font-size: 13px; line-height: 1.5; color: #475569;">
            {st.session_state.event_data['executive_summary'] or "<i>No executive summary generated yet. Navigate to 'AI Refiner' to generate.</i>"}
        </p>
        
        <div class="preview-section-title">4. Session Highlights</div>
        <p style="font-size: 13px; line-height: 1.5; color: #475569;">
            {st.session_state.event_data['session_highlights'] or "<i>No session highlights generated.</i>"}
        </p>
        
        <div class="preview-section-title">5. Feedback & Outcomes</div>
        <p style="font-size: 13px; line-height: 1.5; color: #475569;">
            <b>Feedback Summary:</b><br/>{st.session_state.event_data['student_feedback']}<br/><br/>
            <b>Learning Outcomes:</b><br/>{st.session_state.event_data['learning_outcomes'] or "<i>No learning outcomes generated yet.</i>"}<br/><br/>
            <b>Impact Analysis:</b><br/>{st.session_state.event_data['impact_analysis'] or "<i>No impact analysis generated yet.</i>"}
        </p>
        
        <div class="preview-section-title">6. Conclusion</div>
        <p style="font-size: 13px; line-height: 1.5; color: #475569;">
            {st.session_state.event_data['conclusion'] or "<i>No conclusion generated yet.</i>"}
        </p>
        
        <div class="preview-section-title">7. Signatures</div>
        <table style="width: 100%; margin-top: 30px; border: none;">
            <tr style="border: none;">
                <td style="border: none; font-size: 13px;">
                    <b>Prepared By:</b><br/><br/><br/>_______________________<br/>Event Coordinator
                </td>
                <td style="border: none; font-size: 13px; text-align: right;">
                    <b>Approved By:</b><br/><br/><br/>_______________________<br/>Head of Department / Director
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    current_photos = st.session_state.image_categories["Attached Event Photos"]
    if current_photos:
        st.markdown("<div style='max-width: 800px; margin: 20px auto;'><div class='preview-section-title'>Photo Gallery</div></div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, img_data in enumerate(current_photos):
            col_i = idx % 3
            with cols[col_i]:
                st.image(img_data["bytes"], caption=f"Photo {idx+1}: {img_data['caption']}", use_container_width=True)