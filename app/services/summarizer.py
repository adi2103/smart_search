from abc import ABC, abstractmethod
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

class Summarizer(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str:
        pass

class ExtractiveSummarizer(Summarizer):
    def __init__(self, sentence_count: int = 3):
        self.summarizer = LexRankSummarizer()
        self.sentence_count = sentence_count

    def summarize(self, text: str) -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = self.summarizer(parser.document, self.sentence_count)
        return " ".join(str(sentence) for sentence in summary)

def get_summarizer(provider: str = "extractive") -> Summarizer:
    if provider == "extractive":
        return ExtractiveSummarizer()
    raise ValueError(f"Unknown summarizer provider: {provider}")
