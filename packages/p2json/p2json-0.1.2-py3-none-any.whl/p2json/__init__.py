import json


def tojson(obj):
    start_idx = obj.find("(")
    end_idx = obj.rfind(")")
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        json_data = obj[start_idx + 1 : end_idx].strip()
        try:
            return json.loads(json_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format", obj[start_idx + 1 : end_idx])
    else:
        raise ValueError("No valid JSONP format found.")
