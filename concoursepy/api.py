import json

import requests

class api:
    def __init__(self, url, team, username, password):
        self.url = url
        self.team = team
        self.username = username
        self.password = password
        self.ATC_AUTH = ""
        self.auth()

    def jobs(self, pipeline_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/jobs" % (self.url, self.team, pipeline_name))

    def build_plan(self, build_id):
        return self.get("%s/api/v1/builds/%s/plan" % (self.url, build_id))

    def build(self, build_id):
        return self.get("%s/api/v1/builds/%s" % build_id)

    def versions(self, pipeline_name, resource_name, limit=100):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions?limit=%s" % (self.url, self.team, pipeline_name, resource_name, limit))

    def input_to(self, pipeline_name, resource_name, resource_id):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/input_to" % (self.url, self.team, pipeline_name, resource_name, resource_id))

    def output_of(self, pipeline_name, resource_name, resource_id):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/output_of" % (self.url, self.team, pipeline_name, resource_name, resource_id))

    def trigger(self, pipeline_name, job_name):
        return self.post("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/builds" % (self.url, self.team, pipeline_name, job_name))

    def enable(self, pipeline_name, resource_name, job_name):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/enable" % (self.url, self.team, pipeline_name, resource_name, job_name))

    def disable(self, pipeline_name, resource_name, job_name):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/disable" % (self.url, self.team, pipeline_name, resource_name, job_name))

    def pause_job(self, pipeline_name, job_name):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/pause" % (self.url, self.team, pipeline_name, job_name))

    def unpause_job(self, pipeline_name, job_name):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/unpause" % (self.url, self.team, pipeline_name, job_name))

    def pause_resource(self, pipeline_name, resource_name):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/resources/%s/pause" % (self.url, self.team, pipeline_name, resource_name))

    def unpause_resource(self, pipeline_name, resource_name):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/resources/%s/unpause" % (self.url, self.team, pipeline_name, resource_name))

    def get_pipeline(self, pipeline_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s" % (self.url, self.team, pipeline_name))

    def auth(self):
        r = requests.get("%s/auth/basic/token?team_name=%s" % (self.url, self.team), auth=(self.username, self.password), headers = {'Content-Type': 'application/json'})
        if r.status_code == requests.codes.ok:
            self.ATC_AUTH = json.loads(r.text)['value']
            return True
        return False

    def get(self, url):
        r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': "Bearer %s" % self.ATC_AUTH})
        if r.status_code == 401 or r.text == 'not authorized':
            self.auth()
            r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': "Bearer %s" % self.ATC_AUTH})
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        return False

    def post(self, url, post_data):
        r = requests.post(url, headers={'Content-Type': 'application/json', 'Authorization': "Bearer %s" % self.ATC_AUTH}, data=post_data)
        if r.status_code == 401 or r.text == 'not authorized':
            self.auth()
            r = requests.post(url, headers={'Content-Type': 'application/json', 'Authorization': "Bearer %s" % self.ATC_AUTH}, data=post_data)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        return False

    def put(self, url):
        r = requests.put(url, headers={'Content-Type': 'application/json', 'Authorization': "Bearer %s" % self.ATC_AUTH})
        if r.status_code == 401 or r.text == 'not authorized':
            self.auth()
            r = requests.put(url, headers={'Content-Type': 'application/json', 'Authorization': "Bearer %s" % self.ATC_AUTH})
        if r.status_code == requests.codes.ok:
            return True
        return False
