#!/bin/bash
# Load all test documents and notes into WealthTech Smart Search API
# Usage: bash load_test_data.sh [tenant_id]

TENANT_ID=${1:-1}
BASE_URL="http://localhost:8000"

echo "🏦 Loading WealthTech Smart Search Test Data"
echo "Using tenant_id: $TENANT_ID"
echo "API URL: $BASE_URL"
echo "=================================================="

# Clean existing data for this tenant first
echo "🧹 Cleaning existing data for tenant_id=$TENANT_ID..."
docker compose exec db psql -U user -d wealthtech_db -c "
DELETE FROM meeting_notes WHERE tenant_id = $TENANT_ID;
DELETE FROM documents WHERE tenant_id = $TENANT_ID;
" > /dev/null
echo "✅ Cleanup completed"

# Restart API with correct tenant_id if not using default
if [ "$TENANT_ID" != "1" ]; then
    echo "🔄 Restarting API with tenant_id=$TENANT_ID..."
    cd ..
    # Stop and start with new environment variable
    docker compose stop api
    TENANT_ID=$TENANT_ID docker compose up -d api
    echo "⏳ Waiting for API to be ready..."
    sleep 8
    cd tests
    
    # Create client for non-default tenant
    echo "👤 Creating test client for tenant_id=$TENANT_ID..."
    docker compose exec db psql -U user -d wealthtech_db -c "
    INSERT INTO tenants (id, name) VALUES ($TENANT_ID, 'Test Tenant $TENANT_ID') ON CONFLICT (id) DO NOTHING;
    INSERT INTO clients (tenant_id, first_name, last_name, email) 
    VALUES ($TENANT_ID, 'Test', 'Client', 'test@example.com') 
    ON CONFLICT (tenant_id, email) DO NOTHING;
    " > /dev/null
fi

# Always get the actual client ID for this tenant
CLIENT_ID=$(docker compose exec db psql -U user -d wealthtech_db -t -c "SELECT id FROM clients WHERE tenant_id = $TENANT_ID LIMIT 1;" | tr -d ' ')

# Test API connectivity
echo "🏥 Testing API connectivity..."
if ! curl -s "$BASE_URL/health" > /dev/null; then
    echo "❌ API not responding. Make sure Docker is running:"
    echo "   docker compose up -d"
    exit 1
fi

echo "📄 Loading test documents..."

# Document 1: Portfolio Report
echo "  - Portfolio Performance Report"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/documents" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Q3 2024 Portfolio Performance Report\", \"content\": \"$(cat data/doc_portfolio_report.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

# Document 2: Bank Statement  
echo "  - Bank Statement"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/documents" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Monthly Bank Statement - October 2024\", \"content\": \"$(cat data/doc_bank_statement.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

# Document 3: Tax Filing
echo "  - Tax Return"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/documents" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"2023 Tax Return\", \"content\": \"$(cat data/doc_tax_filing.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

# Document 4: Investment Analysis
echo "  - Investment Analysis"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/documents" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Equity Investment Analysis\", \"content\": \"$(cat data/doc_investment_analysis.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

echo "📝 Loading test notes..."

# Note 1: Client Meeting
echo "  - Client Meeting Notes"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/notes" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"$(cat data/note_client_meeting.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

# Note 2: Investment Committee
echo "  - Investment Committee Minutes"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/notes" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"$(cat data/note_investment_committee.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

# Note 3: Earnings Call
echo "  - Earnings Call Transcript"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/notes" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"$(cat data/note_earnings_call.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

# Note 4: Email Chain
echo "  - Email Chain"
curl -s -X POST "$BASE_URL/clients/$CLIENT_ID/notes" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"$(cat data/note_email_chain.txt | sed 's/"/\\"/g' | tr '\n' ' ')\"}" > /dev/null

echo ""
echo "✅ Test data loaded successfully!"

# Verify data was loaded
echo "🔍 Verifying data upload..."
RESULT_COUNT=$(curl -s "$BASE_URL/search?q=portfolio" | jq '.results | length')
echo "   Found $RESULT_COUNT results for 'portfolio'"

if [ "$RESULT_COUNT" -gt "0" ]; then
    echo "✅ Data verification successful!"
else
    echo "⚠️  No results found. Data may not have uploaded correctly."
fi

echo ""
echo "🔍 Try these search examples:"
echo "  curl \"$BASE_URL/search?q=7.2%25%20return\""
echo "  curl \"$BASE_URL/search?q=Thompson%20Family\""
echo "  curl \"$BASE_URL/search?q=portfolio%20diversification\""
echo "  curl \"$BASE_URL/search?q=investment%20committee&type=note\""
echo "  curl \"$BASE_URL/search?q=tax%20deduction&type=document\""
