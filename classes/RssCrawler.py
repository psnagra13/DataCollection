import feedparser
import datetime

logFolderPath = "logs/rssFeedCrawler/"


def getRssFeedsOnLink(rssLink):

    now = datetime.datetime.now()
    logString = now.strftime("%Y%m%d %H:%M:%S") + "  Processing " + rssLink + "\n"

    rssFeeds = feedparser.parse(rssLink)


    listOfRssFeedObjects = []

    for rssFeed in rssFeeds['entries']:

        try:
            title = (rssFeed['title']).encode('latin-1', 'ignore')

            summary = (rssFeed['summary']).encode('latin-1', 'ignore')
            link = (rssFeed['link']).encode('latin-1', 'ignore')
            date = (rssFeed['published']).encode('latin-1', 'ignore')
            try:
                id = (rssFeed['id']).encode('latin-1', 'ignore')
            except:
                id = link

            rssFeedObject = { "title" :  title , "id":id , "summary":summary , "link" : link , "date": date  }

            listOfRssFeedObjects.append( rssFeedObject )

        except Exception as e:
            logString =  logString  +  str(e) + '\n'


    logString = logString + "Number of Links Crawled = " + str(len(listOfRssFeedObjects)) + "\n"
    writeLogToFile(logString )

    return listOfRssFeedObjects


def writeLogToFile(logString):
    now = datetime.datetime.now()
    todayDate = str(now.strftime("%Y%m%d"))
    with open(logFolderPath + todayDate , "a") as myfile:
        myfile.write(logString + "********************************************************************************************************************************\n\n")


if __name__ == "__main__":
    getRssFeedsOnLink("http://www.tribuneindia.com/rss/feed.aspx?cat_id=5")

