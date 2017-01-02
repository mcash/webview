Introduction
=======================
This technique allows merchants to build a webapp inside the mCASH-app. A common usecase is:

1. User scans a QR, presses a button in his/her browser or in another app or finds the shop in Nearby
2. A webview gets displayed, the content of which is 100% determined by the merchant
3. The webview typically contains a webshop of some sort, where the user selects what to buy
4. The user is then redirected back to the native mCASH app to pay.


Installation
=======================
In this example we use the python web framework Flask to host our application.

`pip install flask`


Run the flask application
=======================
`python webview.py`


Make your application accessible from the interwebz
=======================
I recommend using ngrok. Download it from ngrok.io, create an account and simply do
`ngrok http -subdomain=<your_subdomain> 5000`. You might have to pay a couple of dimes for enabling `HTTPS` though.

This application will then be available on `https://<your_subdomain>.ngrok.io`.
Update the `SERVER_URL` in webview.py accordingly.


mCASH Merchant API setup
=======================
You need to enter your credentials in `mcashhelper.py`. You can obtain them in two ways.

1. Enroll your organization at mcash.no, select integration type `ecom` or `pos` and create a `User` with a `secret` in the protal.
2. Sign up for a test account at https://mcashtestbed.appspot.com/testbed/signup/ - you'll receive further instructions per mail

To obtain a shortlink, go to the `generate_shortlink` page of this application.
In this example, we want to set the callback url to https://url-to-this-application.example/callback. If the callback
url is not HTTPS, you will not receive the `object` part of the callback from mCASH, and will have to modify the code
in `def callback()` to do an HTTPS GET back to mCASH using the `uri` from the `meta` part of the callback.
See http://dev.mca.sh/callbacks.html for details.



How it works
=======================

1. User scans a QR (`shortlink`) or opens a link on the form `mcash://qr?code=[shortlink]/[argstring]`, where [argstring] is optional.
2. mCASH server does a POST callback to the `callback_uri` of the `shortlink`
3. This application's response on that callback is a json object which contains a link to a webview, see http://dev.mca.sh/handlers.html#shortlink
4. The user is presented with that webview, which is opened inside the mCASH app.
5. The content of this webview is up to you, the developer, to decide. It can be a simple webshop, for example.
6. The user clicks a button which redirects the user to the native mCASH payment view.
7. This action invokes another scan behind the scenes, and the mCASH server does again a callback to `callback_uri` of the shortlink
8. The callbacks contains a `scan_token` which is used for sending a payment request to the user who scanned, see http://dev.mca.sh/handlers.html#payment-request
9. Not covered in this example: capture the payment by doing a `PUT {"action":"capture"}` to `/payment_request/[tid]/`, see http://dev.mca.sh/handlers.html#put--payment_request--tid--

TIP: In production one can open `shortlink` (with or without argstring) in any browser, and a QR or button will be
rendered (depending on whether the browser is mobile or not).

TIP 2: You can also add a `callback_uri` parameter to the payment request itself, to receive updates on the payment.

This particular example application works like this: a) If the user scans a shortlink with `webview` as an argstring,
an uri to a webview is returned in the callback response, which the mCASH app will open internally for the user.
b) When the user click "Go to payment" the app opens a link on the form "mcash://qr?code=[shortlink]", which
will make the mCASH app do a "QR-scan" of the shortlink (without the argstring from step a), behind the scenes.

The scan in step b) invokes a payment request. We pop the webview off the stack by redirecting it to `close:`
in a timeout function using javascript, and the user is then back in the native mCASH payment view, ready
to pay.
