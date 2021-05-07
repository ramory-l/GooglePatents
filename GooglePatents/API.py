import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


class GooglePatents():

    def __init__(self):
        self.__baseQueryUrl = 'https://patents.google.com/xhr/query'
        self.resultQuery = ''
        self.page = 0

    def setQuery(self, query):
        proccessedQuery = self.__proccessQuery(query)
        self.resultQuery = f'q={proccessedQuery}'

    def __proccessQuery(self, query):
        proccessedQuery = query.replace(' ', '+')
        self.op = proccessedQuery
        proccessedQuery = f'{proccessedQuery}&op={self.op}&page={self.page}'
        return proccessedQuery

    def setPage(self, page):
        self.page = page
        self.__updateResultQuery()

    def __updateResultQuery(self):
        self.resultQuery = f'q={self.op}&op={self.op}&page={self.page}'

    def getAllPagePatents(self, saveJsonPath='patents.json'):
        patents = []
        self.getOnePagePatents()
        for page in range(self.__totalNumPages):
            self.setPage(page)
            patents.append(self.getOnePagePatents())

        flatPatentsList = []
        for patent in patents:
            flatPatentsList += patent

        with open(saveJsonPath, 'w') as outfile:
            json.dump(flatPatentsList, outfile)

        patents_df = pd.read_json(saveJsonPath)
        return patents_df

    def getOnePagePatents(self):
        if self.resultQuery == '':
            raise ValueError(
                "No query specified, use setQuery method to specify the query.")
        params = {'url': self.resultQuery, 'exp': ''}
        response = requests.get(self.__baseQueryUrl, params=params)
        jsonResponse = json.loads(response.text)
        results = jsonResponse['results']
        self.__setPagePatentsMetadata(results)
        patents = self.__cluster[0]['result']
        self.__patents = self.__proccessPatents(patents)
        return self.__patents

    def __setPagePatentsMetadata(self, results):
        self.__chemExhausted = results['chem_exhausted']
        self.__cluster = results['cluster']
        self.__manyResults = results['many_results']
        self.__numPage = results['num_page']
        self.__summary = results['summary']
        self.__totalNumPages = results['total_num_pages']
        self.__totalNumResults = results['total_num_results']

    def getPagePatentsMetadata(self):
        return {'chemExhausted': self.__chemExhausted,
                'cluster': self.__cluster,
                'manyResults': self.__manyResults,
                'numPage': self.__numPage,
                'summary': self.__summary,
                'totalNumPages': self.__totalNumPages,
                'totalNumResults': self.__totalNumResults}

    def __proccessPatents(self, patentsRaw):
        proccessedPatents = [patent['patent'] for patent in patentsRaw]
        return proccessedPatents

    def getPage(self):
        return self.page

    def getPatentFromQuery(self, patentPublicationNumber):
        baseQueryUrl = 'https://patents.google.com/xhr/result'
        params = {'id': f'patent/{patentPublicationNumber}/en',
                  'qs': self.resultQuery}
        response = requests.get(baseQueryUrl, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('span', {'itemprop': "title"})
        publicationNumber = soup.find("dd", {"itemprop": "publicationNumber"})
        countryCode = soup.find("dd", {"itemprop": "countryCode"})
        countryName = soup.find("dd", {"itemprop": "countryName"})
        priorArtKeywords = soup.find_all(
            "dd", {"itemprop": "priorArtKeywords"})
        priorArtDate = soup.find("time", {"itemprop": "priorArtDate"})
        inventors = soup.find_all("dd", {"itemprop": "inventor"})
        assigneeCurrent = soup.find("dd", {"itemprop": "assigneeCurrent"})
        assigneeOriginal = soup.find("dd", {"itemprop": "assigneeOriginal"})
        priorityDate = soup.find("time", {"itemprop": "priorityDate"})
        filingDate = soup.find("time", {"itemprop": "filingDate"})
        publicationDate = soup.find("time", {"itemprop": "publicationDate"})
        abstract = soup.find("div", {"class": "abstract"})
        return {'title': title.text.strip() if title is not None else None,
                'publicationNumber': publicationNumber.text.strip() if publicationNumber is not None else None,
                'countryCode': countryCode.text.strip() if countryCode is not None else None,
                'countryName': countryName.text.strip() if countryName is not None else None,
                'priorArtKeywords': [priorArtKeyword.text.strip() for priorArtKeyword in priorArtKeywords],
                'priorArtDate': priorArtDate.text.strip() if priorArtDate is not None else None,
                'inventors': [inventor.text.strip() for inventor in inventors],
                'assigneeCurrent': assigneeCurrent.text.strip() if assigneeCurrent is not None else None,
                'assigneeOriginal': assigneeOriginal.text.strip() if assigneeOriginal is not None else None,
                'priorityDate': priorityDate.text.strip() if priorityDate is not None else None,
                'filingDate': filingDate.text.strip() if filingDate is not None else None,
                'publicationDate': publicationDate.text.strip() if publicationDate is not None else None,
                'abstract': abstract.text.strip() if abstract is not None else None}

    def getPatentsDetailsFromJson(self, patentsJson, saveFile='detailedPatents.json'):
        patentsWithDetails = []
        with open(patentsJson, 'r') as patentsJsonFile:
            patents = json.load(patentsJsonFile)
            for patent in patents:
                patentPubNumber = patent['publication_number']
                patentFromQuery = self.getPatentFromQuery(patentPubNumber)
                patentsWithDetails.append(patentFromQuery)

        with open(saveFile, 'w') as outfile:
            json.dump(patentsWithDetails, outfile)

        patentsWithDetailDf = pd.read_json(saveFile)
        return patentsWithDetailDf
