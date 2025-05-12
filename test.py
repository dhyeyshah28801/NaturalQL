from data.dataFetcher import DatabaseManager
import json
DbEngine = DatabaseManager()

schema = DbEngine.fetch_schema()
print(json.dumps(schema, indent=4))