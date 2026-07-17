async function processPDF() {
    const fileInput = document.getElementById('pdfFile');
    const loadingText = document.getElementById('loadingText');
    const resultBox = document.getElementById('resultBox');
    const aiOutput = document.getElementById('aiOutput');

    // ১. চেক করা হচ্ছে ইউজার ফাইল সিলেক্ট করেছে কি না
    if (fileInput.files.length === 0) {
        alert("দয়া করে আগে একটি মেসি লেকচার PDF আপলোড করুন ভাই!");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file); // পাইথনের UploadFile-এর সাথে ম্যাচ করার জন্য ডেটা ফরম্যাট তৈরি

    // ২. স্ক্রিনে লোডিং টেক্সট দেখানো এবং পুরানো রেজাল্ট হাইড করা
    loadingText.style.display = "block";
    resultBox.style.display = "none";

    try {
        // ৩. আমাদের লোকাল পাইথন সার্ভারে ফাইল পাঠানো হচ্ছে
        const response = await fetch('https://cleannotes-ai.onrender.com/upload-pdf', {', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // ৪. যদি কোনো এরর আসে
        if (data.error) {
            alert("Error: " + data.error);
            loadingText.style.display = "none";
            return;
        }

        // ৫. সফল হলে এআই-এর আউটপুট ড্যাশবোর্ডে দেখানো
        aiOutput.innerText = data.ai_analysis;
        resultBox.style.display = "block";

    } catch (error) {
        console.error(error);
        alert("সার্ভার কানেক্ট করা যায়নি! নিশ্চিত করুন আপনার পাইথন Uvicorn সার্ভারটি টার্মিনালে চালু আছে।");
    } finally {
        // কাজ শেষে লোডিং টেক্সট বন্ধ করা
        loadingText.style.display = "none";
    }
}