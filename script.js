async function processPDF() {
    const fileInput = document.getElementById('pdfFile');
    const loadingText = document.getElementById('loadingText');
    const resultBox = document.getElementById('resultBox');
    const aiOutput = document.getElementById('aiOutput');

    // ১. চেক করা হচ্ছে ইউজার ফাইল সিলেক্ট করেছে কি না
    if (fileInput.files.length === 0) {
        alert("দয়া করে আগে একটি পিডিএফ ফাইল সিলেক্ট করুন।");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // ২. লোডিং টেক্সট দেখানো
    loadingText.style.display = "block";
    resultBox.style.display = "none";

    try {
        // ৩. রেন্ডার লাইভ পাইথন সার্ভারে ফাইল পাঠানো হচ্ছে
        const response = await fetch('https://cleannotes-ai.onrender.com/upload-pdf', {
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

        // ৫. সফলভাবে রেসপন্স আসলে স্ক্রিনে দেখানো
        aiOutput.innerHTML = data.notes;
        resultBox.style.display = "block";

    } catch (err) {
        alert("সার্ভারের সাথে যোগাযোগ করা যাচ্ছে না। দয়া করে একটু পর আবার চেষ্টা করুন।");
        console.error(err);
    } finally {
        loadingText.style.display = "none";
    }
}