import json
from datetime import datetime, date
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (set, tuple)):
            return list(obj)
        elif isinstance(obj, (int, float)):
            return obj
        elif isinstance(obj, (str,)):
            return obj
        else:
            return super(CustomEncoder, self).default(obj)