#Python 3.0
import re
import os
import collections
import time
import math
from itertools import groupby
import random
from copy import deepcopy
import numpy
#import other modules as needed
#implement other functions as needed

class kmeans:
	def __init__(self,path_to_collection, stopWordsPath):
		self.docPath = path_to_collection
		self.stopWordsPath = stopWordsPath
		self.totalNumberOfDocuments = 0
		self.dictionary = {}
		self.docIdMapToFileNameMap = {}
		self.docIdToItsTermTfIdfMap = {}
		self.stopWords = []
		self.docIdToItsVectorMap = {}
		self.totalNumberOfClusters = 0
		self.initialRandomCentroids = {}
		self.centroidToVectorMap = {}
		self.clusterToMembersMap = {}
		self.previousCentroidToMemberMap = {}
		pass

	def buildIndexAndCalculateTfIdf(self):
		self.getStopWordsList()

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
		i = 0;
		for eachFile in fileList:
			position = 1
			fileNameLines = [line.rstrip('\n') for line in fileNames[i]]

			for eachLine in fileNameLines:
				wordList = re.split('\W+', eachLine)

			self.docIdMapToFileNameMap[docId] = wordList[2]
			i = i + 1
			self.docIdToItsTermTfIdfMap[docId] = {}
			lines = [line.rstrip('\n') for line in eachFile]

			for eachLine in lines:
				wordList = re.split('\W+', eachLine)
				while '' in wordList:
					wordList.remove('')

				for word in wordList:
					if (word not in self.stopWords):
						if (word.lower() in self.dictionary):
							dictionaryValue = self.dictionary[word.lower()]
							docList = dictionaryValue["docList"]
							if (docId in docList):
								positionList = docList[docId]
								positionList["positionList"].append(position)
								wtd = 1.0 + math.log10(len(positionList["positionList"]))
								positionList["wtd"] = wtd
								position = position + 1
								termFreq = self.docIdToItsTermTfIdfMap[docId][word.lower()]["termFreq"]
								termFreq = termFreq + 1
								self.docIdToItsTermTfIdfMap[docId][word.lower()] = {"tfIdf": (wtd * dictionaryValue["idf"]),
																			   "termFreq": termFreq}
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
								self.docIdToItsTermTfIdfMap[docId][word.lower()] = {"tfIdf": (wtd * dictionaryValue["idf"]),
																			   "termFreq": termFreq}
							# print (docIdToItsTermTfIdfMap[docId][word.lower()])
						else:
							idf = math.log10(self.totalNumberOfDocuments)
							wtd = 1.0 + math.log10(1.0)
							self.dictionary[word.lower()] = {"idf": idf,
														"docList": {docId: {"wtd": wtd, "positionList": [position]}}}
							position = position + 1
							termFreq = 1
							self.docIdToItsTermTfIdfMap[docId][word.lower()] = {"tfIdf": (wtd * idf), "termFreq": termFreq}
						# print (docIdToItsTermTfIdfMap[docId][word.lower()])
					else:
						continue
			docId = docId + 1
		# print (self.docIdToItsTermTfIdfMap[1])

	def getStopWordsList(self):
		"""This method will list the stop words by tokenizing each word from stop words file"""
		stopWordsLines = [line.rstrip('\n') for line in open(self.stopWordsPath)]
		for eachLine in stopWordsLines:
			stopWordsList = re.split('\W+', eachLine)
			while '' in stopWordsList:
				stopWordsList.remove('')

			for eachWord in stopWordsList:
				self.stopWords.append(eachWord)

	def buildDocumentVector(self):
		for eachDocId in self.docIdToItsTermTfIdfMap:
			self.docIdToItsVectorMap[eachDocId] = []
			for eachTerm in self.dictionary:
				if(eachTerm in self.docIdToItsTermTfIdfMap[eachDocId]):
					self.docIdToItsVectorMap[eachDocId].append(self.docIdToItsTermTfIdfMap[eachDocId][eachTerm]["tfIdf"])
				else:
					self.docIdToItsVectorMap[eachDocId].append(0)
		# print (self.docIdToItsVectorMap[42])
		# print (str(self.totalNumberOfDocuments))

	def clustering(self, kvalue):
	#function to implement kmeans clustering algorithm
	#Print out:
	##For each cluster, its RSS values and the document ID of the document closest to its centroid.
    ##Average RSS value
	##Time taken for computation.
		self.totalNumberOfClusters = kvalue
		count = 0
		while (True):
			self.initialRandomCentroids[(random.randint(1, self.totalNumberOfDocuments))] = {}
			count = count + 1
			self.clusterToMembersMap[count]=[]
			if (count == self.totalNumberOfClusters):
				break

		count = 1
		for eachDocId in self.initialRandomCentroids:
			self.centroidToVectorMap[count]=self.docIdToItsVectorMap[eachDocId]
			count = count+1

		stoppingCondition = False
		iterations=0
		while(iterations<20 and stoppingCondition is False):
			self.calculateDistanceFromCentroidAndAssignMembers()
			iterations=iterations+1
			stoppingCondition = self.checkStoppingCondition();
			print ("Running Iteration #"+str(iterations))
			self.calculateNewCentroidVector()

	def calculateDistanceFromCentroidAndAssignMembers(self):
		for eachDoc in self.docIdToItsVectorMap:
			distanceList = {}
			for eachCentroid in self.centroidToVectorMap:
				distance = self.calculateEuclideanDistance(self.docIdToItsVectorMap[eachDoc], self.centroidToVectorMap[eachCentroid])
				distanceList[eachCentroid]=distance
			newClusterId=min(distanceList, key=distanceList.get)
			if(newClusterId not in self.clusterToMembersMap):
				self.clusterToMembersMap[newClusterId] = [eachDoc]
			else:
				self.clusterToMembersMap[newClusterId].append(eachDoc)

	def checkStoppingCondition(self):
		count=0;
		for eachCluster in self.clusterToMembersMap:
			if(len(self.previousCentroidToMemberMap)!=0 and self.previousCentroidToMemberMap[eachCluster] == self.clusterToMembersMap[eachCluster]):
				count=count+1;
		if(count==len(self.clusterToMembersMap)):
			return True
		self.previousCentroidToMemberMap = deepcopy(self.clusterToMembersMap)
		return False;

	def calculateNewCentroidVector(self):
		for k in range(1, self.totalNumberOfClusters+1):
			newCentroid = [];
			count=0;
			for eachDoc in self.clusterToMembersMap[k]:
				if (count == 0):
					newCentroid = deepcopy(self.docIdToItsVectorMap[eachDoc]);
				else:
					for i in range(0, len(self.docIdToItsVectorMap[eachDoc])):
						newCentroid[i] = newCentroid[i] + self.docIdToItsVectorMap[eachDoc][i];
				count = count + 1;
			for i in range(0, len(newCentroid)):
				newCentroid[i] = newCentroid[i] / count;
			self.centroidToVectorMap[k] = newCentroid
			self.clusterToMembersMap[k]=[]

	def calculateEuclideanDistance(self, vector1, vector2):
		#distance = numpy.linalg.norm(numpy.array(vector1) - numpy.array(vector2))
		distance = 0.0
		for i in range(0, len(vector1)):
			distance = distance + ((vector1[i] - vector2[i]) ** 2)
		distance = math.sqrt(distance);
		return distance

	def outputResult(self):
		avgRSS = 0.0
		for eachCluster in self.previousCentroidToMemberMap:
			distanceList = {}
			RSS = 0.0
			for eachMember in self.previousCentroidToMemberMap[eachCluster]:
				#distance = numpy.linalg.norm(numpy.array(self.centroidToVectorMap[eachCluster]) - numpy.array(self.docIdToItsVectorMap[eachMember]))
				distance = 0.0
				for i in range(0, len(self.centroidToVectorMap[eachCluster])):
					distance = distance + ((self.centroidToVectorMap[eachCluster][i] - self.docIdToItsVectorMap[eachMember][i]) ** 2)
				distance = math.sqrt(distance);
				RSS = RSS + (distance**2)
				distanceList[eachMember]=distance
			nearestDocToCentroid = min(distanceList, key=distanceList.get)
			print ("")
			print ("Cluster "+ str(eachCluster) + " nearest document :: "+ str(nearestDocToCentroid))
			print ("Cluster " + str(eachCluster) + " RSS value :: " + str(RSS))
			print ("Cluster " + str(eachCluster) + " Members :: " + str(self.previousCentroidToMemberMap[eachCluster]))
			print ("")
			avgRSS = avgRSS+RSS
		print ("Average RSS value :: " + str(avgRSS/len(self.previousCentroidToMemberMap)))

def main():
	# docCollectionPath = "/Users/HarshPatil/CS429/Assignment_5_K_Means/time/TIME.ALL"
	docCollectionPath = input("Enter path of text file collection ::: ")
	# stopWordsPath = "/Users/HarshPatil/CS429/Assignment_5_K_Means/time/TIME.STP"
	stopWordsPath = input("Enter the stop words file path ::: ")
	# kValue = 25
	kValue = input("Enter number of clusters to be created ::: ")

	kmeansObject = kmeans(docCollectionPath, stopWordsPath)
	startTime = time.time()
	kmeansObject.buildIndexAndCalculateTfIdf()
	kmeansObject.buildDocumentVector()
	endTime = time.time()
	print ("")
	print ("Time taken to build document Vector ::: %s seconds" % (endTime - startTime))
	print ("")

	startTime = time.time()
	kmeansObject.clustering(kValue)
	kmeansObject.outputResult();
	endTime = time.time()
	print ("")
	print ("Total time taken to build cluster ::: %s seconds" % (endTime - startTime))
	print ("")

if __name__ == '__main__':
    main()