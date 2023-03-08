from collections.abc import Mapping
import json
from os.path import join as pathjoin
import re
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError

from sseclient import SSEClient


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
        return self.get(f'teams/{team_name}')

    def get_config(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/config"
        )

    def jobs(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs"
        )

    def list_builds(self):
        return self.get("builds")

    def get_build(self, build_id):
        return self.get(f"builds/{build_id}")

    def build(self, build_id):
        """Leaving this here for backwards compatibility."""
        return self.get_build(build_id)

    def get_build_plan(self, build_id):
        return self.get(f"builds/{build_id}/plan")

    def build_plan(self, build_id):
        """Leaving this here for backwards compatibility."""
        return self.get_build_plan(build_id)

    def send_input_to_build_plan(self, build_id, plan_id):
        return self.put(f"builds/{build_id}/plan/{plan_id}/input")

    def read_output_from_build_plan(self, build_id, plan_id):
        return self.get(f"builds/{build_id}/plan/{plan_id}/input")

    def build_events(
            self, build_id,
            iterator=False, yield_sse_elts=False, return_sse_client=False
    ):
        """Return or yield build events

        Since build events are returned as sse streams by concourse,
        if the build is not finished, this may stall until the end.
        You may wish instead to iterate over incoming results in a thread
        by passing `iterator=True`, otherwise we wait till we receive the
        end of all events (and this can take some time if the build is not
        finished).
        If you pass `yield_sse_elts` along with `iterator=True`, you will
        receive a:
        {
            'data': <parsed data>,
            event: <sseclient.Event>,
            'client': <sseclient.SSEClient>
        }
        dict on each iteration.
        This will allow you to call the `.close()` method on the client in
        order to cleanly interrupt the stream if you want to interrupt it
        before the end (i.e.: on a running build), or to read the raw event.
        If you pass `return_sse_client=True` you only get the
        sseclient.SSEClient instance and manage it yourself.
        """
        return self.get(
            f"builds/{build_id}/events",
            stream=True,
            iterator=iterator,
            yield_sse_elts=yield_sse_elts,
            return_sse_client=return_sse_client
        )

    def build_resources(self, build_id):
        return self.get(f"builds/{build_id}/resources")

    def abort_build(self, build_id):
        return self.put(f"builds/{build_id}/abort")

    def get_build_preparation(self, build_id):
        return self.get(f"builds/{build_id}/preparation")

    def list_all_jobs(self):
        return self.get("jobs")

    def list_jobs(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs"
        )

    def get_job(self, team_name, pipeline_name, job_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}"
        )

    def list_job_builds(self, team_name, pipeline_name, job_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/builds"  # noqa
        )

    def create_job_build(self, team_name, pipeline_name, job_name):
        return self.post(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/builds"  # noqa
        )

    def trigger(self, team_name, pipeline_name, job_name):
        """Leaving this here for backwards compatibility."""
        return self.create_job_build(team_name, pipeline_name, job_name)

    def list_job_inputs(self, team_name, pipeline_name, job_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/inputs"  # noqa
        )

    def get_job_build(self, team_name, pipeline_name, job_name, build_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/builds/{build_name}"  # noqa
        )

    def pause_job(self, team_name, pipeline_name, job_name):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/pause"  # noqa
        )

    def unpause_job(self, team_name, pipeline_name, job_name):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/unpause"  # noqa
        )

    def job_badge(self, team_name, pipeline_name, job_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/jobs/{job_name}/badge"  # noqa
        )

    def main_job_badge(self, pipeline_name, job_name):
        return self.get(
            f"pipelines/{pipeline_name}/jobs/{job_name}/badge"  # noqa
        )

    def list_all_pipelines(self):
        return self.get("pipelines")

    def list_pipelines(self, team_name):
        return self.get(f"teams/{team_name}/pipelines")

    def get_pipeline(self, team_name, pipeline_name):
        return self.get(f"teams/{team_name}/pipelines/{pipeline_name}")

    def pause_pipeline(self, team_name, pipeline_name):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/pause"
        )

    def unpause_pipeline(self, team_name, pipeline_name):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/unpause"
        )

    def list_pipeline_builds(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/builds"
        )

    def pipeline_badge(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/badge"
        )

    def list_all_resources(self):
        return self.get("resources")

    def list_resources(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources"
        )

    def list_resource_types(self, team_name, pipeline_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/resource-types"
        )

    def get_resource(self, team_name, pipeline_name, resource_name):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}"  # noqa
        )

    def list_resource_versions(
        self, team_name, pipeline_name, resource_name, limit=100
    ):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions?limit={limit}"  # noqa
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
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_version_id}"  # noqa
        )

    def enable_resource_version(
        self, team_name, pipeline_name, resource_name, resource_version_id
    ):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_version_id}/enable"  # noqa
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
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_version_id}/disable"  # noqa
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
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_config_version_id}/pin"  # noqa
        )

    def unpin_resource_version(
        self, team_name, pipeline_name, resource_name,
        resource_config_version_id
    ):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_config_version_id}/unpin"  # noqa
        )

    def list_builds_with_version_as_input(
        self, team_name, pipeline_name, resource_name, resource_id
    ):
        return self.get(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_id}/input_to"  # noqa
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
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_id}/output_to"  # noqa
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
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/versions/{resource_version_id}/causality"  # noqa
        )

    def pause_resource(self, team_name, pipeline_name, resource_name):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/pause"  # noqa
        )

    def unpause_resource(self, team_name, pipeline_name, resource_name):
        return self.put(
            f"teams/{team_name}/pipelines/{pipeline_name}/resources/{resource_name}/unpause"  # noqa
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

        If `path` does not have a leading slash self.api_path is prepended, and
        we return something like f'{self.url}/{self.api_path}/{path}'

        If `path` has a leading slash self.api_path is not prepended, and
        we return something like f'{self.url}/{self.api_path}
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
            and isinstance(self.session.headers, Mapping)
            and hasattr(self.session.headers, 'copy')
        ):
            headers = self.session.headers.copy()
        else:
            headers = {}

        headers['Content-Type'] = 'application/json'
        if self.ATC_AUTH is not None and 'Authorization' not in headers:
            headers['Authorization'] = f"Bearer {self.ATC_AUTH}"
        return headers

    @property
    def requests(self):
        if self.session is not None:
            return self.session
        return requests

    @staticmethod
    def _is_response_ok(response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 401:
                return False
            else:
                raise
        return True

    @staticmethod
    def _json_or_other(data):
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                pass
        return data

    @classmethod
    def _event_to_dict(cls, event):
        data = {}
        for attr in ('id', 'event', 'data', 'retry'):
            data[attr] = cls._json_or_other(getattr(event, attr))
        return data

    @classmethod
    def iter_sse_stream(cls, resp, yield_sse_elts=False):
        client = SSEClient(resp)
        for event in client.events():
            data = cls._event_to_dict(event)
            if yield_sse_elts:
                yield {'data': data, 'event': event, 'client': client}
            else:
                yield data
            if event.event == 'end':
                client.close()
                break

    def get(
            self, path,
            stream=False,
            iterator=False,
            yield_sse_elts=False,
            return_sse_client=False
    ):
        url = self._make_api_url(path)
        r = self.requests.get(url, headers=self.headers, stream=stream)
        if not self._is_response_ok(r) and self.has_username_and_passwd:
            self.auth()
            r = self.requests.get(url, headers=self.headers, stream=stream)
        if r.status_code == requests.codes.ok:
            if stream:
                if return_sse_client:
                    return SSEClient(r)
                elif iterator:
                    return self.iter_sse_stream(
                        r, yield_sse_elts=yield_sse_elts
                    )
                else:
                    return list(self.iter_sse_stream(r))
            else:
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
