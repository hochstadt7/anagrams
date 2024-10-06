A small web service for printing similar words in the English language.
Two words w_1 and w_2 are considered similar if w_1 is a letter permutation of w_2 (e.g., "stressed" and "desserts").

In addition, statistics of the service itself are provided, such as:
- Total number of words in the dictionary
- Total number of requests (not including "stats" requests)
- Average time for request handling in nanoseconds (not including "stats" requests)

For the web service, I chose to use the Flask web framework for Python that allows to build web applications and services
quickly and easily. It is a good framework for small to medium applications.

To make it run, as if it is run on Linux environment, I used Dockerfile which uses the python:3.12,
linux based, image.

In the core code of the service, a dictionary which holds the anagrams is pre-computed.
The values are lists of words which are anagrams of each other, and the keys are the sorted
string corresponding to those anagrams.
This dictionary is pre-computed to improve run-time performance when querying anagrams for a given word.

Due to possible synchronization issues, I put a lock when updating some of the variables used to compute
the stats of the service.
