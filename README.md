# concoursepy
concoursepy gives you a way to interact with the concourse api through python

currently supports
 * concourse's basic auth mechanism
 * the endpoints used by the concourse web ui

## Examples
```python3
import concoursepy

ci = concoursepy.api('https://ci.example.com', 'team_a', 'username', 'password')
print(ci.jobs('example_pipeline'))
```
