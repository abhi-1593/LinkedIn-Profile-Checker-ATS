# python -m venv .venv
# .\.venv\Scripts\activate
# pip install streamlit google-generativeai
# pip install python-dotenv==1.0.1
# pip install pdf2image==1.17.0
# pip install poppler-utils==0.1.0
# pip install pdf-info==2.1.0

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import base64
import pdf2image
import io

# setup api key
genai.configure(api_key="AIzaSyDOsV6e2ZadNnHwC7YugCAhkRglayCTDPs")

# Design the front end
st.header("LinkedIn Profile Analysis & ATS Score")
st.subheader(body="ATS Tracking System & Profile SWOT Analysis")
input_text=st.text_area(label="Enter the Job Description",key="Input J.D.")
upload_file=st.file_uploader(label="Upload the Resume",type="pdf")


if upload_file is not None:
    st.write("The File is uploaded Successfully")

# Buttons:
submit1=st.button("Summary of Resume")
submit2=st.button("Calculate ATS Score")

# Prompts

prompt1='''Act as a Technical HR & Ops Manager and your task is to review the profile\
    against the Job Description. Please share your personal evaluation including SWOT analysis\
        of the profile with respect to the Job Description. Give me the profile highlights in pointers.'''

prompt2='''You are a skilled ATS (Application Tracking System) scanner with understanding of\
    Data Science, Machine Learning & Artificail Intelligence followed by\
        Application Tracking System functionality. Your task is to evaluate the resume with the Job Description &\
            give me the percentage match if the resume matches the Job Description.\
                The first output should come as ATS Score: in percentage followed by \
                    missing keywords in the resume (in bullet points) & in the end\
                        give me Improvement Areas along with your final thoughts.'''

# Gen Ai Model....
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# PDF File
def input_pdf_setup(upload_file):
    if upload_file is not None:
        # Convert pdf into Image
        images = pdf2image.convert_from_bytes(upload_file.read())
       
        first_page = images[0]
        # Convert them into Bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Lets put soul into the buttons
if submit1:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemini_response(prompt1,pdf_content,
                                     input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemini_response(prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")
