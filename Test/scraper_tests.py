import unittest
from CyberRatv1.CyberRATWeb.scrapers.instagram_scrapper import get_instagram_posts
from CyberRatv1.CyberRATWeb.scrapers.timeline_post import TimelinePost

from CyberRatv1.CyberRATWeb.services.timeline_analyzer import scan_for_dog_name, scan_for_mothers_maiden

class Tests(unittest.TestCase):

    def test_instagram_scraper(self):
        result = get_instagram_posts('https://www.instagram.com/smittwagner/')
        self.assertTrue(result is not [])

    def test_instagram_dog_name(self):

        results = get_instagram_posts('https://www.instagram.com/johnyboysmith1992/')
        dog_post = scan_for_dog_name(results)

        print("DOG NAME\n"+dog_post)

        self.assertTrue(dog_post is not None)

    def test_instagram_mothers_maiden(self):

        results = get_instagram_posts('https://www.instagram.com/johnyboysmith1992/')
        mothers_maiden = scan_for_mothers_maiden(results)

        print("MOTHERS MAIDEN\n"+mothers_maiden)

        self.assertTrue(mothers_maiden is not None)

if __name__ == '__main__':
    unittest.main()