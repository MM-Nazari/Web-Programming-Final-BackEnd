from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "code": status_code,
            "message": None,
            "data": data,
        }
        if not str(status_code).startswith('2'):

            if isinstance(data, dict):
                try:
                    response["message"] = f'{data["detail"]}'
                except KeyError:
                    # check dict is nested and get nested and last layer
                    while isinstance(data, dict):
                        key, value = data.popitem()
                        data = value
                    response["message"] = f'{value}'
            if isinstance(data, list):
                try:
                    response['code'] = data[0].code
                    response["message"] = data[0]
                except KeyError:
                    response["message"] = data
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
