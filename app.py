from flask import request
from flask import Flask
import requests
import json
import re

app = Flask(__name__)


@app.route('/')
def index():
    return "<p>HuyKaiser Test API</p>"

@app.route('/short')
def short():
    url = request.args.get('url')
    if url == None:
        return "No url"
    elif url == "":
        return "No url"
    else:
        res = requests.get(f"https://thieutrungkien.dev/shorturl?url={url}")
        return json.loads(res.text) 

@app.route('/y2mate')
def y2mate():
    url = request.args.get('url')
    match = re.search(r"youtube\.com/.*v=([^&]*)", url)
    if match:
        resultIDVideo = match.group(1)
        print(resultIDVideo)
        headers = {
            'accept': "*/*",
            'accept-language': "en-US,en;q=0.9,vi;q=0.8",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        data = {
            'url': 'https://youtu.be/' + resultIDVideo,
            'q_auto': 0,
            'ajax': 2
        }
        url = 'https://www.y2mate.com/mates/en68/analyze/ajax'
        res = requests.post(url, headers=headers, data=data)
        home = json.loads(res.text)['result']
        imageSrc = home.split('<div class="thumbnail cover">')[
            1].split('<img src="')[1].split('"')[0]
        title = home.split(
            'caption text-left">')[1].split('</div>')[0].split('<b>')[1].replace("</b>", "")
        size = home.split('<a href="#" rel="nofollow">')[
            8].split('<td>')[1].split('</td>')[0]
        type = home.split('<a href="#" rel="nofollow">')[8].split(
            '</a>')[0].split('(')[0].split(".")[1].strip()
        quality = home.split('<a href="#" rel="nofollow">')[
            8].split('</a>')[0].split('(')[1].split(')')[0].split('kbps')[0]
        id = home.split('var k__id =')[1].split(';')[0].split('"')[1].strip()
        urlOne = 'https://www.y2mate.com/mates/en68/convert'
        _headers = {
            'accept': "*/*",
            'accept-language': "en-US,en;q=0.9,vi;q=0.8",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        _data = {
            'type': 'youtube',
            'v_id': resultIDVideo,
            '_id': id,
            'ajax': '1',
            'token': '',
            'ftype': type,
            'fquality': quality
        }
        res = requests.post(urlOne, headers=_headers, data=_data)
        url = json.loads(res.text)['result']
        urlMusic = url.split('<a href="')[1].split('"')[0]
        infoMusic = {
            'imageSrc': imageSrc,
            'title': title,
            'size': size,
            'type': type,
            'quality': quality,
            'url': urlMusic
        }
        return infoMusic
    else:
        return '<h1>Not found</h1>'

if __name__ == '__main__':
    app.run(debug=True)
