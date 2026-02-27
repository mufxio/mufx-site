#!/usr/bin/env python3
"""
muFX Publication Integrity Verifier
Verifies that article content matches the published SHA-256 hash.

Usage:
  python3 verify.py signal-20260227.html
  python3 verify.py --all
"""

import re, hashlib, sys, os, glob

def verify(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if not match:
        return filename, None, None, "No <article> tag found"

    text = re.sub(r'<[^>]+>', '', match.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    computed = hashlib.sha256(text.encode('utf-8')).hexdigest()

    published = re.search(r'data-hash="([a-f0-9]{64})"', content)
    published = published.group(1) if published else None

    if not published:
        return filename, None, computed, "No published hash found"

    status = "VERIFIED" if computed == published else "MISMATCH"
    return filename, published, computed, status

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        files = sorted(glob.glob("signal-*.html") + glob.glob("weekly-*.html") + glob.glob("q2-*.html"))
    elif len(sys.argv) > 1:
        files = [sys.argv[1]]
    else:
        print("Usage: python3 verify.py <filename.html>")
        print("       python3 verify.py --all")
        sys.exit(1)

    for f in files:
        if not os.path.exists(f):
            print(f"  File not found: {f}")
            continue
        name, pub, comp, status = verify(f)
        icon = "\u2705" if status == "VERIFIED" else "\u274c"
        print(f"  {icon} {name}: {status}")
        if pub and comp and status == "MISMATCH":
            print(f"     Published: {pub}")
            print(f"     Computed:  {comp}")
