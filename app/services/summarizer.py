from abc import ABC, abstractmethod
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import os
from typing import Optional

class Summarizer(ABC):
    @abstractmethod
    def summarize(self, text: str, content_type: str = "document") -> str:
        pass

class ExtractiveSummarizer(Summarizer):
    def __init__(self, sentence_count: int = 3):
        self.summarizer = LexRankSummarizer()
        self.sentence_count = sentence_count

    def summarize(self, text: str, content_type: str = "document") -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = self.summarizer(parser.document, self.sentence_count)
        return " ".join(str(sentence) for sentence in summary)

class GeminiSummarizer(Summarizer):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.genai = genai
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.available = True
        except ImportError:
            raise ImportError("google-generativeai library not available. Install with: pip install google-generativeai")
        except Exception as e:
            raise RuntimeError(f"Gemini initialization failed: {e}")

    def summarize(self, text: str, content_type: str = "document") -> str:
        """Generate abstractive summary using Gemini API with context-specific prompts"""
        if not self.available:
            raise RuntimeError("Gemini summarizer not available")

        if content_type == "note":
            prompt = f"""
You are a financial advisor's assistant summarizing meeting notes. Create a concise summary for financial advisors to quickly understand client interactions.

Requirements:
- Focus on key client concerns, decisions made, and action items
- Highlight investment preferences, risk tolerance, and financial goals discussed
- Use professional advisory language
- Keep the summary to 2-3 sentences maximum
- Emphasize actionable insights for the advisor's next client interaction

Meeting notes to summarize:
{text}

Advisory Summary:"""
        else:  # document
            prompt = f"""
You are a financial document analyst summarizing client documents for financial advisors. Create a concise summary to help advisors quickly understand document contents.

Requirements:
- Focus on key financial insights, recommendations, and important metrics
- Highlight investment strategies, portfolio performance, and risk assessments
- Use professional financial terminology
- Keep the summary to 2-3 sentences maximum
- Emphasize critical information advisors need for client consultations

Document to summarize:
{text}

Advisory Summary:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.genai.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=200
                )
            )

            if response.text:
                return response.text.strip()
            else:
                # Fallback to extractive if no response
                fallback = ExtractiveSummarizer()
                return fallback.summarize(text)

        except Exception as e:
            print(f"Gemini summarization failed: {e}")
            # Fallback to extractive summarization
            fallback = ExtractiveSummarizer()
            return fallback.summarize(text)

class BARTSummarizer(Summarizer):
    def __init__(self):
        try:
            from transformers import pipeline
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU
            )
            self.available = True
        except ImportError:
            raise ImportError("transformers library not available. Install with: pip install transformers torch")
        except Exception as e:
            raise RuntimeError(f"BART initialization failed: {e}")

    def summarize(self, text: str, content_type: str = "document") -> str:
        """Generate abstractive summary using HuggingFace BART"""
        if not self.available:
            raise RuntimeError("BART summarizer not available")

        try:
            # BART works best with 512-1024 tokens, chunk if needed
            max_chunk_length = 1000
            if len(text) > max_chunk_length:
                text = text[:max_chunk_length]

            # Generate summary
            summary = self.summarizer(
                text,
                max_length=150,
                min_length=50,
                do_sample=False
            )

            if summary and len(summary) > 0:
                return summary[0]['summary_text']
            else:
                # Fallback to extractive if no response
                fallback = ExtractiveSummarizer()
                return fallback.summarize(text)

        except Exception as e:
            print(f"BART summarization failed: {e}")
            # Fallback to extractive summarization
            fallback = ExtractiveSummarizer()
            return fallback.summarize(text)

def get_summarizer(provider: str = "extractive") -> Summarizer:
    if provider == "extractive":
        return ExtractiveSummarizer()
    elif provider == "gemini":
        return GeminiSummarizer()
    elif provider == "bart":
        return BARTSummarizer()
    else:
        raise ValueError(f"Unknown summarizer provider: {provider}")
