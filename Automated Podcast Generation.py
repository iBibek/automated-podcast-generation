# -*- coding: utf-8 -*-
 

#import warnings
#warnings.filterwarnings("ignore", category=RuntimeWarning)  


# Automated Podcast Generation
# BIBEK UPADHAYAY
# UNIVERSITY OF NEW HAVEN
#SUPERVISED BY: DR. VAHID Behzadan
import datetime 
today_date= datetime.datetime.today()
todays_date=today_date.strftime("%d %B %Y")
print(todays_date)

from google.cloud import texttospeech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/home/ai2/abc/key.json"
client = texttospeech.TextToSpeechClient()
voice = texttospeech.types.VoiceSelectionParams(language_code="en-US-Standard-A", ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) 
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

"""Importing feed and generating the clean text from those feed"""

import feedparser
import re
f=feedparser.parse("https://artificialintelligence-news.com/feed/") #parse the website from where the feeds need to be extracted




#Function to extract clean text only from the feed
def cleanText(HTML_text):
  ad="Interested in hearing industry leaders discuss subjects like this?"
  ad_start_length=HTML_text.find(ad)
  if(ad_start_length>0):
   HTML_text=HTML_text[:ad_start_length]
  cleanr = re.compile("<.*?>") #claen anything between html <> tags
  asciClear=re.compile("&.*?;") # clean the asci starting with & 
  cleantext = re.sub(cleanr, "", HTML_text)
  cleanedTEXT=re.sub(asciClear, "", cleantext)
  return cleanedTEXT

g=len(f.entries) #calculate the total number of feeds in entries 
sound_files=[] # stores the sound files in this list



from pydub import AudioSegment


song = AudioSegment.from_file("/home/ai2/abc/Big_Day.mp3","mp3") 

#creating different sounds from news-music.mp3
intro=song[:12000]
intro.fade_in(1000).fade_out(10000)
headlines=song[2000:6000]
headlines.fade_in(400).fade_out(3600)
track_change=song[18000:30000]
track_change.fade_in(2000).fade_out(8000)
thunder_music=song[2000:8000]
thunder_music.fade_in(1000).fade_out(3500)
end_music=song[34000:70000]
end_music.fade_in(2000).fade_out(35000)
headlines_bg=song[18000:39000]

headlines

v=[" Hello, and Good Morning. I am Rebecca.",
        " And this is Raymond ",
        "Welcome! to this episode of AI-News-by-AI. Todays date is " +todays_date +". Let's start with the today's headlines. ",
        "Thank you! For listening to our podcast. The AI NEWS BY AI is brought to you by AI. The project is created by Dr. Vahid Behzadan and his student Beebek Upadhayay from University of New Haven. Have a Good Day !"]

v

vs=[]
for i in range(len(v)):
    if(i%2)==0:
        voice = texttospeech.types.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE) 
    else:
        voice = texttospeech.types.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) 
    t2s= texttospeech.types.SynthesisInput(text=v[i]) # create the gTTS object
    response = client.synthesize_speech(t2s, voice, audio_config)

    record_name="/home/ai2/abc/audio_files/vs"+str(i)+".mp3" # provide unique name to each .wav audio files

    with open(record_name, "wb") as out: # write the response to the output file.    
        out.write(response.audio_content)
    vs.append(AudioSegment.from_mp3(record_name))

headlines_audio=[]
Description=""
h=[]
voice = texttospeech.types.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) 
for i in range(g):
    if i<6:
        feed_title=cleanText(f["entries"][i]["title"]) #extract the clean text for title
        feed_title=feed_title[:4990]+". "
        print(feed_title)
        Description=Description+feed_title
        t2s= texttospeech.types.SynthesisInput(text=feed_title) # create the gTTS object
        response = client.synthesize_speech(t2s, voice, audio_config)

        record_name="/home/ai2/abc/head"+str(i+1)+".mp3" # provide unique name to each .wav audio files

        with open(record_name, "wb") as out: # write the response to the output file.    
            out.write(response.audio_content)   
        headlines_audio.append(AudioSegment.from_mp3(record_name))# storing created audio files name in order to play them in console
        h.append(AudioSegment.from_mp3(record_name))# storing created audio files name in order to play them in console


