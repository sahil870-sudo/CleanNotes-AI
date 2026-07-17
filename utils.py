import pypdf

def extract_text_from_pdf(file_path):
    # পিডিএফ ফাইলটি রিড মোডে ওপেন করা হচ্ছে
    reader = pypdf.PdfReader(file_path)
    extracted_text = ""
    
    # লুপ চালিয়ে প্রতিটা পেজের টেক্সট একটার সাথে আরেকটা জোড়া লাগানো হচ্ছে
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
            
    return extracted_text.strip()