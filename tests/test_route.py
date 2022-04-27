from lespy.core.router import Route, compile_route


def test_compile_route():
    compiled = compile_route('/user/<int:id>/')
    
    assert type(compiled) == tuple
    assert compiled[0] == '^/user/(?P<id>[0-9]+)/$'
    assert callable(compiled[1]['id'])
    assert compiled[1]['id'].__name__ == 'IntConverter'

user_get = Route('/user/<int:id>/', 'get_user', ['GET'], lambda r: r)

def test_name():
    assert user_get.name == 'get_user'

def test_paths():
    assert user_get.path == '/user/<int:id>/'
    assert user_get._re_path == '^/user/(?P<id>[0-9]+)/$'

def test_match():
    match = user_get.match('/user/100/')
    assert match is not None
    assert match['id'] == 100

def test_reverse():
    assert user_get.reverse(id=100) == '/user/100/'
    assert Route('/', 'home', ['GET'], lambda r: r).reverse() == '/' # type: ignore    
