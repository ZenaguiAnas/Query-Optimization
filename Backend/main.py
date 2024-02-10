import json

from flask import Flask, request, jsonify
from sqlglot import parse
from sqlglot.errors import ParseError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/ValidateSQL', methods=['POST'])
def validate_query():
    data = request.get_json()
    query = data.get('query', '')

    try:
        # Utiliser sqlglot pour valider la syntaxe SQL
        parse(query)

        # Si la syntaxe de la requête est valide, retourner un objet JSON avec le résultat
        return jsonify({'result': 'Valid SQL Query'})
    except ParseError as e:
        # Si une erreur de syntaxe est détectée, retourner un objet JSON avec le message d'erreur
        error_description = e.errors[0]['description']
        line_number = e.errors[0]['line']
        column_number = e.errors[0]['col']
        context = e.errors[0]['start_context']
        highlight = e.errors[0]['highlight']
        end_context = e.errors[0]['end_context']

        return jsonify({
                           'error': f"Invalid SQL Query: {error_description}. Error at line {line_number}, column {column_number}. Context: {context} {highlight} {end_context}"})


@app.route('/execution_plan')
def execution_plan():  # put application's code here
    body = request.json
    query = body['query']
    # !! sql injection !!
    return {'execution_plan': get_execution_plan(query)}


def get_execution_plan(query):
    import oracledb

    #  Connection string(todo : put it in a config file)
    un = 'C##mohcine'
    cs = '34.68.75.241/free'
    pw = 'mohcine'

    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"EXPLAIN PLAN FOR {query}")
            cursor.execute(f"select * from table(dbms_xplan.display(null, null, 'SERIAL'))")
            plan = cursor.fetchall()
            # Process the plan into JSON format
            json_plan = {'execution_plan': []}
            for row in plan:
                json_plan['execution_plan'].append(dict(zip([d[0] for d in cursor.description], row)))

            return json.dumps(json_plan)


if __name__ == '__main__':
    app.run(port=5000)
