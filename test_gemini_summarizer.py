import pytest
import os
from app.services.summarizer import GeminiSummarizer, get_summarizer

class TestGeminiSummarizer:
    
    def test_gemini_requires_api_key(self):
        """Test GeminiSummarizer requires API key"""
        # Clear environment variable
        old_key = os.environ.pop('GEMINI_API_KEY', None)
        
        try:
            with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
                GeminiSummarizer()
        finally:
            if old_key:
                os.environ['GEMINI_API_KEY'] = old_key
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="GEMINI_API_KEY not available")
    def test_gemini_summarization_real(self):
        """Test actual Gemini summarization with real API"""
        summarizer = GeminiSummarizer()
        
        test_text = "This comprehensive investment strategy report analyzes current market conditions and provides detailed recommendations for portfolio optimization. The report examines various asset classes including equities, bonds, and real estate. Market volatility has increased due to geopolitical tensions and inflation concerns."
        
        result = summarizer.summarize(test_text, content_type="document")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert len(result) < len(test_text)  # Should be more concise
    
    def test_get_summarizer_factory(self):
        """Test summarizer factory returns correct type"""
        if os.getenv('GEMINI_API_KEY'):
            gemini_summarizer = get_summarizer("gemini")
            assert isinstance(gemini_summarizer, GeminiSummarizer)
