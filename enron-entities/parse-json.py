import json

entities = []

with open('Entity.json', 'r') as f:
  for line in f:
    entities.append(json.loads(line))

embeddings = json.load(open('entity_embeddings.json', 'r'))

