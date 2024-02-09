from flask import Flask, request
import sqlvalidator

app = Flask(_name_)


@app.route('/ValidateSQL', methods=['GET'])
def validate_query():
    get_body = request.get_json()
    query = get_body['query']
    sql_query = sqlvalidator.parse(query)
    if not sql_query.is_valid():
        return "Invalid SQL Query"
    return "Valid SQL Query"


if _name_ == '_main_':
  app.run(port=5000)