# Ear-Decomposition-Analysis
Analysis of the Schmidt's (2013b) algorithm for finding Ear (Chain) decomposition of a graph and checking its connectivity

##Ear Decomposition algorithm
Steps:
1. Go through each unvisited node (visit it), start the Block with it.
  2. Find DFS tree from that node
  3. Go through each DFS tree node N1
    4. Find a backedge from N1:
      * If there is none, continue 3rd step
      * If there is a backedge, start an Ear with N1:
    5. Go through backedge, visit new node N2, and continue identifying the Ear
    6. Go to parent node N3 of N2 in DFS tree.
    7. Repeat step 6 until N3 is a node that was already visited before
    8. Append Ear to the block
  9. Append Block to the block list
10. When all nodes are visited return the block list


##Analysis
* Time efficiency with different graph scale
* Time efficiency with different graph type
* Time efficiency with different edge density
* Time efficiency compared to other block finding algorithms


##Sources
Author: ramchandra (2020)
https://codeforces.com/blog/entry/80932

Author: Jens M. Schmidt (2019)
https://arxiv.org/ftp/arxiv/papers/1209/1209.0700.pdf


##Run it online
https://colab.research.google.com/drive/1tnwNdPF2X5UZlzxnf1AgTHC3ccmBX0sl?usp=sharing
