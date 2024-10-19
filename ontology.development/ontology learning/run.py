from ontoML import create_app
from ontoML.ontoai_builder import create_ontology, onto_to_graph, save_ontology, visualize_graph
from ontoML.ontoai_validator import run_reasoning, validate_ontology_with_shacl

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
