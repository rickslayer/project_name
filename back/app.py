import requests

endpoint = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/thiago?localidade=3503901"
names = requests.get(endpoint)
obj = names.json()[0]['res']

for item in obj:
    print(item)