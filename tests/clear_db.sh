#!/bin/bash
# Clean test data from WealthTech Smart Search API database
# Usage: bash clean_test_data.sh

echo "🧹 Cleaning WealthTech Smart Search Test Data"
echo "⚠️  This will remove ALL documents and notes (keeping clients)"
echo ""

read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled"
    exit 1
fi

echo "🗑️  Cleaning database..."

# Clean documents and notes but keep clients
docker compose exec db psql -U user -d wealthtech_db -c "
DELETE FROM meeting_notes;
DELETE FROM documents;
" > /dev/null

echo "✅ Database cleaned successfully!"
echo "📊 Remaining data:"

# Show remaining counts
docker compose exec db psql -U user -d wealthtech_db -c "
SELECT 
    'clients' as table_name,
    COUNT(*) as count
FROM clients
UNION ALL
SELECT 
    'documents' as table_name,
    COUNT(*) as count
FROM documents
UNION ALL
SELECT 
    'meeting_notes' as table_name,
    COUNT(*) as count
FROM meeting_notes;
"

echo ""
echo "🎉 Cleanup complete! Database is ready for fresh testing."
echo ""
echo "💡 Usage:"
echo "  1. bash clean_test_data.sh     # Clean database"
echo "  2. bash load_test_data_simple.sh  # Load fresh test data"
echo "  3. Test your searches without duplicates"
