import PyPDF2

def process_book():
    # Yahan apni PDF ka exact naam likhna hai jo tumne medibot folder mein rakha hai
    book_path = "heart_book.pdf" 
    text = ""
    try:
        # PDF read karna start karo
        pdf_reader = PyPDF2.PdfReader(book_path)
        
        # Pura text nikalne ke liye har page loop ke through read karna
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
        return text
        
    except FileNotFoundError:
        print("🚨 Error: Book nahi mili. Check karo ki PDF medibot folder mein hai ya nahi.")
        return "Standard cardiology principles apply."
    except Exception as e:
        print(f"🚨 Error reading book: {e}")
        return "Standard cardiology principles apply."