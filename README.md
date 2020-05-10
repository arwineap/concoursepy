# concoursepy
concoursepy gives you a way to interact with the concourse api through python

currently supports
 * concourse's local user mechanism
 * the endpoints used by the concourse web ui

Use a version prior to 0.0.8 for concourse 3.x

## Examples
```python3
import concoursepy

ci = concoursepy.api('https://ci.example.com', 'username', 'password')
print(ci.jobs('example_pipeline'))

# Or with token istead of username and password:
ci = concoursepy.api('https://ci.example.com', token='SomeLongTokenString')
print(ci.jobs('example_pipeline'))

```
