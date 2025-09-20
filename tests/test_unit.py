"""
Unit tests for WealthTech Smart Search API
Tests core business logic, edge cases, and regression prevention
"""
import pytest
from unittest.mock import patch, MagicMock
import os

from src.utils.summarizer import get_summarizer, ExtractiveSummarizer, GeminiSummarizer, BARTSummarizer
from src.utils.search import reciprocal_rank_fusion
from src.utils.embedder import get_embedder, LocalEmbedder
from src.utils.validation import validate_client_exists, validate_content_length, validate_search_query
from src.config import settings
from fastapi import HTTPException


class TestSummarizerService:
    """Test summarizer service for regression prevention"""

    def test_get_summarizer_factory(self):
        """Test factory returns correct types"""
        assert isinstance(get_summarizer("extractive"), ExtractiveSummarizer)

        if os.getenv("GEMINI_API_KEY"):
            assert isinstance(get_summarizer("gemini"), GeminiSummarizer)

        assert isinstance(get_summarizer("bart"), BARTSummarizer)

    def test_get_summarizer_invalid_provider(self):
        """Test factory handles invalid providers"""
        with pytest.raises(ValueError, match="Unknown summarizer provider"):
            get_summarizer("invalid_provider")

    def test_extractive_summarizer_edge_cases(self):
        """Test extractive summarizer edge cases"""
        summarizer = ExtractiveSummarizer()

        # Empty content
        result = summarizer.summarize("", content_type="document")
        assert result == ""

        # Very short content
        short_text = "Short."
        result = summarizer.summarize(short_text, content_type="document")
        assert result == short_text

        # Single sentence
        single = "This is a single sentence."
        result = summarizer.summarize(single, content_type="document")
        assert result == single

    @patch('src.utils_ai.summarizer.ExtractiveSummarizer')
    def test_gemini_fallback_mechanism(self, mock_extractive):
        """Test Gemini falls back to extractive on failures"""
        if not os.getenv("GEMINI_API_KEY"):
            pytest.skip("GEMINI_API_KEY not available")

        mock_extractive_instance = MagicMock()
        mock_extractive_instance.summarize.return_value = "Fallback summary"
        mock_extractive.return_value = mock_extractive_instance

        summarizer = GeminiSummarizer()

        with patch.object(summarizer.model, 'generate_content', side_effect=Exception("API Error")):
            result = summarizer.summarize("Test content", content_type="document")
            assert result == "Fallback summary"
            mock_extractive_instance.summarize.assert_called_once()


class TestSearchService:
    """Test RRF search algorithm for regression prevention"""

    def test_rrf_basic_functionality(self):
        """Test basic RRF functionality"""
        fts_results = [(1, 0.9), (2, 0.8), (3, 0.7)]
        vector_results = [(3, 0.9), (1, 0.8), (4, 0.7)]

        result = reciprocal_rank_fusion(fts_results, vector_results)

        assert isinstance(result, list)
        assert len(result) == 4
        assert all(isinstance(item, tuple) and len(item) == 2 for item in result)

        scores = [score for _, score in result]
        assert scores == sorted(scores, reverse=True)

    def test_rrf_empty_lists(self):
        """Test RRF with empty input lists"""
        result = reciprocal_rank_fusion([], [])
        assert result == []

        result = reciprocal_rank_fusion([(1, 0.9)], [])
        assert len(result) == 1

        result = reciprocal_rank_fusion([], [(1, 0.9)])
        assert len(result) == 1

    def test_rrf_duplicate_ids(self):
        """Test RRF handles duplicate IDs correctly"""
        fts_results = [(1, 0.9), (2, 0.8)]
        vector_results = [(1, 0.8), (2, 0.7)]

        result = reciprocal_rank_fusion(fts_results, vector_results)

        assert len(result) == 2
        assert result[0][0] == 1  # ID 1 should have higher combined score

    def test_rrf_different_k_values(self):
        """Test RRF with different k parameters"""
        fts_results = [(1, 0.9), (2, 0.8)]
        vector_results = [(2, 0.9), (1, 0.8)]

        result_k60 = reciprocal_rank_fusion(fts_results, vector_results, k=60)
        result_k10 = reciprocal_rank_fusion(fts_results, vector_results, k=10)

        assert result_k60[0][1] != result_k10[0][1]


class TestValidationService:
    """Test validation functions for security and regression prevention"""

    def test_validate_content_length_valid(self):
        """Test content length validation with valid content"""
        validate_content_length("Short content")
        validate_content_length("A" * 1000)
        validate_content_length("A" * 50000)  # At limit

    def test_validate_content_length_invalid(self):
        """Test content length validation with invalid content"""
        with pytest.raises(HTTPException) as exc_info:
            validate_content_length("A" * 50001)

        assert exc_info.value.status_code == 400
        assert "Content too long" in str(exc_info.value.detail)

    def test_validate_content_length_custom_limit(self):
        """Test content length validation with custom limit"""
        with pytest.raises(HTTPException):
            validate_content_length("A" * 101, max_length=100)

    def test_validate_search_query_valid(self):
        """Test search query validation with valid queries"""
        validate_search_query("investment portfolio")
        validate_search_query("a")
        validate_search_query("A" * 1000)

    def test_validate_search_query_invalid(self):
        """Test search query validation with invalid queries"""
        with pytest.raises(HTTPException) as exc_info:
            validate_search_query("")
        assert exc_info.value.status_code == 400
        assert "cannot be empty" in str(exc_info.value.detail)

        with pytest.raises(HTTPException):
            validate_search_query("   ")

        with pytest.raises(HTTPException) as exc_info:
            validate_search_query("A" * 1001)
        assert exc_info.value.status_code == 400
        assert "too long" in str(exc_info.value.detail)


class TestEmbedderService:
    """Test embedder service edge cases"""

    def test_get_embedder_factory(self):
        """Test embedder factory"""
        embedder = get_embedder("local")
        assert isinstance(embedder, LocalEmbedder)

    def test_get_embedder_invalid_provider(self):
        """Test embedder factory with invalid provider"""
        with pytest.raises(ValueError, match="Unknown embedder provider"):
            get_embedder("invalid_provider")

    def test_local_embedder_consistency(self):
        """Test local embedder produces consistent results"""
        embedder = LocalEmbedder()

        text = "Test document for embedding"
        result1 = embedder.encode(text)
        result2 = embedder.encode(text)

        assert (result1 == result2).all()
        assert len(result1) == 384


class TestConfiguration:
    """Test configuration settings"""

    def test_settings_defaults(self):
        """Test default configuration values"""
        assert settings.tenant_id == 1
        assert settings.embeddings_provider == "local"
        assert settings.summarizer == "gemini"
