from flask import Flask, request, jsonify
from joblib import load
app = Flask(__name__)

model = load("../models/mallicius-detector.pkl")


def url_model_format(url="mp3raid.com/music/krizz_kaliko.html"):
    df = {}
    for htt in ['http',"https"]:
        df[htt] = int(htt in url)
        url = url.split("://")[-1]    
    
    url = url.replace("www.","")
    
    for end in [".com",".net",".gov",".edu"]:
        df[end] = int(end in url)
    
    df['dotCount'] = url.count(".")
    df['SlashCount'] = url.count("/")
    df['InterrogationCount'] = url.count("?")
    df['lenUrl'] = len(url)
    return df



@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        formated_url = url_model_format(request.form['url'])
        prob = model.predict_proba([list(formated_url.values())])[0][1]
        return jsonify({
            'url':request.form['url'],
            'prob':prob
        })
    else:
        return "<p>Hello, World!!!!!!!!!!</p>"  