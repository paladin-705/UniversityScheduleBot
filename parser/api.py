from config import url, token
import requests
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def add_organization(organization, faculty, group):
    data = (
        {"key": token,
         'data': [
             {
                 'organization': organization,
                 'faculty': faculty,
                 'group': group,
             }
         ]
         }
    )
    res = requests.post(url + '/api/organization', json=data, verify=False)
    answer = json.loads(res.text)

    if len(answer['failed']) != 0:
        with open('failed-organization.txt', "a") as file:
            for d in answer['failed']:
                file.write(str(d['data']) + '\n')
        return None

    if len(answer['ok']) != 0:
        return answer['ok'][0]['tag']

    return None


def add_lesson(tag, day, number, week_type, time_start, time_end, title, classroom, lecturer):
    data = (
        {"key": token,
         'data': [
             {
                 'tag': tag,
                 'day': day,
                 'number': number,
                 'week_type': week_type,
                 'time_start': time_start,
                 'time_end': time_end,
                 'title': title,
                 'classroom': classroom,
                 'lecturer': lecturer
             }
         ]
         }
    )
    res = requests.post(url + '/api/schedule', json=data, verify=False)
    answer = json.loads(res.text)

    if len(answer['failed']) != 0:
        with open('failed-schedule.txt', "a") as file:
            for d in answer['failed']:
                file.write(str(d['data']) + '\n')
        return False

    return True
