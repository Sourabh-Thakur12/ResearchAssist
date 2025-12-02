import json
import re

class SynthesizerAgent:

    def __init__(self):
        print("[Synthesizer] Initialized")

    # -----------------------------------------------
    # Extract key points (simple NLP-style extraction)
    # -----------------------------------------------
    def extract_points(self, text: str):
        lines = re.split(r'[.;!?]\s+', text)
        points = []

        for l in lines:
            l = l.strip()
            if len(l) < 40:
                continue

            # heuristic filters
            if any(x in l.lower() for x in [
                "study", "research", "suggest", "evidence", "date",
                "archaeolog", "inscription", "astronom", "histor", "scholar"
            ]):
                points.append(l)

        return points[:5]  # limit per document

    # -----------------------------------------------
    # Answer Synthesis Logic
    # -----------------------------------------------
    def synthesize_answer(self, question, documents):
        final_points = []
        citations = []

        for doc in documents:
            content = doc.get("cleaned_content", "")
            url = doc.get("url")

            extracted = self.extract_points(content)

            if extracted:
                final_points.extend(extracted)
                citations.append({"title": doc.get("title"), "url": url})

        # If nothing extracted, fallback to summaries
        if not final_points:
            final_points = [doc.get("summary", "") for doc in documents]

        # Create final narrative
        answer = f"### **Answer: {question}**\n\n"

        for p in final_points:
            answer += f"- {p}\n"

        # Attach citations
        answer += "\n### **Sources Used**\n"
        for c in citations:
            answer += f"- {c['title']} → {c['url']}\n"

        return answer

    # -----------------------------------------------
    # MAIN RUN
    # -----------------------------------------------
    def run(self, docprocessor_json: str) -> str:
        print("\n[Synthesizer] RUNNING...")

        try:
            data = json.loads(docprocessor_json)
        except:
            return "ERROR: invalid JSON passed into Synthesizer"

        question = data.get("core_question", "")
        documents = data.get("documents", [])

        if not documents:
            return "No documents received from DocProcessor"

        answer = self.synthesize_answer(question, documents)

        print("[Synthesizer] DONE")
        return answer
