from PyPDF2 import PdfReader

def middle_read_pdf(file:str):
    """
    Read the text content from a PDF file.

    Args:
        file (str): The path to the PDF file.

    Returns:
        str: The extracted text content from the PDF file.
    """
    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        # Clean Data
        text = text.replace("\t", " ")
        text = text.replace("\r", " ")
        text = text.replace("\f", " ")
        text = text.replace("\v", " ")

        return {
            "status": 200,
            "message": text
        }
    
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {str(e)}")
        return {
            "status": 500,
            "message": "Error during PDF reading"
        }