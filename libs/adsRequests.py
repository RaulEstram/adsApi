import requests

from libs.strings import getText


class AdsRequests:

    # Constructor
    def __init__(self):
        self._token = "TnEWAPDi8n5R3taijqXleJDTZ5LNDr2LMJjOOsec"
        self._endpoint = "https://api.adsabs.harvard.edu/v1/search/query?q={key}&rows=200&fl=author,title,pub,bibcode,doi,volume,year,page_range,links_dat,id,count_pages&sort=date desc"

    def getDictData(self, key: str) -> dict:
        """
        Función para realizar una petición al ENDPOINT y que regresa un dict con la información limpia
        :param key: Llave de la búsqueda
        :return: Retorna un dict con la información recopilada limpia
        """
        try:
            res = requests.get(self._endpoint.format(key=key), headers={'Authorization': 'Bearer ' + self._token})
            res = res.json()
            if 'error' in res.keys():
                return {"status": False, "error": getText("ADS_REQUESTS:ERROR_RESPONSE").format(error=res['error'])}
            data = self._getCleanDictWithAllArticles(res)
            return {"status": True, "data": data}
        except requests.exceptions.ConnectionError:
            return {"status": False, "error": getText("ADS_REQUESTS:ERROR_CONNECTION-ERROR")}
        except Exception:
            return {"status": False, "error": getText("ADS_REQUESTS:ERROR_UNKNOWN")}

    @staticmethod
    def _getCleanDataByArticle(data: dict) -> dict:
        """
        Función que regresa un dict con la información de un artículo
        :param data: Un dict con la información del artículo en sucio
        :return: Un dict con la información del artículo en limpio
        """
        keys = data.keys()
        return {
            'authors': "".join(map(str, data['author'])) if 'author' in keys else "",
            'title': data['title'][0] if 'title' in keys else "",
            'pub': data['pub'] if 'pub' in keys else "",
            'url': f"https://ui.adsabs.harvard.edu/abs/{data['bibcode'] if 'bibcode' in keys else ''}/abstract",
            'bibcode': data['bibcode'] if 'bibcode' in keys else "",
            'doi': data['doi'][0] if 'doi' in keys else "",
            'page_range': data['page_range'] if 'page_range' in keys else "",
            'volume': data['volume'] if 'volume' in keys else "",
            'year': data['year'] if 'year' in keys else "",
            'id_article': data['id'] if 'id' in keys else "",
            "page_count": data['page_count'] if 'page_count' in keys else "",
        }

    def _getCleanDictWithAllArticles(self, data: dict) -> dict:
        """
        Función que realiza una petición al ENDPOINT y que regresa la información limpia para el usuario final
        :param data: Un dict con la información obtenida de la petición al ENDPOINT.
        :return: Un dict con la información de todos los artículos en limpio
        """
        dict_data = {}
        count = 1
        for element in data['response']['docs']:
            element_data = self._getCleanDataByArticle(element)
            dict_data[count] = element_data
            count += 1
        return dict_data
