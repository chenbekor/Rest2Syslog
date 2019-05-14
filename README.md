<h1 align="center">
  <img src="https://repository-images.githubusercontent.com/184577526/6d042f80-7056-11e9-9b2b-8e90c0ab0f40"/>
</h1>

Many products out there support ingestion of data via syslog. Some examples include: Kafka, Elasticsearch, Splunk, Redis, QRadar, the list goes on and on. If you seek to consume some REST API, fetch some items via json parsing and feed those items into **any** Syslog destination this project is for you!

REST2Syslog collects data from any REST API and sends it over to any configurable syslog destination.

What does REST2Syslog (R2S) provides:


The initial implementation includes a Proofpoint CASB platform extension. I'll be glad to accpet pull requests for additional extensions!

Feel free to send any feedback/question. [just open an issue](../issues).

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