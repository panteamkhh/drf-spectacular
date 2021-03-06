import yaml
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import OpenAPIRenderer, JSONRenderer


class OpenApiYamlRenderer(OpenAPIRenderer):
    media_type = 'application/vnd.oai.openapi'

    def render(self, data, media_type=None, renderer_context=None):
        # disable yaml advanced feature 'alias' for clean, portable, and readable output
        class Dumper(yaml.SafeDumper):
            def ignore_aliases(self, data):
                return True

        def error_detail_representer(dumper, data):
            return dumper.represent_dict({'string': str(data), 'code': data.code})
        Dumper.add_representer(ErrorDetail, error_detail_representer)

        return yaml.dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            Dumper=Dumper
        ).encode('utf-8')


class OpenApiYamlRenderer2(OpenApiYamlRenderer):
    media_type = 'application/yaml'


class OpenApiJsonRenderer(JSONRenderer):
    media_type = 'application/vnd.oai.openapi+json'

    def get_indent(self, accepted_media_type, renderer_context):
        return super().get_indent(accepted_media_type, renderer_context) or 4


class OpenApiJsonRenderer2(OpenApiJsonRenderer):
    media_type = 'application/json'
