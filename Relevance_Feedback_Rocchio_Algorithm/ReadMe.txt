                                              How to run
===========================================================================================================
1) Unzip given file
2) Make sure you have python installed on your pc. I have used 3.6.0 version
3) Open terminal
4) Excute below commands
    a) python index.py
    b) It will ask you to enter the file path containing input text files. Paste the directory path and press enter
        Example - "/Users/HarshPatil/CS429/Assignment_3_Relevance_Feedback/time/TIME.ALL"
    c) It will ask you to enter path of the stop words file (file, where all the stop words are written).
        Example - "/Users/HarshPatil/CS429/Assignment_3_Relevance_Feedback/time/TIME.STP"
    d) It will ask you to enter path of the query file (file, where the query is written). Refer "query" file
        Example - "/Users/HarshPatil/CS429/Assignment_3_Relevance_Feedback/query"
    e) It will build index and gives you an option to print dictionary and doc id to file name map
    f) Press 3 to continue
    g) It will ask you to enter total number of files to be retrieved
        enter integer value example : 8
    h) It will print top K relevant documents using cosine similarity and prompt user to input
       which method of relevance feedback to be chosen
    i) Select 1 for maual user feedback
    j) Repeat below steps 5 times.
        1) Enter number of relevant documents
        2) Enter all the relevant doc ids
        3) Enter number of non-relevant documents
        4) Enter all the non-relevant doc ids
        5) It will use Rocchio algorithm and print top K documents

    k) Run the program again
    l) Select 2 for Pseudo Relevance Feedback
    m) It will run Rocchio algorith 5 times by taking top 3 results as relevant document and print results

5) Have a look at attached "Output.txt" file to view entire result.
6) Change query in "query" file and repeat above steps