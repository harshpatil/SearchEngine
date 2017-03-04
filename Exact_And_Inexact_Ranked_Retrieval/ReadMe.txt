                                              How to run
===========================================================================================================
1) Unzip given file
2) Make sure you have python installed on your pc. I have used 3.6.0 version
3) Open terminal
4) Excute below commands
    a) python index.py
    b) It will ask you to enter directory path containing input text files. Paste the directory path and press enter
        Example - "/Users/HarshPatil/CS429/Assignment_1_Boolean_Retrieval/collection"
    c) It will ask you to enter path of the stop words file (file, where all the stop words are written).
        Example - "/Users/HarshPatil/CS429/Assignment_2_Ranked_Retrieval/stop-list.txt"
    d) It will ask you to enter path of the query file (file, where all the queries are written). Refer "queries" file
        Example - "/Users/HarshPatil/CS429/Assignment_1_Boolean_Retrieval/queries"
    e) It will build index and print time taken to build index
    f) It will build champion list and print time taken to build index
    g) It will build cluster of leaders to followers and print time taken to build index
    h) It will prompt for total number of documents to be retreived
        Example - Enter 10 or 5
    i) It will display retrieval methods to chose from. Select your method and press enter
    j) It will read every line of query file, treat each line as a new query and perform search on them
    k) prints search result along with time taken.
    l) Have a look at attached "output.txt" file to view entire result.
    m) Add new query terms to "queries" file and check search results.


	                                            Performance
=============================================================================================================
    1) Avg time taken to build inverted index for given set of text file --> 1.5 to 2.5 seconds
    2) Avg time taken to build champion list for R=20 --> 0.2 to 0.4 seconds
    3) Avg time taken to build cluster --> 0.8 to 1.0 seconds

