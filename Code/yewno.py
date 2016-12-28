import pandas as pd
import nltk
import itertools
import re
from os import listdir
from os.path import isfile, join

#Google's language detect package
import langdetect

#acquire the book data from the gutenberg python package
from gutenberg.query import get_etexts
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

#Global variables for sentence splitting
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

class Yewno():
	def __init__(self, title=0, author=0):
		self.title = title
		self.author = author
		#self.get_text(self.title, self.author) #This is the gutenberg method
		self.data_path = '../Data/'
		self.save_path = '../Output/'
		self.final_df = self.controller()

	def controller(self):
		books = self.gather_books(self.data_path)
		book_df = pd.DataFrame()
		for book in books:
			print(book)
			temp = self.open_text(self.data_path+book)
			temp.to_csv(self.save_path+'cleaned_'+book+'.csv', index=False)
			book_df = book_df.append(temp)
		return(book_df)

	def open_text(self, bookpath):
		with open(bookpath, encoding='utf-8') as f:
			content = f.readlines()
			all_text = " ".join(content)
			sentences = self.split_sentences(all_text)
			cleaned_sentences = []
			for sentence in sentences:
				words = sentence.strip().split(" ")
				if len(words) >= 2:
					num_words = len(words)
					cleaned_sentences.append((" ".join(words), num_words))
			temp = pd.DataFrame(cleaned_sentences, columns=['sentence', 'num_words'])
			temp['google_language'] = temp['sentence'].apply(lambda x: self.get_language_google(x))
			temp['stopwords_language'] = temp['sentence'].apply(lambda x: self.get_language_stopword(x))
			name = bookpath.split('.')[2].split('/')[2]
			temp['book_name'] = [name]*len(cleaned_sentences)
		return(temp)

	def gather_books(self, data_path):
		""" Temporary text loader while pipeline for automatic text loading is set up """
		all_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
		books = []
		for file in all_files:
			if file.endswith('.txt'):
				books.append(file)
		return(books)

	def get_text(self, title, author):
		"""
		This function will access the title and author of a book from the
		Gutenberg project and save the data as a csv file
		PROBLEM HERE -- gutenberg goes down a lot, so getting a full text 
		did not work. To bypass that, I downloaded some books of mixed languages.
		"""
		guten_number = get_etexts('title', title)[0]
		text = strip_headers(load_etext(guten_number)).strip()
		return(text)

	def split_sentences(self, text):
		""" This function takes in a Gutenberg book and splits into sentences """
		text = " " + text + "  "
		text = text.replace("\n"," ")
		text = re.sub(prefixes,"\\1<prd>",text)
		text = re.sub(websites,"<prd>\\1",text)
		if "Ph.D" in text: 
			text = text.replace("Ph.D.","Ph<prd>D<prd>")
		text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
		text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
		text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
		text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
		text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
		text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
		text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
		if "”" in text: 
			text = text.replace(".”","”.")
		if "\"" in text: 
			text = text.replace(".\"","\".")
		if "!" in text: 
			text = text.replace("!\"","\"!")
		if "?" in text: 
			text = text.replace("?\"","\"?")
		text = text.replace(".",".<stop>")
		text = text.replace("?","?<stop>")
		text = text.replace("!","!<stop>")
		text = text.replace("<prd>",".")
		sentences = text.split("<stop>")
		sentences = sentences[:-1]
		sentences = [s.strip() for s in sentences]
		return(sentences)

	def get_language_google(self, input_text):
		"""
		This function uses Google's package 'langdetect' to detect the language
		of a sentence.

		Input: 
		input_text: a single text record from pandas series

		Output:
		The likelihoods of all languages for the sentence
		"""
		likelihood = {}
		for item in langdetect.detect_langs(input_text):
			likelihood[item.lang] = item.prob
		return(likelihood)

	def get_language_stopword(self, input_text):
		""" 
		This function is modified from a function written by author of H6O6.com to 
		give a likelihood of a text record's language (danish, dutch, english, finnish, 
		french, german, hungarian, italian, norwegian, portuguese, russian, spanish, 
		swedish, turkish) based on different stopwords dictionary.
		
		Input:
		input_text: a single text record from pandas series
		
		Output:
		The likeliehoods of all languages per sentence
		"""
		input_words = nltk.wordpunct_tokenize(input_text)

		likelihood = {}
		for language in nltk.corpus.stopwords._fileids:
			likelihood[language] = len(set(input_words) & set(nltk.corpus.stopwords.words(language)))
		likelihood = {k:v for k,v in likelihood.items() if v}
		return(likelihood)

if __name__ == '__main__':
	yewno = Yewno()
	yewno.final_df.to_csv(yewno.save_path+'all_books.csv', index=False)
