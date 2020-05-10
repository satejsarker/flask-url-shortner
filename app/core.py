import flask
import flask_restful
import marshmallow


class HashKeyNotProvidedError(Exception):
    """Raise when no hash key is provided for a ddb request."""


class CommonSchema(marshmallow.Schema):

    def dumps(self, *args, **kwargs):
        kwargs['sort_keys'] = True
        return super().dumps(*args, **kwargs)


class CommonListResponseSchema(CommonSchema):
    items = marshmallow.fields.List(marshmallow.fields.Str())


class CommonResource(flask_restful.Resource):

    @staticmethod
    def _create_headers(item_id):
        """Create a header for the response.

        :param item_id: the resource id.
        :type item_id: marshmallow.fields.UUID
        :return: a set of headers
        :rtype: dict{str, str}
        """
        return {'Location': f"{flask.request.base_url}/{item_id}"}

    def _make_item_url(self, item_id):
        """Construct a url for a given item.

        :param item_id: the items unique id
        :type item_id: str
        :return: the items url
        :rtype: str
        """

    def retrieve(self, item_id):
        """Get an item via its unique id.

        :param item_id: the items unique id
        :type item_id: str
        :return: an instance of the models class
        :rtype: dict{str, any}
        """
        model_obj = self.model.get(hash_key=item_id)
        out = self.get_schema().dumps(model_obj.to_dict())
        return out

    @staticmethod
    def common_error(message=None, status_code=404):

        response = {"msg": "operation failed, please try again "}
        if message is not None:
            response = {"msg": message}
            return response, status_code
        return response, 500

    def retrieve_list(self, hash_key=None):
        """Get a list of items via their range key.

        :param hash_key: the global secondary index for the table.
        :type hash_key: str
        :return: a list of item urls
        :rtype: dict{str, str}
        """
        if hash_key is None:
            raise HashKeyNotProvidedError('hash_key is not found')

        objs = list(self.model.affiliation_index.query(hash_key=hash_key))
        item_urls = [self._make_item_url(obj.id) for obj in objs]
        out = CommonListResponseSchema().dumps(
            {'items': item_urls}
        )
        return out

    def create(self, **kwargs):
        """Create a resource.

        :param kwargs: the resources attributes.
        :rtype kwargs: dict{str, any}
        :return: tuple(dict, int, dict)
        """
        obj = self.model.create_instance_from_dict(kwargs)
        obj.save()

        out = self.create_schema().dumps(obj.to_dict())
        headers = self._create_headers(obj.id)
        return out, 201, headers

    def delete_item(self, item_id):
        """Delete a resource.

        :param item_id: the resources unique id
        :type item_id: str
        :return: a simple response
        :rtype: tuple(str, int)
        """
        obj = self.model.get(hash_key=item_id)
        obj.delete()
        return '', 204
