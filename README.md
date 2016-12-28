# yewno
yewno project

# Project Workflow

## MVP1: Create Gutenberg book pipeline
	- Create a pipeline to pull data from Gutenberg.org - STALL
		- Saved books to specific file folder for now
	- Use that pipeline to save a few books into csv format - COMPLETE
	- Expansion idea: Retrieve books based on more metadata (i.e. Author, Topic/Subject)
	- Database idea: Set up a database rather than saving books as CSV

## MVP2: Preprocess book data
	- Preprocess the book data in the data folder - COMPLETE
	- Save the preprocessed data - COMPLETE
	- Expansion idea: More pre process steps to get cleaner text (i.e. stemming, etc.)

## MVP3: Test book data for language
	- Create algorithm to test each sentence in book for language - COMPLETE
	- Save the algorithmic percentage of language per sentence per book - COMPLETE
	- Expansion idea: Extend more ways to detect languages, compare against each other

## MVP4: Create feedback loop for crowd sourced corrections
	- If a crowd source response to a sentence corrects that sentence language, if that response is "overwelming", then change the label from the detected language to the crowd sourced language

## MVP5: Create front end for the solution
## MVP6: Now, with labeled data, we can train models to detect language using machine learning
