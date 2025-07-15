from google import genai
from flask import url_for

import os
from dotenv import load_dotenv

gemini = genai.Client(api_key=os.getenv("GEMINI_KEY"))

filedir = os.path.dirname(__file__)
appdir = os.path.dirname(filedir)
filepath = os.path.join(appdir, "data", "CV.txt")
print(filepath)
with open(filepath, "r") as f:
    my_profile = f.read()

def generate_proposal(job_description, my_profile, job_title):
    """
    Generate a proposal for a job using Google Gemini.
    """
    prompt = f"""
    I am an Upwork freelancer. I have found a food opportunity.
    My profile is given below:
    {my_profile}
    Here is the job that I am proposing for:
    Title: {job_title}
    Description: {job_description}
    Create a professional proposal for this job.
    """
    
    response = gemini.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
    return response.text

# prompt = """
#     I am an Upwork freelancer. I have found a food opportunity.
#     My profile is given below:
#     .....
#     Here is the job that i am proposing for:
#     ...
#     Create a professional proposal for ...
# """

# response = gemini.models.generate_content(
#     model="gemini-2.5-flash", contents=prompt
# )
# print(response.text)