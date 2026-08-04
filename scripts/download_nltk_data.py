"""Download the optional corpora used for full lemmatization and stopwords."""

import nltk


for package in ("stopwords", "wordnet", "omw-1.4"):
    print(f"Downloading {package}...")
    nltk.download(package, quiet=False)

print("NLTK data is ready.")
