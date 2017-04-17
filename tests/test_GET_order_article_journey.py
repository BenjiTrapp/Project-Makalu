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

    ######################### Following redirects #########################

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

    ######################### NOT Following redirects #########################

    def test_should_return_302_when_orderarticle_step1_page_is_called_with_get_not_following_redirects(self):
        # when
        response = self.app.get('/OrderArticle/1', follow_redirects = False)

        # then
        self.assertEqual(response.status_code, 302)

    def test_should_return_302_when_orderarticle_step2_page_is_called_with_get_not_following_redirects(self):
        # when
        response = self.app.get('/OrderArticle/2', follow_redirects = False)

        # then
        self.assertEqual(response.status_code, 302)

    def test_should_return_302_when_orderarticle_step3_page_is_called_with_get_not_following_redirects(self):
        # when
        response = self.app.get('/OrderArticle/3', follow_redirects = False)

        # then
        self.assertEqual(response.status_code, 302)

    def test_should_return_302_when_orderarticle_step4_page_is_called_with_get_not_following_redirects(self):
        # when
        response = self.app.get('/OrderArticle/4', follow_redirects = False)

        # then
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
