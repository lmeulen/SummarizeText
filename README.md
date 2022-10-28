# SummarizeText

A Python class to generate a summary for a given text or text file.

Usage:
```
summ =  Summarizer()

# Initialize manualy
summ.set_language('dutch')
summ.set_summary_length(3)

# Or detect language to use
summ.detect_language(text)

# Summarize a text
print(summ.summarize("..."))
# Summarize the contents of a text file
print(summarize_file('longtext.txt', split_at=250))
```
