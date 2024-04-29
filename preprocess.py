# Import necessary libraries
import re

# Function to preprocess text
def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert text to lowercase
    text = text.lower()
    # Tokenization (split text into words)
    tokens = text.split()
    # Remove stopwords
    stopwords = set(["the", "is", "and", "in", "a", "to", "of", "for", "with", "on", "by", "it", "as"])
    tokens = [token for token in tokens if token not in stopwords]
    # Join tokens back into a single string
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

# Load your article
with open('C:\Users\Yaman\Desktop\Depression', 'r') as file:
    article_text = file.read()

# Preprocess the article
preprocessed_article = preprocess_text(article_text)

# Print the preprocessed article
print(preprocessed_article)
