from flask import jsonify
from flask_restful import Resource
from libs.adsRequests import AdsRequests


class Ads(Resource):

    def get(self, key):
        ads = AdsRequests()
        response = ads.getDictData(key)
        return jsonify(response)
