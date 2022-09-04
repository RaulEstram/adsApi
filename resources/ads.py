from flask import jsonify
from flask_restful import Resource
from libs.adsRequests import AdsRequests


class Ads(Resource):

    def post(self, key):
        ads = AdsRequests()
        return jsonify(ads.getDictData(key))
