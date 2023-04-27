import json
import time
from datetime import datetime, timedelta

import rest_framework.status as http_status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import requests, csv, os

TEMPO_CLIENT_ID = "2d1Rg7Nj2GankVs580AqOhivW6R72Q"
JIRA_BASIC_TOKEN = "aGFpLnRydW9uZ0BkYXRhZmx1Y3QuY29tOkFUQVRUM3hGZkdGMEtYYWwwLWZHUlh0WWVqeE52MENId3ltUXllcWRRY0pQcWFxRF8wcTJwZDJpbDIxTVBGZ2tRMVJydnhScmYxc2QyWGRUd3RNTWxyR1Y5ZEttWjk1VFNDNjk1b0JpNXJVWUNqYkVmSlJ1VS1VU0dYR09vOTNlTkNRRGwtUFRUX0JoSUZwTG1SZVNGMGFRNXJEVTlOZ3lENXRBNk1QWVRHUVBHTkhCQUVHYVlkWT0xRTE3MzIxMw=="
TZ = {"JST": 9}  # JST = GMT + 9

jira_time_spent_record: dict = {
    "issue_type": "",
    "issue_key": "",
    "issue_id": "",
    "parent_id": "",
    "summary": "",
    "assignee": "",
    "assignee_id": "",
    "reporter": "",
    "reporter_id": "",
    "priority": "",
    "status": "",
    "resolution": "",
    "created": "",
    "updated": "",
    "due_date": "",
    "time_spent": "",
    "sum_time_spent": "",
    "project_key": "",
    "project_name": "",
    "project_type": "",
    "project_lead": "",
    "project_lead_id": "",
    "project_description": "",
    "project_url": "",
}


def MiliSecondsToGmt(
    milisec: int = 0, tz: int = 0, format: str = "%Y-%m-%dT%H:%M:%S.%f"
) -> str:
    # GMT + TZ
    return (datetime.fromtimestamp(milisec / 1000) + timedelta(hours=tz)).strftime(
        format
    ) + f"+{tz}"


def GetProjectDetail(proj_id: str = None) -> dict:
    if not id:
        return None

    headers = {"Authorization": f"Basic {JIRA_BASIC_TOKEN}"}
    resp = requests.get(
        "https://datafluct-international.atlassian.net/rest/api/2/project/" + proj_id,
        headers=headers,
    )
    resp_data = resp.json()
    if "errors" in resp_data:
        return None

    return {
        "lead_id": resp_data["lead"]["accountId"],
        "lead_name": resp_data["lead"]["displayName"],
        "project_description": resp_data["description"],
        "project_url": f"https://datafluct-international.atlassian.net/browse/{resp_data['key']}",
    }


def PrepareDataToStore(data: dict) -> list:
    # This function is used for 'Web request body' = 'Automation format'
    # if 'Web request body' has been changed, this function will raise error.PLEASE CHECK AUTOMATION CAREFULLY.
    jira_time_spent_record["issue_type"] = data["fields"]["issuetype"]["name"]
    jira_time_spent_record["issue_key"] = data["key"]
    jira_time_spent_record["issue_id"] = data["id"]
    jira_time_spent_record["parent_id"] = (
        # if issue doen't have parent, response data doesn't have "parent" field
        data["fields"]["parent"]["id"]
        if "parent" in data["fields"] and data["fields"]["parent"]
        else ""
    )
    jira_time_spent_record["summary"] = data["fields"]["summary"]
    jira_time_spent_record["assignee"] = data["fields"]["assignee"]["displayName"]
    jira_time_spent_record["assignee_id"] = data["fields"]["assignee"]["accountId"]
    jira_time_spent_record["reporter"] = data["fields"]["reporter"]["displayName"]
    jira_time_spent_record["reporter_id"] = data["fields"]["reporter"]["accountId"]
    jira_time_spent_record["priority"] = data["fields"]["priority"]["name"]
    jira_time_spent_record["status"] = data["fields"]["status"]["name"]
    jira_time_spent_record["resolution"] = (
        data["fields"]["resolution"]["name"]
        if "resolution" in data["fields"] and data["fields"]["resolution"]
        else ""
    )
    jira_time_spent_record["created"] = MiliSecondsToGmt(
        milisec=data["fields"]["created"], tz=TZ["JST"]
    )

    jira_time_spent_record["updated"] = (
        MiliSecondsToGmt(milisec=data["fields"]["updated"], tz=TZ["JST"])
        if "updated" in data["fields"]
        else ""
    )
    jira_time_spent_record["due_date"] = (
        data["fields"]["duedate"] if "duedate" in data["fields"] else ""
    )
    jira_time_spent_record["time_spent"] = data["fields"]["timetracking"][
        "timeSpentSeconds"
    ]
    jira_time_spent_record["sum_time_spent"] = data["fields"]["timetracking"][
        "originalEstimateSeconds"
    ]

    jira_time_spent_record["project_key"] = data["fields"]["project"]["key"]
    jira_time_spent_record["project_name"] = data["fields"]["project"]["name"]
    jira_time_spent_record["project_type"] = data["fields"]["project"]["projectTypeKey"]

    data_row = [v for _, v in jira_time_spent_record.items()]
    return data_row