sound_files=[]
#Working code
#including gsc in the recursive function
#RECURSIVE function in order to generate small feed(<5000 characters) and small audios and combine into one.
def feed_fragmentation(long_feed,i,j, max_length=4990): 
        
        if len(long_feed) < max_length:           
            
            t2s= texttospeech.types.SynthesisInput(text=long_feed) # create the gTTS object
            response = client.synthesize_speech(t2s, voice, audio_config)
            record_name="/home/ai2/abc/news_"+str(i)+"_"+str(j)+".mp3" # provide unique name to each .wav audio files
            with open(record_name, "wb") as out: # write the response to the output file.    
                out.write(response.audio_content)              
            if(j==1):               
                sound_files.append(record_name)# storing created audio files name in order to play them in console
            else:
                return     
        else:
            new=long_feed[:max_length]
            d_l=new[len(new)::-1].find(".")        
            cutoff=max_length-d_l
            pre_text=long_feed[:cutoff]
            process=long_feed[cutoff:]            
            t2s= texttospeech.types.SynthesisInput(text=pre_text) # create the gTTS object
            response = client.synthesize_speech(t2s, voice, audio_config)
            record_name="/home/ai2/abc/news_"+str(i)+"_"+str(j)+".mp3" # provide unique name to each .wav audio files
            with open(record_name, "wb") as out: # write the response to the output file.    
                out.write(response.audio_content)   
            j= j+1            
            feed_fragmentation(process,i,j,max_length)            
          
        if(j>1):
            
            b=song[:100]
            for r in range(j):
                b= b + AudioSegment.from_mp3("/home/ai2/abc/news_"+str(i)+"_"+str(r+1)+".mp3")                
            b.export("/home/ai2/abc/news_"+str(i)+"_"+"1"+".mp3",format="mp3")
            sound_files.append("/home/ai2/abc/news_"+str(i)+"_"+"1"+".mp3")
            

for i in range(g):
    if i<6:     
        if (i % 2) ==0:
            voice = texttospeech.types.VoiceSelectionParams(language_code="en-US-Standard-A", ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) 
        else:
            voice = texttospeech.types.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)   

        feed_title= cleanText(f["entries"][i]["title"]) #extract the clean text for title
        feed_summary=cleanText(f["entries"][i] ["content"][0]["value"]) # extract the clean text for the summary of news feed
        feed_summary=feed_summary.replace("\n"," ")
        feed=feed_summary  # WAS concatenate the news with title and summary into one                
        feed_fragmentation(feed,i,1,max_length=4990)

headlines_with_bg=[]
for i in range(len(headlines_audio)):
    headlines_with_bg.append(headlines_audio[i].overlay(headlines_bg-15))


# ------------------------------#
#Algorithm to create the headlines with continous background track with auto adjustment.
bgt=song[79000:135000] #bgt= back ground track : extracting the background music from the song
gap=3000
gt=song[:gap]-100    #gs=gap-song: this is the silent duration of song
start_gap=5000 # start gap: this is the silent gap for starting of headline
gst=song[:start_gap]-100 #song track gap for starting of headline
th=song[:1] #total_headlines : save the speech only of all the headlines
th=th+gst# adding the silent gap in the starting of headline

hbg=song[79000:109000] # hbg= headlines_BackGround : background in which headlines will be overlapped
h_length=0 # headlines total length
for i in range(len(h)):
   if(h[i]==h[-1]): #is it is the last titile of headlines then make the silent gap after that little longer, such that music gets little longer
        th = th+ h[i] + gt + gt # making the last pause longer for bg sound
   else:
        th = th+ h[i] + gt
#to make the length of the headlines speech and its background equal length, by reducing or englarging the background track
if(len(th)-len(bgt) > 0):
    bgt=bgt+bgt[:len(th)-len(bgt)]
    print(" bg track got enlarged")
else:
    bgt=bgt[:len(th)]
    print("bg tack got reduced")
hs=[] # hs= Headlines Start: the starting point for the headlines speech
he=[] # he= Headlines End: the ending point for headlines speech

# getting the value for hs and he to adjust the background track
for i in range(len(h)):
    if i==0: 
        hs.append(start_gap) 
        he.append(len(h[0])+start_gap)
    else:
        hs.append((he[i-1]+gap))
        he.append(hs[i] + len(h[i]))   

bg=song[:0] # BackGround which is going to be used, its good idea not to modify the "bgt" but make "bgt" as the source
bg=bgt[:start_gap] # add the starting gap in the actual BackGround
for i in range(len(h)):
    if(h[i]==h[-1]):
        bg=bg + (bgt[hs[i]:he[i]]-20) + bgt[he[i]:len(bgt)]
        print("ran only once")
    else:    
        bg=bg + (bgt[hs[i]:he[i]]-20) + bgt[he[i]:hs[i+1]]
gth=th.overlay(bg)    # overlapping the background track and the headlines
final_1=intro.fade_out(1000)+vs[0]+vs[1]+vs[2]+gth





#--------------------------------#






 
final_1.export("/home/ai2/abc/final_1.mp3",format="mp3")

 # The index should be written very accurately

todays_date=today_date.strftime("%d-%B-%Y")

