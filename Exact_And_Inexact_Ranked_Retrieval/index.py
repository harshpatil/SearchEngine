#Python 3.0
import re
import os
import collections
import time
import math
import random
#import other modules as needed

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMapToFileNameMap = {}
# Map of document id to all of it's terms tf-idf
docIdToItsTermTfIdfMap = {}
# Map of document id to it's length
docIdToItsLengthMap = {}
# Map of dictionary terms to it's champion list
championListMap = {}
# Map of leaders to all it's followers
leadersToFollowersMap = {}

class index:
	def __init__(self,docPath, stopWordsPath):
		"""
		set input documents directory path, stop words file path and total numbers of documents to default value
		:param docPath:
		:param stopWordsPath:
		"""
		self.docPath = docPath
		self.stopWordsPath = stopWordsPath
		self.totalNumberOfDocuments = 0
		pass

	def buildIndex(self):
		#function to read documents from collection, tokenize and build the index with tokens
		# implement additional functionality to support methods 1 - 4
		#use unique document integer IDs
		"""
			1) This method gets invoked once user inputs dictionary path
			2) Iterates through all the files in the dictionary
			3) For each file, read every line and stores it in lines list.
			4) Then iterates through lines list and split each line using '\W+' de limiter
			5) Removes all the empty words and iterates through wordsList
			6) Convert each word to lower case and if word is not in the stop words list, it will search for word in dictionary keys.
			7) If word is present in dictionary, search for document Id.
			8) If document id is same as current doc id, append the position of the word to posting list else, create a new map with
				docId as key and position as value.
			9) If word is not present in dictionary, create a new entry in map with word as key, it's docId and position as value
			10) Example map ->
					"word" : {docId : [position_List], docId : [positionList]}
			11) Each file is given a unique doc id
			12) position variable is used calculate position of all words and is initialized to 1 everytime a new file is opened to read
			13) While iterating through each words it will also maintain a map of document id to all it's terms tf-idf score.
			14) Everytime the word is repeated in a doc, tf-idf will be calculated and updated value will be stored in docIdToItsTermTfIdfMap
			15) In the end, for every file it will call buildDocToItsLengthMap method to calculate it's length
		"""
		stopWords = self.getStopWordsList()
		#print (stopWords)

		fileList = [f for f in os.listdir(self.docPath) if os.path.isfile(os.path.join(self.docPath, f))]
		self.totalNumberOfDocuments = float(len(fileList))
		docId = 1
		for eachFile in fileList:
			position = 1
			docIdMapToFileNameMap[docId] = eachFile
			docIdToItsTermTfIdfMap[docId] = {}
			lines = [line.rstrip('\n') for line in open(self.docPath + "/" + eachFile)]

			for eachLine in lines:
				wordList = re.split('\W+', eachLine)

				while '' in wordList:
					wordList.remove('')

				for word in wordList:
					if (word.lower() not in stopWords):
						if (word.lower() in dictionary):
							dictionaryValue = dictionary[word.lower()]
							docList = dictionaryValue["docList"]
							if (docId in docList):
								positionList = docList[docId]
								positionList["positionList"].append(position)
								wtd = 1.0 + math.log10(len(positionList["positionList"]))
								positionList["wtd"] = wtd
								position = position + 1
								docIdToItsTermTfIdfMap[docId][word.lower()] = (wtd * dictionaryValue["idf"])
							else:
								totalDocWithWord = len(docList)
								totalDocWithWord=float(totalDocWithWord+1)
								idf = math.log10(self.totalNumberOfDocuments/totalDocWithWord);
								dictionaryValue["idf"] = idf
								wtd = 1.0 + math.log10(1.0)
								docList[docId] = {"wtd":wtd, "positionList":[position]}
								position = position + 1
								docIdToItsTermTfIdfMap[docId][word.lower()] = (wtd * dictionaryValue["idf"])
						else:
							idf = math.log10(self.totalNumberOfDocuments)
							wtd = 1.0 + math.log10(1.0)
							dictionary[word.lower()] = {"idf":idf, "docList":{docId:{"wtd":wtd, "positionList":[position]}}}
							position = position + 1
							docIdToItsTermTfIdfMap[docId][word.lower()] = (wtd * idf)
					else:
						continue
			docId = docId + 1

		self.buildDocToItsLengthMap()

	def getStopWordsList(self):
		"""
		This method will list of stop words by tokenizing each word from stop words file
		"""
		stopWords = [];
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
				docIdToItsTermTfIdfMap[eachDoc][eachTerm] = dictionary[eachTerm]["idf"] * dictionary[eachTerm]["docList"][eachDoc]["wtd"]
				sumOfSquareOfTfIdf = sumOfSquareOfTfIdf + docIdToItsTermTfIdfMap[eachDoc][eachTerm] ** 2
			docIdToItsLengthMap[eachDoc] = math.sqrt(sumOfSquareOfTfIdf)

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

		print ("Top "+ k +" Ranked Documents ::: ")
		counter = 0
		for docId in sorted(scores, key=scores.get, reverse=True):
			print ("Doc Returned ==> " + str(docIdMapToFileNameMap[docId]))
			counter = counter + 1
			if (counter == int(k)):
				break

	def exact_query(self, query_terms, k):
		#function for exact top K retrieval (method 1)
		#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
		"""
		1) This method is called whenever user selects option "1" to retreive top K documents by passing below parameters
		:param query_terms:
		:param k:
		:return:
		2) This method will iterate through query terms and identify duplicates if any.
		3) Build query term to it's occurance map
		4) Calls calculateCosineSimilarityAndPrintSearchDocument method to calculate cosine similarity and prints top K docs
		"""
		queryTermToOccurenceMap = {}
		for eachTerm in query_terms:
			if eachTerm not in queryTermToOccurenceMap:
				queryTermToOccurenceMap[eachTerm] = 1
			else:
				oldNumber = queryTermToOccurenceMap[eachTerm]
				oldNumber = oldNumber + 1
				queryTermToOccurenceMap[eachTerm] = oldNumber

		self.calculateCosineSimilarityAndPrintSearchDocument(k, dictionary, queryTermToOccurenceMap)

	def buildChampionList(self):
		"""
		1) This method gets executed as soon as inverted index is built
		2) This iterates through dictionary and stores top R documents with highest tf-idf from posting list
		:return:
		"""
		totalDocsToBeKeptInChampionList = 20
		for eachTerm in dictionary:
			postingList = dictionary[eachTerm]["docList"]
			counter = 0
			championListMap[eachTerm] = {"idf":dictionary[eachTerm]["idf"], "docList":{}}
			for eachDocId in sorted(postingList, key=lambda  x:postingList[x]["wtd"], reverse=True):
				mapValue = championListMap[eachTerm]["docList"];
				mapValue[eachDocId]= {"wtd": postingList[eachDocId]["wtd"]};
				counter = counter + 1
				if(counter == totalDocsToBeKeptInChampionList):
					break;

	def inexact_query_champion(self, query_terms, k):
		#function for exact top K retrieval using champion list (method 2)
		#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
		"""
			1) This method is called whenever user selects option "2" to retreive top K documents by passing below parameters
			:param query_terms:
			:param k:
			:return:
			2) This method will iterate through query terms and identify duplicates if any.
			3) Build query term to it's occurance map
			4) Calls calculateCosineSimilarityAndPrintSearchDocument method to calculate cosine similarity using champion list
			and prints top K docs
			"""
		queryTermToOccurenceMap = {}
		for eachTerm in query_terms:
			if eachTerm not in queryTermToOccurenceMap:
				queryTermToOccurenceMap[eachTerm] = 1
			else:
				oldNumber = queryTermToOccurenceMap[eachTerm]
				oldNumber = oldNumber + 1
				queryTermToOccurenceMap[eachTerm] = oldNumber

		self.calculateCosineSimilarityAndPrintSearchDocument(k, championListMap, queryTermToOccurenceMap)

	def inexact_query_index_elimination(self, query_terms, k):
		#function for exact top K retrieval using index elimination (method 3)
		#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
		"""
			1) This method is called whenever user selects option "3" to retreive top K documents by passing below parameters
			:param query_terms:
			:param k:
			:return:
			2) This method will iterate through query terms and identify duplicates if any.
			3) Maintains a map of query term to it's idf value
			4) Calls calculateCosineSimilarityAndPrintSearchDocument method to calculate cosine similarity using
			half of the query terms (terms with highest idf is used) and prints top K docs
			"""
		queryTermToOccurenceMap = {}
		queryTermToIdfMap = {}
		eliminatedQueryTermToOccurenceMap = {}

		for eachTerm in query_terms:
			if eachTerm not in queryTermToOccurenceMap:
				queryTermToOccurenceMap[eachTerm] = 1
				queryTermToIdfMap[eachTerm] = dictionary[eachTerm]["idf"]
			else:
				oldNumber = queryTermToOccurenceMap[eachTerm]
				oldNumber = oldNumber + 1
				queryTermToOccurenceMap[eachTerm] = oldNumber

		count=0
		for term in sorted(queryTermToIdfMap, key=lambda x: queryTermToIdfMap[x], reverse=True):
			eliminatedQueryTermToOccurenceMap[term] = queryTermToOccurenceMap[term]
			count= count + 1
			if(count == (len(queryTermToIdfMap)/2)):
				break

		self.calculateCosineSimilarityAndPrintSearchDocument(k, dictionary, eliminatedQueryTermToOccurenceMap)

	def buildCluster(self):
		"""
		1) This method is executed once inverted index and champioList is created
		2) This method will randomly select sqrt(N) documents as leaders and calculate it's followers
		3) Maintains a map ot leader to it's followers list
		:return:
		"""
		# leaderList = [160,84,228,229,166,330,396,109,239,216,178,340,377,280,25,379,156,381,254,325]
		# for item in leaderList:
		# 	leadersToFollowersMap[item] ={}
		totalNumberOfLeaders = math.floor(math.sqrt(self.totalNumberOfDocuments))
		count = 0
		while(True):
			leadersToFollowersMap[(random.randint(1, self.totalNumberOfDocuments))] = {}
			count = count + 1
			if (count == totalNumberOfLeaders):
				break
		# print (leadersToFollowersMap)
		# print (len(leadersToFollowersMap))

		for eachFollower in docIdToItsLengthMap:
			if (eachFollower not in leadersToFollowersMap):
				scores = {}
				for eachTerm in docIdToItsTermTfIdfMap[eachFollower]:
					postingListOfTerm = dictionary[eachTerm]["docList"]
					tfIdfOfEachTermInFollower = dictionary[eachTerm]["idf"] * (postingListOfTerm[eachFollower]["wtd"])
					for eachDoc in postingListOfTerm:
						if(eachDoc in leadersToFollowersMap):
							tfIdfOfTermInDocument = dictionary[eachTerm]["idf"] * dictionary[eachTerm]["docList"][eachDoc]["wtd"]
							if (eachDoc in scores):
								scores[eachDoc] = scores[eachDoc] + (tfIdfOfEachTermInFollower * tfIdfOfTermInDocument)
							else:
								scores[eachDoc] = tfIdfOfEachTermInFollower * tfIdfOfTermInDocument

				for docId in scores:
					scores[docId] = scores[docId] / (docIdToItsLengthMap[docId] * docIdToItsLengthMap[eachFollower])
				count = 0
				for docId in sorted(scores, key=scores.get, reverse=True):
					if(count == 1):
						break;
					else:
						count = count + 1
						if(len(leadersToFollowersMap[docId]) == 0):
							leadersToFollowersMap[docId] = [eachFollower]
						else:
							leadersToFollowersMap[docId].append(eachFollower)
		# print (leadersToFollowersMap)

	def getCandidateList(self, scores, k):
		"""
		This method is called to identify candidate list in cluster pruning
		:param scores:
		:param k:
		:return:
		"""
		count = 0;
		candidateList = [];
		for i in sorted(scores, key=scores.get, reverse=True):
			if (count >= int(k)):
				break;
			else:
				candidateList.append(i);
				count = count + 1;
				for eachFollower in leadersToFollowersMap[i]:
					candidateList.append(eachFollower);
					count = count + 1;
		return candidateList;

	def inexact_query_cluster_pruning(self, query_terms, k):
		#function for exact top K retrieval using cluster pruning (method 4)
		#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
		"""
			1) This method is called whenever user selects option "4" to retreive top K documents by passing below parameters
			:param query_terms:
			:param k:
			:return:
			2) This method will iterate through query terms and identify duplicates if any.
			3) Calculates tf-idf of each term against all the leaders in cluster in leadersToFollowersMap
			4) Identifies candidate list, calculate tf-idf for all the candidates and prints top K docs with highest score
			"""
		queryTermToOccurenceMap = {}
		for eachTerm in query_terms:
			if eachTerm not in queryTermToOccurenceMap:
				queryTermToOccurenceMap[eachTerm] = 1
			else:
				oldNumber = queryTermToOccurenceMap[eachTerm]
				oldNumber = oldNumber + 1
				queryTermToOccurenceMap[eachTerm] = oldNumber

		#print (queryTermToOccurenceMap)
		scores = {}
		queryTermToItsLengthMap = {}

		for eachTerm in queryTermToOccurenceMap:
			postingListOfTerm = dictionary[eachTerm]["docList"]
			tfIdfOfQueryTerm = dictionary[eachTerm]["idf"] * (1.0 + math.log10(queryTermToOccurenceMap[eachTerm]))
			queryTermToItsLengthMap[eachTerm] = tfIdfOfQueryTerm
			for docId in leadersToFollowersMap:
				if(docId in postingListOfTerm):
					tfIdfOfTermInDocument = dictionary[eachTerm]["idf"] * postingListOfTerm[docId]["wtd"]
					if (docId in scores):
						scores[docId] = scores[docId] + (tfIdfOfQueryTerm * tfIdfOfTermInDocument)
					else:
						scores[docId] = tfIdfOfQueryTerm * tfIdfOfTermInDocument

		sumOflengthOfAllQueryTerms = 0.0
		for eachTerm in queryTermToItsLengthMap:
			sumOflengthOfAllQueryTerms = sumOflengthOfAllQueryTerms + queryTermToItsLengthMap[eachTerm] ** 2

		for docId in scores:
			scores[docId] = scores[docId] / (docIdToItsLengthMap[docId] * math.sqrt(sumOflengthOfAllQueryTerms))

		candidateList=self.getCandidateList(scores,k);
		# print (candidate_set)
		print ("Top "+ k +"  Ranked Documents ::: ")
		newScores={}
		for eachTerm in queryTermToOccurenceMap:
			postingListOfTerm = dictionary[eachTerm]["docList"]
			for docId in candidateList:
				if(docId in postingListOfTerm):
					tfIdfOfTermInDocument = dictionary[eachTerm]["idf"] * postingListOfTerm[docId]["wtd"]
					if (docId in newScores):
						newScores[docId] = newScores[docId] + (queryTermToItsLengthMap[eachTerm] * tfIdfOfTermInDocument)
					else:
						newScores[docId] = queryTermToItsLengthMap[eachTerm] * tfIdfOfTermInDocument

		for docId in newScores:
			newScores[docId] = newScores[docId] / (docIdToItsLengthMap[docId] * math.sqrt(sumOflengthOfAllQueryTerms))

		# print (newScores)
		counter = 0
		for docId in sorted(newScores, key=newScores.get, reverse=True):
			# print docId;
			print ("Doc Returned ==> " + str(docIdMapToFileNameMap[docId]))
			counter = counter + 1
			if (counter == int(k)):
				break

	def print_dict(self):
	#function to print the terms and posting list in the index
		for key in dictionary:
			print (key + " --> "+ str(dictionary[key]))

	def print_doc_list(self):
	# function to print the documents and their document id
		for key in docIdMapToFileNameMap:
			print ("Doc ID: " + str(key) + " ==> " + str(docIdMapToFileNameMap[key]))

