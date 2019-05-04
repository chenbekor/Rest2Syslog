<h1 align="center">
  <img src="https://repository-images.githubusercontent.com/184577526/72267a80-6eae-11e9-9cf3-5225a4d14677"/><br>
  REST2Syslog
</h1>

REST2Syslog alllows collecting data from any REST API and send it to a configurable syslog destination.

The initial implementation is based on a specific need I had to integate with the Proofpoint CASB platform. Any other REST API can be added. Some refactor is required to support this.

Feel free to submit pull requests or send and feedback/question.

<h2>Testing</h2>
Code coverage (from the projects's root directory):
```bash
coverage run --source . --omit *_test*,*infra* -m pytest tests/
```
Code coverage reporting:
```bash
coverage report
```
