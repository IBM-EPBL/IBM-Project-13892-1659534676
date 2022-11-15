from flask import Flask , request , redirect
import os
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics

from flask import render_template
import requests

API_KEY = "3-djqxBIyr1X0buXEcoEXxxf00-a4C3qPf9L53Soe4Vv"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

@app.route("/")
def index():
    print(os.getcwd())
    return render_template("index.html",score=100)

@app.route("/predict",methods=['POST'])
def predict():
    gre_score=request.form["gre"]
    toefl_score=request.form["toefl"]
    ur_value=request.form["ur"]
    lor_score=request.form["lor"]
    sop_score=request.form["sop"]
    cgpa_value=request.form["cgpa"]
    rp_value=request.form["rp"]
    t=[[int(gre_score),int(toefl_score),int(ur_value),float(sop_score),float(lor_score),float(cgpa_value),int(rp_value)]]
    payload_scoring = {"input_data": [{"fields": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']], "values": t }]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e327ebc2-eb51-46a5-b2c3-57c81badc74e/predictions?version=2022-11-15', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    
    output= response_scoring.json()["predictions"][0]["values"][0][0]
    op=(output*100)
    while op>=100:
        op-=2
    while op<5:
        op+=5
    op=round(op,2)
    if op>=50:
        return render_template("success.html",score=op)
    else:
        return render_template("fail.html",score=op)

if __name__ == "__main__":
    app.run(debug=True)