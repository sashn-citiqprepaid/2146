import json

import falcon.asgi
from falcon import HTTPError
from falcon.errors import HTTPRouteNotFound
from falcon.errors import WebSocketDisconnected
from falcon.request import Request
from falcon.response import Response
from falcon.asgi.ws import WebSocket


'''
############################
MIDDLEWARE
############################
Use the header key 'websocket-auth' with the value of anything but 'good' to make the middleware raise a HTTPError
'''
class WebsocketAuthMiddleware:
    BASE_WS_MESSAGE_URL = 'ws://0.0.0.0:8005/messages'
    WEBSOCKET_AUTH_HEADER_KEY = 'websocket-auth'

    async def process_request_ws(self, req, ws):
        try:
            if req.url == self.BASE_WS_MESSAGE_URL:
                if req.headers.get(self.WEBSOCKET_AUTH_HEADER_KEY) == 'good':
                    pass   
                elif req.headers.get(self.WEBSOCKET_AUTH_HEADER_KEY) == 'bad':    
                    # invalid header
                    raise HTTPError(status=falcon.HTTP_401, title="Invalid header")

        except ValueError as e:
            print("EXCEPTION WebsocketAuthMiddleware: ", e)


'''
#############################
ERROR HANDLER
#############################
'''

async def my_error_handler(req, resp, ex, params, ws=None):
    '''
    Internal bug, even when specifying the websocket close status code a 403 is called.
    If the websocket is not closed a 500 is raised because of the bug, by calling websocket.close we
    are circumventing the bug but have no control over the websocket status code response.
    This is becuase of the crash, there is no cleanup on crash just a straight 500.

    created an issue: https://github.com/falconry/falcon/issues/2146
    '''


    if type(ex) == HTTPRouteNotFound:
        resp.status = 404
        resp.text = json.dumps({'error': 'Route Not Found'})
    else:
        # await ws.close(code=WSStatusCode.NORMAL_CLOSURE)                # <-- 403 with, 500 without           
        raise HTTPError(status=418, title='Custom Websocket Error')   

'''
#############################
COLLECTION
#############################
'''
class Messages:

    async def on_websocket(self, req: Request, ws: WebSocket):
        while True:
            try:
                if ws.unaccepted:
                    print('Establishing...')
                    await ws.accept()
                if ws.ready:
                    await ws.send_text('SERVER: Hello')
                    client_text = await ws.receive_text()
                    print('CLIENT:', client_text)
            
            except WebSocketDisconnected:
                print('Disconnected...')
                break
            except Exception as e:
                print('EXCEPTION: ', e)
                break



def create_app():
    app = falcon.asgi.App(middleware=[WebsocketAuthMiddleware()]) 
    app.ws_options.max_receive_queue = 4

    ####################
    # error handler
    ####################
    app.add_error_handler(HTTPError, my_error_handler)

    ####################
    # routes
    ####################
    app.add_route('/messages', Messages())

    return app

def get_asgi_app():

    return create_app()