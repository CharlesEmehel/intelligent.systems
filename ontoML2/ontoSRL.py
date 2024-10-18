from owlready2 import *
import rdflib
from rdflib import Namespace, Literal
import brickschema
from brickschema.namespaces import A, BRICK, UNIT
import tensorflow
import torch

onto_path.append("D:/Users/cem/data/git/namespace3/ontoRepo")
onto = get_ontology("https://github.com/I-NERGY/DataModel/blob/main/Resources/Ontology/OWL/i-nergy-ontology-01.owl")
onto.load()

with onto:
    class DistributionGridNetwork(onto.Pizza):
      equivalent_to = [
        onto.Pizza
      & ( onto.has_topping.some(onto.MeatTopping)
        | onto.has_topping.some(onto.FishTopping)
        ) ]
      def eat(self): print("Beurk! I'm vegetarian!")

onto.Pizza    # pizza_onto.Pizza

test_pizza = onto.Pizza("test_pizza_owl_identifier")
test_pizza.has_topping = [ onto.CheeseTopping(),
                           onto.TomatoTopping(),
                           onto.MeatTopping  () ]

Grid_RDF_Graph =rdflib()

Grid_RDF_Graph.save()                                                       

# test_pizza.__class__    # onto.Pizza

# Execute HermiT and reparent instances and classes
sync_reasoner()

# test_pizza.__class__   # onto.NonVegetarianPizza

# test_pizza.eat()  # Beurk! I'm vegetarian !


# create a namespace for the building
BLDG = Namespace("urn:my-building-name#")

# create a graph object to store the Brick model
g = brickschema.Graph()
g.bind("bldg", BLDG)

# create a datastructure for floors + rooms
rooms_and_floors = {
    "Floor1": ["Room1", "Room2", "Room3"],
    "Floor2": ["Room4"],
}

for floor, room_list in rooms_and_floors.items():
    # Use the strings in the datastructure to refer to entities in the Brick model.
    # By putting "BLDG[floor]" into the graph, we implicitly create the entity.
    g.add((BLDG[floor], A, BRICK.Floor))
    for room in room_list:
        g.add((BLDG[room], A, BRICK.Room))
        g.add((BLDG[room], BRICK.isPartOf, BLDG[floor]))

# save the file to disk
g.serialize("my-building.ttl", format="ttl")
