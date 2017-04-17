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

    def test_should_return_200_when_main_page_is_called_with_get(self):
        # when
        response = self.app.get('/', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_login_page_is_called_with_get(self):
        # when
        response = self.app.get('/login', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_logout_page_is_called_with_get(self):
        # when
        response = self.app.get('/logout', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_orderarticle_step1_page_is_called_with_get(self):
        # when
        response = self.app.get('/OrderArticle/1', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_orderarticle_step2_page_is_called_with_get(self):
        # when
        response = self.app.get('/OrderArticle/2', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_orderarticle_step3_page_is_called_with_get(self):
        # when
        response = self.app.get('/OrderArticle/3', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_orderarticle_step4_page_is_called_with_get(self):
        # when
        response = self.app.get('/OrderArticle/4', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_csrf_protected_page_is_called_with_get(self):
        # when
        response = self.app.get('/CSRFProtected', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_notes_page_is_called_with_get(self):
        # when
        response = self.app.get('/Notes', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_probalistic_logout_page_is_called_with_get(self):
        # when
        response = self.app.get('/ProbabilisticLogout', follow_redirects = True)

        # then
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
