import random
import markov_2
import sys
from local_settings import *
# Edited for running direct on Ras Pi using cron
# Instead of giving up on a failed tweet retries until success
# Altered to bring in pre-prepared brain from disk


if __name__=="__main__":
      
        # Read back brain generated by ingest.py
    mine = markov_2.MarkovChainer(2,BRAIN_PATH)

        # this section does the actual building of tweet
        # changed it to try again on failure, default was to just give up
                        
    for i in range(0,49):
        print mine.generate_sentence()