def main():
	"""
		1) main method prompts for directory path containing input text files, path of the stop words file
		and path of the query file where all the query terms are mentioned
		2) creates an object of index class and calls build Index
		3) Once index is built, it will print dictonory
		4) Then, it will prompt for value K (How many top ranked documents to be retrieved
		5) Display's the different options of retrieval methods
		6) Enter your method of retrieval
		7) It will read each line from query file, tokenize query terms and perform search using selected method
		6) Prints time taken to fetch top K documents
	"""

	# docCollectionPath = "/Users/HarshPatil/CS429/Assignment_2_Ranked_Retrieval/collection"
	docCollectionPath = input("Enter path of text file collection ::: ")
	# stopWordsPath = "/Users/HarshPatil/CS429/Assignment_2_Ranked_Retrieval/stop-list.txt"
	stopWordsPath = input("Enter the stop words file path ::: ")
	# queryFile = "/Users/HarshPatil/CS429/Assignment_2_Ranked_Retrieval/queries"
	queryFile = input("Enter path of query file ::: ")

	indexObject = index(docCollectionPath, stopWordsPath)
	startTime = time.time()
	indexObject.buildIndex()
	endTime = time.time()
	print ("Index built in ::: %s seconds" % (endTime - startTime))

	startTime = time.time()
	indexObject.buildChampionList()
	endTime = time.time()
	print ("Champion List built in ::: %s seconds" % (endTime - startTime))

	startTime = time.time()
	indexObject.buildCluster()
	endTime = time.time()
	print ("Cluster built in ::: %s seconds" % (endTime - startTime))
	print ("")

	totalDocsToBeRetrieved = input("Enter number of docs to be retrieved ::: ")
	print ("")

	while(True):
		print ("Enter 1 for Exact Search")
		print ("Enter 2 to search using Champion List")
		print ("Enter 3 to search using Index Elimination")
		print ("Enter 4 to search using Cluster Pruning")
		print ("Enter 5 to print dictionary")
		print ("Enter 6 to print docId to file name map")
		print ("Enter Any other number to exit" + "\n")

		searchChoice = input("Enter your choice from above ::: ")
		print ("")

		QueryLines = [line.rstrip('\n') for line in open(queryFile)]
		for eachLine in QueryLines:
			wordList = re.split('\W+', eachLine)

			while '' in wordList:
				wordList.remove('')

			wordsInLowerCase = []

			for word in wordList:
				wordsInLowerCase.append(word.lower())

			if (searchChoice == "1"):
				print ("Query Terms ::: " + str(wordsInLowerCase))
				queryStartTime = time.time()
				indexObject.exact_query(wordsInLowerCase, totalDocsToBeRetrieved)
				queryEndTime = time.time()
				print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
				print ("")
			elif (searchChoice == "2"):
				print ("Query Terms ::: " + str(wordsInLowerCase))
				queryStartTime = time.time()
				indexObject.inexact_query_champion(wordsInLowerCase, totalDocsToBeRetrieved)
				queryEndTime = time.time()
				print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
				print ("")
			elif (searchChoice == "3"):
				print ("Query Terms ::: " + str(wordsInLowerCase))
				queryStartTime = time.time()
				indexObject.inexact_query_index_elimination(wordsInLowerCase, totalDocsToBeRetrieved)
				queryEndTime = time.time()
				print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
				print ("")
			elif (searchChoice == "4"):
				print ("Query Terms ::: " + str(wordsInLowerCase))
				queryStartTime = time.time()
				indexObject.inexact_query_cluster_pruning(wordsInLowerCase, totalDocsToBeRetrieved)
				queryEndTime = time.time()
				print("Retrieved in ::: %s seconds" % (queryEndTime - queryStartTime))
				print ("")
			elif (searchChoice == "5"):
				indexObject.print_dict()
				print ("")
			elif (searchChoice == "6"):
				indexObject.print_doc_list()
				print ("")
			else:
				return

if __name__ == '__main__':
    main()
