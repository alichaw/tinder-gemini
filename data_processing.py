from pathlib import Path
from file_upload import upload_file

def load_markdown_files(folder_path):
    """Load all Markdown files from the specified folder."""
    documents = []
    for file_path in Path(folder_path).rglob("*.md"):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            documents.append({"file": file_path.name, "content": content, "path": file_path})
    return documents

def upload_and_prepare_context(folder_path):
    """Upload all Markdown files and prepare their combined context."""
    documents = load_markdown_files(folder_path)
    context = ""
    uploaded_files = []

    for doc in documents:
        cleaned_content = doc["content"]  # Assuming content is already cleaned
        context += cleaned_content + " "
        uploaded_files.append(upload_file(doc["path"]))

    return context.strip(), uploaded_files
