import pytest
import requests
import time
import os
from typing import Dict, List

BASE_URL = "http://localhost:8000"

class TestWealthTechAPI:
    """Integration tests for WealthTech Smart Search API"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """Test API availability"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        return BASE_URL
    
    def test_client_validation(self, api_client):
        """Test client validation returns 404 for invalid client"""
        response = requests.post(
            f"{api_client}/clients/999/documents",
            json={"title": "Test", "content": "Test content"}
        )
        assert response.status_code == 404
        assert "Client 999 not found" in response.json()["detail"]
    
    def test_input_validation(self, api_client):
        """Test input validation returns 422 for invalid data"""
        # Empty content
        response = requests.post(
            f"{api_client}/clients/1/documents",
            json={"title": "Test", "content": ""}
        )
        assert response.status_code == 422
        
        # Empty search query
        response = requests.get(f"{api_client}/search", params={"q": ""})
        assert response.status_code == 400
        assert "Search query cannot be empty" in response.json()["detail"]
        
        # Invalid search type
        response = requests.get(f"{api_client}/search", params={"q": "test", "type": "invalid"})
        assert response.status_code == 400
        assert "Type must be 'document' or 'note'" in response.json()["detail"]
    
    def test_extractive_summarization(self, api_client):
        """Test extractive summarization (default mode)"""
        # Set extractive mode
        os.environ["SUMMARIZER"] = "extractive"
        
        doc_data = {
            "title": "Extractive Test Document",
            "content": "This is a comprehensive financial analysis document. It examines investment strategies and portfolio management. The document provides detailed recommendations for asset allocation. Risk management is a key component of the analysis. The report concludes with actionable insights for financial advisors."
        }
        
        response = requests.post(f"{api_client}/clients/1/documents", json=doc_data)
        assert response.status_code == 201
        
        result = response.json()
        assert result["title"] == doc_data["title"]
        assert result["content"] == doc_data["content"]
        assert len(result["summary"]) <= len(doc_data["content"])
        assert "financial" in result["summary"].lower()
    
    def test_gemini_summarization(self, api_client):
        """Test Gemini API summarization if available"""
        if not os.getenv("GEMINI_API_KEY"):
            pytest.skip("GEMINI_API_KEY not available")
        
        os.environ["SUMMARIZER"] = "gemini"
        
        doc_data = {
            "title": "Gemini Test Document", 
            "content": "This comprehensive investment portfolio analysis examines client asset allocation strategies for 2024. The portfolio demonstrates strong performance with technology holdings representing 25% of total assets, healthcare at 20%, and financial services at 15%. Performance metrics show a 12% annual return over the past three years, outperforming the benchmark S&P 500 by 3.2%. Risk assessment reveals a beta coefficient of 0.85, indicating lower volatility than the overall market. Recommendations include rebalancing to maintain target allocations and considering ESG-focused investments."
        }
        
        response = requests.post(f"{api_client}/clients/1/documents", json=doc_data)
        assert response.status_code == 201
        
        result = response.json()
        assert result["title"] == doc_data["title"]
        assert len(result["summary"]) <= len(doc_data["content"])
        # Gemini should provide more concise, advisor-focused summaries
        assert any(keyword in result["summary"].lower() for keyword in ["return", "performance", "portfolio"])
    
    def test_bart_summarization(self, api_client):
        """Test BART local summarization"""
        os.environ["SUMMARIZER"] = "bart"
        
        doc_data = {
            "title": "BART Test Document",
            "content": "This advanced portfolio risk management guide provides comprehensive strategies for institutional investors. The document covers various risk assessment methodologies including Value at Risk (VaR), stress testing, and scenario analysis. Modern portfolio theory suggests diversification across asset classes to minimize risk while maximizing returns. Quantitative risk models help identify potential portfolio vulnerabilities and concentration risks. Regular monitoring of correlation patterns between assets is essential for effective risk management."
        }
        
        response = requests.post(f"{api_client}/clients/1/documents", json=doc_data)
        assert response.status_code == 201
        
        result = response.json()
        assert result["title"] == doc_data["title"]
        assert len(result["summary"]) <= len(doc_data["content"])
        # BART should provide abstractive summaries
        assert any(keyword in result["summary"].lower() for keyword in ["risk", "portfolio", "management"])
    
    def test_note_creation_all_modes(self, api_client):
        """Test note creation with all summarization modes"""
        note_content = "Client meeting focused on retirement planning goals. Client is 55 years old and wants to retire by 65. Currently has $750K in retirement accounts and contributes $25K annually. Discussed asset allocation strategy: 60% stocks, 35% bonds, 5% cash. Client comfortable with moderate risk tolerance. Next steps: review Social Security projections and update beneficiary information."
        
        note_ids = []
        
        for mode in ["extractive", "gemini", "bart"]:
            if mode == "gemini" and not os.getenv("GEMINI_API_KEY"):
                continue
                
            os.environ["SUMMARIZER"] = mode
            
            response = requests.post(
                f"{api_client}/clients/1/notes",
                json={"content": note_content}
            )
            assert response.status_code == 201
            
            result = response.json()
            assert result["content"] == note_content
            assert len(result["summary"]) <= len(note_content)
            assert "retirement" in result["summary"].lower()
            
            note_ids.append(result["id"])
        
        return note_ids
    
    def test_hybrid_search_functionality(self, api_client):
        """Test hybrid search with FTS and vector search"""
        # Reset to extractive for consistent testing
        os.environ["SUMMARIZER"] = "extractive"
        
        # Search for investment-related content
        response = requests.get(f"{api_client}/search", params={"q": "investment portfolio"})
        assert response.status_code == 200
        
        results = response.json()
        assert results["query"] == "investment portfolio"
        assert len(results["results"]) > 0
        
        # Verify results have required fields
        for result in results["results"]:
            assert "id" in result
            assert "type" in result
            assert result["type"] in ["document", "note"]
            assert "score" in result
            assert "summary" in result
            assert "content" in result
            
        # Verify RRF ranking produces reasonable scores
        scores = [r["score"] for r in results["results"]]
        assert all(score > 0 for score in scores), "All scores should be positive"
        assert len(set(scores)) > 1 or len(scores) == 1, "Should have varied scores or single result"
        
        return results["results"]
    
    def test_search_type_filtering(self, api_client):
        """Test search filtering by document/note type"""
        # Search documents only
        response = requests.get(f"{api_client}/search", params={"q": "portfolio", "type": "document"})
        assert response.status_code == 200
        
        doc_results = response.json()["results"]
        assert all(r["type"] == "document" for r in doc_results)
        
        # Search notes only
        response = requests.get(f"{api_client}/search", params={"q": "client", "type": "note"})
        assert response.status_code == 200
        
        note_results = response.json()["results"]
        assert all(r["type"] == "note" for r in note_results)
        
        # Search both types
        response = requests.get(f"{api_client}/search", params={"q": "retirement"})
        assert response.status_code == 200
        
        all_results = response.json()["results"]
        types = {r["type"] for r in all_results}
        assert len(types) >= 1  # Should have at least one type
    
    def test_summarization_quality_comparison(self, api_client):
        """Compare summarization quality across all 3 phases"""
        test_content = "This comprehensive financial planning document analyzes retirement strategies for high-net-worth individuals. The analysis covers tax-efficient withdrawal strategies, estate planning considerations, and legacy wealth transfer mechanisms. Key recommendations include maximizing Roth IRA conversions during low-income years, implementing charitable giving strategies for tax benefits, and establishing family limited partnerships for wealth transfer. The document also addresses healthcare cost planning and long-term care insurance considerations. Risk management strategies include diversification across asset classes and geographic regions."
        
        summaries = {}
        
        for mode in ["extractive", "gemini", "bart"]:
            if mode == "gemini" and not os.getenv("GEMINI_API_KEY"):
                continue
                
            os.environ["SUMMARIZER"] = mode
            
            response = requests.post(
                f"{api_client}/clients/1/documents",
                json={"title": f"{mode.title()} Quality Test", "content": test_content}
            )
            assert response.status_code == 201
            
            result = response.json()
            summaries[mode] = {
                "summary": result["summary"],
                "compression": len(result["summary"]) / len(test_content),
                "id": result["id"]
            }
        
        # Verify all summaries are shorter than original
        for mode, data in summaries.items():
            assert data["compression"] < 1.0, f"{mode} summary should be shorter than original"
            assert "retirement" in data["summary"].lower() or "financial" in data["summary"].lower()
        
        return summaries
    
    def test_error_scenarios_comprehensive(self, api_client):
        """Test all error scenarios return proper HTTP codes"""
        # 404 - Invalid client
        response = requests.post(f"{api_client}/clients/999/documents", json={"title": "Test", "content": "Test"})
        assert response.status_code == 404
        
        # 422 - Invalid input (empty content)
        response = requests.post(f"{api_client}/clients/1/documents", json={"title": "Test", "content": ""})
        assert response.status_code == 422
        
        # 400 - Invalid search parameters
        response = requests.get(f"{api_client}/search", params={"q": ""})
        assert response.status_code == 400
        
        response = requests.get(f"{api_client}/search", params={"q": "test", "type": "invalid"})
        assert response.status_code == 400
        
        # 422 - Missing required fields
        response = requests.post(f"{api_client}/clients/1/documents", json={"title": "Test"})
        assert response.status_code == 422
    
    def test_end_to_end_workflow(self, api_client):
        """Test complete workflow: create documents/notes → search → verify results"""
        os.environ["SUMMARIZER"] = "extractive"
        
        # Create test document
        doc_response = requests.post(
            f"{api_client}/clients/1/documents",
            json={
                "title": "E2E Test Investment Strategy",
                "content": "This document outlines a comprehensive investment strategy for retirement planning. The strategy focuses on diversified portfolio allocation with emphasis on long-term growth and risk management."
            }
        )
        assert doc_response.status_code == 201
        doc_id = doc_response.json()["id"]
        
        # Create test note
        note_response = requests.post(
            f"{api_client}/clients/1/notes",
            json={
                "content": "Client meeting to discuss investment strategy implementation. Client approved the diversified portfolio approach and agreed to monthly review meetings."
            }
        )
        assert note_response.status_code == 201
        note_id = note_response.json()["id"]
        
        # Search for created content
        search_response = requests.get(f"{api_client}/search", params={"q": "investment strategy"})
        assert search_response.status_code == 200
        
        results = search_response.json()["results"]
        result_ids = [r["id"] for r in results]
        
        # Verify our created content appears in search results
        assert doc_id in result_ids or note_id in result_ids
        
        # Verify search results contain summaries
        for result in results:
            if result["id"] in [doc_id, note_id]:
                assert len(result["summary"]) > 0
                assert len(result["summary"]) <= len(result["content"])  # Summary can be same length for short content
                break
        else:
            pytest.fail("Created content not found in search results")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
