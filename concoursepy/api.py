import collections
import json
from os.path import join as pathjoin
import re
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError


LOGIN_REG = re.compile(r'"/sky/issuer/auth/local.*?"')


class Api:
    def __init__(self, url, username=None, password=None, token=None):
        self.url = url
        self.api_path = '/api/v1/'
        self.username = username
        self.password = password
        self.ATC_AUTH = token
        self.session = None
        self.auth()

    def list_teams(self):
        return self.get('teams')

    def get_team(self, team_name):
        return self.get('teams/%s' % team_name)

    def get_config(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/config" % (team_name, pipeline_name)
        )

    def jobs(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs" % (team_name, pipeline_name)
        )

    def list_builds(self):
        return self.get("builds")

    def get_build(self, build_id):
        return self.get("build/%s" % build_id)

    def build(self, build_id):
        """Leaving this here for backwards compatibility."""
        return self.get_build(build_id)

    def get_build_plan(self, build_id):
        return self.get("builds/%s/plan" % build_id)

    def build_plan(self, build_id):
        """Leaving this here for backwards compatibility."""
        return self.get_build_plan(build_id)

    def send_input_to_build_plan(self, build_id, plan_id):
        return self.put("builds/%s/plan/%s/input" % (build_id, plan_id))

    def read_output_from_build_plan(self, build_id, plan_id):
        return self.get("builds/%s/plan/%s/input" % (build_id, plan_id))

    def build_events(self, build_id):
        return self.get("builds/%s/events" % build_id)

    def build_resources(self, build_id):
        return self.get("builds/%s/resources" % build_id)

    def abort_build(self, build_id):
        return self.put("builds/%s/abort" % build_id)

    def get_build_preparation(self, build_id):
        return self.get("builds/%s/preparation" % build_id)

    def list_all_jobs(self):
        return self.get("jobs")

    def list_jobs(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs" % (team_name, pipeline_name)
        )

    def get_job(self, team_name, pipeline_name, job_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs/%s" % (
                team_name, pipeline_name, job_name
            )
        )

    def list_job_builds(self, team_name, pipeline_name, job_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs/%s/builds" % (
                team_name, pipeline_name, job_name
            )
        )

    def create_job_build(self, team_name, pipeline_name, job_name):
        return self.post(
            "teams/%s/pipelines/%s/jobs/%s/builds" % (
                team_name, pipeline_name, job_name
            )
        )

    def trigger(self, team_name, pipeline_name, job_name):
        """Leaving this here for backwards compatibility."""
        return self.create_job_build(team_name, pipeline_name, job_name)

    def list_job_inputs(self, team_name, pipeline_name, job_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs/%s/inputs" % (
                team_name, pipeline_name, job_name
            )
        )

    def get_job_build(self, team_name, pipeline_name, job_name, build_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs/%s/builds/%s" % (
                team_name, pipeline_name, job_name, build_name
            )
        )

    def pause_job(self, team_name, pipeline_name, job_name):
        return self.put(
            "teams/%s/pipelines/%s/jobs/%s/pause" % (
                team_name, pipeline_name, job_name
            )
        )

    def unpause_job(self, team_name, pipeline_name, job_name):
        return self.put(
            "teams/%s/pipelines/%s/jobs/%s/unpause" % (
                team_name, pipeline_name, job_name
            )
        )

    def job_badge(self, team_name, pipeline_name, job_name):
        return self.get(
            "teams/%s/pipelines/%s/jobs/%s/badge" % (
                team_name, pipeline_name, job_name
            )
        )

    def main_job_badge(self, pipeline_name, job_name):
        return self.get(
            "pipelines/%s/jobs/%s/badge" % (pipeline_name, job_name)
        )

    def list_all_pipelines(self):
        return self.get("pipelines")

    def list_pipelines(self, team_name):
        return self.get("teams/%s/pipelines" % team_name)

    def get_pipeline(self, team_name, pipeline_name):
        return self.get("teams/%s/pipelines/%s" % (team_name, pipeline_name))

    def pause_pipeline(self, team_name, pipeline_name):
        return self.put(
            "teams/%s/pipelines/%s/pause" % (team_name, pipeline_name)
        )

    def unpause_pipeline(self, team_name, pipeline_name):
        return self.put(
            "teams/%s/pipelines/%s/unpause" % (team_name, pipeline_name)
        )

    def list_pipeline_builds(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/builds" % (team_name, pipeline_name)
        )

    def pipeline_badge(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/badge" % (team_name, pipeline_name)
        )

    def list_all_resources(self):
        return self.get("resources")

    def list_resources(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/resources" % (team_name, pipeline_name)
        )

    def list_resource_types(self, team_name, pipeline_name):
        return self.get(
            "teams/%s/pipelines/%s/resource-types" % (team_name, pipeline_name)
        )

    def get_resource(self, team_name, pipeline_name, resource_name):
        return self.get(
            "teams/%s/pipelines/%s/resources/%s" % (
                team_name, pipeline_name, resource_name
            )
        )

    def list_resource_versions(
        self, team_name, pipeline_name, resource_name, limit=100
    ):
        return self.get(
            "teams/%s/pipelines/%s/resources/%s/versions?limit=%s" % (
                team_name, pipeline_name, resource_name, limit
            )
        )

    def versions(self, team_name, pipeline_name, resource_name, limit=100):
        """Leaving this here for backwards compatibility."""
        return self.list_resource_versions(
            team_name, pipeline_name, resource_name, limit
        )

    def get_resource_version(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.get(
            "teams/%s/pipelines/%s/resources/%s/versions/%s" % (
                team_name, pipeline_name, resource_name, resource_version_id
            )
        )

    def enable_resource_version(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.put(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/enable" % (
                team_name, pipeline_name, resource_name, resource_version_id
            )
        )

    def enable(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.enable_resource_version(
            team_name, pipeline_name, resource_name, resource_version_id
        )

    def disable_resource_version(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.put(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/disable" % (
                team_name, pipeline_name, resource_name, resource_version_id
            )
        )

    def disable(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.disable_resource_version(
            team_name, pipeline_name, resource_name, resource_version_id
        )

    def pin_resource_version(
        self, team_name, pipeline_name, resource_name,
        resource_config_version_id
    ):
        return self.put(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/pin" % (
                team_name, pipeline_name, resource_name,
                resource_config_version_id
            )
        )

    def unpin_resource_version(
        self, team_name, pipeline_name, resource_name,
        resource_config_version_id
    ):
        return self.put(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/unpin" % (
                team_name, pipeline_name, resource_name,
                resource_config_version_id
            )
        )

    def list_builds_with_version_as_input(
        self, team_name, pipeline_name, resource_name, resource_id
    ):
        return self.get(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/input_to" % (
                team_name, pipeline_name, resource_name, resource_id
            )
        )

    def input_to(self, team_name, pipeline_name, resource_name, resource_id):
        """Leaving this here for backwards compatibility."""
        return self.list_builds_with_version_as_input(
            team_name, pipeline_name, resource_name, resource_id
        )

    def list_builds_with_version_as_output(
        self, team_name, pipeline_name, resource_name, resource_id
    ):
        return self.get(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/output_to" % (
                team_name, pipeline_name, resource_name, resource_id
            )
        )

    def output_of(self, team_name, pipeline_name, resource_name, resource_id):
        """Leaving this here for backwards compatibility."""
        return self.list_builds_with_version_as_output(
            team_name, pipeline_name, resource_name, resource_id
        )

    def get_resource_causality(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.get(
            "teams/%s/pipelines/%s/resources/%s/versions/%s/causality" % (
                team_name, pipeline_name, resource_name, resource_version_id
            )
        )

    def pause_resource(self, team_name, pipeline_name, resource_name):
        return self.put(
            "teams/%s/pipelines/%s/resources/%s/pause" % (
                team_name, pipeline_name, resource_name
            )
        )

    def unpause_resource(self, team_name, pipeline_name, resource_name):
        return self.put(
            "teams/%s/pipelines/%s/resources/%s/unpause" % (
                team_name, pipeline_name, resource_name
            )
        )

    def _close_session(self):
        if isinstance(self.session, requests.Session):
            self.session.close()
        self.session = None

    def _set_new_session(self):
        self._close_session()
        self.session = requests.Session()
        return self.session

    def _get_skymarshal_auth(self):
        cookies_dict = self.session.cookies.get_dict()
        for key in ('skymarshal_auth', 'skymarshal_auth0'):
            if key in cookies_dict:
                return cookies_dict[key].split('"')[1].split()[1]
        # We did not find a token:
        self._close_session()
        raise ValueError("Couldn't read Token")

    def _make_api_url(self, path):
        """Return the api's full  url.

        If `path` does not have a leading slash self.api_path is prepended and
        we return something like '%s/%s/%s' % (self.url, self.api_path, path)

        If `path` has a leading slash self.api_path is not prepended and
        we return something like '%s/%s/%s' % (self.url, path)
        """
        return urljoin(self.url, pathjoin(self.api_path, path))

    @staticmethod
    def _get_login_post_path(html_txt):
        return LOGIN_REG.search(html_txt).group().strip('"')

    @property
    def has_username_and_passwd(self):
        return self.username is not None and self.password is not None

    def auth(self):
        if self.has_username_and_passwd:
            self.ATC_AUTH = None
            session = self._set_new_session()
            r = session.get(urljoin(self.url, "/sky/login"))
            if r.status_code == 200:
                post_path = self._get_login_post_path(r.text)
                r = session.post(
                    urljoin(self.url, post_path),
                    data={'login': self.username, 'password': self.password}
                )
                try:
                    r.raise_for_status()
                except HTTPError:
                    self._close_session()
                    raise
                else:
                    # Yes, this case does not raise any HTTPError, the return
                    # code is 200...
                    if "invalid username and password" in r.text:
                        raise ValueError("Invalid username and password")
                    if r.status_code == requests.codes.ok:
                        self.ATC_AUTH = self._get_skymarshal_auth()
                    else:
                        self._close_session()
        if self.ATC_AUTH:
            return True
        return False

    @property
    def headers(self):
        if (
            hasattr(self.session, 'headers')
            and isinstance(self.session.headers, collections.Mapping)
            and hasattr(self.session.headers, 'copy')
        ):
            headers = self.session.headers.copy()
        else:
            headers = {}

        headers['Content-Type'] = 'application/json'
        if self.ATC_AUTH is not None and 'Authorization' not in headers:
            headers['Authorization'] = "Bearer %s" % self.ATC_AUTH
        return headers

    @property
    def requests(self):
        if self.session is not None:
            return self.session
        return requests

    @staticmethod
    def _is_response_ok(response):
        if response.status_code == 401 or response.text == 'not authorized':
            return False
        return True

    def get(self, path):
        url = self._make_api_url(path)
        r = self.requests.get(url, headers=self.headers)
        if not self._is_response_ok(r) and self.has_username_and_passwd:
            self.auth()
            r = self.requests.get(url, headers=self.headers)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        else:
            r.raise_for_status()
        return False

    def post(self, path, data=None):
        url = self._make_api_url(path)
        kwargs = {'headers': self.headers}
        if data is not None:
            kwargs['data'] = data
        r = self.requests.post(url, **kwargs)
        if not self._is_response_ok(r) and self.has_username_and_passwd:
            self.auth()
            r = self.requests.post(url, **kwargs)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        else:
            r.raise_for_status()
        return False

    def put(self, path, data=None):
        url = self._make_api_url(path)
        kwargs = {'headers': self.headers}
        if data is not None:
            kwargs['data'] = data
        r = self.requests.put(url, **kwargs)
        if not self._is_response_ok(r) and self.has_username_and_passwd:
            self.auth()
            r = self.requests.put(url, **kwargs)
        if r.status_code == requests.codes.ok:
            return True
        else:
            r.raise_for_status()
        return False
