from owlready2 import *
import rdflib
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
