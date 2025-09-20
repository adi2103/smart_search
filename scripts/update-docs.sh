#!/bin/bash
# Update API documentation from running server

set -e

echo "🔄 Updating API documentation..."

# Check if API is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ API not running. Start with: docker compose up -d"
    exit 1
fi

# Create docs directory if it doesn't exist
mkdir -p docs

# Download OpenAPI schema
echo "📥 Downloading OpenAPI schema..."
curl -s http://localhost:8000/openapi.json > docs/openapi.json

# Generate markdown documentation
echo "📝 Generating markdown documentation..."
python3 -c "
import json

# Read OpenAPI schema
with open('docs/openapi.json', 'r') as f:
    schema = json.load(f)

# Generate markdown
md = f'''# {schema['info']['title']} API Documentation

**Version:** {schema['info']['version']}  
**Description:** {schema['info']['description']}

## Base URL
\`http://localhost:8000\`

## Endpoints

'''

for path, methods in schema['paths'].items():
    for method, details in methods.items():
        md += f'### {method.upper()} {path}\n\n'
        md += f'**Summary:** {details.get(\"summary\", \"N/A\")}\n\n'
        
        if 'parameters' in details:
            md += '**Parameters:**\n'
            for param in details['parameters']:
                required = ' (required)' if param.get('required') else ''
                md += f'- \`{param[\"name\"]}\` ({param[\"in\"]}){required}: {param.get(\"description\", \"N/A\")}\n'
            md += '\n'
        
        if 'requestBody' in details:
            md += '**Request Body:**\n'
            content = details['requestBody']['content']
            if 'application/json' in content:
                md += f'Content-Type: application/json\n\n'
        
        md += '**Responses:**\n'
        for code, response in details['responses'].items():
            md += f'- \`{code}\`: {response.get(\"description\", \"N/A\")}\n'
        md += '\n---\n\n'

# Write markdown file
with open('docs/API.md', 'w') as f:
    f.write(md)
"

echo "✅ Documentation updated:"
echo "   - docs/openapi.json"
echo "   - docs/API.md"
echo ""
echo "💡 To commit changes:"
echo "   git add docs/ && git commit -m 'docs: update API documentation'"
