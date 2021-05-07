import json
import requests


class GooglePatentsAPI():

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
        self.updateResultQuery()

    def updateResultQuery(self):
        self.resultQuery = f'q={self.op}&op={self.op}&page={self.page}'

    def getPagePatents(self):
        if self.resultQuery == '':
            raise ValueError(
                "No query specified, use setQuery method to specify the query.")
        params = {'url': self.resultQuery, 'exp': ''}
        response = requests.get(self.__baseQueryUrl, params=params)
        jsonResponse = json.loads(response.text)
        results = jsonResponse['results']
        self.chemExhausted = results['chem_exhausted']
        self.cluster = results['cluster']
        self.manyResults = results['many_results']
        self.numPage = results['num_page']
        self.summary = results['summary']
        self.totalNumPages = results['total_num_pages']
        self.totalNumResults = results['total_num_results']
        self.patents = self.cluster[0]['result']
        return self.patents

    def getPage(self):
        return self.page
