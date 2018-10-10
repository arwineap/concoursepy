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

    def list_builds(self):
        return self.get("%s/api/v1/builds" % (self.url))

    def get_build(self, build_id):
        return self.get("%s/api/v1/build/%s" % (self.url, build_id))

    def build(self, build_id):
        """Leaving this here for backwards compatibility."""
        return self.get_build(build_id)

    def get_build_plan(self, build_id):
        return self.get("%s/api/v1/builds/%s/plan" % (self.url, build_id))

    def build_plan(self, build_id):
        """Leaving this here for backwards compatibility."""
        return self.get_build_plan(build_id)

    def send_input_to_build_plan(self, build_id, plan_id):
        return self.put("%s/api/v1/builds/%s/plan/%s/input" % (self.url, build_id, plan_id))

    def read_output_from_build_plan(self, build_id, plan_id):
        return self.get("%s/api/v1/builds/%s/plan/%s/input" % (self.url, build_id, plan_id))

    def build_events(self, build_id):
        return self.get("%s/api/v1/builds/%s/events" % (self.url, build_id))

    def build_resources(self, build_id):
        return self.get("%s/api/v1/builds/%s/resources" % (self.url, build_id))

    def abort_build(self, build_id):
        return self.put("%s/api/v1/builds/%s/abort" % (self.url, build_id))

    def get_build_preperation(self, build_id):
        return self.get("%s/api/v1/builds/%s/preperation" % (self.url, build_id))

    def list_resource_versions(self, pipeline_name, resource_name, limit=100):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions?limit=%s" % (self.url, self.team, pipeline_name, resource_name, limit))

    def versions(self, pipeline_name, resource_name, limit=100):
        """Leaving this here for backwards compatibility."""
        return self.list_resource_versions(pipeline_name, resource_name, limit)

    def get_resource_version(self, pipeline_name, resource_name, resource_version_id):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s" % (self.url, self.team, pipeline_name, resource_name, resource_version_id))

    def enable_resource_version(self, pipeline_name, resource_name, resource_version_id):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/enable" % (self.url, self.team, pipeline_name, resource_name, resource_version_id))

    def enable(self, pipeline_name, resource_name, resource_version_id):
        return self.enable_resource_version(pipeline_name, resource_name, resource_version_id)

    def disable_resource_version(self, pipeline_name, resource_name, resource_version_id):
        return self.put("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/disable" % (self.url, self.team, pipeline_name, resource_name, resource_version_id))

    def disable(self, pipeline_name, resource_name, resource_version_id):
        return self.disable_resource_version(pipeline_name, resource_name, resource_version_id)

    def list_builds_with_version_as_input(self, pipeline_name, resource_name, resource_id):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/input_to" % (self.url, self.team, pipeline_name, resource_name, resource_id))

    def input_to(self, pipeline_name, resource_name, resource_id):
        """Leaving this here for backwards compatibility."""
        return self.list_builds_with_version_as_input(pipeline_name, resource_name, resource_id)

    def list_builds_with_version_as_output(self, pipeline_name, resource_name, resource_id):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/resources/%s/versions/%s/output_to" % (self.url, self.team, pipeline_name, resource_name, resource_id))

    def output_of(self, pipeline_name, resource_name, resource_id):
        """Leaving this here for backwards compatibility."""
        return self.list_builds_with_version_as_output(pipeline_name, resource_name, resource_id)

    def create_job_build(self, pipeline_name, job_name):
        return self.post("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/builds" % (self.url, self.team, pipeline_name, job_name))

    def trigger(self, pipeline_name, job_name):
        """Leaving this here for backwards compatibility."""
        return self.create_job_build(pipeline_name, job_name)

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

    def list_all_jobs(self):
        return self.get("%s/api/v1/jobs")

    def list_jobs(self, pipeline_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/jobs" % (self.url, self.team, pipeline_name))

    def get_job(self, pipeline_name, job_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/jobs/%s")

    def list_job_builds(self, pipeline_name, job_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/builds" % (self.url, self.team, pipeline_name, job_name))

    def get_job_build(self, pipeline_name, job_name, build_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/builds/%s" % (self.url, self.team, pipeline_name, job_name, build_name))

    def job_badge(self, pipeline_name, job_name):
        return self.get("%s/api/v1/teams/%s/pipelines/%s/jobs/%s/badge" % (self.url, self.team, pipeline_name, job_name))

    def main_job_badge(self, pipeline_name, job_name):
        return self.get("%s/api/v1/pipelines/%s/jobs/%s/badge" % (self.url, pipeline_name, job_name))

    def auth(self):
        self.ATC_AUTH = None
        session = requests.Session()
        r = session.get("%s/sky/login" % self.url)
        if r.status_code == 200:
            post_url = list(filter(lambda x: '/sky/issuer/auth/local' in x, r.text.split("\n")))[0].strip().split('"')[1]
            r = session.post("%s%s" % (self.url, post_url), data={'login': self.username, 'password': self.password})
            if r.status_code == requests.codes.ok:
                self.ATC_AUTH = session.cookies.get_dict()['skymarshal_auth'].split('"')[1].split()[1]
        if self.ATC_AUTH:
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
