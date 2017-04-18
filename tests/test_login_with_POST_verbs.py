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

    def test_should_return_200_when_login_page_is_called_with_post_and_valid_credentials(self):
        # when
        response = self.app.post('/login', content_type = 'multipart/form-data', follow_redirects = True,
                                 data = {'user': 'user', 'pwd': 'hallo', 'redirectto': 'home', 'submit': 'Login'})

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_login_correctly_when_called_with_post_and_valid_credentials(self):
        #given
        expected = str('Logged in as user')

        # when
        result = self.app.post('/login', content_type = 'multipart/form-data', follow_redirects = True,
                                 data = {'user': 'user', 'pwd': 'hallo', 'redirectto': 'home', 'submit': 'Login'})

        # then
        self.assertTrue(expected in str(result.data))

    def test_should_return_200_when_login_page_is_called_with_post_and_invalid_credentials(self):
        # when
        result = self.app.post('/login', content_type = 'multipart/form-data', follow_redirects = True,
                                 data = {'user': 'wrong', 'pwd': 'wrong', 'redirectto': 'home', 'submit': 'Login'})

        # then
        self.assertEqual(result.status_code, 200)

    def test_should_NOT_login__when_called_with_post_and_invalid_credentials(self):
        # given
        expected = str('User wrong unknown!')

        # when
        result = self.app.post('/login', content_type = 'multipart/form-data', follow_redirects = True,
                               data = {'user': 'wrong', 'pwd': 'wrong', 'redirectto': 'home', 'submit': 'Login'})

        # then
        self.assertTrue(expected in str(result.data))


    def test_should_return_400_when_login_page_is_called_with_post_and_no_credentials(self):
        # when
        response = self.app.post('/login', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
