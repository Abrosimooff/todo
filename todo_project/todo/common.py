# -*- coding:utf-8 -*-
import json
from json import JSONEncoder
from django.http import HttpResponse


class JsonResponseMix(object):
    """ Возвращатель JSON"""

    def render_to_response(self, context):
        data = json.dumps(context, cls=JSONEncoder)
        return self.get_json_response(data)

    def get_json_response(self, content, **kwargs):
        return HttpResponse(content, content_type='application/json', **kwargs)
