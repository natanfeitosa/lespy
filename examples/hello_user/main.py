from lespy import App, Request, Response

app = App('hello_user')

@app.get('/')
def home(request: Request):
    return Response('<p>Hello world</p>')

@app.get('/<name>/')
def hello_name(req: Request):
    name = req.PARAMS["name"]

    res = Response(f'<h1>Hello {name}</h1>')
    return res

if __name__ == '__main__':
    from apy import run
    run(app, '')
