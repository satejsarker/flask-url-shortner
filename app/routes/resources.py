"""routing file for the microservice """
import logging
import uuid
from datetime import datetime

import flask
import flask_restful
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from app.core import CommonResource
from app.model import Database
from app.schema import UrL

API_BP = flask.Blueprint('api', __name__)
API = flask_restful.Api(API_BP)

LOGGER = logging.getLogger(__name__)


@API.resource('/api', methods=["GET", "POST"], strict_slashes=False, endpoint="get_api for all url")
class Shortener(CommonResource):
    main_url_table = "urls"
    hits_table = "urls_hits"
    model = Database()

    @use_args({"title": fields.Str(required=True)}, locations=['query'])
    def get(self, args):
        """get request : search on  partial or full match
        :return json object with details information
        """
        res = self.model.search_url(self.main_url_table, args['title'])
        if res is None:
            return {"msg": "search not found"}, 404
        for i in range(len(res)):
            hits, hit_times = res[i]['hits'], res[i]['hit_times']
            print(hits, hit_times)
            if len(hit_times) != 0 and hits != 0:
                ratio = self._hit_cal(all_hits=hit_times, total_hit=hits)
                res[i]['hourly_hits_ratio'] = ratio

        return UrL().dump(res,many=True), 200

    def _hit_cal(self, all_hits, total_hit):
        """hit calculation helper function """
        if len(all_hits) > 1:
            start, end = all_hits[0], all_hits[-1]
            date_time_end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
            date_time_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
            diff = date_time_end - date_time_start
            hour = diff.seconds / 3600
            print(hour)
            ratio = "{:.3f}".format(round(total_hit) / hour)
            return ratio
        return total_hit

    @use_args(UrL)
    def post(self, args):
        """
            created short url object if the title is not present yet


        :param args:
        :return:
        """
        data = args
        base_url = flask.request.base_url
        _info = uuid.uuid4()
        _id = str(_info).split('-')[0]
        short_url = f"{base_url}/{_id}"
        data.update(dict(id=str(_info).split('-')[0]
                         , hits=0, short_url=short_url))
        if self.model.insert_data(args, Shortener.main_url_table) is None:
            return {"msg": "insert failed as title already exist"}, 500
        return UrL().dump(args), 201


@API.resource('/api/<string:id>', methods=["GET"], strict_slashes=False, endpoint="get_api_short_url")
class ShortenerAPi(CommonResource):
    """redirect to the full url """
    main_url_table = "urls"
    hits_table = "urls_hits"
    model = Database()

    @use_kwargs({"id": fields.Str(required=True)}, locations=['view_args'])
    def get(self, **kwargs):
        """url will be redirect and calculate the hit and ratio for the short url"""
        update, res = self.model.update_url(self.main_url_table, kwargs['id'])
        if res is None:
            return {"msg": "search Url not found"}, 404
        redirect_url = res['full_url']
        return flask.redirect(redirect_url)
