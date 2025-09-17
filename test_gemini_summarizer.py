"""
Test suite for Gemini summarization functionality
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from app.services.summarizer import GeminiSummarizer, ExtractiveSummarizer, get_summarizer


class TestGeminiSummarizer:
    """Test cases for GeminiSummarizer class"""

    def test_initialization_with_api_key(self):
        """Test GeminiSummarizer initializes correctly with valid API key"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
            with patch('google.generativeai.configure') as mock_configure:
                with patch('google.generativeai.GenerativeModel') as mock_model:
                    summarizer = GeminiSummarizer()
                    assert summarizer.api_key == 'test-api-key'
                    assert summarizer.available is True
                    mock_configure.assert_called_once_with(api_key='test-api-key')

    def test_initialization_without_api_key(self):
        """Test GeminiSummarizer raises error without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
                GeminiSummarizer()

    def test_initialization_import_error(self):
        """Test GeminiSummarizer handles missing google-generativeai library"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
            with patch('builtins.__import__', side_effect=ImportError):
                with pytest.raises(ImportError, match="google-generativeai library not available"):
                    GeminiSummarizer()

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_summarize_success(self, mock_model_class, mock_configure):
        """Test successful summarization with Gemini API"""
        # Setup mocks
        mock_response = MagicMock()
        mock_response.text = "This investment portfolio shows strong performance with 15% returns and recommends diversification into emerging markets."

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
            summarizer = GeminiSummarizer()

            test_text = "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management."

            result = summarizer.summarize(test_text)

            assert result == "This investment portfolio shows strong performance with 15% returns and recommends diversification into emerging markets."
            mock_model.generate_content.assert_called_once()

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_summarize_fallback_on_api_error(self, mock_model_class, mock_configure):
        """Test fallback to extractive summarization on API error"""
        # Setup mocks to simulate API error
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
            with patch('app.services.summarizer.ExtractiveSummarizer') as mock_extractive:
                mock_extractive_instance = MagicMock()
                mock_extractive_instance.summarize.return_value = "Fallback extractive summary"
                mock_extractive.return_value = mock_extractive_instance

                summarizer = GeminiSummarizer()
                test_text = "Test document content for summarization."

                result = summarizer.summarize(test_text)

                assert result == "Fallback extractive summary"
                mock_extractive_instance.summarize.assert_called_once_with(test_text)

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_summarize_fallback_on_empty_response(self, mock_model_class, mock_configure):
        """Test fallback to extractive summarization on empty response"""
        # Setup mocks to simulate empty response
        mock_response = MagicMock()
        mock_response.text = None

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
            with patch('app.services.summarizer.ExtractiveSummarizer') as mock_extractive:
                mock_extractive_instance = MagicMock()
                mock_extractive_instance.summarize.return_value = "Fallback extractive summary"
                mock_extractive.return_value = mock_extractive_instance

                summarizer = GeminiSummarizer()
                test_text = "Test document content for summarization."

                result = summarizer.summarize(test_text)

                assert result == "Fallback extractive summary"
                mock_extractive_instance.summarize.assert_called_once_with(test_text)


class TestSummarizerFactory:
    """Test cases for get_summarizer factory function"""

    def test_get_extractive_summarizer(self):
        """Test factory returns ExtractiveSummarizer for 'extractive' provider"""
        summarizer = get_summarizer("extractive")
        assert isinstance(summarizer, ExtractiveSummarizer)

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_get_gemini_summarizer(self, mock_model, mock_configure):
        """Test factory returns GeminiSummarizer for 'gemini' provider"""
        summarizer = get_summarizer("gemini")
        assert isinstance(summarizer, GeminiSummarizer)

    def test_get_unknown_provider(self):
        """Test factory raises error for unknown provider"""
        with pytest.raises(ValueError, match="Unknown summarizer provider: unknown"):
            get_summarizer("unknown")


class TestFinancialDomainPrompts:
    """Test cases for financial domain-specific prompts"""

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_financial_prompt_structure(self, mock_model_class, mock_configure):
        """Test that financial domain prompts are used correctly"""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'}):
            summarizer = GeminiSummarizer()
            test_text = "Investment analysis document"

            summarizer.summarize(test_text)

            # Verify the prompt contains financial domain instructions
            call_args = mock_model.generate_content.call_args[0][0]
            assert "financial document summarization expert" in call_args
            assert "financial insights" in call_args
            assert "financial terminology" in call_args
            assert "financial advisors" in call_args
            assert test_text in call_args
