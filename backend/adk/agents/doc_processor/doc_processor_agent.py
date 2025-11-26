import json
from typing import List, Dict
import re
from adk.tools.pdf_processor import PDFProcessor # Assuming this tool exists

class DocProcessorAgent:
    """
    Processes raw content: removes boilerplate, extracts main body, 
    sections text, and chunks text for structured parsing.
    """

    def __init__(self):
        # Initialize any necessary components (e.g., text segmentation model)
        self.pdf_processor = PDFProcessor() # For handling PDF content in future

    def _remove_boilerplate(self, html_content: str) -> str:
        """
        A simple, heuristic-based function to strip common HTML tags and boilerplate.
        A production system would use libraries like BeautifulSoup or trafilatura.
        """
        # 1. Remove script and style tags
        cleaned_text = re.sub(r'<script\b[^>]*>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        cleaned_text = re.sub(r'<style\b[^>]*>.*?</style>', '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
        
        # 2. Extract visible text (a very crude method, needs improvement for production)
        text_only = re.sub(r'<[^>]+>', ' ', cleaned_text).strip()
        
        # 3. Simplify whitespace
        text_only = re.sub(r'\s+', ' ', text_only).strip()
        
        return text_only

    def _section_and_chunk_text(self, text: str, max_chunk_size: int = 1024) -> List[Dict]:
        """
        Segments the cleaned text into logical sections (heuristically based on headers)
        and then chunks them into smaller parts for LLM processing.
        """
        sections = []
        
        # A simple heuristic: split by double newline to get paragraphs/sections
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        current_section = "Main Body" # Default section name
        
        for p in paragraphs:
            # Simple header detection (e.g., all caps, short line)
            if len(p.split()) < 10 and p.isupper():
                current_section = p.strip()
                continue

            # Check if adding the current paragraph exceeds the chunk size
            if len(current_chunk) + len(p) + 1 > max_chunk_size:
                if current_chunk:
                    sections.append({
                        "section_title": current_section,
                        "text_chunk": current_chunk.strip()
                    })
                current_chunk = p
            else:
                current_chunk += " " + p

        # Add the last chunk
        if current_chunk:
            sections.append({
                "section_title": current_section,
                "text_chunk": current_chunk.strip()
            })
            
        return sections

    def run(self, retriever_output_json: str) -> str:
        """
        Executes the document processing logic on the raw documents.

        :param retriever_output_json: JSON string from RetrieverAgent.
        :return: JSON string containing processed documents with text chunks.
        """
        try:
            input_data = json.loads(retriever_output_json)
            documents: List[Dict] = input_data.get("documents", [])
            core_question = input_data.get("core_question")
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON input from RetrieverAgent"})

        processed_documents: List[Dict] = []
        
        for doc in documents:
            raw_content = doc.get("raw_extracted_content", "")
            url = doc.get("url", "N/A")
            
            print(f"DocProcessor: Processing document: {doc.get('title')}")

            if not raw_content:
                print(f"DocProcessor: Skipping document with no raw content: {url}")
                continue

            # 1. Remove Boilerplate (if it's not a PDF)
            if not url.lower().endswith('.pdf'):
                cleaned_text = self._remove_boilerplate(raw_content)
            else:
                # Placeholder for PDF handling
                cleaned_text = self.pdf_processor.extract_text(raw_content)

            if not cleaned_text:
                print(f"DocProcessor: Content extraction failed for: {url}")
                continue

            # 2. Section and Chunk Text
            text_chunks = self._section_and_chunk_text(cleaned_text)

            # 3. Create the final processed document object
            processed_documents.append({
                "source_url": url,
                "source_title": doc.get("title"),
                "relevance_score": doc.get("relevance_score"),
                "processed_chunks": text_chunks
            })

        # Output structure must strictly adhere to the contract for PaperReaderAgent
        output_json = {
            "core_question": core_question,
            "processed_documents": processed_documents
        }
        
        return json.dumps(output_json, indent=2)


# --- Mock Implementations for adk/tools/ ---
class PDFProcessor:
    def extract_text(self, raw_data: str) -> str:
        # Mock for PDF text extraction
        return "This is a mock text from a PDF. It is clean and ready to be chunked."


# Example of how to run the agent:
if __name__ == '__main__':
    # Mock input from RetrieverAgent
    mock_retriever_output = json.dumps({
        "core_question": "What are the latest findings in multi-agent system reflection?",
        "documents": [
            {
                "title": "Agent Reflection Mechanisms",
                "url": "http://example.com/agent-reflection",
                "snippet": "Mechanisms for self-correction.",
                "raw_extracted_content": "<html><body><header>Logo</header><h1>Agent Reflection Mechanisms</h1><p>Introduction: Reflection is key to multi-agent accuracy.</p><h2>METHODOLOGY</h2><p>We used iterative prompting with a CriticAgent. The result was <b>90% accuracy</b> improvement. This is a significant claim.</p><footer>Copyright 2024</footer></body></html>",
                "relevance_score": 0.95
            }
        ]
    })

    doc_processor = DocProcessorAgent()
    output = doc_processor.run(mock_retriever_output)
    print("\n--- DocProcessorAgent Output ---")
    print(output)