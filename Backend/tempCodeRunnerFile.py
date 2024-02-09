from flask import Flask, request
from sqlglot import parse
from sqlglot.errors import ParseError

app = Flask(__name__)

@app.route('/ValidateSQL', methods=['POST'])
def validate_query():
    data = request.get_json()
    query = data.get('query', '')

    try:
        # Utiliser sqlglot pour valider la syntaxe SQL
        parse(query)
        
        # Si la syntaxe de la requête est valide, retourner "Valid SQL Query"
        return "Valid SQL Query"
    except ParseError as e:
        # Si une erreur de syntaxe est détectée, retourner "Invalid SQL Query" avec le message d'erreur
        error_description = e.errors[0]['description']
        line_number = e.errors[0]['line']
        column_number = e.errors[0]['col']
        context = e.errors[0]['start_context']
        highlight = e.errors[0]['highlight']
        end_context = e.errors[0]['end_context']
        
        return f"Invalid SQL Query: {error_description}. Error at line {line_number}, column {column_number}. Context: {context} {highlight} {end_context}"

if __name__ == '__main__':
    app.run(port=5000)
