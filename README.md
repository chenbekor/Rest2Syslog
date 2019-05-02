# REST2Syslog
REST2Syslog alllows collecting data from any REST API and send it to a configurable syslog destination.

The initial implementation is based on syslog-ng but it can be easily enhanced to any syslog compatible collector. pull requests are more than welcomed!

Also, the initial implementation is based on a specific need I had to integate with the Proofpoint CASB platform. Any other REST API can be added easily.

The current implementation shows how to send the collected data to IBM QRadar (which supports syslog sources). It is very easy to extedn to any other syslog destination.

Feel free to submit pull requests or send and feedback/question.
