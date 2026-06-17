class SchemaValidationError(Exception):
    def __init__(self, errors):
        pass


class SchemaRegistry:
    def __init__(self, schema_base_path):
        pass

    def register(self, schema_id, version, schema):
        raise NotImplementedError

    def get(self, schema_id, version):
        raise NotImplementedError


class PayloadValidator:
    def __init__(self, registry):
        pass

    def validate(self, payload, schema_id, version, strict=True):
        raise NotImplementedError

    def validate_event(self, event):
        raise NotImplementedError

    def validate_job(self, job):
        raise NotImplementedError
