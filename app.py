import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
import json


# --- LOTTIE ANIMATION LOADER ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")



# --- API SETUP ---
try:
    GOOGLE_API_KEY_2 = st.secrets["GEMINI_API_KEY_2"]
    genai.configure(api_key=GOOGLE_API_KEY_2)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")



#--- CSS FILE ---
st.set_page_config(page_title="AI Study Buddy", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# --- NAVIGATION ---
st.sidebar.title("📚 AI Study Buddy")
st.sidebar.write("### Choose a tool below:")
app_mode = st.sidebar.radio("", [
    "🌟 Concept Explainer", 
    "📝 Notes Summarizer", 
    "🧠 Quiz Generator",
    "💻 Code Explainer & Debugger",
    "🧮 Step-by-Step Solver",
    "📅 Schedule Generator"
])

with st.sidebar:
    st_lottie(lottie_ai, height=150, key="sidebar_ai")



# ---ALL SIX FEATURES---

if app_mode == "🌟 Concept Explainer":
    st.title("AI Concept Explainer")
    user_topic = st.text_input("What topic would you like me to explain?")
    if st.button("Explain"):
        if user_topic:
            with st.spinner("Thinking..."):
                prompt = f"""
                    You are an expert tutor. 
                    Explain this complex concept in simple terms with bullet points: {user_topic}
                    """
                st.markdown(model.generate_content(prompt).text)
        else:
            st.warning("Please enter a topic.")


elif app_mode == "📝 Notes Summarizer":
    st.title("AI Notes Summarizer")
    user_notes = st.text_area("Paste your long study notes here:", height=200)
    if st.button("Summarize"):
        if user_notes:
            with st.spinner("Summarizing..."):
                prompt = f"Summarize these study notes into a 1-sentence overview and a bulleted list of key points: {user_notes}"
                st.markdown(model.generate_content(prompt).text)
        else:
            st.warning("Please paste some notes.")


elif app_mode == "🧠 Quiz Generator":
    st.title("AI Quiz Generator")
    quiz_input = st.text_area("Paste notes or type a topic to generate a question quiz:", height=150)
    if st.button("Generate Quiz"):
        if quiz_input:
            with st.spinner("Writing questions..."):
                prompt = f"""
                    Create a question multiple-choice quiz based on this topic/notes: {quiz_input}. 
                
                    You MUST format it strictly using Markdown lists. Format exactly like this:
                
                    **Question 1:** [Write the question here]
                    * A) [Option A]
                    * B) [Option B]
                    * C) [Option C]
                    * D) [Option D]
                
                    **Correct Answer:** [Answer]
                    """
                st.markdown(model.generate_content(prompt).text)
        else:
            st.warning("Please provide a topic or notes.")


elif app_mode == "💻 Code Explainer & Debugger":
    st.title("AI Code Explainer & Debugger")
    user_code = st.text_area("Paste your code snippet here:", height=200)
    if st.button("Analyze Code"):
        if user_code:
            with st.spinner("Reading code..."):
                prompt = f"""
                    Analyze this code: 
                        1. Explain what it does. 
                        2. Point out bugs. 
                        3. Suggest improvements. 
                        Code: {user_code}
                    """                            
                st.markdown(model.generate_content(prompt).text)
        else:
            st.warning("Please paste some code.")


elif app_mode == "🧮 Step-by-Step Solver":
    st.title("AI Step-by-Step Solver")
    user_problem = st.text_input("Type your academic problem (Math, Science, Logic, etc.):")
    if st.button("Solve Problem"):
        if user_problem:
            with st.spinner("Calculating..."):
                prompt = f"""
                    You are an expert academic tutor.
                    Provide a highly structured, professional, step-by-step solution for the following problem. 
                
                Problem: {user_problem}
                
                Strictly on to the following formatting rules:
                1. **Structure**: 
                   - **Problem Overview**: Briefly state what needs to be solved.
                   - **Given Information**: List the known facts or variables.
                   - **Step-by-Step Solution**: Break down the logic into distinct, numbered steps. Give each step a concise bold title (e.g., **Step 1: Apply the Formula**).
                   - **Final Answer**: State the final result clearly in a dedicated section at the bottom.
                
                2. **Equation Formatting (CRITICAL)**: 
                   - Place EVERY equation, formula, matrix, or sequence on its own separate line using block LaTeX formatting.
                   - You MUST wrap every equation exactly in double dollar signs (example: $$ x^2 + y^2 = z^2 $$).
                   - You MUST leave a blank empty line before and after every $$ block so Streamlit renders it perfectly.
                   - Never write complex equations inline with standard text.
                
                3. **Tone & Style**: 
                   - Professional, academic, and highly readable.
                   - Remove all conversational filler (e.g., do not say "Let's solve this" or "Here is the answer"). 
                """
                st.markdown(model.generate_content(prompt).text)
        else:
            st.warning("Please enter a problem.")
            
            
elif app_mode == "📅 Schedule Generator":
    st.title("AI Study Schedule Generator")
    col1, col2 = st.columns(2)
    with col1:
        user_syllabus = st.text_area("Enter your syllabus topics (separated by commas):")
    with col2:
        user_days = st.number_input("How many days until the exam?", min_value=1)
    
    if st.button("Create Schedule"):
        if user_syllabus:
            with st.spinner("Drafting timetable..."):
                prompt = f"""
                    Create a practical study schedule for {user_days} days using these topics: {user_syllabus}. 
                    Format as a daily timetable.
                    """
                st.markdown(model.generate_content(prompt).text)
        else:
            st.warning("Please enter your syllabus topics.")
