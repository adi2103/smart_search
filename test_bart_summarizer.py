import pytest
from app.services.summarizer import BARTSummarizer, get_summarizer

class TestBARTSummarizer:
    
    def test_bart_initialization(self):
        """Test BART summarizer initializes correctly"""
        summarizer = BARTSummarizer()
        assert summarizer.available is True
        assert hasattr(summarizer, 'summarizer')
    
    def test_bart_summarization_real(self):
        """Test actual BART summarization functionality"""
        summarizer = BARTSummarizer()
        
        test_text = "This investment portfolio analysis examines asset allocation strategies and risk management approaches for financial advisory clients. The comprehensive report evaluates various investment vehicles and provides recommendations for portfolio optimization."
        
        result = summarizer.summarize(test_text, content_type="document")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert len(result) <= len(test_text)  # Should be same or shorter
    
    def test_get_summarizer_factory(self):
        """Test summarizer factory returns correct type"""
        bart_summarizer = get_summarizer("bart")
        assert isinstance(bart_summarizer, BARTSummarizer)
        
        extractive_summarizer = get_summarizer("extractive")
        assert extractive_summarizer.__class__.__name__ == "ExtractiveSummarizer"

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
