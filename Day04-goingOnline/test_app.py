import unittest

import app as star_app


class StarAppTests(unittest.TestCase):
    def setUp(self):
        star_app.app.config["TESTING"] = True
        self.client = star_app.app.test_client()

    def test_home_page_shows_supported_ranges(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"2,500", response.data)
        self.assertIn(b"15,000", response.data)
        self.assertIn(b"1e-04", response.data)
        self.assertIn(b"1e+04", response.data)

    def test_valid_measurements_return_plot_and_comparison(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "5778", "luminosity_Lsun": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Catalog comparison", response.data)
        self.assertIn(b"data:image/png;base64,", response.data)
        self.assertIn(b"does not prove", response.data)

    def test_temperature_outside_diagram_range_is_rejected(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "1", "luminosity_Lsun": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Temperature must be between 2,500 and 15,000 K", response.data)
        self.assertNotIn(b"Catalog comparison", response.data)

    def test_luminosity_outside_diagram_range_is_rejected(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "5000", "luminosity_Lsun": "0"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Luminosity must be between 0.0001 and 10000 L", response.data)
        self.assertNotIn(b"Catalog comparison", response.data)


if __name__ == "__main__":
    unittest.main()
