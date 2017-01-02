# coding=utf-8


from flask import Flask, render_template, request, redirect, jsonify
import mcashhelper as mcash



app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webview')
def webview_preview():
    return render_template('webview.html')


@app.route('/webview/<scan_token>')
def webview(scan_token):
    return render_template('webview.html', shortlink=mcash.SHORTLINK)


@app.route('/callback', methods=['POST'])
def callback():
    obj = request.get_json(force=True).get('object')
    scan_token = obj.get('id')
    argstring = obj.get('argstring')

    # Open webview if the argstring says so
    if argstring == 'webview':
        return jsonify(uri='https://krgr.ngrok.io/webview/%s' % scan_token)
    # Or send a payment request
    else:
        mcash.create_payment_request('1.00', scan_token)
        return ''
        

@app.route('/generate_shortlink', methods=['GET', 'POST'])
def generate_shortlink():
    if request.method == 'GET':
        return render_template('generate_shortlink.html')

    else:  # Method is POST
        callback_uri = request.form.get('callback_uri')
        shortlink_id, res = mcash.create_shortlink(callback_uri)
        qr_image_url = 'https://api.mca.sh/shortlink/v1/qr_image/%s/' % shortlink_id if shortlink_id else None

        if not qr_image_url:
            return "Couldn't create shortlink :( <br> %s" % res.content

        shortlink = "http://mca.sh/s/%s/" % shortlink_id

        return render_template('shortlink_generated.html', shortlink=shortlink, qr_image_url=qr_image_url)


if __name__ == '__main__':
    app.run(debug=True)
