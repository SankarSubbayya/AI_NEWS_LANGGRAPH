#!/bin/bash

# Serve MkDocs documentation locally
echo "🚀 Starting MkDocs documentation server..."
echo ""
echo "📖 Documentation will be available at:"
echo "   http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

.venv/bin/python -m mkdocs serve

