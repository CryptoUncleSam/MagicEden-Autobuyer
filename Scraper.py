import requests


class Scraper:
    def __init__(self, config):
        self.baseUrl = 'https://api-mainnet.magiceden.dev/v2/'
        self.config = config


    def getCollections(self):
        print("Getting all collections from MagicEden.io...")

        collections = list()
        counter = 0

        while True:
            response = requests.get(self.baseUrl + f"collections?offset={counter}").json()
            if len(response) < 1:
                break

            for i in range(len(response)):
                collections.append({"symbol": response[i]['symbol'], "name": response[i]['name']})

            counter += len(response)

        print("Done\n")
        return collections


    def getListing(self, symbol):
        print('Getting all the NFT from the marketplace...')

        listings = list()
        try:
            response = requests.get(self.baseUrl + f'collections/{symbol}/listings?offset=0').json()
            for i in range(len(response)):
                listings.append({'price': response[i]['price'], 'tokenMint': response[i]['tokenMint']})
        except Exception as e:
            print(e)

        return listings


    def getEligibleListings(self, listings):
        eligibleListings = list()
        listingPrices = list()

        for listing in listings:
            if listing['price'] <= self.config['willingPrice']:
                eligibleListings.append(listing)
                listingPrices.append(listing['price'])

        return eligibleListings, listingPrices
