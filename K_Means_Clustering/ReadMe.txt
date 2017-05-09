                                              How to run
===========================================================================================================
1) Unzip given file
2) Make sure you have python installed on your pc. I have used 3.6.0 version
3) Open terminal
4) Excute below commands
    a) python kmeans.py
    b) It will ask you to enter the file path containing input text files.
        Example - "/Users/HarshPatil/CS429/Assignment_5_K_Means/time/TIME.ALL"
    c) It will ask you to enter path of the stop words file (file, where all the stop words are written).
        Example - "/Users/HarshPatil/CS429/Assignment_5_K_Means/time/TIME.STP"
    d) It will ask you to enter the number of clusters to be created
        Example - 5
    e) It will build index and generate document vector for each doc
    f) It will start computing. Once computation is complete:
        - It will print nearest document for each cluster
        - RSS value of each cluster
        - Members of each cluster
        - Average RSS value
        - Total time taken for computation

5) Have a look at attached "Output.txt" file to view entire result.