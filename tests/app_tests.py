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

    def test_should_return_200_when_main_page_is_called(self):
        # when
        response = self.app.get('/', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_login_page_is_called(self):
        # when
        response = self.app.get('/login', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_logout_page_is_called(self):
        # when
        response = self.app.get('/logout', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_orderarticle_step1_page_is_called(self):
        # when
        response = self.app.get('/OrderArticle/1', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()