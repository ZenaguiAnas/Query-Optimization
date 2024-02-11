import json

from flask import Flask, request, jsonify
from sqlglot import parse
from sqlglot.errors import ParseError
from flask_cors import CORS
import oracledb

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


@app.route('/ExecutionPlan')
def execution_plan():  # put application's code here
    body = request.json
    query = body['query']

    return {'execution_plan': get_execution_plan(query)}


@app.route('/ExecuteQuery', methods=['POST'])
def execute_query_route():
    body = request.json
    query = body['query']
    try:
        result = execute_query(query)
        return {'result': json.loads(result)['result']}
    except Exception as e:
        return {'error': str(e)}
    
@app.route('/test', methods=['POST'])
def connect_to_db():
    body = request.json
    username= body['username']
    host = body['host']
    password= body['password']
    try:

       cursor = connect_db(username, host, password)
       return jsonify({'message': 'Connected to database successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def execute_query(query):
    cursor = connect_db()
    cursor.execute(query)
    result = cursor.fetchall()
    # Process the plan into JSON format
    json_result = {'result': []}
    for row in result:
        json_result['result'].append(dict(zip([d[0] for d in cursor.description], row)))

    return json.dumps(json_result)


def connect_db(username, host, password):
    # Connection string(todo : put it in a config file)
    un = username
    cs = host
    pw = password

    connection = oracledb.connect(user=un, password=pw, dsn=cs)
    cursor = connection.cursor()
    return cursor


def get_execution_plan(query):
    cursor = connect_db()
    cursor.execute(f"EXPLAIN PLAN FOR {query}")
    cursor.execute(f"select * from table(dbms_xplan.display(null, null, 'SERIAL'))")
    plan = cursor.fetchall()
    # Process the plan into JSON format
    json_plan = {'execution_plan': []}
    for row in plan:
        json_plan['execution_plan'].append(dict(zip([d[0] for d in cursor.description], row)))

    return json.dumps(json_plan)



@app.route('/test1', methods=['GET'])
def test():
    return "anas"


if __name__ == '__main__':
    app.run(port=5000)
