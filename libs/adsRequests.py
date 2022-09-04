import os
import requests


class AdsRequests:

    # Constructor
    def __init__(self):
        self._token = "TnEWAPDi8n5R3taijqXleJDTZ5LNDr2LMJjOOsec"
        self._endpoint = "https://api.adsabs.harvard.edu/v1/search/query?q={key}&rows=200&fl=author,title,pub,bibcode,doi,volume,year,page_range,links_data&sort=date desc"


    def getDictData(self, key: str) -> dict:
        """
        Función para realizar una petición al ENDPOINT y que regresa un dict con la información limpia
        :param key: Llave de la búsqueda
        :return: Retorna un dict con la información recopilada limpia
        """

        response = requests.get(self._endpoint.format(key=key), headers={'Authorization': 'Bearer ' + self._token})
        data = self._getCleanDictWithAllArticles(response.json())
        return data

    @staticmethod
    def _getCleanDataByArticle(data: dict) -> dict:
        """
        Función que regresa un dict con la información de un artículo
        :param data: Un dict con la información del artículo en sucio
        :return: Un dict con la información del artículo en limpio
        """
        keys = data.keys()
        return {
            'authors': "".join(map(str, data['author'])),
            'title': data['title'][0],
            'pub': data['pub'],
            'url': "url",
            'bibcode': data['bibcode'],
            'doi': data['doi'][0],
            'page_range': data['page_range'] if 'page_range' in keys else "Undefined",
            'volume': data['volume'],
            'year': data['year'],
        }

    def _getCleanDictWithAllArticles(self, data: dict) -> dict:
        """
        Función que realiza una petición al ENDPOINT y que regresa la información limpia para el usuario final
        :param data: Un dict con la información obtenida de la petición al ENDPOINT.
        :return: Un dict con la información de todos los artículos en limpio
        """
        dict_data = {}
        count = 0
        for element in data['response']['docs']:
            element_data = self._getCleanDataByArticle(element)
            dict_data[count] = element_data
            count += 1
        return dict_data