from lespy import App, Request, run

app = App('hello_world')

@app.get('/')
def home(request: Request):
    return 'Hello world'

if __name__ == '__main__':
    run(app, '')
