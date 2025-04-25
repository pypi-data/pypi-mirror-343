# GitHub API

Fluent GitHub API generated from OpenAPI spec.

## Installation

```bash
pip install github-fluent-api
```

## Usage

```python
from github_fluent_api import GitHubAPI

gh = GitHubAPI(api_key=...)

issues = gh.repos.issues.list(
    owner="foo",
    repo="bar",
    creator="kenny",
    assignee="spenny",
    direction="desc",
    labels="bug,ui,@high",
    mentioned="bobby",
    milestone=123,
    page=1,
    per_page=100,
    since="2025-04-23T00:00:00Z",
    sort="created",
    state="open",
)

for issue in issues:
    print(issue.number, issue.title)

```