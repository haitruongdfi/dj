# added for testing

import datetime
import logging  # use this for log

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

logger = logging.getLogger()


def hello_reader(req):
    logger.warning(
        "WARN - Homepage was accessed at " + str(datetime.datetime.now()) + " hours!"
    )
    return HttpResponse("<h1>Hello, I am learning logging</h1>")


# Create your views here.
class MyList(View):  # this is used for testing int folder tests/
    raw_list = []

    def __init__(self, l=[]):
        self.raw_list = [str(i) for i in l]

    def showList(self):
        print(",".join(self.raw_list))

    def ascList(self):
        return self.raw_list.sort()
        # return (",".join(self.raw_list))

    def desList(self):
        return self.raw_list.sort(reverse=True)
        # return (",".join(self.raw_list))
