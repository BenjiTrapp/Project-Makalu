from ProjectMakaluApp import app
import unittest


class BasicTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        # given
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_returned_data_when_main_page_is_called(self):
        # given
        expected = str(b'<!doctype html>\n<html>\n    <head>\n        <title>Project Makalu - Broken Session'
                       b' Handling Shop</title>\n        <link rel="stylesheet" href="/static/style.css">\n'
                       b'        <link rel="icon" href="/static/favicon.ico" />\n    </head>\n    <body>\n'
                       b'        <div class="header">\n            <div class="logo" align="left">anna group'
                       b'</div>\n            <a href="/">Home</a>\n            \n                <a href="/login">'
                       b'Login</a>\n            \n        </div>\n        <div class="content">\n            \n'
                       b'<a href="/CSRFProtected">CSRF Protection</a><br>\n<a href="/ProbabilisticLogout">'
                       b'Probabilistic Logout</a><br>\n<a href="/OrderArticle/1">Order an Article</a><br>\n'
                       b'<a href="/Notes">Notes</a>\n\n        </div>\n    </body>\n</html>')

        # when
        result = self.app.get('/')

        # then
        self.assertTrue(expected in str(result.data))

    def test_returned_data_when_login_page_is_called(self):
        # given
        expected = str(b'<!doctype html>\n<html>\n    <head>\n        <title>Project Makalu - Broken Session Handling'
                       b' Shop</title>\n        <link rel="stylesheet" href="/static/style.css">\n        '
                       b'<link rel="icon" href="/static/favicon.ico" />\n    </head>\n    <body>\n        '
                       b'<div class="header">\n            <div class="logo" align="left">anna group</div>\n'
                       b'            <a href="/">Home</a>\n            \n                <a href="/login">Login</a>\n'
                       b'            \n        </div>\n        <div class="content">\n            \n<h1>Login</h1>\n'
                       b'<form action="/login" method="POST">\n    Username: <input type="text" name="user"><br>\n'
                       b'    Password: <input type="password" name="pwd"><br>\n    <input type="hidden" '
                       b'name="redirectto" value="home">\n    <input type="submit" value="Login">\n</form>\n<br>\n'
                       b'<div style="color: red;"></div><br>\n\n        </div>\n    </body>\n</html>')

        # when
        result = self.app.get('/login')

        # then
        self.assertTrue(expected in str(result.data))

    def test_returned_data_when_logout_page_is_called(self):
        # given
        expected = str(b'<!doctype html>\n<html>\n    <head>\n        <title>Project Makalu - Broken Session Handling '
                       b'Shop</title>\n        <link rel="stylesheet" href="/static/style.css">\n        <link rel='
                       b'"icon" href="/static/favicon.ico" />\n    </head>\n    <body>\n        <div class="header">\n'
                       b'            <div class="logo" align="left">anna group</div>\n            <a href="/">Home</a>'
                       b'\n            \n                <a href="/login">Login</a>\n            \n        </div>\n'
                       b'        <div class="content">\n            \n<h1>Login</h1>\n<form action="/login" '
                       b'method="POST">\n    Username: <input type="text" name="user"><br>\n    Password: '
                       b'<input type="password" name="pwd"><br>\n    <input type="hidden" name="redirectto" '
                       b'value="home">\n    <input type="submit" value="Login">\n</form>\n<br>\n<div style="color:'
                       b' red;">You have successfully logged out.</div><br>\n\n        </div>\n    </body>\n</html>')

        # when
        result = self.app.get('/logout')

        # then
        self.assertTrue(expected in str(result.data))


if __name__ == "__main__":
    unittest.main()
