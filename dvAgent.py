import streamlit as st
from io import StringIO
from dotenv import load_dotenv
from groq import Groq
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os


#if choice1 == 1:
client = Groq(
api_key=os.environ.get("GROQ_API_KEY"),
)
# Title of the app
st.title("LegitMate.ai–Legal assistance 24/7💎")

# Write text
st.write("Welcome to your Legal Matrimonial Assistant app!")

# Initialize chat history with a health-focused system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional AI Legal Assistant and Drafting Expert, specialized in Indian matrimonial cases, including domestic violence (DV), dowry harassment (498A), divorce, maintenance, child custody, and related family law matters." 
                "You are skilled in Indian Penal Code (IPC), Criminal Procedure Code (CrPC), Hindu Marriage Act (HMA), Protection of Women from Domestic Violence Act (PWDVA), Dowry Prohibition Act, and other relevant matrimonial laws."

                "Your role is to:"
                "- Your help maily focused on male victims/their relative who are being framed in false matrimony cases done by wife/girlfrinds or her family members."
                "- Help users understand their legal case status and explain possible outcomes in simple, non-technical language. "
                "- Identify common risks, causes, and provide risk resolution ideas. "
                "- Assist in drafting petitions, affidavits, replies, written statements, counter-affidavits, settlement drafts, and other legal documents in proper Indian legal style. "
                "- Provide sample formats for FIR quashing, bail applications, discharge petitions, cross-examination questions, case strategies, and appeals. "
                "- If requested, provide output in different formats (Word, PDF, plain text, or tabular summaries)." 
                "- Always show output in clear, professional, and court-usable format with proper legal language. "
                "- When possible, include detailed analysis, root cause reasoning, and suggestions for strengthening the user’s legal position. "

                "If a user asks about anything unrelated to Indian matrimonial/domestic violence cases, reply:"
                "I am here to help with Indian matrimonial and domestic violence related legal queries and drafting support." 
                "Please ask about DV cases, 498A, matrimonial disputes, custody, maintenance, divorce, or related legal drafting."

            )
        }
    ]

with st.sidebar:
    st.header("💬 Enter/Upload Your Code/File")
    with st.form("chat_form", clear_on_submit=True):
        #user_input = st.text_input("Hi, How can I help you today ?", key="input_box")
        choice1 = st.radio(
            "Enter your Language choice:",
            (1, 2),
            format_func=lambda x: "Hindi" if x == 1 else "English"
        )        
        user_input=st.text_area("Hi, How can I help you today ?", height=50)
        uploaded_file = st.file_uploader(
        "Attach a supporting file (optional)", 
        type=["txt", "docx", "pdf"])  # Restrict to text files only
        
        submitted = st.form_submit_button("Submit")
    
    #user_input=st.text_input("Hi, How can I help you today ?")
    #Submit button to control execution
    if submitted:
        if not user_input:  # Text is mandatory
            st.error("⚠️ Please enter text before submitting.")
        else:
            st.success("✅ Processing your request...")
            #st.write("Text entered:", text_val)    
            if uploaded_file:
                st.write("File uploaded:", uploaded_file.name)
            else:
                st.info("No file uploaded (that’s okay!)")
                
#text_data=""    
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    content = ""
    contentTbl=""
    #st.write(file_type)
    if file_type == "txt":
        # Read as text
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        content = stringio.read()
        text_data=content
        #st.write(text_data)
    else:
        st.error("⚠️ Unsupported file type. Please upload a .py file.")
        text_data=""
else:
    text_data=""

messages = st.session_state.messages
if choice1==1:
    messages.append({"role":"user", "content": user_input+text_data+"Please reply in Hindi language."}) 
else:
    messages.append({"role":"user", "content": user_input+text_data+"Please reply in English language."}) 

#messages.append({"role":"user", "content": user_input+text_data})
if submitted:
    try:
        chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile"
            )  
        response=chat_completion.choices[0].message.content
        st.markdown(response)
    except:
        st.markdown("An unexpected error occurred!")


