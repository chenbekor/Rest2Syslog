<h1 align="center">
  <img src="https://repository-images.githubusercontent.com/184577526/6d042f80-7056-11e9-9b2b-8e90c0ab0f40"/>
</h1>

Many products out there support ingestion of data via syslog. Some examples include: Kafka, Elasticsearch, Splunk, Redis, QRadar, the list goes on and on. If you seek to consume any REST API, fetch some items, parse into valid syslog messages and feed those messages into **any** Syslog destination this project is for you!

REST2Syslog collects data from any REST API parses the response, and sends it over to any configurable syslog destination. It is heavily based on [syslog-ng](https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.18/administration-guide/2#TOPIC-1043883) and implented as a [python source plugin](https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.18/administration-guide/23#TOPIC-1043966)

REST2Syslog (R2S) features:
1. Execute your API calls periodically using a configurable interval parameter
2. Provides authentication flow for tokens/refresh tokens. Authentication scheme is configurable.
3. Provides out of the box support for pagination : many APIs requires iterating over pages of data.
4. State persistency - supports fetching delta since last invocation. This is crucial for efficient quota consumption. Some API providers will limit your rate and daily quota so this is important!
5. Parses response into individual items
6. Transform your Items into common message formats such as IBM QRadar [LEEF](https://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/9989d3d7-02c1-444e-92be-576b33d2f2be/page/3dc63f46-4a33-4e0b-98bf-4e55b74e556b/attachment/a19b9122-5940-4c89-ba3e-4b4fc25e2328/media/QRadar_LEEF_Format_Guide.pdf) or HP ArcSight [CEF](https://protect724.hp.com/docs/DOC-1072)
7. handles errors gracefully
8. handles sending messages
9. extensions API - built in extensability (read here how - TBD)
10. unit tested with >92% code coverage
11. open sourced ;)

The initial implementation includes a Proofpoint CASB Alerts extension. I'll be glad to accpet pull requests for additional extensions!

Feel free to send any feedback/question. [just open an issue](https://github.com/chenbekor/Rest2Syslog/issues).

# Deployment
## Dependencies
   - python3
   make sure you have python
   - [requests](https://2.python-requests.org/en/master/)
   - syslog-ng (>= 3.18)

## Installation
   - Install syslog-ng (=> 3.18)
   - Copy / Clone the r2s scripts

   -- it is recommended to create a dedicated folder (called 'r2s') and git clone this project into it

   -- in case syslog-ng is started/stopped using systemctl you should append the root folder (eg - r2s) path to the PYTHONPATH environment variable like this:
   ```sh
PYTHONPATH="<path-to-your-python-file>
```
for example:
```sh
PYTHONPATH="/opt/syslog-ng/etc/r2s"
```

   -- Alternatively to a dedicated folder you can copy the python r2s scripts into sbin
   
   - Edit the syslog-ng configuration file (usually located at /etc/syslog-ng/syslog-ng.conf)

   -- Add this syslog-ng source s_r2s. you should change the paramters (see parameters description below the following snippet)
```sh
source s_r2s{
    python(
      class("r2s.source.REST2SyslogSource")
      options("company_name","Company_Name")
      options("product_name","Product_Name")
      options("product_version","Product_Version")
      options("interval",60)
      options("auth_url","https://url.to.auth.endpoint/example")
      options("alerts_url","https://url.to.items.endpoint/example")
      options("api_key","your_api_key")
      options("client_id","your_client_id")
      options("client_secret","your_client_secret")
      options("max_pages",0)
      options("extensions","pcasb_alerts")
      options('pcasb_alerts.formatter_module','r2s.extensions.proofpoint.pcasb.alerts_formatter')
      options('pcasb_alerts.formatter_class','PCASBAlertsFormatter')
      options('pcasb_alerts.api_adaptor_module','r2s.extensions.proofpoint.pcasb.alerts_api_adaptor')
      options('pcasb_alerts.api_adaptor_class','PCASBAlertsAPIAdaptor')
    );
};
```
-- in addition to the above syslog-ng source, you should also add some destination. Here is an example destination to a remote syslog server. Any valid syslog-ng destination will do!
```sh
destination d_tcp { syslog("10.10.0.1" transport("tcp") port(514) ); };
```
-- finally, wire the source and the destination in order to drive traffic (aka items) from the source into the destination.
```sh
log {source(s_r2s); destination(d_tcp); };
```


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