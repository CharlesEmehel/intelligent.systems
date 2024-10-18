from owlready2 import (get_ontology, Thing, DataProperty, ObjectProperty,
                      AnnotationProperty, SymmetricProperty)
from rdflib import Graph, Literal
from rdflib.namespace import Namespace, RDF, RDFS, OWL, XSD
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import scipy as sp
AIEO = "http://aieo.org/aieo.owl"
AIEO_NS = Namespace(AIEO + "#")

def create_ontology():
   onto = get_ontology(AIEO)
   # ... [Same code for ontology creation]
   with onto:
       # Classes
       class Energy(Thing): pass
       class Data(Thing): pass
       class System(Thing): pass
       class ObjectiveFunction(Thing): pass
       class DataAnalytics(Thing): pass
       class EnergySource(Thing): pass
       class RenewableEnergy(Energy): pass
       class NonRenewableEnergy(Energy): pass
       class PowerPlant(Energy): pass
       class EnergyLoad(Energy): pass
       class Emission(Energy): pass
       class Solar(RenewableEnergy): pass
       class Wind(RenewableEnergy): pass
       class Hydro(RenewableEnergy): pass
       class Biomass(RenewableEnergy): pass
       class Coal(NonRenewableEnergy): pass
       class Gas(NonRenewableEnergy): pass
       # Properties
       class hasName(DataProperty):
           domain = [Energy]
           range = [str]
       class produces(ObjectProperty, SymmetricProperty):
           domain = [Energy]
           range = [Energy]
       class contains(ObjectProperty):
           domain = [Data]
           range = [Data]
       class producesEmission(ObjectProperty, SymmetricProperty):
           domain = [Coal]
           range = [Emission]
       class usesSource(ObjectProperty, SymmetricProperty):
           domain = [PowerPlant]
           range = [EnergySource]
       class hasLoad(ObjectProperty, SymmetricProperty):
           domain = [PowerPlant]
           range = [EnergyLoad]
       class cem(AnnotationProperty):
           pass
       # Individuals
       myPlant = PowerPlant("myPlant")
       ourPlant = PowerPlant("ourPlant")
   return onto

def bind_namespaces(g):
   g.bind("aieo", AIEO_NS)
   g.bind("rdf", RDF)
   g.bind("rdfs", RDFS)
   g.bind("owl", OWL)

def add_classes_to_graph(g):
   classes = [
       (AIEO_NS.Energy, "Energy", OWL.Thing),
       (AIEO_NS.RenewableEnergy, "Renewable Energy", AIEO_NS.Energy),
       # ... [Add other classes in the same manner]
       (AIEO_NS.NonRenewableEnergy, "Non-Renewable Energy", AIEO_NS.Energy),
       (AIEO_NS.Solar, "Solar", AIEO_NS.RenewableEnergy),
       (AIEO_NS.Wind, "Wind", AIEO_NS.RenewableEnergy),
       (AIEO_NS.Coal, "Coal", AIEO_NS.NonRenewableEnergy),
       (AIEO_NS.Oil, "Oil", AIEO_NS.NonRenewableEnergy)
   ]
   for (cls, label, superclass) in classes:
       g.add((cls, RDF.type, OWL.Class))
       g.add((cls, RDFS.label, Literal(label)))
       g.add((cls, RDFS.subClassOf, superclass))

def add_properties_to_graph(g):
   # As an example, let's add the `hasName` property
   g.add((AIEO_NS.produces, RDF.type, OWL.ObjectProperty))
   g.add((AIEO_NS.produces, RDFS.domain, AIEO_NS.Energy))
   g.add((AIEO_NS.produces, RDFS.range, AIEO_NS.Energy))
   # ... [Add other properties in the same manner]
   # As an example, let's add the `produces` property
   g.add((AIEO_NS.hasName, RDF.type, OWL.DatatypeProperty))
   g.add((AIEO_NS.hasName, RDFS.domain, AIEO_NS.Energy))
   g.add((AIEO_NS.hasName, RDFS.range, XSD.str))
   # ... [Add other properties in the same manner]

def add_individuals_to_graph(g):
   # As an example, let's add the `myPlant` individual
   g.add((AIEO_NS.myPlant, RDF.type, AIEO_NS.PowerPlant))
   # ... [Add other individuals in the same manner]

def onto_to_graph(onto):
   g = Graph()
   bind_namespaces(g)
   add_classes_to_graph(g)
   add_properties_to_graph(g)
   add_individuals_to_graph(g)
   owl_file = onto.save(file="temp.owl", format="rdfxml")
   g.parse("temp.owl", format="application/rdf+xml", data=owl_file)
   return g

