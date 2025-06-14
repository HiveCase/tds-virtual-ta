import json
import os
from pathlib import Path
from bs4 import BeautifulSoup
import markdown
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def process_discourse_json(json_file):
    """Process a single Discourse JSON file into documents"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = []
    for post in data.get('posts', []):
        # Extract clean text from Discourse HTML
        soup = BeautifulSoup(post.get('cooked', ''), 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        if text:
            metadata = {
                'source': f"discourse_{post['id']}",
                'url': f"https://discourse.onlinedegree.iitm.ac.in/t/{post['topic_slug']}/{post['topic_id']}/{post['post_number']}",
                'title': post.get('topic_title', ''),
                'date': post.get('created_at', '')
            }
            documents.append(Document(page_content=text, metadata=metadata))
    
    return documents

def process_markdown_file(md_file):
    """Process a single markdown file into documents"""
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Convert markdown to plain text
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, 'html.parser')
    plain_text = soup.get_text(separator=' ', strip=True)
    
    if plain_text:
        metadata = {
            'source': os.path.basename(md_file),
            'url': '',  # Course content might not have URLs
            'title': os.path.basename(md_file),
            'date': os.path.getmtime(md_file)
        }
        return [Document(page_content=plain_text, metadata=metadata)]
    return []

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def process_all_data(discourse_dir, course_dir, output_file="processed/chunks.json"):
    """Process all data from both sources"""
    all_documents = []
    
    # Process Discourse JSON files
    for json_file in Path(discourse_dir).glob("*.json"):
        all_documents.extend(process_discourse_json(json_file))
    
    # Process course markdown files
    for md_file in Path(course_dir).glob("**/*.md"):
        all_documents.extend(process_markdown_file(md_file))
    
    # Chunk documents
    chunked_docs = chunk_documents(all_documents)
    
    # Save processed chunks
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([doc.dict() for doc in chunked_docs], f, indent=2)
    
    return chunked_docs

if __name__ == "__main__":
    discourse_dir = "../data/discourse"
    course_dir = "../data/course"
    process_all_data(discourse_dir, course_dir)