import os 
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

load_dotenv()

#Pull the keys out of hiding dynamically
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- INITIALIZE THE TOOLS ---
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query):
    response = tavily_client.search(query=query, search_depth="advanced", max_results=5)
    return response['results']


def generate_report(topic, search_results):
    context_text = ""
    for i, article in enumerate(search_results, 1):
        context_text += f"Source [{i}]: {article['title']}\n"
        context_text += f"URL: {article['url']}\n"
        context_text += f"Content: {article['content']}\n\n"
    
    full_prompt = (
        f"You are an expert AI Research Assistant. Your job is to read the provided search results "
        f"and write a highly comprehensive, structured report about the topic: '{topic}'.\n\n"
        f"Your report MUST include the following clear sections:\n"
        f"1. Executive Summary\n"
        f"2. Key Takeaways (bullet points)\n"
        f"3. Detailed Findings (broken down into logical sub-topics)\n"
        f"4. Cited Sources (List the URLs provided below, matching the [Source X] numbers used in your text).\n\n"
        f"Here are the search results you must use:\n"
        f"{context_text}"
    )
    
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    return response.text


# --- STREAMLIT CONFIG & DESIGN OVERRIDE ---
st.set_page_config(page_title="Researchly", page_icon="🔍", layout="centered")

# Injection of custom CSS to turn the generic Streamlit page into a bespoke UI
st.markdown("""
    <style>
    /* Main Background & Font Setup */
    .stApp {
        background-color: #0F172A;
    }
    h1 {
        font-family: 'Inter', sans-serif;
        color: #F8FAFC !important;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
        margin-bottom: 5px !important;
    }
    .sub-header {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Styling the TextInput Box */
    div[data-baseweb="input"] {
        background-color: #1E293B !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
        padding: 4px;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"]:focus-within {
        border: 1px solid #38BDF8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.2) !important;
    }
    input {
        color: #F1F5F9 !important;
    }
    
    /* Styling the Main Action Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4) !important;
    }
    div.stButton > button:first-child:active {
        transform: translateY(1px) !important;
    }
    
    /* Styling the generated report paper-card */
    .report-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 2.5rem;
        margin-top: 2rem;
        color: #E2E8F0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    hr {
        border-color: #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- VISUAL CONTENT ---
st.markdown("<h1>🔍 Researchly</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>A platform where you can get a report within seconds and save your time!</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Search Input
topic = st.text_input("Enter topic", placeholder="e.g., Solid state battery commercialization timeline 2026")

# Padding
st.write("")

# Process Execution
if st.button("Generate Report"):
    if not topic.strip():
        st.warning("Please submit a valid research objective.")
    else:
        with st.spinner("Preparing..."):
            try:
                # Core Engine Execution
                raw_results = search_web(topic)
                report = generate_report(topic, raw_results)
                
                # Render results inside our highly-styled HTML card wrapper
                st.markdown("### Your report is ready!")
                st.markdown(f"<div class='report-card'>{report}</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Custom Export action
                st.download_button(
                    label="📥 Export Intel Briefing (.md)",
                    data=report,
                    file_name=f"{topic.replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"An engine failure occurred during report generation: {e}")