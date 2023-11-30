from database import get_most_similar_vector_id
import json

query = input("Restaurant description: ")
most_similar_id = get_most_similar_vector_id(query)
json_results = [result for result in most_similar_id]
json_object = json.dumps(json_results, indent=4)
json_object = json.loads(json_object)
print(json_object[0][1])
