
#!/bin/bash
# Code formatting script for Sierra Agent

echo 🔧 Running code formatters...

echo 📦 Organizing imports with isort...
isort src/ --profile black

echo 🖤 Formatting code with black...
black src/ --line-length 121

echo 🔍 Checking code style with flake8...
flake8 src/

echo 🧹 Removing trailing whitespace...
find . -name "*.py" -type f -exec sed -i '' 's/[[:space:]]*$//' {} +

echo ✅ Code formatting complete!

