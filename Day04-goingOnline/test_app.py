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
        self.assertIn(b"Enter only the exponent", response.data)
        self.assertIn(b"Range: -4 to 4", response.data)

    def test_valid_measurements_return_plot_and_comparison(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "5778", "luminosity_exponent": "0"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Catalog comparison", response.data)
        self.assertIn(b"data:image/png;base64,", response.data)
        self.assertIn(b"10<sup>0</sup> L", response.data)
        self.assertIn(b"does not prove", response.data)

    def test_temperature_outside_diagram_range_is_rejected(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "1", "luminosity_exponent": "0"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Temperature must be between 2,500 and 15,000 K", response.data)
        self.assertNotIn(b"Catalog comparison", response.data)

    def test_luminosity_exponent_outside_range_is_rejected(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "5000", "luminosity_exponent": "5"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Luminosity exponent must be between -4 and 4", response.data)
        self.assertNotIn(b"Catalog comparison", response.data)

    def test_fractional_luminosity_exponent_is_rejected(self):
        response = self.client.post(
            "/",
            data={"temperature_K": "5000", "luminosity_exponent": "-2.5"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"whole-number luminosity exponent", response.data)
        self.assertNotIn(b"Catalog comparison", response.data)


if __name__ == "__main__":
    unittest.main()