# Create your views here.
class ShowJiraInfo(APIView):
    """
    Jira Automation use POST method to push data to backend.
    request.data : a dict of data from Jira.
    """

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # if not os.path.exists("csv/"):
        #     os.mkdir("csv/")
        # data_row = [v for _, v in jira_time_spent_record.items()]
        # with open("csv/file.csv", mode="a", encoding="utf-8", newline="") as csvfile:
        #     csvwriter = csv.writer(csvfile)
        #     csvwriter.writerow(data_row)
        return JsonResponse({"message": "Hahaha"})

    def post(self, request, format=None):
        if not os.path.exists("csv/"):
            os.mkdir("csv/")

        # use this line to check this function
        # print(request.data)
        # l = PrepareDataToStore(request.data)

        # need to call API to get project lead of the current object
        # get project detail data. All issues of each request belongs to same project
        project_detail = GetProjectDetail(str(request.data["fields"]["project"]["id"]))
        # init global variable: jira_time_spent_record
        if project_detail:
            jira_time_spent_record["project_lead"] = project_detail["lead_name"]
            jira_time_spent_record["project_lead_id"] = project_detail["lead_id"]
            jira_time_spent_record["project_description"] = project_detail[
                "project_description"
            ]
            jira_time_spent_record["project_url"] = project_detail["project_url"]

        # get data from Jira Automation
        try:
            with open(
                f"csv/jira_time_spent{round(time.time())}.csv",
                mode="w",
                encoding="utf-8",
                newline="",
            ) as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(PrepareDataToStore(request.data))
        except Exception as e:
            print("====>", e)

        # file_name = f"result{round(time.time())}.json"
        # with open(file_name, "a") as f:
        #     f.write(json.dumps(request.data, indent=4))

        return Response(
            {"message": "OK"},
            status=http_status.HTTP_200_OK,
        )


class GetTempoTokens(APIView):
    # this endpoint uses the REST API as an application developer
    # this approach may be a wrong way!!!
    permission_classes = [AllowAny]

    def get(self, request):
        # get and show Authorization Code of Tempo.
        # Tempo needs a Redirect URL to give Authorization code
        authorization_code = request.GET.get("code")
        # print(authorization_code)
        data = {
            "grant_type": "authorization_code",
            "client_id": "fc8364816f554545979c790adf8d8b62",
            "client_secret": "71DBA4308FC7731095F91632B087F765D9A5FE4C8100DC5EEBC8AB810171A5F5",
            "redirect_uri": "https://ec54-2405-4802-80f1-6600-9542-e503-1181-75bc.ngrok-free.app/jira/GetTempoTokens/",
            "code": authorization_code,
        }
        resp = requests.post("https://api.tempo.io/oauth/token/", data=data)
        print(resp.status_code)
        resp_json = resp.json()
        print(type(resp_json))
        print(json.dumps(resp_json, indent=4))
        return JsonResponse({"message": "This is endpoint for Tempo tokens"})


class GetTempoWorklog(APIView):
    # This endpoint uses the REST API as an individual user
    permission_classes = [AllowAny]

    def get(self, req):
        query_string = {"limit": 500}
        headers = {"Authorization": f"Bearer {TEMPO_CLIENT_ID}"}
        resp = requests.get(
            "https://api.tempo.io/4/worklogs", headers=headers, params=query_string
        )
        print(resp.url)
        print(resp.status_code)

        return JsonResponse({"results": resp.json()["results"]})
