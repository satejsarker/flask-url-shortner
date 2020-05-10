from datetime import datetime

from marshmallow import fields, validate

from app.core import CommonSchema


class UrL(CommonSchema):
    full_url = fields.Url(required=True, validate=validate.Length(min=5), data_key="url")
    title = fields.Str(data_key="title")
    id = fields.Str()
    short_url = fields.Str()
    created_at = fields.Str(missing=str(datetime.now()))
    hit_times = fields.List(fields.String, missing=[])
    hits = fields.Int()
    hourly_hits_ratio = fields.Str()

    class Meta:
        dump_only = ('id', 'hits', 'short_url', 'hourly_hits')
