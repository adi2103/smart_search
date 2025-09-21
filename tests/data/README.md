# Test Data Files

Realistic financial documents and meeting notes for testing the WealthTech Smart Search API.

## Files

**Documents:**
- `doc_portfolio_report.txt` - Q3 2024 Portfolio Performance (7.2% return)
- `doc_bank_statement.txt` - Monthly Bank Statement  
- `doc_tax_filing.txt` - Individual Tax Return (Form 1040)
- `doc_investment_analysis.txt` - Equity Investment Analysis

**Notes:**
- `note_client_meeting.txt` - Thompson Family Client Meeting
- `note_investment_committee.txt` - Investment Committee Minutes
- `note_earnings_call.txt` - TechCorp Q3 Earnings Call
- `note_email_chain.txt` - Portfolio Rebalancing Email Thread

## Usage

```bash
# Load all test data
bash run_e2e_tests.sh 2

# Clean database before testing
bash clear_db.sh 2
```

## Key Search Terms

- **"7.2% return"** → Portfolio report (exact match)
- **"Thompson Family"** → Client meeting (exact match)  
- **"portfolio diversification"** → Multiple results (semantic search)
