from fastapi import FastAPI, UploadFile, File
import shutil
import os
from google import genai
from utils import extract_text_from_pdf

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # সমস্ত ফ্রন্টএন্ড ফাইলকে অ্যাক্সেস দেওয়ার জন্য
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# আপলোড করা ফাইল রাখার জন্য টেম্পোরারি ফোল্ডার
UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ⚠️ এখানে তোমার aistudio.google.com থেকে নেওয়া ফ্রি API Key-টি বসাবে
GEMINI_API_KEY = "AQ.Ab8RN6IpDFKgVyJGdJlLybDxPx1qtRxTVhNI93x7vsUdXQLGmQ"

# গুগলের জেনারেটিভ এআই ক্লায়েন্ট ইনিশিয়ালাইজ করা
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@app.get("/")
def home():
    return {"message": "Welcome to CleanNotes AI Server!"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # ১. ফাইলের পাথ তৈরি ও সেভ করা
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # ২. পিডিএফ থেকে টেক্সট বের করা
    pdf_text = extract_text_from_pdf(file_path)
    
    # ৩. কাজ শেষে টেম্পোরারি ফাইলটি ডিলিট করা
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # যদি পিডিএফে কোনো টেক্সট না পাওয়া যায়
    if not pdf_text.strip():
        return {"error": "পিডিএফ থেকে কোনো টেক্সট পড়া যায়নি ভাই!"}

    # ৪. এআই প্রম্পট ইঞ্জিনিয়ারিং (আমরা এআই-কে সুনির্দিষ্ট ফরম্যাটে ডেটা দিতে বাধ্য করছি)
    prompt = f"""
    You are an expert academic assistant. Analyze the following study content extracted from a PDF and generate highly structured revision notes in friendly native Bengali.
    
    Analyze this text:
    {pdf_text}
    
    Strictly provide the response in this exact format (do not use markdown headers outside this format):
    
    Cleaned Notes:
    [Write comprehensive, clean, bulleted study notes here]
    
    Short Summary:
    [Write a concise 3-4 sentence summary here]
    
    Key Concepts:
    [List the main concepts discussed]
    
    Important Formulas:
    [List all mathematical/scientific formulas found. If none, write 'No formulas in this topic']
    
    Important Questions:
    [Generate 3-5 high-yield questions based on the text for student practice]
    """

    try:
        # ৫. Gemini 2.5 Flash মডেল কল করা (যা সবচেয়ে ফাস্ট এবং ফ্রি)
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # ফ্রন্টএন্ডের জন্য এআই-এর রেসপন্স টেক্সট পাঠানো
        return {
            "filename": file.filename,
            "ai_analysis": response.text
        }
        
    except Exception as e:
        return {"error": f"Gemini API Error: {str(e)}"}