from app_adk.agents.query_parser.parser import runner as query_parser_runner
from app_adk.agents.retriever.retriever import RetrieverAgent
from app_adk.agents.doc_processor.runner import DocProcessorAgent
from app_adk.agents.synthesizer.paper_reader_runner import run_synthesizer
import json
import asyncio


class Orchestrator:

    def __init__(self):
        print("\n=== Orchestrator Initialized ===")
        self.retriever = RetrieverAgent()
        self.doc_processor = DocProcessorAgent()

    async def run(self, user_question: str):
        print("\n====== PIPELINE START ======\n")

        # ------------------------------------------
        # 1. QUERY PARSER
        # ------------------------------------------
        print("[1] Running QueryParserAgent...")
        parser_output = await query_parser_runner(user_question)

        with open("app_adk/agents/query_parser/prompt.json", "w") as f:
            f.write(parser_output)
        print("[1] DONE — Query parser JSON saved.\n")

        # ------------------------------------------
        # 2. RETRIEVER
        # ------------------------------------------
        print("[2] Running RetrieverAgent...")
        retriever_output = await self.retriever.run(parser_output)

        with open("app_adk/agents/retriever/prompt.json", "w") as f:
            f.write(retriever_output)
        print("[2] DONE — Retriever JSON saved.\n")

        # ------------------------------------------
        # 3. DOC PROCESSOR
        # ------------------------------------------
        print("[3] Running DocProcessorAgent...")
        doc_processed = self.doc_processor.run(retriever_output)

        with open("app_adk/agents/doc_processor/prompt.json", "w") as f:
            f.write(doc_processed)
        print("[3] DONE — DocProcessor JSON saved.\n")

        # ------------------------------------------
        # 4. SYNTHESIZER
        # ------------------------------------------
        print("[4] Running PaperReaderAgent / Synthesizer...")

        final_answer = run_synthesizer(doc_processed)

        with open("app_adk/agents/synthesizer/output.md", "w") as f:
            f.write(final_answer)

        print("[4] DONE — Final synthesized output saved.\n")

        print("====== PIPELINE COMPLETE ======\n")
        return final_answer


if __name__ == "__main__":

    user_q = input("\nEnter your research question: ")

    orch = Orchestrator()
    final_output = asyncio.run(orch.run(user_q))

    print("\n=== FINAL ANSWER ===\n")
    print(final_output)
