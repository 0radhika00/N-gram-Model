from tokenizer import Tokenizer


N = int(input("Enter N for N-gram: "))
file_path = input("Enter filepath: ")

# Instantiate Tokenizer
cls = Tokenizer()

# Process the text file
token = cls.text_file(file_path)
token = cls.identifiers_tokenizer(token)
token = cls.sentence_tokenizer(token)
token = cls.split_sentences_into_words(token)


n_grams = []
for sentence in token:
    if len(sentence) < N:
        continue
    sentence_with_s = ['<s>'] + sentence +['</s>']
    for i in range(len(sentence_with_s) - N + 1):
        n_grams.append(tuple(sentence_with_s[i:i+N]))

print(n_grams)