#tm=headlines_bg[:500]-5+thunder_music.fade_in(1000)-5
tr=song[90000:105000]
tm=(tr[:3000]-10)+tr[3000:11000]+(tr[11000:].fade_out(1000))
#####################################################
end=song[144000:]
end_track=(end[:3000]-10)+(end[3000:33000])
#####################################################
final_2=AudioSegment.from_mp3("/home/ai2/abc/final_1.mp3")
for i in range(len(sound_files)):
     final_2=final_2+AudioSegment.from_mp3(sound_files[i])+tm
final_2=final_2 +vs[3]+ end_track
final_2.export("/var/www/html/ai-news/podcast-episodes/"+todays_date+"-v2.mp3",format="mp3")

 
 #create feed.rss
 #sftp://root@167.99.234.149/var/www/html/ai-news/feed.xml
 # /var/www/html/ai-news/podcast-episodes/
 #inside Item
Link="http://167.99.234.149/ai-news/feed.rss/"
this_day=today_date.strftime("%d-%b-%Y") 
PubDate=today_date.strftime("%a, %d %b %Y %H:%M:%S +0000") 
LastBuildDate=PubDate
WebMaster="AI-NEWS-BY-AI, University of New Haven"
ChannelDescription="AI-NEWS podcast is created for AI enthusiasts. For any person it is a hassel to goto different websites and search for AI news and updates. Now the users can listen to this daily podcast and can get all the updates and news around the world on AI."
Author="AI-NEWS-BY-AI, University of New Haven"
tag="tag:ai-news-by-ai:track/"+this_day
Title=todays_date
Audio_URL="/var/www/html/ai-news/podcast-episodes/"+todays_date+"-v2.mp3" 

x=len(final_2)/1000
mins=int(x/60)
secs=int(x%60)
Duration= "00:" + str(mins) + ":" + str(secs)

Summary="AI-News"+todays_date
Subtitle=Summary
Description="Artificial Intelligence "

#Item_Info=unicode(Item_Info,"utf-8")
#extract this from p1.txt and paste on .xml
Channel_Info="""

<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<atom:link href="http://167.99.234.149/ai-news/feed.rss" rel="self" type="application/rss+xml"/>
<atom:link href="http://167.99.234.149/ai-news/feed.rss" rel="next" type="application/rss+xml"/>
<title>AI-NEWS-Daily</title>
<link>"""+Link+"""</link>
<pubDate>"""+PubDate+"""</pubDate>
<lastBuildDate>"""+PubDate+"""</lastBuildDate>
<ttl>60</ttl>
<language>en</language>
<copyright>All rights reserved</copyright>
<webMaster>"""+WebMaster+"""</webMaster>
<description>"""+ChannelDescription+"""</description>
<itunes:subtitle>Podcast by AI</itunes:subtitle>
<itunes:owner>
<itunes:name>AI-NEWS-BY-AI</itunes:name>
<itunes:email>bupad1@unh.newhaven.edu</itunes:email>
</itunes:owner>
<itunes:author>"""+Author+"""</itunes:author>
<itunes:explicit>no</itunes:explicit>
<itunes:image href="http://167.99.234.149/ai-news/ai-news-by-ai.png"/>
<image>
<url>http://167.99.234.149/ai-news/ai-news-by-ai.png</url>
<title>AI-NEWS</title>
<link>http://soundcloud.com/user-188104526</link>
</image>
<itunes:category text="Technology"/>        
"""

#extracting this from p2.txt and paste on .xml
#Item block
Item_Info="""

<item>
<guid isPermaLink="false">"""+this_day+"""</guid>
<title>""" + Title +"""</title>
<pubDate>"""+PubDate+"""</pubDate>
<link>"""+Link+"""</link>
<itunes:duration>"""+Duration+"""</itunes:duration>
<itunes:author>AI</itunes:author>
<itunes:explicit>no</itunes:explicit>
<itunes:summary>"""+Summary+"""</itunes:summary>
<itunes:subtitle> """+Subtitle+"""</itunes:subtitle>
<description>"""+Description+"""</description>
<enclosure type="audio/mpeg" url= "http://167.99.234.149/ai-news/podcast-episodes/"""+todays_date+"""-v2.mp3"  length="20609820"/>
<itunes:image href="http://167.99.234.149/ai-news/ai-news-by-ai.png"/>
</item>

"""



with open("/var/www/html/ai-news/p2.txt", "r") as p2_text:
    p2=p2_text.read()

new_p2=Item_Info+p2

with open("/var/www/html/ai-news/p2.txt", "w") as p2_text:
    p2_text.write(new_p2)

#Channel_Info=unicode(Channel_Info,"utf-8")
with open("/var/www/html/ai-news/p1.txt", "r") as rss:
    r1=rss.read()

#item tags only
with open("/var/www/html/ai-news/p2.txt", "r") as rss:
    r2=rss.read()
#end of xml file
r3="""

</channel>
</rss>
"""

rss_template=r1+r2+r3
with open("/var/www/html/ai-news/feed.xml", "w") as rss:
    rss.write(rss_template)
