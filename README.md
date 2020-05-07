# automated-podcast-generation
The project generates the podcast automatically by curating the content from the website and convert them into the speech file using Google WaveNet for speech generation. Program also update .XML file to publish every podcast episode into Apple's iTunes.

Frist setup the virtual environment

Install the dependencies packages:

    pip install google-cloud-texttospeech

    pip install feedparser

    pip install AudioSegment

    pip install pydub

The background music is Big_Day.mp3
The Google Text-To-Speech API needs credentials to work which should be downloaded in the .json format from Google Cloud.
It only allows <5000 characters to be converted. So the recursive funciton feed_fragmentation slice the larger text.

The program extract the text content from https://artificialintelligence-news.com/feed/. The text is first cleaned via cleanText() function


The background is added to the audio files, the volume of background is automatically adjusted by the algorithm.

For each podcast episode, the following codes get updated in the .xml file.

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
        <enclosure type="audio/mpeg" url= "http://167.99.234.149/ai-news/podcast-episodes/""" \
            +todays_date+"""-v2.mp3" \ length="20609820"/>
        <itunes:image href="http://167.99.234.149/ai-news/ai-news-by-ai.png"/>
        </item>


You can find the podcast episodes here: http://167.99.234.149/ai-news/podcast-episodes/

You can find the .XML here: http://167.99.234.149/ai-news/feed.xml

The Apple's iTunes channel link is: https://podcasts.apple.com/us/podcast/ai-news-daily/id1491115711

YouTube Video link explaining the project is: https://studio.youtube.com/video/atnHaGyWRpI/




