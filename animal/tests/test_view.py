from django.test import TestCase

from ..views import MyList


class MyListTestCase(TestCase):
    def test_MyList(self):
        l = MyList([8, 5, 89, 2, 2, 7, 3, 2])

        l.ascList()
        self.assertEqual(l.raw_list, ["2", "2", "2", "3", "5", "7", "8", "89"])

        l.desList()
        self.assertEqual(l.raw_list, ["89", "8", "7", "5", "3", "2", "2", "2"])
