"""
Test suite for BART summarization functionality
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.summarizer import BARTSummarizer, get_summarizer


class TestBARTSummarizer:
    """Test cases for BARTSummarizer class"""
    
    @patch('transformers.pipeline')
    def test_initialization_with_model_caching(self, mock_pipeline):
        """Test BARTSummarizer uses model caching correctly"""
        mock_model = MagicMock()
        mock_pipeline.return_value = mock_model
        
        # First initialization should load model
        summarizer1 = BARTSummarizer()
        assert summarizer1.available is True
        mock_pipeline.assert_called_once()
        
        # Second initialization should use cached model
        mock_pipeline.reset_mock()
        summarizer2 = BARTSummarizer()
        assert summarizer2.available is True
        mock_pipeline.assert_not_called()  # Should use cache
        
        # Both should reference same cached model
        assert summarizer1.summarizer is summarizer2.summarizer
    
    def test_initialization_import_error(self):
        """Test BARTSummarizer handles missing transformers library"""
        with patch('builtins.__import__', side_effect=ImportError):
            with pytest.raises(ImportError, match="transformers library not available"):
                BARTSummarizer()
    
    @patch('transformers.pipeline')
    def test_summarize_success(self, mock_pipeline):
        """Test successful summarization with BART"""
        # Setup mocks
        mock_summary_result = [{'summary_text': 'This is a BART-generated abstractive summary of the financial document.'}]
        mock_model = MagicMock()
        mock_model.return_value = mock_summary_result
        mock_pipeline.return_value = mock_model
        
        summarizer = BARTSummarizer()
        test_text = "This document provides a comprehensive analysis of the client investment portfolio for 2024. The portfolio shows strong performance in technology stocks with a 15% return. Key recommendations include diversifying into emerging markets and increasing bond allocation for risk management."
        
        result = summarizer.summarize(test_text)
        
        assert result == "This is a BART-generated abstractive summary of the financial document."
        mock_model.assert_called_once()
        
        # Verify BART-specific parameters
        call_args = mock_model.call_args
        assert call_args[1]['do_sample'] is False
        assert call_args[1]['truncation'] is True
    
    @patch('transformers.pipeline')
    def test_summarize_long_document_chunking(self, mock_pipeline):
        """Test document chunking for long texts"""
        mock_summary_result = [{'summary_text': 'Chunked summary'}]
        mock_model = MagicMock()
        mock_model.return_value = mock_summary_result
        mock_pipeline.return_value = mock_model
        
        summarizer = BARTSummarizer()
        
        # Create a long document (> 800 chars)
        long_text = "This is a very long document. " * 50  # ~1500 chars
        
        result = summarizer.summarize(long_text)
        
        assert result == "Chunked summary"
        
        # Verify text was chunked
        call_args = mock_model.call_args[0][0]
        assert len(call_args) <= 800
    
    @patch('transformers.pipeline')
    def test_summarize_fallback_on_error(self, mock_pipeline):
        """Test fallback to extractive summarization on BART error"""
        # Setup mocks to simulate BART error
        mock_model = MagicMock()
        mock_model.side_effect = Exception("BART processing error")
        mock_pipeline.return_value = mock_model
        
        with patch('app.services.summarizer.ExtractiveSummarizer') as mock_extractive:
            mock_extractive_instance = MagicMock()
            mock_extractive_instance.summarize.return_value = "Fallback extractive summary"
            mock_extractive.return_value = mock_extractive_instance
            
            summarizer = BARTSummarizer()
            test_text = "Test document content for summarization."
            
            result = summarizer.summarize(test_text)
            
            assert result == "Fallback extractive summary"
            mock_extractive_instance.summarize.assert_called_once_with(test_text, "document")
    
    @patch('transformers.pipeline')
    def test_summarize_fallback_on_empty_response(self, mock_pipeline):
        """Test fallback to extractive summarization on empty BART response"""
        # Setup mocks to simulate empty response
        mock_model = MagicMock()
        mock_model.return_value = []  # Empty response
        mock_pipeline.return_value = mock_model
        
        with patch('app.services.summarizer.ExtractiveSummarizer') as mock_extractive:
            mock_extractive_instance = MagicMock()
            mock_extractive_instance.summarize.return_value = "Fallback extractive summary"
            mock_extractive.return_value = mock_extractive_instance
            
            summarizer = BARTSummarizer()
            test_text = "Test document content for summarization."
            
            result = summarizer.summarize(test_text)
            
            assert result == "Fallback extractive summary"
            mock_extractive_instance.summarize.assert_called_once_with(test_text, "document")


class TestBARTSummarizerFactory:
    """Test cases for BART in get_summarizer factory function"""
    
    @patch('transformers.pipeline')
    def test_get_bart_summarizer(self, mock_pipeline):
        """Test factory returns BARTSummarizer for 'bart' provider"""
        mock_pipeline.return_value = MagicMock()
        
        summarizer = get_summarizer("bart")
        assert isinstance(summarizer, BARTSummarizer)


class TestBARTSummarizerIntegration:
    """Integration test cases for BART summarizer"""
    
    @patch('transformers.pipeline')
    def test_adaptive_summary_length(self, mock_pipeline):
        """Test that summary length adapts to input length"""
        mock_model = MagicMock()
        mock_model.return_value = [{'summary_text': 'Adaptive summary'}]
        mock_pipeline.return_value = mock_model
        
        summarizer = BARTSummarizer()
        
        # Test short text
        short_text = "Short document."
        summarizer.summarize(short_text)
        
        short_call_args = mock_model.call_args[1]
        short_max_length = short_call_args['max_length']
        
        mock_model.reset_mock()
        
        # Test longer text
        long_text = "This is a much longer document with more content. " * 10
        summarizer.summarize(long_text)
        
        long_call_args = mock_model.call_args[1]
        long_max_length = long_call_args['max_length']
        
        # Longer text should get longer summary allowance
        assert long_max_length >= short_max_length
