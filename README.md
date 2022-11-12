# SummarizeText

A Python class to generate a summary for a given text or text file.

Usage:
```
summ =  Summarizer(language='dutch', summary_length=3)
# or (defaults to dutch, summary length of 3:
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
For more information, see:
* [Summarize a text in Python](https://towardsdatascience.com/summarize-a-text-with-python-b3b260c60e72?sk=9d66f3557b7f41b4e7eae1688c5b8120) on Medium
