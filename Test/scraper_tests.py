import unittest
from CyberRatv1.CyberRATWeb.scrapers.scrappers import *

from CyberRatv1.CyberRATWeb.services.timeline_analyzer import scan_for_dog_name,\
    scan_for_mothers_maiden, scan_for_city_names,\
    scan_for_street_name, scan_for_favourite_book

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


    def test_gather_locations(self):
        results = get_instagram_posts('https://www.instagram.com/johnyboysmith1992/')
        city_names = scan_for_city_names(results)

        print(city_names)

        self.assertTrue(city_names is not None)


    def test_for_street_name(self):
        results = get_instagram_posts('https://www.instagram.com/johnyboysmith1992/')
        street_name = scan_for_street_name(results)
        print(street_name)

        self.assertTrue(street_name is not None)

    def test_favourite_book(self):
        results = get_instagram_posts('https://www.instagram.com/johnyboysmith1992/')
        favourite_book = scan_for_favourite_book(results)

        print(favourite_book)

        self.assertTrue(favourite_book is not None)


if __name__ == '__main__':
    unittest.main()