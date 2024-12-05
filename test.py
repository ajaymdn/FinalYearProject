import nltk

nltk.download()

from nltk.tokenize import sent_tokenize

text = "Hello, Mr. Smith. How are you today? The weather is great, and city is awesome. The sky is pinkish-blue. You shouldn't eat cardboard"

print(sent_tokenize(text))