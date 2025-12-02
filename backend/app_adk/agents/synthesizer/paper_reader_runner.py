import json
from app_adk.agents.synthesizer.synthesizer import SynthesizerAgent

def run_synthesizer(doc_processor_json: str):
    """
    Accepts stringified JSON from DocProcessor
    Returns synthesized final answer
    """

    # Convert doc processor output string → dict
    data = json.loads(doc_processor_json)

    synth = SynthesizerAgent()
    out = synth.run(json.dumps(data))

    # Save output
    with open("app_adk/agents/synthesizer/output_answer.md", "w", encoding="utf-8") as f:
        f.write(out)

    print("\n✅ Saved final answer to synthesizer/output_answer.md")
    return out 
