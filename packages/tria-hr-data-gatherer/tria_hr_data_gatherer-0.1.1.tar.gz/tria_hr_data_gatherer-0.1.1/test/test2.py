import json
from tria_hr_api import TriaHRAPI

api = TriaHRAPI(
    base_url="https://decasport.triahr.com",
    client_id="13_61ev6jlbu6ko8sgk4cg0cg0scss4oc8sg8wkwsokoowo48gooo",
    client_secret="4jqizm9xg1kwk8c88gkow0w0owkcss4sk8kg4c0kkwwwwo0gos"
)

params = {'company_id': 1}

response = api.undefined_request(endpoint='/api/v1/work-positions/', method='GET', params=params)

print(json.dumps(response.get('data', []), indent=2))

