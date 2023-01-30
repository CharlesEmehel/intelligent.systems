from ontoML import app
# from ontoML import create_app


# Checks if the main.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)

