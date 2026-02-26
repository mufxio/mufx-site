#!/bin/bash
# ═══════════════════════════════════════════════════════════
# muFX — Article Hash Generator
# Run before git commit to inject SHA-256 hashes into articles.
# 
# Usage:
#   ./tools/hash-articles.sh           # Hash all signal/thematic/outlook pages
#   ./tools/hash-articles.sh --dry-run # Show hashes without modifying files
#
# How it works:
#   1. Finds all article HTML files (signal-*, thematic-*, q*-outlook, flash-*)
#   2. Extracts the <article> body text (strips HTML tags)
#   3. Generates SHA-256 hash of the text content
#   4. Injects hash into the data-hash attribute on the <article> tag
#   5. The hash is displayed in the article header via CSS + a small JS snippet
#
# The git commit SHA + timestamp becomes the public proof.
# Anyone can verify: clone repo → run this script → compare hashes.
# ═══════════════════════════════════════════════════════════

set -e

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Find article files
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$(dirname "$SCRIPT_DIR")"

ARTICLE_FILES=$(find "$SITE_DIR" -maxdepth 1 -name "signal-*.html" -o -name "thematic-*.html" -o -name "q*-outlook.html" -o -name "flash-*.html" | sort)

if [[ -z "$ARTICLE_FILES" ]]; then
    echo "No article files found."
    exit 0
fi

echo "═══════════════════════════════════════════════════════"
echo "  muFX Hash Generator"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════"
echo ""

CHANGED=0

for FILE in $ARTICLE_FILES; do
    FILENAME=$(basename "$FILE")
    
    # Extract text content from <article> tags, strip all HTML
    # This is the canonical content that gets hashed
    BODY_TEXT=$(python3 -c "
import re, sys
with open('$FILE', 'r') as f:
    html = f.read()
# Extract article body
match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if not match:
    # Try without article tags — use body
    match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
if match:
    text = match.group(1)
    # Remove script, style, svg blocks
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', text, flags=re.DOTALL)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    print(text)
else:
    print('')
" 2>/dev/null)
    
    if [[ -z "$BODY_TEXT" ]]; then
        echo "  ⚠  $FILENAME — no article content found, skipping"
        continue
    fi
    
    # Generate SHA-256
    HASH=$(echo -n "$BODY_TEXT" | shasum -a 256 | cut -d' ' -f1)
    SHORT_HASH="${HASH:0:12}"
    
    echo "  $FILENAME"
    echo "    SHA-256: $HASH"
    echo "    Short:   $SHORT_HASH"
    
    if [[ "$DRY_RUN" == true ]]; then
        echo "    [dry-run — not modified]"
        echo ""
        continue
    fi
    
    # Inject hash into article tag as data attribute
    # Replace data-hash="..." if it exists, or add it to <article
    python3 -c "
import re
with open('$FILE', 'r') as f:
    html = f.read()

# Update or add data-hash on <article> tag
if 'data-hash=' in html:
    html = re.sub(r'data-hash=\"[^\"]*\"', 'data-hash=\"$HASH\"', html)
else:
    html = html.replace('<article class=\"article-body\">', '<article class=\"article-body\" data-hash=\"$HASH\">')
    html = html.replace('<article>', '<article data-hash=\"$HASH\">')

# Also remove any old integrity-box footer section (the big explanation block)
# We're replacing it with the header hash
html = re.sub(r'<div style=\"max-width:760px;margin:40px auto.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
# Also remove class-based integrity box
html = re.sub(r'<div[^>]*class=\"integrity-box\".*?</div>\s*</div>', '', html, flags=re.DOTALL)

with open('$FILE', 'w') as f:
    f.write(html)
" 2>/dev/null
    
    CHANGED=$((CHANGED + 1))
    echo "    ✅ Hash injected"
    echo ""
done

echo "═══════════════════════════════════════════════════════"
echo "  $CHANGED file(s) updated"
if [[ "$DRY_RUN" == true ]]; then
    echo "  (dry run — no files modified)"
fi
echo "═══════════════════════════════════════════════════════"
