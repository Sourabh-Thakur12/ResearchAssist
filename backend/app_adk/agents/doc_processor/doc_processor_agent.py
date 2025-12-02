import json
import re
from bs4 import BeautifulSoup


class DocProcessorAgent:

    def __init__(self):
        print("[DocProcessor] Initialized")

    # -----------------------------
    # Clean HTML → plain text
    # -----------------------------
    def clean_html(self, html: str) -> str:
        print("[DocProcessor] Cleaning HTML...")

        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        # Remove navigation/footer/sidebar
        for selector in [
            "header", "footer", "nav", "aside",
            "[class*=header]", "[class*=nav]", "[class*=footer]",
            "[id*=header]", "[id*=nav]", "[id*=footer]"
        ]:
            for t in soup.select(selector):
                t.extract()

        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        print(f"[DocProcessor] Cleaned HTML length: {len(text)} characters")
        return text

    # -----------------------------
    # Summarize text
    # -----------------------------
    def summarize(self, text: str) -> str:
        print("[DocProcessor] Summarizing...")
        if not text:
            return ""

        sentences = re.split(r'(?<=[.!?]) +', text)
        return " ".join(sentences[:2])

    # -----------------------------
    # Relevance score
    # -----------------------------
    def compute_relevance(self, text: str, keywords: list) -> float:
        print("[DocProcessor] Scoring relevance...")
        text_lower = text.lower()
        matches = sum(1 for k in keywords if k.lower() in text_lower)
        score = min(1.0, matches / max(1, len(keywords)) + 0.2)
        print(f"[DocProcessor] Score = {score}")
        return score

    # -----------------------------
    # MAIN PROCESSOR
    # -----------------------------
    def run(self, retriever_json: str) -> str:
        print("\n[DocProcessor] Running...")
        print(f"[DocProcessor] Incoming JSON size: {len(retriever_json)} bytes")

        try:
            data = json.loads(retriever_json)
        except Exception as e:
            print("[DocProcessor] ERROR: cannot parse retriever JSON!", e)
            return json.dumps({"error": "Invalid JSON"}, indent=2)

        documents = data.get("documents", [])
        print(f"[DocProcessor] Documents found: {len(documents)}")

        core_question = data.get("core_question", "")
        keywords = re.findall(r"\w+", core_question)

        processed_docs = []

        for i, doc in enumerate(documents):
            print(f"\n[DocProcessor] Processing document #{i+1}")

            raw = doc.get("raw_extracted_content")

            # Debug raw type
            print(f"[DocProcessor] raw_extracted_content type: {type(raw)}")

            # Skip list results (search result lists)
            if isinstance(raw, list):
                print("[DocProcessor] Skipping because raw content is a LIST (search results).")
                continue

            if not isinstance(raw, str):
                print("[DocProcessor] Skipping because raw content is not string!")
                continue

            cleaned_text = self.clean_html(raw)
            summary = self.summarize(cleaned_text)
            score = self.compute_relevance(cleaned_text, keywords)

            processed_docs.append({
                "title": doc.get("title", "Untitled"),
                "url": doc.get("url"),
                "cleaned_content": cleaned_text,
                "summary": summary,
                "relevance_score": score
            })

        output = {
            "core_question": core_question,
            "documents": processed_docs
        }

        final_json = json.dumps(output, indent=2)
        print("\n[DocProcessor] Final JSON size:", len(final_json), "bytes")
        print("[DocProcessor] DONE.\n")

        return final_json
