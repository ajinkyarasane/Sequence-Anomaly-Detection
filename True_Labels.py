import json
import copy
import pandas as pd

ontology = json.load(open('/content/ontology.json'))

graph = copy.deepcopy(ontology)

for node1 in graph:
  for node2 in graph:
    if node2["id"] in node1["child_ids"]:
      node2["parent"] = node1["id"]

for node1 in graph:
  if "parent" not in node1.keys():
    node1["parent"] = None

def find_root(graph, node):
  if node["parent"] is None:
    return node["name"]
  parent = None
  for nd in graph:
    if nd["id"] == node["parent"]:
      parent = nd
      break
  return find_root(graph, parent)

for node in graph:
  node["root"] = find_root(graph, node)

human_sounds = []
animal = []
music = []
natural_sounds = []
sounds_of_things = []
ambiguous = []
channel_environment_and_background = []

for node in graph:
  if node["root"] == "Human sounds":
    human_sounds.append(node["id"])
  if node["root"] == "Animal":
    animal.append(node["id"])
  if node["root"] == "Music":
    music.append(node["id"])
  if node["root"] == "Natural sounds":
    natural_sounds.append(node["id"])
  if node["root"] == "Sounds of things":
    sounds_of_things.append(node["id"])
  if node["root"] == "Source-ambiguous sounds":
    ambiguous.append(node["id"])
  if node["root"] == "Channel, environment and background":
    channel_environment_and_background.append(node["id"])


vocabulary = pd.read_csv("/content/vocabulary.csv")


human_sounds_filtered = []
animal_filtered = []
music_filtered = []
natural_sounds_filtered = []
sounds_of_things_filtered = []
ambiguous_filtered = []
channel_environment_and_background_filtered = []
for sound1 in human_sounds:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        human_sounds_filtered.append(sound1)
for sound1 in animal:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        animal_filtered.append(sound1)

for sound1 in music:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        music_filtered.append(sound1)

for sound1 in natural_sounds:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        natural_sounds_filtered.append(sound1)

for sound1 in sounds_of_things:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        sounds_of_things_filtered.append(sound1)

for sound1 in ambiguous:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        ambiguous_filtered.append(sound1)

for sound1 in channel_environment_and_background:
    for sound2 in vocabulary["ontology_id"]:
      if sound1 == sound2:
        channel_environment_and_background_filtered.append(sound1)
  
human_sounds_names = []
animal_names = []
music_names = []
natural_sounds_names = []
sounds_of_things_names = []
ambiguous_names = []
channel_environment_and_background_names = []

for id in human_sounds_filtered:
  for node in graph:
    if node["id"] == id:
      human_sounds_names.append(node["name"])

for id in animal_filtered:
  for node in graph:
    if node["id"] == id:
      animal_names.append(node["name"])

for id in music_filtered:
  for node in graph:
    if node["id"] == id:
      music_names.append(node["name"])

for id in natural_sounds_filtered:
  for node in graph:
    if node["id"] == id:
      natural_sounds_names.append(node["name"])

for id in sounds_of_things_filtered:
  for node in graph:
    if node["id"] == id:
      sounds_of_things_names.append(node["name"])

for id in ambiguous_filtered:
  for node in graph:
    if node["id"] == id:
      ambiguous_names.append(node["name"])


name_id = {}
for (name, id) in zip(vocabulary["name"], vocabulary["ontology_id"]):
  name_id[id] = name
name_id


True_Natural = []
for sound in natural_sounds_filtered:
  True_Natural.append(name_id[sound])

True_Ambigous = []
for sound in ambiguous_filtered:
  True_Ambigous.append(name_id[sound])

True_Hs = []
for sound in human_sounds_filtered:
  True_Hs.append(name_id[sound])

True_SoT = []
for sound in sounds_of_things_filtered:
  True_SoT.append(name_id[sound])

True_A = []
for sound in animal_filtered:
  True_A.append(name_id[sound])

True_M = []
for sound in music_filtered:
  True_M.append(name_id[sound])