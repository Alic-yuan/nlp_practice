# -*- coding:utf-8 -*-
'''
@Author: yuan
@Date: 2018-08-09 17:44:32
'''

from flask import Flask, request, jsonify
import pydat
import json
app = Flask(__name__)

dat = pydat.Dat()
with open("resource/data/ner_short/ext_entity") as fopen:
    lines = fopen.readlines()
    for line in lines:
        dat.add_word(line.strip())
    dat.make()

@app.route("/shortOrgExtraction", methods=["POST"])
def org_extraction():
    try:
        data = json.loads(request.get_data())
    except Exception as error:
        print(error)
        return jsonify(dict())
    content = data.get("content")
    entities = dat.search(content)
    print(entities)
    return jsonify(entities)

if __name__ == "__main__":
    app.run(port=8082)
    
