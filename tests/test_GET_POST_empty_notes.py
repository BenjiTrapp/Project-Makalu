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
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_should_return_200_when_notes_page_is_called_with_post_and_adding_an_emty_note(self):
        # when
        response = self.app.post('/Notes',
                                 content_type = 'multipart/form-data',
                                 follow_redirects = True,
                                 data = {'action': 'add',
                                         'submit': 'Add'})
        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_notes_page_is_called_with_post_and_deleting_empty_note(self):
        # when
        response = self.app.post('/Notes',
                                 content_type = 'multipart/form-data',
                                 follow_redirects = True,
                                 data = {'action': 'delete',
                                         'id': '1',
                                         'submit': 'Delete'})

        # then
        self.assertEqual(response.status_code, 200)

    ##### Tests to show lousy implementation for GET

    def test_should_return_200_when_notes_page_is_called_with_get_and_adding_an_emty_note(self):
        # when
        response = self.app.get('/Notes',
                                content_type = 'multipart/form-data',
                                follow_redirects = True,
                                data = {'action': 'add',
                                        'submit': 'Add'}
                                )

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_200_when_notes_page_is_called_with_get_and_deleting_empty_note(self):
        # when
        response = self.app.get('/Notes',
                                content_type = 'multipart/form-data',
                                follow_redirects = True,
                                data = {'action': 'delete',
                                        'id': '1',
                                        'submit': 'Delete'}
                                )

        # then
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
