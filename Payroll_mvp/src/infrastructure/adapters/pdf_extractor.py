import pdfplumber
from io import BytesIO
from src.application.ports import TextExtractorPort

class PDFTextExtractor(TextExtractorPort):
    async def extract_text(self, file_content: bytes) -> str:
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            raise RuntimeError(f"Error al leer el PDF: {str(e)}")