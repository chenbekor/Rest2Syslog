<h1 align="center">
  <img src="https://repository-images.githubusercontent.com/184577526/6d042f80-7056-11e9-9b2b-8e90c0ab0f40"/>
</h1>

REST2Syslog collects data from any REST API and sends it over to any configurable syslog destination.

The initial implementation is based on a specific need I had to integate with the Proofpoint CASB platform. Any other REST API can be added. Some refactoring is required to support this (in the works).

Feel free to submit pull requests or send any feedback/question.

# Deployment
## Dependencies
   - python3
   - [requests](https://2.python-requests.org/en/master/)
   - syslog-ng (>= 3.18)

## Installation
   - Install syslog-ng (=> 3.18)
   - Copy the configuration file into etc
   - Copy the python scripts into sbin
   - Alternatively you work from a git clone, but setting PYTHONPATH in the service file.
   - Edit configuration (more details TBD)

## Architecture

<h1 align="center">
  <img src="https://github.com/chenbekor/Rest2Syslog/blob/master/wiki/images/R2S-Architecture.png"/>
</h1>

TBD - Explain the flow

# Testing
Code coverage (from the projects's root directory):
```sh
coverage run --source . --omit *_test*,*infra* -m pytest tests/
```
Code coverage reporting:
```sh
coverage report
```
Code coverage html report:
```sh
coverage html
```