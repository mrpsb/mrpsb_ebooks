import random
import twitter
import markov_2
import pyttsx
import sys
import urllib
import images

from local_settings import *

# Edited for running direct on Ras Pi using cron
# Instead of giving up on a failed tweet retries until success
# Altered to bring in pre-prepared brain from disk

try:
    if sys.argv[1] == "JFDI":
        ODDS = 1
except:
    pass

def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

if __name__=="__main__":
        
    if DEBUG==False:
        guess = random.choice(range(ODDS))
    else:
        guess = 0

    if guess == 0:
        if DEBUG == False:
            api = connect()
                           
        success = False
        imgtweet = False

        # Read back brain generated by ingest.py
        mine = markov_2.MarkovChainer(2,BRAIN_PATH)

        # this section does the actual building of tweet
        # changed it to try again on failure, default was to just give up

        while success == False:
            
            ebook_tweet = ""  # this clears out any previous unsuccessful attempt
            
            ebook_tweet = mine.generate_sentence()
   
            # if a tweet is very short, this uses it to search imgur with the
            # tweet as query and post the tweet with the image
            
            if ebook_tweet != None and len(ebook_tweet) < 80:

                if mine.duplicate_tweet(ebook_tweet) == False:

                    print "I'm going to post a disgusting image: " + ebook_tweet
                    # connect to Google Image Search, search for an image, if you don't find
                    # one then don't bother

                    img = images.grabImage(images.searchCleanup(ebook_tweet))

                    if len(img) > 0:
                    # Quite a few sites don't like being hit for direct download
                    # With HTTPlib so just give up for now and drop the image
                    # Further investigation needed!                        
			try:
			    print "Image Found " + img
                            grabfile = urllib.URLopener()
                            print "Grabbing file " + img
                            imgfile = grabfile.retrieve(img)

                            success = True
                            imgtweet = True
                        except:
                            print "This site doesn't like me touching it"
                            success = True
                            imgtweet = False

                    else:
                        print "No Image Found"
                        success = True
                        imgtweet = False

                else:
                    ebook_tweet += " " + mine.generate_sentence()
                    imgtweet = False

            if imgtweet == False:
                #throw out tweets that match anything from the source account.
                if ebook_tweet != None and len(ebook_tweet) < 138:

                    print "Success!"
                    success = True

                    if mine.duplicate_tweet(ebook_tweet) == False:
                        pass
                    else:
                        print "TOO SIMILAR: " + ebook_tweet
                        success = False
                        imgtweet = False

                elif ebook_tweet == None:
                    print "I done goofed, there's nothing in the tweet"
                    success = False
                elif len(ebook_tweet) >= 120:
                    print "That's too long, whoopsypoops"
                    success = False
                else:
                    print "I have no idea what I'm doing"
                    success = False
            
        # Couldn't find anything wrong with the tweet so here goes
            if success == True:
                if DEBUG == False:
                    if imgtweet == True:
                        # status = api.PostMedia(ebook_tweet, open(imgfile[0],"rb"))
						
			if random.choice(range(10)) == 0:
                            print "OH SHIT YOU ROLLED A 10 THINGS ARE GOING TO GET POLITICAL"
			    status = api.PostMedia("So much for the tolerant left", open(imgfile[0],"rb"))
			else:
	                    status = api.PostMedia(ebook_tweet, open(imgfile[0],"rb"))
						
                        print status.text.encode('UTF-8')

                    else:
                        status = api.PostUpdate(ebook_tweet)
                        s = status.text.encode('utf-8')
                        print s
                        spk = pyttsx.init()
                        spk.setProperty('rate',100)
                        spk.setProperty('voice','english_rp')
                        spk.say(s)
                        spk.runAndWait()
                        
                else:
                    print "SUCCESS: " + ebook_tweet
                
    else:
        print "This time I'm not doing a tweet, so there" #message if the random number fails.
