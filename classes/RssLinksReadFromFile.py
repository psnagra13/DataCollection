
## this function reads the file containing rss links
## It returns a list of Objects  : [{"rssLink" :rssLink ,"newpaperName":newspaperName }]
def getRssLinks(filePath):
    with open(filePath) as file:
        listOfLines = file.read().splitlines()

    rssLinksListOfObjects = []

    for line in listOfLines:
        lineSplit= line.split(" ")

        # If the line doesnot have valid data
        if len(lineSplit) <2:
            continue

        rssLink = lineSplit[0]
        newspaperName = lineSplit[1]
        object = {"rssLink" :rssLink ,"newspaperName":newspaperName }
        rssLinksListOfObjects.append(object)

    return rssLinksListOfObjects


if __name__ == "__main__":
    rssLinksFilePath = "../resources/rssLinks/listOfRssLinksIndia"
    print getRssLinks(rssLinksFilePath)