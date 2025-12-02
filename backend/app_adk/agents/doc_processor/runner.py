import json
from app_adk.agents.doc_processor.doc_processor_agent import DocProcessorAgent

def run_doc_processor():
    input_path = "app_adk/agents/retriever/prompt.json"
    data = json.load(open(input_path))

    processor = DocProcessorAgent()
    out = processor.run(json.dumps(data))

    print("\n--- DOC PROCESSOR OUTPUT ---\n")
    print(out)

    with open("app_adk/agents/doc_processor/prompt.json", "w", encoding="utf-8") as f:
        f.write(out)

    print("\n✅ Saved doc_processor/prompt.json")

if __name__ == "__main__":
    run_doc_processor()
