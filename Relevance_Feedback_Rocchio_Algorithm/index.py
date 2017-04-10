#Python 3.0
import re
import os
import collections
import time
import math
import random
from itertools import groupby
#import other modules as needed

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMapToFileNameMap = {}
# Map of document id to all of it's terms tf-idf
docIdToItsTermTfIdfMap = {}
# Map of document id to it's length
docIdToItsLengthMap = {}
stopWords = []
resultDocuments = []
alpha=1
beta=0.75
gamma=0.15



class index:
	def __init__(self,path, stopWordsPath):
		"""
		set input documents directory path, stop words file path and total numbers of documents to default value
		:param docPath:
		:param stopWordsPath:
		"""
		self.docPath = path
		self.stopWordsPath = stopWordsPath
		self.totalNumberOfDocuments = 0
		pass

	def buildIndex(self):
		#function to read documents from collection, tokenize and build the index with tokens
		# implement additional functionality to support relevance feedback
		#use unique document integer IDs

		stopWords = self.getStopWordsList()
		# print (stopWords)
		# print (len(stopWords))

		fileList = []
		fileNames = []
		rFile = re.compile("\*+TEXT \d")
		with open(self.docPath) as files:
			for k, g in groupby(files, key=lambda x: rFile.search(x)):
				if not k:
					# print list(g)
					fileList.append(list(g))
				if k:
					# print list(g)
					fileNames.append(list(g))

		self.totalNumberOfDocuments = float(len(fileList))
		# print (self.totalNumberOfDocuments)
		docId = 1
		i=0;
		for eachFile in fileList:
			position = 1
			fileNameLines = [line.rstrip('\n') for line in fileNames[i]]

			for eachLine in fileNameLines:
				wordList = re.split('\W+', eachLine)

			docIdMapToFileNameMap[docId] = wordList[2]
			i=i+1
			docIdToItsTermTfIdfMap[docId] = {}
			lines = [line.rstrip('\n') for line in eachFile]

			for eachLine in lines:
				wordList = re.split('\W+', eachLine)
				while '' in wordList:
					wordList.remove('')

				for word in wordList:
					if (word not in stopWords):
						if (word.lower() in dictionary):
							dictionaryValue = dictionary[word.lower()]
							docList = dictionaryValue["docList"]
							if (docId in docList):
								positionList = docList[docId]
								positionList["positionList"].append(position)
								wtd = 1.0 + math.log10(len(positionList["positionList"]))
								positionList["wtd"] = wtd
								position = position + 1
								termFreq = docIdToItsTermTfIdfMap[docId][word.lower()]["termFreq"]
								termFreq = termFreq + 1
								# docIdToItsTermTfIdfMap[docId][word.lower()] = (wtd * dictionaryValue["idf"])
								docIdToItsTermTfIdfMap[docId][word.lower()] = {"tfIdf":(wtd * dictionaryValue["idf"]), "termFreq":termFreq}
								# print (docIdToItsTermTfIdfMap[docId][word.lower()])
							else:
								totalDocWithWord = len(docList)
								totalDocWithWord = float(totalDocWithWord + 1)
								idf = math.log10(self.totalNumberOfDocuments / totalDocWithWord);
								dictionaryValue["idf"] = idf
								wtd = 1.0 + math.log10(1.0)
								docList[docId] = {"wtd": wtd, "positionList": [position]}
								position = position + 1
								termFreq = 1
								# docIdToItsTermTfIdfMap[docId][word.lower()] = (wtd * dictionaryValue["idf"])
								docIdToItsTermTfIdfMap[docId][word.lower()] = {"tfIdf": (wtd * dictionaryValue["idf"]), "termFreq": termFreq}
								# print (docIdToItsTermTfIdfMap[docId][word.lower()])
						else:
							idf = math.log10(self.totalNumberOfDocuments)
							wtd = 1.0 + math.log10(1.0)
							dictionary[word.lower()] = {"idf": idf, "docList": {docId: {"wtd": wtd, "positionList": [position]}}}
							position = position + 1
							termFreq = 1
							# docIdToItsTermTfIdfMap[docId][word.lower()] = (wtd * idf)
							docIdToItsTermTfIdfMap[docId][word.lower()] = {"tfIdf": (wtd * idf), "termFreq": termFreq}
							# print (docIdToItsTermTfIdfMap[docId][word.lower()])
					else:
						continue
			docId = docId + 1
		self.buildDocToItsLengthMap()

	def getStopWordsList(self):
		"""
        This method will list the stop words by tokenizing each word from stop words file
        """
		# stopWords = [];
		stopWordsLines = [line.rstrip('\n') for line in open(self.stopWordsPath)]
		for eachLine in stopWordsLines:
			stopWordsList = re.split('\W+', eachLine)

			while '' in stopWordsList:
				stopWordsList.remove('')

			for eachWord in stopWordsList:
				stopWords.append(eachWord)

		return stopWords


	def buildDocToItsLengthMap(self):
		"""
        This method will calculate document id length and store it in docIdToItsLengthMap
        """
		for eachDoc in docIdToItsTermTfIdfMap:
			sumOfSquareOfTfIdf = 0.0
			for eachTerm in docIdToItsTermTfIdfMap[eachDoc]:
				docIdToItsTermTfIdfMap[eachDoc][eachTerm]["tfIdf"] = dictionary[eachTerm]["idf"] * dictionary[eachTerm]["docList"][eachDoc]["wtd"]
				sumOfSquareOfTfIdf = sumOfSquareOfTfIdf + docIdToItsTermTfIdfMap[eachDoc][eachTerm]["tfIdf"] ** 2
			docIdToItsLengthMap[eachDoc] = math.sqrt(sumOfSquareOfTfIdf)


	def rocchio(self, query_terms, pos_feedback, neg_feedback, alpha, beta, gamma, queryTermToOccurenceMap, k):
	#function to implement rocchio algorithm
	#pos_feedback - documents deemed to be relevant by the user
	#neg_feedback - documents deemed to be non-relevant by the user
	#Return the new query  terms and their weights

		positiveFeedBackVector = {}
		negativeFeedBackVector = {}
		rocchioResultVector = {}
		totalNumberOfPositiveDocs = len(pos_feedback)
		totalNumberOfNegativeDocs = len(neg_feedback)
		rocchioDictionary = []
		# fileNameToDocIdMap = dict(zip(docIdMapToFileNameMap.values(), docIdMapToFileNameMap.keys()))
		if(queryTermToOccurenceMap is None):
			queryTermToOccurenceMap = {}
			for eachTerm in query_terms:
				if eachTerm not in queryTermToOccurenceMap:
					queryTermToOccurenceMap[eachTerm] = 1
				else:
					oldNumber = queryTermToOccurenceMap[eachTerm]
					oldNumber = oldNumber + 1
					queryTermToOccurenceMap[eachTerm] = oldNumber

			for eachTerm in queryTermToOccurenceMap:
				if(eachTerm not in rocchioDictionary):
					rocchioDictionary.append(eachTerm)

		for document in resultDocuments:
			for key in docIdToItsTermTfIdfMap[document]:
				if(key not in rocchioDictionary):
					rocchioDictionary.append(key)

		for eachDoc in pos_feedback:
			for eachTerm in docIdToItsTermTfIdfMap[int(eachDoc)]:
				if(eachTerm in positiveFeedBackVector):
					count = positiveFeedBackVector[eachTerm]
					positiveFeedBackVector[eachTerm] = count + (docIdToItsTermTfIdfMap[int(eachDoc)][eachTerm]["termFreq"]*(beta/totalNumberOfPositiveDocs))
				else:
					positiveFeedBackVector[eachTerm] = (docIdToItsTermTfIdfMap[int(eachDoc)][eachTerm]["termFreq"]*(beta/totalNumberOfPositiveDocs))


		for eachDoc in neg_feedback:
			for eachTerm in docIdToItsTermTfIdfMap[int(eachDoc)]:
				if(eachTerm in negativeFeedBackVector):
					count = negativeFeedBackVector[eachTerm]
					negativeFeedBackVector[eachTerm] = count + (docIdToItsTermTfIdfMap[int(eachDoc)][eachTerm]["termFreq"]*(gamma/totalNumberOfNegativeDocs))
				else:
					negativeFeedBackVector[eachTerm] = (docIdToItsTermTfIdfMap[int(eachDoc)][eachTerm]["termFreq"]*(gamma/totalNumberOfNegativeDocs))

		for eachTerm in rocchioDictionary:
			queryValue = 0.0;
			if eachTerm in queryTermToOccurenceMap:
				queryValue = queryTermToOccurenceMap[eachTerm];
			pFValue = 0.0;
			if eachTerm in positiveFeedBackVector:
				pFValue = positiveFeedBackVector[eachTerm];
			nFValue = 0.0;
			if eachTerm in negativeFeedBackVector:
				nFValue = negativeFeedBackVector[eachTerm];
			weight = queryValue + pFValue - nFValue;
			if weight > 0.0:
				rocchioResultVector[eachTerm] = weight;

		self.calculateCosineSimilarityUsingRocchioFeedback(k, dictionary, rocchioResultVector)
		print (rocchioResultVector)
		# print (len(rocchioResultVector))
		return rocchioResultVector

	def calculateCosineSimilarityUsingRocchioFeedback(self, k, searchIndex, rocchioResultVector):
		"""
		This method will take rocchio result vector as parameter and calculate cosine similarity score for each term and prints top k documents
		"""
		scores = {}
		queryTermToItsLengthMap = {}

		for eachTerm in rocchioResultVector:
			postingListOfTerm = searchIndex[eachTerm]["docList"]
			tfIdfOfQueryTerm = rocchioResultVector[eachTerm]
			queryTermToItsLengthMap[eachTerm] = tfIdfOfQueryTerm
			for docId in postingListOfTerm:
				tfIdfOfTermInDocument = searchIndex[eachTerm]["idf"] * searchIndex[eachTerm]["docList"][docId]["wtd"]
				if (docId in scores):
					scores[docId] = scores[docId] + (tfIdfOfQueryTerm * tfIdfOfTermInDocument)
				else:
					scores[docId] = tfIdfOfQueryTerm * tfIdfOfTermInDocument

		sumOflengthOfAllQueryTerms = 0.0
		for eachTerm in queryTermToItsLengthMap:
			sumOflengthOfAllQueryTerms = sumOflengthOfAllQueryTerms + queryTermToItsLengthMap[eachTerm] ** 2

		for docId in scores:
			scores[docId] = scores[docId] / (docIdToItsLengthMap[docId] * math.sqrt(sumOflengthOfAllQueryTerms))

		print ("Top "+ str(k) +" Ranked Documents ::: ")
		counter = 0
		for docId in sorted(scores, key=scores.get, reverse=True):
			# print ("Doc Returned ==> " + str(docIdMapToFileNameMap[docId]))
			print ("Doc Returned ==> " + str(docId))
			resultDocuments.append(docId)
			counter = counter + 1
			if (counter == int(k)):
				break

	def calculateCosineSimilarityAndPrintSearchDocument(self, k, searchIndex, queryTermToOccurenceMap):
		"""
		This method will take below parameters and calculate cosine similarity score for each term in query
		and prints top k documents
		:param k:
		:param searchIndex:
		:param queryTermToOccurenceMap:
		:return:
		"""
		scores = {}
		queryTermToItsLengthMap = {}

		for eachTerm in queryTermToOccurenceMap:
			postingListOfTerm = searchIndex[eachTerm]["docList"]
			tfIdfOfQueryTerm = searchIndex[eachTerm]["idf"] * (1.0 + math.log10(queryTermToOccurenceMap[eachTerm]))
			queryTermToItsLengthMap[eachTerm] = tfIdfOfQueryTerm
			for docId in postingListOfTerm:
				tfIdfOfTermInDocument = searchIndex[eachTerm]["idf"] * searchIndex[eachTerm]["docList"][docId]["wtd"]
				if (docId in scores):
					scores[docId] = scores[docId] + (tfIdfOfQueryTerm * tfIdfOfTermInDocument)
				else:
					scores[docId] = tfIdfOfQueryTerm * tfIdfOfTermInDocument

		sumOflengthOfAllQueryTerms = 0.0
		for eachTerm in queryTermToItsLengthMap:
			sumOflengthOfAllQueryTerms = sumOflengthOfAllQueryTerms + queryTermToItsLengthMap[eachTerm] ** 2

		for docId in scores:
			scores[docId] = scores[docId] / (docIdToItsLengthMap[docId] * math.sqrt(sumOflengthOfAllQueryTerms))

		print ("Top "+ str(k) +" Ranked Documents ::: ")
		counter = 0
		for docId in sorted(scores, key=scores.get, reverse=True):
			# print ("Doc Returned ==> " + str(docIdMapToFileNameMap[docId]))
			print ("Doc Returned ==> " + str(docId))
			resultDocuments.append(docId)
			counter = counter + 1
			if (counter == int(k)):
				break

	def query(self, query_terms, k):
	#function for exact top K retrieval using cosine similarity
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
		queryTermToOccurenceMap = {}
		for eachTerm in query_terms:
			if eachTerm not in queryTermToOccurenceMap:
				queryTermToOccurenceMap[eachTerm] = 1
			else:
				oldNumber = queryTermToOccurenceMap[eachTerm]
				oldNumber = oldNumber + 1
				queryTermToOccurenceMap[eachTerm] = oldNumber

		self.calculateCosineSimilarityAndPrintSearchDocument(k, dictionary, queryTermToOccurenceMap)

	def print_dict(self):
    #function to print the terms and posting list in the index
		for key in dictionary:
			print (key + " --> " + str(dictionary[key]))
		print (len(dictionary))

	def print_doc_list(self):
	# function to print the documents and their document id
		for key in docIdMapToFileNameMap:
			print ("Doc ID: " + str(key) + " ==> " + str(docIdMapToFileNameMap[key]))

