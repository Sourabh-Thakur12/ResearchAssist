class BrowserTool:
    """
    MOCK TOOL: Simulates fetching and scraping the raw HTML content of a URL.
    In a real system, this would use a library like requests + BeautifulSoup/Trafilatura.
    """
    def __init__(self):
        print("BrowserTool initialized.")

    def scrape(self, url: str) -> str:
        """
        Fetches and returns the raw content of a given URL.

        :param url: The URL to scrape.
        :return: The raw content (mock HTML/text).
        """
        print(f"MOCK BrowserTool: Attempting to scrape {url}")

        if "loops-paper" in url:
            return (
                "<html><body><header>Logo and Nav Bar</header>"
                "<h1>The Power of Reflection Loops</h1>"
                "<p>Introduction: Reflection is the core mechanism enabling self-correction in a multi-agent system. "
                "The **LoopManagerAgent** controls the reflection, deciding whether to re-run the **RetrieverAgent** "
                "or the **PaperReaderAgent**.</p>"
                "<h2>Results: Accuracy Metrics</h2>"
                "<p>We observed a mean accuracy gain of $A=0.35$ using three reflection cycles.</p>"
                "<footer>Contact us at info@mock-science.com</footer></body></html>"
            )
        elif "adk-blog" in url:
            return (
                "<html><body><h1>ADK Workflows</h1><p>The ADK orchestrator uses a JSON graph to define the agent flow: "
                "QueryParser -> Retriever -> DocProcessor. This ensures deterministic and modular execution.</p>"
                "<footer>End of article.</footer></body></html>"
            )
        elif "pitfalls" in url:
            return (
                "<html><body><article><h1>Common Pitfalls</h1><p>A major pitfall is handling **boilerplate text**. "
                "The **DocProcessorAgent** must aggressively clean the raw content to prevent extraction errors downstream.</p>"
                "</article></body></html>"
            )
        else:
            return ""