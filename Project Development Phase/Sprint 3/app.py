from flask import Flask , request , redirect
import os
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics

from flask import render_template
model = pickle.load(open('regressor.dat','rb'))

app=Flask(__name__)

@app.route("/")
def index():
    print(os.getcwd())
    return render_template("Start-Page.html",score=100)

@app.route("/predict",methods=['POST'])
def predict():
    gre_score=request.form["gre"]
    toefl_score=request.form["toefl"]
    ur_value=request.form["ur"]
    lor_score=request.form["lor"]
    sop_score=request.form["sop"]
    cgpa_value=request.form["cgpa"]
    rp_value=request.form["rp"]
    t=[[int(gre_score),int(toefl_score),int(ur_value),int(lor_score),int(sop_score),int(cgpa_value),int(rp_value)]]
    print(type(model))
    output=model.predict(t)
    op=(output[0]*100)
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