from classes import RssLinksReadFromFile
from classes import RssCrawler


RssLinksFilePathList = ["resources/rssLinks/listOfRssLinksIndia"]

for RssLinksFilePath in RssLinksFilePathList:

    # Get dictionary of RssLinks in the form of dictionary { rssLink : newspaperName }
    rssLinksListOfObjects = RssLinksReadFromFile.getRssLinks(RssLinksFilePath)

    for rssLinkObject in rssLinksListOfObjects:

        rssLink = rssLinkObject['rssLink']
        newspaperName = rssLinkObject['newspaperName']

        listOfRssFeedsPublished= RssCrawler.getRssFeedsOnLink(rssLink)

        print listOfRssFeedsPublished







