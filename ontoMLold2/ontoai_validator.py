from owlready2 import get_ontology, sync_reasoner_hermit, sync_reasoner_pellet
from rdflib import Graph
import tempfile
import os
from pyshacl import validate

def run_reasoning(ontology_path):
   # Detect format from file extension
   _, file_extension = os.path.splitext(ontology_path)
   if file_extension == ".ttl":
       input_format = "turtle"
       rdf_format = "application/rdf+xml"
       output_format = "turtle"
   elif file_extension in [".owl", ".rdf"]:
       input_format = "xml"
       rdf_format = "application/rdf+xml"
       output_format = "rdfxml"
   else:
       raise ValueError(f"Unsupported file extension '{file_extension}'. Please use '.ttl', '.rdf', or '.owl'.")
   # Use rdflib to parse the ontology file in its respective format
   graph = Graph()
   graph.parse(ontology_path, format=input_format)
   # Convert the graph to RDF/XML format for owlready2 processing
   rdf_xml_data = graph.serialize(format=rdf_format)
   # Write the RDF/XML data to a temporary file
   with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".rdf") as temp:
       temp.write(rdf_xml_data)
       temp.flush()  # Ensure that the written content is flushed to disk
       temp_file_name = temp.name
   # Load the ontology from the temporary file with owlready2
   onto = get_ontology(temp_file_name).load()
   # Run the reasoner
   with onto:
       sync_reasoner_hermit()  # Synchronize the reasoner with HermiT, infer facts
   #    sync_reasoner_pellet()  # Synchronize the reasoner with HermiT, infer facts
   # Create a new rdflib graph and parse the reasoned RDF/XML data into it
   graph2 = Graph()
   graph2.parse(data=rdf_xml_data, format=rdf_format)
   # Serialize the reasoned graph in the original format
   output_file = os.path.join("../data", "ai_energy_ontology_reasoned" + file_extension)
   graph2.serialize(destination=output_file, format=input_format)
   print(f"Reasoned ontology saved to {output_file}")

def validate_ontology_with_shacl(data_graph: Graph, shapes_graph_str: str) -> bool:
   """
   Validates an ontology (as an rdflib Graph) against SHACL shapes.
   Args:
   - data_graph (Graph): The ontology to validate.
   - shapes_graph_str (str): The SHACL shapes as a string.
   Returns:
   - bool: True if the ontology is valid, False otherwise.
   - results_graph: An RDF graph that contains detailed information about the validation process and any
     violations that were found. You can query this graph or serialize it to a file to inspect the
     violations.
   - results_text: A human-readable string that provides information about the validation results, including
     details of any violations. It can be printed to the console for quick inspection.
   - _: The underscores '_, _' in place of results_graph or results_text ignores the detailed results graph and text.
   """
   # Validate
   conforms, results_graph, results_text = validate(data_graph,
                       shacl_graph=shapes_graph_str,
                       ont_graph=None,
                       inference='rdfs',
                       abort_on_first=False
   )
   return conforms, results_graph, results_text

if __name__ == "__main__":
   run_reasoning("../data/ai_energy_ontology.owl")  # Adjust path as needed
   print("Reasoning with OWLREADY done!")
   print("Validating with SHACL, please wait...!!")
   # Using the Validation Function:
   '''
   You can call the validate_ontology_with_shacl function after you've created your ontology to check if it
   adheres to the SHACL constraints:
   '''
   is_valid, results_graph, results_text  = validate_ontology_with_shacl("../data/ai_energy_ontology_reasoned.owl", "../data/shacl_shape_test.ttl")
   if is_valid:
       print("The ontology is valid according to the SHACL shapes.")
   else:
       print("The ontology is not valid according to the SHACL shapes.")
   print(results_graph)
   print(results_text)

