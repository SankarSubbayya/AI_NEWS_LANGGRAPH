#!/bin/bash

# Build MkDocs documentation
echo "🔨 Building MkDocs documentation..."
echo ""

.venv/bin/python -m mkdocs build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Documentation built successfully!"
    echo ""
    echo "📁 Output directory: site/"
    echo ""
    echo "🌐 To deploy:"
    echo "   1. Upload 'site/' directory to your web server"
    echo "   2. Or use: mkdocs gh-deploy (for GitHub Pages)"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check the errors above."
    echo ""
fi

