import json

from flask import Flask, request, jsonify
from sqlglot import parse
from sqlglot.errors import ParseError
from flask_cors import CORS
import oracledb
# from src.optimizer import optimize_query

# from transformers import AutoPeftModelForCausalLM, AutoTokenizer
# from transformers import pipeline
from src.model import optimizer

from dotenv import dotenv_values
config = dotenv_values()

app = Flask(__name__)
CORS(app)

# QUERY_DATASET = config.get("QUERY_DATASET")
# MODEL = config.get("MODEL")
# HUB_MODEL_ID = config.get("HUB_MODEL_ID")
# HUB_ORGANIZATION = config.get("HUB_ORGANIZATION")
# HUB_TOKEN = config.get("HUB_TOKEN")

# model = AutoPeftModelForCausalLM.from_pretrained(MODEL, load_in_4bit=True)
# tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
# tokenizer.pad_token = tokenizer.eos_token
# tokenizer.padding_side = "right"
# pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=300)


# def optimize_query(query):
#     prompt = "You are a chatbot specializing in optimizing SQL queries within the Oracle syntax ecosystem. Your primary functionality is to provide optimized query. "
#     result = pipe(f"<s>[INST] {prompt+query} [/INST]")
#     chatbot_response = result[0]['generated_text']

#     print(chatbot_response)

#     return chatbot_response

@app.route('/api/optimize', methods=['POST'])
def chatbot_llama():
    query = request.json.get('query')
    chatbot_response = optimizer(query)
    return jsonify({'chatbot_response': chatbot_response})


# @app.route('/api/optimize', methods=['POST'])
# def optimize():
#     data = request.get_json()
#     input_query = data.get('input_query')

#     if input_query:
#         optimized_query = optimize_query(input_query)
#         return jsonify({'optimized_query': optimized_query})

#     return jsonify({'error': 'Input query not provided'}), 400


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


@app.route('/ExecutionPlan')
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
