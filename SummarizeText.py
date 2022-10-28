import os
from nltk import tokenize, word_tokenize
from nltk.corpus import stopwords

class Summarizer:
    """
    A class used to summarize texts.

    This class can summarize texts from strings, list of string or a file.
    It can use language specific stop word lists containg words to ignore during the 
    determination of the most important subjects of the text. The language and stop word lists
    can be set seperately or can be detected automatically from a text.

    Attributes
    ----------
    stop_words : set
        a set of stopwords. These are ignored when searching for the most used
        words in the text
    language : str
        the current selected language. The stop words set is language specific
    summary_legth : int
        the default number of sentences to use for the summary.

    """
    
    stop_words:set = {}
    language:str = None
    summary_length:int = 0
    
    def __init__(self, language:str='dutch', summary_length:int=3):
        """
        :param str language: The language to use, defaults to 'dutch'
        :paran int summary_length: The default length for the summary to generate, defaults to 3
        """
        self.set_language(language)
        self.set_summary_length(summary_length)
    
    def set_language(self, lang:str) -> None:
        """
        Sets the language to use and set the stop words to the default
        list provided by NLTK corpus for this language
        :param str lang: The language to use
        """
        try:
            self.stop_words = set(stopwords.words(lang))
            self.language = lang
        except:
            self.stop_words = {}
            self.language = None
        
    def set_stop_words(self, stop_words:set) -> None:
        """
        Sets the stop words to the provided list.
        :param set stop_words: The stop words to use
        """
        if stop_words:
            self.stop_words = set(stop_words)
        else:
            self.stop_words = {}
        
    def read_stopwords_from_file(self, language:str, filename:str) -> None:
        """
        Read the stop words from the specified file and set the language to
        the given language name
        :param strlanguage: The name of the language to set
        :param str filename: The name of the file containing the stop words
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                 text = " ".join(f.readlines())
            self.stop_words = set(text.split())  # prevent duplicate entries
            self.language = language
        except:
            self.stop_words = {}
            self.language = None
            
    def set_summary_length(self, summary_length:int) -> None:
        """
        Sets the default length for the summaries to be created
        :param int summary_length: The new default length
        """
        self.summary_length = summary_length
    
    def summarize(self, text:str or list, summary_length:int=None) -> str:
        """
        Summarize the given text. The text can either be a string or a list of
        strings. The string or each element in the list can contain multiple
        sentences.
        The language and stop word set have been initialized and are used. If no
        summary length is given as parameter, the default length is used.
        :param (str or list) text: The text to summarize
        :param int summary_length: The length of the summary to generate, optional
        :return: A string with the summary of the given text
        :rtype: str
        """
        
        # Length of summary to generate, if not specified use default
        if not summary_length:
            summary_length = self.summary_length

        # Make a list of all the sentences in the given text
        sentences = []
        if type(text) == str:
            sentences.extend(tokenize.sent_tokenize(text))
        elif type(text) == list:
            for text_part in text:
                sentences.extend(tokenize.sent_tokenize(text_part))
        else:
            return None    
        
        # Determine for each word, not being a stop word, the number of occurences
        # in the text. This word frequency determines the importance of the word.
        word_weights={}
        for sent in sentences:
            for word in word_tokenize(sent):
                word = word.lower()
                if len(word) > 1 and word not in self.stop_words:
                    if word in word_weights.keys():            
                        word_weights[word] += 1
                    else:
                        word_weights[word] = 1

        # The weight of each sentence equals the sum of the word importance for
        # each word in the sentence
        sentence_weights={}
        for sent in sentences:
            sentence_weights[sent] = 0
            for word in word_tokenize(sent) :  
                word = word.lower()
                if word in word_weights.keys():            
                    sentence_weights[sent] += word_weights[word]
        highest_weights = sorted(sentence_weights.values())[-summary_length:]

        # The summary consists of the sentences with the highest sentence weight, in the
        # same order as they occur in the original text
        summary=""
        for sentence,strength in sentence_weights.items():  
            if strength in highest_weights:
                summary += sentence + " "
        summary = summary.replace('_', ' ').strip()
        return summary

    def summarize_file(self, filename:str, encoding:str="utf-8", split_at:int=50, summary_length:int=None) -> str:
        """
        Summarize the content of the given file. The content of the file is splitted in
        chunks of a given size. The size is specified as number of sentences. For each chunk
        a summary is created. These summaries are concatenated to create the summary of the 
        total contents of the file
        The language and stop word set have been initialized and are used. If no
        summary length is given as parameter, the default length is used.
        :param str filename: The name of the file with the text to summarize
        :param str encoding: The encoding of the file, defaults to utf-8
        :param int split_at: The size of the chunks to summarize, defaults to 50
        :param int summary_length: The length of the summary to generate, optional
        :return: A string with the summary of the given text
        :rtype: str
        """
        if not os.path.exists(filename):
            return None

        # Read and clean te text from the specified file
        with open(filename, "r", encoding=encoding) as f:
            text = " ".join(f.readlines())
            text = text.replace('\n', ' ').replace('  ', ' ').strip()

        # Create a list of all sentences in the text and split this list
        # in chunks of n sentences, n being the split_at value
        sentences = []
        for sent in tokenize.sent_tokenize(text):
            sentences.append(sent)
        chunks = [sentences[x:x+split_at] for x in range(0, len(sentences), split_at)]

        # The summary is a concatenation of the summary of each chunk of sentences
        summary = []
        for c in chunks:
            summary.append(summarize(c, summary_length))
        summary = " ".join(summary)    
        return summary
    
    def detect_language(self,text:str) -> str:
        """
        Detect the language of the given text and initialize the object
        accordingly (setting language and set of stop words)
        :param str text: The text to analyse to find to laguage
        :return: The name of the detected language
        :rtype: str
        """
        ratios = {}
        tokens = word_tokenize(text)
        words = [word.lower() for word in tokens]

        # Determine for eah language how often the given text contains a stop 
        # word of the specific language. This is done for all languages supported
        # by NLTK corpus.
        for language in stopwords.fileids():
            stopws = set(stopwords.words(language))
            count = 0
            for word in words:
                if word in stopws:
                        count += 1
            ratios[language] = count

        # The language with the highest ocucrence rate of stop words is 
        # selected as language
        text_language = max(ratios, key=ratios.get)
        self.set_language(text_language)
        return text_language
