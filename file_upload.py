import google.generativeai as genai
from pathlib import Path
import mimetypes

def configure_gemini_api(api_key):
    """Configure the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)

def upload_file(file_path):
    """Upload a file to Gemini API and return its metadata."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Detect the MIME type or set manually for known types
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        if file_path.suffix == ".md":
            mime_type = "text/md"
        elif file_path.suffix == ".pdf":
            mime_type = "application/pdf"
        elif file_path.suffix == ".txt":
            mime_type = "text/plain"
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

    # Upload the file to Gemini API
    uploaded_file = genai.upload_file(file_path, mime_type=mime_type)
    print(f"Uploaded {file_path.name} as {uploaded_file.name}")
    return uploaded_file.name  # Return the file's unique name for API use