def main():

	# docCollectionPath = "/Users/HarshPatil/CS429/Assignment_3_Relevance_Feedback/time/TIME.ALL"
	docCollectionPath = input("Enter path of text file collection ::: ")
	# stopWordsPath = "/Users/HarshPatil/CS429/Assignment_3_Relevance_Feedback/time/TIME.STP"
	stopWordsPath = input("Enter the stop words file path ::: ")
	# queryFile = "/Users/HarshPatil/CS429/Assignment_3_Relevance_Feedback/query"
	queryFile = input("Enter path of the query file ::: ")

	indexObject = index(docCollectionPath, stopWordsPath)
	startTime = time.time()
	indexObject.buildIndex()
	endTime = time.time()
	print ("")
	print ("Index built in ::: %s seconds" % (endTime - startTime))
	print ("")

	while (True):
		print ("Enter 1 to print dictionary")
		print ("Enter 2 to print doc id map")
		print ("Enter 3 to continue")
		printChoice = input("Enter your choice from top ::: ")
		if (printChoice == "1"):
			indexObject.print_dict()
			print ("")
		elif (printChoice == "2"):
			indexObject.print_doc_list()
			print ("")
		else:
			print ("")
			break

	totalDocsToBeRetrieved = input("Enter number of docs to be retrieved ::: ")
	print ("")

	wordsInLowerCase = []

	QueryLines = [line.rstrip('\n') for line in open(queryFile)]
	for eachLine in QueryLines:
		wordList = re.split('\W+', eachLine)

		while '' in wordList:
			wordList.remove('')
		# wordsInLowerCase = []
		for word in wordList:
			if (word not in stopWords):
				wordsInLowerCase.append(word.lower())

	print ("Query Terms ::: " + str(wordsInLowerCase))
	queryStartTime = time.time()
	indexObject.query(wordsInLowerCase, totalDocsToBeRetrieved)
	queryEndTime = time.time()
	print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
	print ("")

	queryTermToOccurenceMap=None
	print ("Enter 1 for Rocchio Feedback")
	print ("Enter 2 for Pseudo Feedback")
	print ("Enter 3 to exit")
	choice = input("Enter your choice from top ::: ")
	if(choice == "1"):
		feedbackCount = 0
		while (feedbackCount < 5):
			feedbackCount = feedbackCount + 1
			totalNumberOfRelevantDocs = input("Enter number of relevant documents ::: ")
			positiveFeedback = []
			negativeFeedback = []
			i = 0
			while (i < int(totalNumberOfRelevantDocs)):
				docId = input("Enter relevant document Id from above ::: ")
				positiveFeedback.append(docId)
				i = i + 1

			totalNumberOfNonRelevantDocs = input("Enter number of non-relevant documents ::: ")
			j = 0
			while (j < int(totalNumberOfNonRelevantDocs)):
				docId = input("Enter non-relevant document Id from above ::: ")
				negativeFeedback.append(docId)
				j = j + 1

			print ("")
			queryStartTime = time.time()
			queryTermToOccurenceMap = indexObject.rocchio(wordsInLowerCase, positiveFeedback, negativeFeedback, alpha,
														  beta, gamma, queryTermToOccurenceMap, totalDocsToBeRetrieved)
			queryEndTime = time.time()
			print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
			print ("")

	elif (choice == "2"):
		feedbackCount = 0
		while (feedbackCount < 5):
			feedbackCount = feedbackCount + 1
			positiveFeedback = []
			negativeFeedback = []
			i = 0
			while (i < 3):
				positiveFeedback.append(resultDocuments[i])
				i = i + 1
			print ("")
			queryStartTime = time.time()
			queryTermToOccurenceMap = indexObject.rocchio(wordsInLowerCase, positiveFeedback, negativeFeedback, alpha,
														  beta, gamma, queryTermToOccurenceMap, totalDocsToBeRetrieved)
			queryEndTime = time.time()
			print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
			print ("")
	else:
		print ("Thanks for testing me")
		return

if __name__ == '__main__':
    main()

