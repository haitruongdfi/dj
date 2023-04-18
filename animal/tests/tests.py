import datetime
import logging

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Animal

logger = logging.getLogger("haitruongLogger")  # logger is set in LOGGING of settings.py

# Create your tests here.
class AnimalTestCase(
    TestCase
):  # to create a test case in your Django project, you will define a class that inherits from TestCase.
    def setUp(self):
        # this method will run before each unit test case
        # print("hello")
        Animal.objects.create(name="lion", sound="roar", size="big", age=3)
        Animal.objects.create(name="cat", sound="meow", age=1)
        Animal.objects.create(name="duck", sound="quack", age=2)

    def tearDown(self):
        print("This line was printed out from tearDown() method")

    def test_animal_speak(self):  # test case method MUST begin with "test"
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")

        logger.info("Start of test animal speak at " + str(datetime.datetime.now()))
        logger.debug(lion.speak())
        self.assertEqual(lion.speak(), "lion speaks roar")

        logger.debug(cat.speak())
        self.assertEqual(cat.speak(), "cat speaks meow")
        logger.info("End of test animal speak")
        logger.debug("------")

    def test_animal_size(self):
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")

        self.assertEqual(lion.howBig(), "big")
        self.assertEqual(cat.howBig(), "sml")

    def even_number(self, val):
        if (val % 2) != 0:
            raise ValidationError(
                "%(value)s is not an even number", params={"value": val}
            )

    def test_animal_age_is_number(self):
        pet = Animal.objects.get(name="cat")
        with self.assertRaises(ValidationError):
            self.even_number(pet.age)
