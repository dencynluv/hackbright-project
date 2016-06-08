# import unittest
# from unittest import TestCase
# import server
# from server import app

# # to test:
# # python test.py
# # coverage:
# # coverage run --omit=env/* test.py
# # coverage run --source=. test.py
# # for report:
# # coverage report -m

# class MyAppIntegrationTestCase(TestCase):
#     def setUp(self):
#         self.client = server.app.test_client()
#         server.app.config['TESTING'] = True
#         server.app.config['DEBUG'] = False

#     def test_home(self):
#         test_client = server.app.test_client()
#         result = test_client.get('/')
#         self.assertIn('<h3 class="login-labels">Sign In</h3>', result.data)

#     # def test_homepage_route(self):
#     #     test_client = server.app.test_client()
#     #     result = test_client.get('/homepage')
#     #     self.assertIn('<h1>TEST</h1>', result.data)

#     # def test_favorites_route(self):
#     #     test_client = server.app.test_client()
#     #     result = test_client.get('/favorites')
#     #     self.assertIn('<h1>Favorites</h1>', result.data)

#     # def tearDown(self):
#     #     print "(tearDown ran)"

# if __name__ == "__main__":
#     unittest.main() 