import unittest

class TestManhattanAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from app import app as flask_app
        except ModuleNotFoundError as exc:
            raise unittest.SkipTest(f"Flask app dependency missing: {exc}")

        cls.app = flask_app

    def setUp(self):
        self.client = self.app.test_client()

    def test_manhattan_success(self):
        response = self.client.post(
            "/manhattan",
            json={"df1": [[1, 2], [3, 4]], "df2": [[2, 0], [1, 3]]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"distance": 6.0})

    def test_home_route(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    def test_unknown_route_returns_404(self):
        response = self.client.get("/favicon.ico")

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_missing_required_keys(self):
        response = self.client.post("/manhattan", json={"df1": [[1, 2]]})

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_shape_mismatch(self):
        response = self.client.post(
            "/manhattan",
            json={"df1": [[1, 2], [3, 4]], "df2": [[1, 2, 3]]},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("shapes must match", response.get_json()["error"])

    def test_non_numeric_data(self):
        response = self.client.post(
            "/manhattan",
            json={"df1": [[1, 2], [3, 4]], "df2": [["x", 0], [1, 3]]},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("numeric", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
