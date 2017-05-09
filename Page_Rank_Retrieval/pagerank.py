#Python 3.0
import re
import os
import collections
import time
#import other modules as needed

class pagerank:

	def __init__(self, inputFilePath, outputFilePath):
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		self.totalPages = 0
		self.totalLinks = 0
		self.alpha = 0.15
		self.topK = 10
		self.matrix = self.readInputFileAndCreateTransitionMatrixWithTeleporting()
		pass

	"""This method computes page rank and writes top 10 pages to console.
	It maintains page rank of all documents in the output file"""
	def pagerank(self, input_file):
		#function to implement pagerank algorithm
		#input_file - input file that follows the format provided in the assignment description

		powerVector = self.createPageRankByPowerMethod()
		# print(powerVector)
		pageIdToPageRankMap = {}
		for id in range(len(powerVector)):
			pageIdToPageRankMap[id] = powerVector[id]

		output = open(self.outputFilePath, 'w')
		counter = 0
		for id in sorted(pageIdToPageRankMap, key=pageIdToPageRankMap.get, reverse=True):
			counter = counter+1
			if(counter <= self.topK):
				print("Page Id:" + str(id) + ", Page Rank:" + str(pageIdToPageRankMap[id]))
			output.write("Page Id:" + str(id) + ", Page Rank:" + str(pageIdToPageRankMap[id]))
			output.write("\n")

	"""This method computes adjacency matrix after applying teleportation rate"""
	def readInputFileAndCreateTransitionMatrixWithTeleporting(self):
		lineNumber = 0
		for eachLine in open(self.inputFilePath, 'rt').readlines():
			if(lineNumber == 0):
				self.totalPages = int(eachLine.strip())
				matrix = [[0 for i in range(self.totalPages)] for j in range(self.totalPages)]
			elif(lineNumber == 1):
				totalLinks = int(eachLine.strip())
			else:
				link = re.split('\W+', eachLine.strip())
				matrix[int(link[0])][int(link[1])] = 1
			lineNumber = lineNumber + 1

		multiplier = (self.alpha/self.totalPages)
		for i in range(self.totalPages):
			links = 0;
			for j in range(self.totalPages):
				if(matrix[i][j] == 1):
					links = links+1
			for j in range(self.totalPages):
				if(links != 0):
					probability = (1-((self.totalPages-links)*multiplier))/links
					probability = round(probability, 2)
				if(matrix[i][j]==0):
					matrix[i][j]=multiplier
				elif(matrix[i][j]==1):
					matrix[i][j] = probability
		# print(matrix)
		return matrix

	"""Computes page rank using iterative power method.
	Convergence happens when the difference between sum of power vector across iterations
	is less than 0.0001. This value was set as per standard TextRank algorithm."""
	def createPageRankByPowerMethod(self):
		firstVector=[]
		secondVector=[]
		for i in range(self.totalPages):
			firstVector.append(self.alpha)
			secondVector.append(self.alpha)

		while(True):
			for i in range(len(firstVector)):
				newValue = 0.0
				for j in range(self.totalPages):
					newValue = newValue + (firstVector[j]*self.matrix[j][i])
				secondVector[i] = newValue
			firstVectorSum = sum(firstVector)
			secondVectorSum = sum(secondVector)
			if(abs(firstVectorSum-secondVectorSum) <= 0.0001):
				return firstVector
			else:
				firstVector=secondVector.copy()

def main():
	# inputFile = "/Users/HarshPatil/CS429/Assignment_4_Page_Rank/test1.txt"
	inputFile = input("Enter path of the input file ::: ")
	# outputFile = "/Users/HarshPatil/CS429/Assignment_4_Page_Rank/output.txt"
	outputFile = input("Enter path of the output file ::: ")
	pagerankObject = pagerank(inputFile, outputFile);
	pagerankObject.pagerank(inputFile)

if __name__ == '__main__':
    main()
