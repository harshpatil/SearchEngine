#Python 2.7.3
#-*- coding: latin-1 -*-
import re
import os
import collections
import time

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMap = {}

class index:

	def __init__(self,path):
		self.path = path
		pass

	def buildIndex(self):
		#function to read documents from collection, tokenize and build the index with tokens
		#index should also contain positional information of the terms in the document --- term: [(ID1,[pos1,pos2,..]), (ID2, [pos1,pos2,…]),….]
		#use unique document IDs
		"""
		1) This method gets invoked as soon as user inputs dictionary path
		2) Iterates through all the files in the dictionary
		3) For each file, read every line and stores it in lines list.
		4) Then iterates through lines list and split each line using '\W+' de limiter
		5) Removes all the empty words and iterates through wordsList
		6) Convert each word to lower case and search for word in dictionary keys.
		7) If word is present in dictionary, search for document Id.
		8) If document id is same as current doc id, append the position of the word to posting list else, create a new map with
			docId as key and position as value.
		9) If word is not present in dictionary, create a new entry in map with word as key, it's docId and position as value
		10) Example map ->
				"word" : {docId : [position_List], docId : [positionList]}
		11) Each file is given a unique doc id
		12) position variable is used calculate position of all words and is initialized to 1 everytime a new file is opened to read
		"""
		docId = 1
		fileList = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
		for eachFile in fileList:
			position = 1
			# docName = "Doc_Id_" + str(docId)
			# docName =  str(docId)
			docIdMap[docId] = eachFile
			lines = [line.rstrip('\n') for line in open(self.path + "/" + eachFile)]

			for eachLine in lines:
				wordList = re.split('\W+', eachLine)

				while '' in wordList:
					wordList.remove('')

				for word in wordList:
					if (word.lower() in dictionary):
						postingList = dictionary[word.lower()]
						if(docId in postingList):
							postingList[docId].append(position)
							position = position + 1
						else:
							postingList[docId] = [position]
							position = position + 1
					else:
						dictionary[word.lower()] = {docId:[position]}
						position = position + 1
			docId = docId + 1

		# for key in dictionary:
		# 	print key
		# print dictionary
		# print len(dictionary)

	def and_query(self, query_terms):
		#function for identifying relevant docs using the index
		""" This method takes list of query terms as input
		1) If the length of query_terms is equal to 1, It will get the posting list for the only term. If no result is found,
		   appropriate message will be printed. Else, print the respective file name by traversing docIdToFileName map
		   for all the posting lists.
		2) If there are more than 1 item in query_terms, it will get posting list for first and second term. Then calls mergePostingList()
		 	by passing posting lists of term0 and term1. The merge result will be used to get intersection of posting list of term3.
		 	This will be repeated for all the subsequent query terms.
		3) Result of step 2 will have merged list of all the query terms
		4) Uses the final merged list to traverse through DocIdToFileName map and prints respective file names
		"""
		if (len(query_terms) == 1):
			resultList = self.getPostingList(query_terms[0])
			if not resultList:
				print ""
				printString = "Result for the Query ::: " + query_terms[0]
				print printString
				print "0 documents returned as there is no match"
				return
			else:
				print ""
				printString = "Result for the Query ::: " + query_terms[0]
				print printString
				print "Total documents retrieved ::: " + str(len(resultList))
				for items in resultList:
					print docIdMap[items]
		else:
			resultList = []
			for i in range(1, len(query_terms)):
				if(len(resultList) == 0):
					resultList = self.mergePostingList(self.getPostingList(query_terms[0]), self.getPostingList(query_terms[i]))
				else:
					resultList = self.mergePostingList(resultList, self.getPostingList(query_terms[i]))

			print ""
			printString = "Result for the Query ::: "
			i = 1
			for keys in query_terms:
				if(i == len(query_terms)):
					printString += " " + str(keys)
				else:
					printString += " " + str(keys) + " AND"
					i=i+1

			print printString
			print "Total documents retrieved ::: " + str(len(resultList))
			for items in resultList:
				print docIdMap[items]

	def getPostingList(self, term):
		""" Takes term as input parameter, It will search for key in the index, if any of the key matches search term,
		posting list of that key will be returned as a list. If key is not found returns None"""
		if (term in dictionary):
			postingList = dictionary[term]
			keysList = []
			for keys in postingList:
				keysList.append(keys)
			keysList.sort()
			# print keysList
			return keysList
		else:
			return None

	def mergePostingList(self, list1, list2):
		""" This function takes 2 lists as input parameters and returns intersection of both in a sorted form """
		mergeResult = list(set(list1) & set(list2))
		mergeResult.sort()
		# print mergeResult
		return mergeResult

	def print_dict(self):
        #function to print the terms and posting list in the index
		""" Iterate through dictionary map and print all the keys and respective values """
		for key in dictionary:
			print key + " --> "+ str(dictionary[key])

	def print_doc_list(self):
		# function to print the documents and their document id
		""" Iterate through documentIdToFileName map and print all the keys and respective values """
		#print docIdMap
		for key in docIdMap:
			print "Doc ID: " + str(key) + " ==> " + str(docIdMap[key])

def main():
	"""
	1) main method prompts for directory path containing input text files and path of the query file where all the query
	terms are mentioned
	2) creates an object of index class and calls build Index
	3) Once index is built, it will print dictonory
	4) Then, prints document id fileName map
	5) Read each line from query file, tokenize query terms and perform search on newly built index
	6) print time taken to perform these actions
	"""
	# indexObject = index("/Users/HarshPatil/CS429/Assignment_1_Boolean_Retrieval/collection")
	docCollectionPath = raw_input("Enter path of text file collection ::: ")
	# queryFile = "/Users/HarshPatil/CS429/Assignment_1_Boolean_Retrieval/queries"
	queryFile = raw_input("Enter path of query file ::: ")
	indexObject = index(docCollectionPath)
	startTime = time.time()
	indexObject.buildIndex()
	endTime = time.time()
	print ""
	print ("Index built in ::: %s seconds" % (endTime - startTime))
	print ""
	print "Dictionary ::::"
	indexObject.print_dict()

	print ""
	print "Document List ::::"
	indexObject.print_doc_list()
	print ""

	QueryLines = [line.rstrip('\n') for line in open(queryFile)]
	for eachLine in QueryLines:
		wordList = re.split('\W+', eachLine)

		while '' in wordList:
			wordList.remove('')

		wordsInLowerCase = []
		for word in wordList:
			wordsInLowerCase.append(word.lower())

		queryStartTime = time.time()
		indexObject.and_query(wordsInLowerCase)
		queryEndTime = time.time()
		print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))

if __name__ == '__main__':
    main()
