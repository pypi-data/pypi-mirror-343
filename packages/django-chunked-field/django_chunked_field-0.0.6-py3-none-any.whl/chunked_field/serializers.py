import json

from rest_framework import serializers


class ChunkedJSONField(serializers.Field):
    def to_representation(self, value):
        # `value` here is the raw string returned by the chunked field.
        if value is None or value.strip() == '':
            return None
        return json.loads(value.replace('\'', '"'))

    def to_internal_value(self, data):
        # `data` here is the incoming Python object from the request.
        # Convert it to a JSON string to store in the chunked field.
        return json.dumps(data)
