import streamlit as st
import json
from datetime import datetime
import os
from agent import DoctorAgent
from utils import format_report_for_streamlit, save_report_to_file

# Page configuration
st.set_page_config(page_title="MedSense Health Assistant", page_icon="🩺", layout="wide")

# Initialize session state variables
if 'doctor_agent' not in st.session_state:
    st.session_state.doctor_agent = DoctorAgent()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'consultation_active' not in st.session_state:
    st.session_state.consultation_active = False
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""

# Function to handle sending a message
def process_input():
    user_input = st.session_state.user_input
    if user_input and user_input.strip():
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Mark consultation as active
        st.session_state.consultation_active = True
        
        # Process message through doctor agent
        response = st.session_state.doctor_agent.process_message(user_input)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Function to start a new consultation
def new_consultation():
    st.session_state.doctor_agent = DoctorAgent()
    st.session_state.messages = []
    st.session_state.consultation_active = False
    st.session_state.report_generated = False
    st.session_state.report_content = ""

# Function to generate a report
def generate_report():
    report = st.session_state.doctor_agent.generate_report()
    st.session_state.report_content = report
    st.session_state.report_generated = True
    return report

# App header
st.title("🩺 MedSense Health Assistant")
st.markdown("""
Welcome to MedSense, your AI health assistant. Describe your symptoms and I'll help guide you.

**Disclaimer**: This tool is for informational purposes only and not a substitute for professional medical advice.
""")

# Sidebar
with st.sidebar:
    st.header("Options")
    
    # New consultation button
    if st.button("Start New Consultation", key="new_consultation"):
        new_consultation()
    
    # Generate report button (only enabled if consultation is active)
    if st.session_state.consultation_active:
        if st.button("Generate Consultation Report", key="generate_report"):
            generate_report()
    
    # Display report if generated
    if st.session_state.report_generated:
        st.markdown("### Consultation Report")
        st.download_button(
            label="Download Report",
            data=st.session_state.report_content,
            file_name=f"medsense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
    # Display medical disclaimer
    st.markdown("---")
    st.markdown("""
    **Medical Disclaimer**:
    
    The information provided by MedSense is not a substitute for professional medical advice, diagnosis, or treatment. 
    Always seek the advice of your physician or other qualified health provider with any questions about your medical condition.
    """)

# Main chat interface
st.subheader("Chat with Dr. MedSense")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input - Fixed the issue with on_submit
if not st.session_state.report_generated:
    st.chat_input(
        "Describe your symptoms...", 
        key="user_input", 
        on_submit=process_input
    )

# Show initial instruction if no messages yet
if not st.session_state.messages:
    st.info("👋 Hello! I'm Dr. MedSense. Please describe your symptoms or health concerns, and I'll do my best to help.")

# Display the report if generated
if st.session_state.report_generated:
    st.subheader("Consultation Report")
    st.markdown(format_report_for_streamlit(st.session_state.report_content))

# Footer
st.markdown("---")
st.caption("MedSense AI Health Assistant - For demonstration purposes only")