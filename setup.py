import bs4
from urllib.request import urlopen as openURL
from bs4 import BeautifulSoup as soup

productDict = {'A': "4k Monitors", 'B': "1TB SSDs", 'C': "Powerful Graphics Cards"}


def getPage(url) -> [["item_container"]]:
    """open URL and returns its HTML code parsedPage"""
    pageList = []

    sortByRating = "&Order=RATING"
    pageSize = "&PageSize=96"
    pageNumber = "&page="
    numPages = numOfProducts // 96 + 1
    for n in range(numPages):
        newUrl = url + sortByRating + pageSize + pageNumber + str(n + 1)
        webData = openURL(newUrl)
        webText = webData.read()
        webData.close()

        parsedPage = soup(webText, "html.parser")
        pageList.append(parsedPage.findAll("div", {"class", "item-container"}))
    return pageList


def displayLowestPriceoftheBestRated(allPages: [["item_container"]], productName: str, numOfProducts: int):
    """find and display product with lowest price on page"""
    lowestPrice = -1
    lowestPriceTitle = ""
    processedProducts = 0
    for page in allPages:  # loop through each page of 96 products per page
        for product in page:  # look through all 96 products on page
            if processedProducts == numOfProducts:  # if searched num is what user asked for, we are done
                break

            allStrongs = product.findAll("strong")  # price is in one of the strong sections
            title = product.find("a", {"class", "item-title"})  # title is found here with .text tag

            price = 0
            for sub in allStrongs:
                try:
                    price = int(sub.string)  # if doesnt error, price is now the price for this product
                except ValueError:
                    continue

            if price != 0 and price < lowestPrice or lowestPrice == -1:
                lowestPrice = price
                lowestPriceTitle = title

            processedProducts += 1

    print(f"The cheapest product amongst the {numOfProducts} best rated {productName} on Newegg is:\n"
          f"  {lowestPriceTitle.text}\n  Price: ${str(lowestPrice)}\n")


if __name__ == '__main__':
    productSelection = input("Which product(s) would you like to look at?\n" +
                             "    A) 4k Monitors\n" +
                             "    B) 1TB SSDs\n" +
                             "    C) Powerful Graphics Cards\n" +
                             "    D) All of the above\n").strip().upper()
    while True:
        try:
            numOfProducts = int(input("How many of the top products would you like to process?\n"))
            if numOfProducts > 0:
                break
        except ValueError:
            "do nothing"
        print("Please enter a valid positive integer.")

    if productSelection in 'AD':
        FourKmonitorUrlRating = "https://www.newegg.com/p/pl?N=100160979%20601305587"
        displayLowestPriceoftheBestRated(getPage(FourKmonitorUrlRating), productDict['A'], numOfProducts)

    if productSelection in 'BD':
        SSD_1TBUrlRating = "https://www.newegg.com/p/pl?N=100011693%20600414920"
        displayLowestPriceoftheBestRated(getPage(SSD_1TBUrlRating), productDict['B'], numOfProducts)

    if productSelection in 'CD':
        bestGPUsUrlRating = "https://www.newegg.com/p/pl?N=100007709%20601321572%20600419577%20600565061%20601202919" \
                            "%20601203927%20601305993%20601203901%20601294835%20601295933%20601194948%20601330988" \
                            "%20601329884"
        displayLowestPriceoftheBestRated(getPage(bestGPUsUrlRating), productDict['C'], numOfProducts)
