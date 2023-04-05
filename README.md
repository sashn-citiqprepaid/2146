# 2146

Minimal reproducible example for issue [2146](https://github.com/falconry/falcon/issues/2146)



#### install

```bash
pyenv virtualenv 3.11.1 2146
```

```bash
pyenv activate 2146
```

```bash
python -m pip install -r requirements.txt
```

#### run 

```bash
gunicorn -k uvicorn.workers.UvicornWorker --bind  0.0.0.0:8005 --reload 'app:get_asgi_app()' -w 1 --log-level='trace'
```


## api client (postman)
With postman you can create a websocket connection. With the new connection use the following values: <br/>
URL: ```ws://0.0.0.0:8005/messages``` <br/>
HEADER: KEY: ```websocket-auth``` VALUE: ```good``` (for normal operation you can send text back and forth) <br/>
HEADER: KEY: ```websocket-auth``` VALUE: ```bad``` (to see the bug show) <br/>



<hr/>
<br/>
<br/>

When the header has the value of "bad" you should see something like the following: <br/>
```bash
[2023-04-05 15:22:14 +0200] [136487] [ERROR] Exception in ASGI application
Traceback (most recent call last):
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/falcon/asgi/app.py", line 1000, in _handle_websocket
    await process_request_ws(req, web_socket)
  File "/Desktop/2146/app.py", line 29, in process_request_ws
    raise HTTPError(status=falcon.HTTP_401, title="Invalid header")
falcon.http_error.HTTPError: <HTTPError: 401 Unauthorized>

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/falcon/asgi/app.py", line 1095, in _handle_exception
    await err_handler(req, resp, ex, params, **kwargs)
  File "/Desktop/2146/app.py", line 57, in my_error_handler
    raise HTTPError(status=418, title='Custom Websocket Error')
falcon.http_error.HTTPError: <HTTPError: 418>

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/uvicorn/protocols/websockets/websockets_impl.py", line 238, in run_asgi
    result = await self.app(self.scope, self.asgi_receive, self.asgi_send)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/falcon/asgi/app.py", line 312, in __call__
    await self._handle_websocket(spec_version, scope, receive, send)
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/falcon/asgi/app.py", line 1018, in _handle_websocket
    if not await self._handle_exception(req, None, ex, params, ws=web_socket):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/.pyenv/versions/2146/lib/python3.11/site-packages/falcon/asgi/app.py", line 1100, in _handle_exception
    self._compose_error_response(req, resp, error)
  File "falcon/app.py", line 975, in falcon.app.App._compose_error_response
AttributeError: 'NoneType' object has no attribute 'status'
[2023-04-05 15:22:14 +0200] [136487] [INFO] connection open
[2023-04-05 15:22:14 +0200] [136487] [INFO] connection closed
```