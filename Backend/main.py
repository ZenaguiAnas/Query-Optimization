import json
import time

from flask import Flask, request, jsonify, Response
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
        return jsonify({'success': True, 'message': 'your sql is valid'}), 200
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


@app.route('/ExecutionPlan', methods=['POST'])
def execution_plan():  # put application's code here
    body = request.json
    query = body['query']
    username = body['username']
    host = body['host']
    password = body['password']

    return {'execution_plan': get_execution_plan(query, username, host, password)}


@app.route('/ExecuteQuery', methods=['POST'])
def execute_query_route():
    body = request.json
    query = body['query']
    username = body['username']
    host = body['host']
    password = body['password']

    try:
        return execute_query(query, username, host, password)
    except Exception as e:
        return {'error': str(e)}


@app.route('/connect_db', methods=['POST'])
def connect_to_db():
    body = request.json
    username = body['username']
    host = body['host']
    password = body['password']
    try:

        connect_db(username, host, password)
        return jsonify({'message': 'Connected to database successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stream-optimization')
def generate_large_csv():
    def generate():
        for i in range(1):
            yield f""""data: # | Column 1 Header | Column 2 Header | Column 3 Header |
|-----------------|-----------------|-----------------|
| Row 1, Column 1 | Row 1, Column 2 | Row 1, Column 3 |
| Row 2, Column 1 | Row 2, Column 2 | Row 2, Column 3 |
| Row 3, Column 1 | Row 3, Column 2 | Row 3, Column 3 |
 \n\n"""

    return generate(), {"Content-Type": "text/event-stream"}


def execute_query(query, username, host, password):
    cursor = connect_db(username, host, password)
    cursor.execute(query)
    result = cursor.fetchall()
    # Process the plan into JSON format
    json_result = {'result': []}
    for row in result:
        json_result['result'].append(dict(zip([d[0] for d in cursor.description], row)))

    return json_result


def connect_db(username, host, password):
    # Connection string(todo : put it in a config file)
    un = username
    cs = host
    pw = password

    connection = oracledb.connect(user=un, password=pw, dsn=cs)
    cursor = connection.cursor()
    return cursor


def get_execution_plan(query, username, host, password):
    cursor = connect_db(username, host, password)
    cursor.execute(f"EXPLAIN PLAN FOR {query}")
    cursor.execute(f"select * from table(dbms_xplan.display(null, null, 'SERIAL'))")
    plan = cursor.fetchall()
    # Format execution plan
    formatted_execution_plan = []
    for row in plan[5:]:
                if '-' in row[0]:
                    # If the row contains only dashes, append it as a single entry
                   continue
                else:
                    row_values = [value.strip() for value in row[0].split("|")]
                    print(row_values)
                    formatted_execution_plan.append({
                        'Id': row_values[1],
                        'Operation': row_values[2],
                        'Name': row_values[3],
                        'Rows': row_values[4],
                        'Bytes': row_values[5],
                        'Cost': row_values[6],
                        'Time': row_values[7] 
                    })
    return json.dumps(formatted_execution_plan)


if __name__ == '__main__':
    app.run(port=5000)
