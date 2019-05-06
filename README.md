<h1 align="center">
  <img src="https://repository-images.githubusercontent.com/184577526/f6114e80-6f10-11e9-9aac-498d91f82230"/><br>
  REST2Syslog
</h1>

REST2Syslog collects data from any REST API and sends it over to any configurable syslog destination.

The initial implementation is based on a specific need I had to integate with the Proofpoint CASB platform. Any other REST API can be added. Some refactoring is required to support this (in the works).

Feel free to submit pull requests or send any feedback/question.

# Deployment
## Dependencies
   - python3
   - [requests](https://realpython.com/python-requests/)
   - syslog-ng (>= 3.18)

## Installation
   - Install syslog-ng (=> 3.18)
   - Copy the configuration file into etc
   - Copy the python scripts into sbin
   - Alternatively you work from a git clone, but setting PYTHONPATH in the service file.
   - Edit configuration (more details TBD)


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