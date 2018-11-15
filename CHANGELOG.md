#### * 0.0.9
<details>
<summary>Moved team configuration into each method instead of as a global setting (**breaking change**)</summary>
<br>
Previously you would configure your object with your url, user, pass, and team. Concoursepy would login and use those credentials for everything. This meant all commands run against the one team. Now with concourse 4.x we can login without a team, and access all the resources we have permission to. In order to facilitate that we moved the team configuration into each of the methods
<br>
Changed methods:
<ul>
<li>jobs</li>
<li>list_jobs</li>
<li>list_job_inputs</li>
<li>get_job_build</li>
<li>pause_job</li>
<li>unpause_job</li>
<li>job_badge</li>
<li>list_pipelines</li>
<li>get_pipeline</li>
<li>pause_pipeline</li>
<li>unpause_pipeline</li>
<li>list_pipeline_builds</li>
<li>pipeline_badge</li>
<li>list_resources</li>
<li>list_resource_types</li>
<li>get_resource</li>
<li>list_resource_versions</li>
<li>get_resource_version</li>
<li>enable_resource_version</li>
<li>disable_resource_version</li>
<li>pin_resource_version</li>
<li>unpin_resource_version</li>
<li>list_builds_with_version_as_input</li>
<li>list_builds_with_version_as_output</li>
<li>pause_resource</li>
<li>unpause_resource</li>

</ul>
</details>
<br>
<details>
<summary>Added missing methods from atc</summary>
<br>
The following methods were missing from concoursepy but exist in upstream concourse's routes.go. This commit gets us much closer to complete parity.
<ul>
<li>list_job_inputs</li>
<li>list_all_pipelines</li>
<li>list_pipelines</li>
<li>get_pipeline</li>
<li>pause_pipeline</li>
<li>unpause_pipeline</li>
<li>list_pipeline_builds</li>
<li>pipeline_badge</li>
<li>list_all_resources</li>
<li>list_resources</li>
<li>list_resource_types</li>
<li>get_resource</li>
<li>pin_resource_version</li>
<li>unpin_resource_version</li>
<li>get_resource_causality</li>
</ul>
</details>

#### * 0.0.8
<details>
<summary>Updated auth method from concourse 3.x style basic login to 4.x style local login (**breaking change**)</summary>
<br />
0.0.7 is the last version you can use with concourse 3.x
</details>
