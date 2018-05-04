import feedparser
import time
from dateutil import parser
import MySQLdb

class rss_crawler_own:
    def __init__ (self,file_path,ip,user1,password,data_base,table):

        self.list_of_links=self.get_list_of_links(file_path)  # read file(with all rss links of 1 country) from path and store all links in the list

        self.errors=""
        self.error_count=0
        self.error_count=self.error_count+1



        self.db = MySQLdb.connect(host=ip, user=user1, passwd=password, db=data_base)
        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        self.cur = self.db.cursor()
        i=0

        for link1 in self.list_of_links:
                                                    # for every link, read the newsfeed on that page
                                                    #   and  update it in our sql server if not already present

            feed = self.crawl(link1)

            newspaper = self.which_newspaper(link1)

            for key in feed['entries']:
                try:


                            title = (key['title']).encode('latin-1', 'ignore')
                            id = (key['id']).encode('latin-1', 'ignore')

                            summary = (key['summary']).encode('latin-1', 'ignore')
                            link = (key['link']).encode('latin-1', 'ignore')
                            date1 = (key['published']).encode('latin-1', 'ignore')




                            h = (self.hash(id))
                            intdate = int(self.convert_date_to_int(date1))
                            article_downloaded = 0
                            already_present_or_not =( self.check_already_present(hash, id,table))

                            try:
                                if already_present_or_not == 0:
                                    self.add_to_database(id, link, date1, intdate, summary, title, article_downloaded, newspaper, h,table)

                            except Exception as e:
                                self.errors= self.errors + 'error in insert mainfun  ' + str(e) + '\n '
                                self.error_count = self.error_count + 1


                except Exception as e:
                    self.errors = self.errors + 'error in ::' + link1 + str(e) + '\n'
                    self.error_count = self.error_count + 1



    def crawl(self,link):
        feed = feedparser.parse(link)
        return feed


    def get_list_of_links(self,file_path):
        with open(file_path) as f:
            lines = f.read().splitlines()
        return lines

    def which_newspaper(self,link):

        sub = link[7:19]
        if sub == 'timesofindia':
            return 'toi'
        sub = link[11:19]
        if sub == 'thehindu':
            return 'thehindu'

        sub = link[11:25]
        if sub == 'hindustantimes':
            return 'hindustantimes'

        sub = link[7:20]
        if sub == 'indianexpress':
            return 'indianexpress'

        sub = link[11:23]
        if sub == 'tribuneindia':
            return 'tribuneindia'
        sub = link[11:20]
        if sub == 'dailypost':
            return 'dailypost'

        sub = link[7:32]
        if sub == 'feeds.feedburner.com/ndtv':
            return 'ndtv'

        sub = link[7:30]
        if sub == 'feeds.feedburner.com/ga':
            return 'ndtv'


        sub = link[7:17]

        if sub == 'feeds.bbci':
            return 'bbc'

        sub = link[7:20]
        if sub == 'feeds.reuters':
            return 'reuters'

        sub = link[28:31]
        if sub == 'Geo' or sub == 'geo':
            return 'geo'

        sub = link[28:32]
        if sub == 'Asia':
            return 'asianet'



        sub = link[11:16]
        if sub == 'samaa':
            return 'samaa.tv'

        sub = link[13:30]
        if sub == 'pakistantelegraph':
            return 'pakistantelegraph'

        sub = link[7:14]
        if sub == 'arynews':
            return 'arynews'

        sub = link[11:17]
        if sub == 'suchtv':
            return 'suchtv'

        sub = link[7:14]
        if sub == 'tribune':
            return 'tribune'



        sub = link[11:14]
        if sub == 'wsj':
            return 'wall_street_journal'

        sub = link[7:18]
        if sub == 'rss.nytimes':
            return 'ny_times'

        sub = link[7:24]
        if sub == 'rssfeeds.usatoday':
            return 'usa_today'

        sub = link[7:22]
        if sub == 'www.latimes.com':
            return 'la_times'

        sub = link[7:13]
        if sub == 'nypost':
            return 'ny_post'

        sub = link[7:27]
        if sub == 'feeds.washingtonpost':
            return 'washington_post'

        sub = link[7:22]
        if sub == 'www.nydailynews':
            return 'ny_daily'

        sub = link[7:18]
        if sub == 'chicagopost':
            return 'chicago_post'

        sub = link[11:17]
        if sub == 'denver':
            return 'denverpost'

        sub = link[7:24]
        if sub == 'www.chicagotribune':
            return 'chicago_tribune'

        # extract newspapername from link
        return 'other'

    def convert_date_to_int(self,str1):
        #     convert date to integer value
        dt = parser.parse(str1)
        str1 = str(dt.date())
        str1 = str1.replace('-', '')
        return str1

    def hash(self,str):
        try:
            h = 0
            for i, c in enumerate(str):
                h = h + ord(c) * i
            return h
        except:
            print 'error in hash'
            return 0

    def __unicode__(self):
        return unicode(self.some_field) or u''


    def check_already_present(self,h, id1,table):
        try:
            self.cur.execute("""SELECT id from """ + table + """ where hash_of_id= %s """, (h,))
            self.db.commit()
            x = self.cur.fetchall()
            # print len(x)
            for row in x:

                if row == id1:
                    return 1

            return 0

        except:

            return 0

    def add_to_database(self,id, link, date1, intdate, summary, title, article_downloaded, newspaper, h,table):

        try:
            self.cur.execute("""INSERT INTO """ + table + """ VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (id, link, date1, intdate, summary, title, article_downloaded, newspaper, h))
            self.db.commit()

        except MySQLdb.Error, e:
            self.errors = self.errors +'sql insertion error in :: ' + link +'    ' + str(e) + '\n'
            self.error_count = self.error_count + 1
            pass



