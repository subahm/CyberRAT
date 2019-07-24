import unittest
from CyberRatv1.CyberRATWeb.scrapers.instagram_scrapper import get_instagram_posts

class ScrapperTests(unittest.TestCase):

    def test_instagram_scraper(self):
        result = get_instagram_posts('https://www.instagram.com/smittwagner')
        self.assertTrue(result is not [])

if __name__ == '__main__':
    unittest.main()