def visualize_graph(g: Graph):
   G = nx.MultiDiGraph()  # or DiGraph, MultiGraph, MultiDiGraph
   for subj, pred, obj in g:
       G.add_edge(subj, obj, title=str(pred), weight=4, capacity=15, length=250.7)
   nt = Network(notebook=True, cdn_resources='remote')
   nt.from_nx(G)
   # Define node colors and other properties
   color_map = {
       AIEO_NS.Energy: 'white',
       AIEO_NS.RenewableEnergy: 'green',
       AIEO_NS.NonRenewableEnergy: 'red',
       AIEO_NS.Solar: 'yellow',
       AIEO_NS.Wind: 'cyan',
       AIEO_NS.PowerPlant: 'yellow',
       AIEO_NS.EnergyLoad: 'yellow',
       AIEO_NS.Emission: 'brown',
       AIEO_NS.Biomass: 'cyan',
       AIEO_NS.Hydro: 'cyan',
       AIEO_NS.Gas: 'cyan',
       AIEO_NS.System: 'magenta',
       AIEO_NS.Data: 'magenta',
       AIEO_NS.DataAnalytics: 'magenta',
       AIEO_NS.ObjectiveFunction: 'magenta',
       # ... add other class-color mappings as needed
   }
   # Modify the shape, size, borderDashes, and color of each node
   for node in nt.nodes:
       node_id = node['id']
       if isinstance(node_id, str) and node_id.startswith('http'):
           node_id = node_id.split('#')[1] if '#' in node_id else node_id.rsplit('/', 1)[-1]
       node_color = color_map.get(node_id, 'gray')  # default color
       node['shape'] = 'ellipse'
       node['size'] = 50
       node['borderDashes'] = [50, 50]
       node['color'] = {"background": node_color, "border": "black"}
   # Ensure arrows are displayed on edges
   for edge in nt.edges:
       edge['arrows'] = 'to'
   # JavaScript to disable physics after stabilization
   js_code = """
   network.on("stabilizationIterationsDone", function() {
       network.setOptions( { physics: false } );
   });
   """
   nt.options.physics = {True}
   nt.show('ontology_RDF_graph.html')
   nt.toggle_physics(True)
   nt.show_buttons(filter_=['physics'])
   #nt.enable_physics(True)
   nt.write_html('ontology_RDF_graph.html', notebook=True, override=True)
   with open('ontology_RDF_graph.html', 'a') as f:
       f.write('<script type="text/javascript">' + js_code + '</script>')
   nt.show('ontology_RDF_graph.html')

def save_ontology(g, file_format, destination):
   format_mappings = {
       "ttl": "ttl",
       "rdfxml": "rdfxml",
       "rdf": "application/rdf+xml",
       "xml": "xml",
       "owlxml": "owlxml",
       "n3": "n3",
       "nqs": "nquads",
       "json-ld": "json-ld"
   }
   rdf_format = format_mappings.get(file_format)
   if rdf_format == "rdfxml":
       onto.save(file="../data/ai_energy_ontology.owl", format="rdfxml")
   else:
        g.serialize(destination=destination, format=rdf_format)
   if not rdf_format:
       print(f"Unsupported format: {file_format}")

if __name__ == '__main__':
 # Create ontology with owlready2
    onto = create_ontology()
    onto.classes()
    list(onto.classes())
    for c in onto.classes():
        print(c.name)
    # Convert ontology to rdflib graph
    ontology_graph = onto_to_graph(onto)
    print(f"The ontology_graph return object is {ontology_graph}")
    # Visualize the graph (Add this line to visualize)
    visualize_graph(ontology_graph)
    # Choose file format and path
    file_format = input("Choose file format (ttl/owl/rdf/xml/owlxml/n3/nqs/json-ld): ")
    file_path = f"./data/ai_energy_ontology.{file_format}"
    if file_format == 'ttl':
        save_ontology(ontology_graph, 'ttl', file_path)
    elif file_format == 'owl':
        save_ontology(ontology_graph, 'rdfxml', file_path)
    elif file_format == 'rdf':
        save_ontology(ontology_graph, 'application/rdf+xml', file_path)
    elif file_format == 'xml':
        save_ontology(ontology_graph, 'xml', file_path)
    elif file_format == 'owlxml':
        save_ontology(ontology_graph, 'owlxml', file_path)
    elif file_format == 'n3':
        save_ontology(ontology_graph, 'n3', file_path)
    elif file_format == 'nqs':
        save_ontology(ontology_graph, 'nquads', file_path)
    elif file_format == 'json-ld':
        save_ontology(ontology_graph, 'json-ld', file_path)
    else:
        print(f"Unsupported format: {file_format}")
    print(f"Ontology saved to {file_path}.")