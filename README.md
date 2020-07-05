<h1 align="center">
  <img src="https://repository-images.githubusercontent.com/184577526/6d042f80-7056-11e9-9b2b-8e90c0ab0f40"/>
</h1>

If you seek to consume any REST API, fetch some items/events/messages, format them into valid syslog messages and feed them into **any** Syslog destination Rest2Syslog (R2S) is a perfect choice!

Why syslog? Many products/platforms out there support ingestion of data (inbound messages) using the syslog standard for messages. Some product examples include: Kafka, Elasticsearch, Splunk, Redis, QRadar, the list goes on and on. If you want to send messages from your Platform's REST API (eg Message Source) into other products (eg Message Destination), it is very likely that syslog is a viable protocol. R2S will help you get the job done faster - all you need to do is extend R2S to support your specific RESTful APIs. Read on for the full details on how to extend R2S.

Why R2S on top of syslog-ng? syslog-ng is a free and open-source implementation of the syslog protocol for Unix and Unix-like systems. It extends the original syslogd model with content-based filtering, rich filtering capabilities, flexible configuration options and adds important features to syslog, like using TCP for transport. More over, syslog-ng is extensible by design and allows writing custom sources and destinations. This allows us to implement REST2Syslog as a custom source.

REST2Syslog collects data from any REST API extract relevant fields, formats syslog messages, and sends them over to any configurable syslog destination. It is heavily based on [syslog-ng](https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.18/administration-guide/2#TOPIC-1043883) and implented as a [python source plugin](https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.18/administration-guide/23#TOPIC-1043966)

REST2Syslog (R2S) features:
1. Execute your API calls periodically using a configurable interval parameter
2. Provides authentication flow for tokens/refresh tokens. Authentication scheme is configurable.
3. Provides out of the box support for pagination : many APIs requires iterating over pages of data.
4. State persistency - supports fetching delta since last invocation. This is crucial for efficient quota consumption. Some API providers will limit your rate and daily quota so this is important!
5. Parses response into individual items
6. Transform your Items into standard message formats such as IBM QRadar [LEEF](https://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/9989d3d7-02c1-444e-92be-576b33d2f2be/page/3dc63f46-4a33-4e0b-98bf-4e55b74e556b/attachment/a19b9122-5940-4c89-ba3e-4b4fc25e2328/media/QRadar_LEEF_Format_Guide.pdf) or HP ArcSight [CEF](https://community.microfocus.com/dcvta86296/attachments/dcvta86296/connector-documentation/1197/2/CommonEventFormatV25.pdf)
7. handles errors gracefully
8. handles sending messages as syslog messages
9. extensions API - write your own custom extensions (read below for details)
10. unit tested with >92% code coverage

The initial implementation includes a [Proofpoint CASB](https://www.proofpoint.com/au/products/cloud-app-security-broker) Alerts extension plus an Events extension. Those extensions will pull alerts/events from the Proofpoint CASB platform and stream those items into any valid syslog-ng destination. 

# Writing custom extensions
In order to extend R2S with your custom extensions, you will need to implement three python classes: a API Adaptor, a Paginator and an Item formatter. Please review the existing extensions for more details. You can find two extensions inside the folder r2s/extensions/proofpoint/pcasb.

I'll be glad to accpet pull requests for additional extensions!

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

     - git clone this project into a local folder

     - in case syslog-ng is started/stopped using systemctl you should append the root folder (eg - r2s) path to the PYTHONPATH environment variable like this:
        ```sh
        PYTHONPATH="<full-path-to-your-python-file>"
        ```
        for example:
        ```sh
        PYTHONPATH="/opt/sysconfig/syslog-ng/Rest2Syslog/"
        ```
        For recent Red Hat Enterprise Linux, Fedora, and CentOS distributions that use systemd, the systemctl command sources the /etc/sysconfig/syslog-ng file before starting syslog-ng OSE. (On openSUSE and SLES, /etc/sysconfig/syslog file.) Append the following line to the end of this file: 
        ```sh
        PYTHONPATH="<full-path-to-your-python-file>"
        ```

      - Alternatively to a dedicated folder you can copy the python r2s scripts into sbin
   
   - Edit the syslog-ng configuration file (usually located at /etc/syslog-ng/syslog-ng.conf)

      - Add this syslog-ng source s_r2s. you should change the paramters (see parameters description below the following snippet)
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
      - in addition to the above syslog-ng source, you should also add some destination. Here is an example destination to a remote syslog server. Any valid syslog-ng destination will do!
        ```sh
        destination d_tcp { syslog("10.10.0.1" transport("tcp") port(514) ); };
        ```
      - finally, wire the source and the destination in order to drive traffic (aka items) from the source into the destination.
        ```sh
        log {source(s_r2s); destination(d_tcp); };
        ```


## Architecture

<h1 align="center">
  <img src="https://github.com/chenbekor/Rest2Syslog/blob/master/wiki/images/R2S-Architecture.png"/>
</h1>

The following table summarizes key components in the R2S system with a description of what they do and how they interconnect with other components in the system:
<table>
<thead>
<tr>
<th>Component Name</th><th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Syslog-ng client</td>
<td>the main process running r2s is a syslog-ng client. Usually this process is setup as system service which is launched automatically on system startup. The syslog-ng client loads r2s if it is properly defined in the syslog-ng.conf file as described above. Once r2s is loaded, syslog-ng will call the <code>run</code> method which is the entry point in r2s.
</td>
</tr>
<tr>
<td>REST2SyslogSource</td>
<td>This is the main class in r2s. It is implementing a syslog-ng Source (see syslog-ng documentation if you're not familiar with what is a Source). In turn, this component loads any pre-defined extensions as described in the syslog-ng.conf file under the key "extensions". Per each of the loaded Extensions, a call to <code>doWork</code> will occur every X seconds as defined in the Sleep "interval" parameter.</td>
</tr>
<tr>
<td>Extension</td>
<td>r2s can load multiple Extensions. each extension loads its own <code>Paginator</code> and calls its <code>fetchPageItems</code> until there are no more pages left (eg - max_pages reached) or no new items exist in the API response. Also - the extension will stop processing if the Service is halted for some reason.</td>
</tr>
<tr>
<td>Paginator</td>
<td>On bootstrap, this compoent will load an API Adaptor and a Formatter as configured in the r2s configuration parameters. The main method is <code>fetchPageItems</code> where the Paginator calls the API Adapator to fetch the next page, followed by a call to the Formatter in order to wrap each response item for message parsing and formatting (eg - LEEF / CEF format)</td>
</tr>
<td>API Adaptor</td>
<td>The API Adaptor, implements the API calls. It handles authentication, and items fetching. the main method here is <code>fetchItems</code> which calls the REST API and extact the response payload. When extending R2S the formatter is one of the required extension components.</td>
</tr>
<td>Formatter</td>
<td>wraps API specific entities and tranlate them into a well defined format. This component abstracts away the details of how to translate a specific response json scheme. When extending R2S the formatter is one of the required extension components.</td>
</tr>
</table>

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