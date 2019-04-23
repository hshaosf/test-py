"""Main application module"""
import os
import json
import jsend
import sentry_sdk
import falcon
from .resources.welcome import Welcome
from .resources.callback import Callback
from .resources.datastore import Datastore

WEB_PATH = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.pardir,
        'web',
        'public'))

def start_service():
    """Start this service
    set SENTRY_DSN environmental variable to enable logging with Sentry
    """
    # Initialize Sentry
    sentry_sdk.init(os.environ.get('SENTRY_DSN'))
    # Initialize Falcon
    api = falcon.API()
    if os.environ.get('environment') == 'development':
        api.resp_options.secure_cookies_by_default = False
    else:
        api.resp_options.secure_cookies_by_default = True            
    api.add_route('/welcome', Welcome())
    api.add_route('/callback/{name}', Callback())
    api.add_route('/datastore/{method}', Datastore())
    api.add_sink(web_index, prefix='^/$')
    api.add_static_route('/', WEB_PATH)
    #api.add_sink(default_error, '')
    return api

def default_error(_req, resp):
    """Handle default error"""
    resp.status = falcon.HTTP_404
    msg_error = jsend.error('404 - Not Found')

    sentry_sdk.capture_message(msg_error)
    resp.body = json.dumps(msg_error)

def web_index(_req, resp):
    """Handle index page"""
    resp.content_type = 'text/html; charset=utf-8'
    filename = os.path.join(WEB_PATH, 'index.html')
    with open(filename, 'rt') as fileobj:
        content = fileobj.read()
        script = '<script type="text/javascript">var __web={"auth_domain":"'+str(os.environ['AUTH_DOMAIN'])+'", "auth_id":"'+str(os.environ['AUTH_ID'])+'"}</script>'
        resp.body = content.replace("</body>", script+"</body>")
