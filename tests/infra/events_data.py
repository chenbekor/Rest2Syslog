import json

options = { 'max_pages':10,
            'extension_name.formatter_module':'r2s.extensions.proofpoint.pcasb.events_formatter',
            'extension_name.formatter_class':'PCASBEventsFormatter',
            'extension_name.api_adaptor_module':'r2s.extensions.proofpoint.pcasb.events_api_adaptor',
            'extension_name.api_adaptor_class':'PCASBEventsAPIAdaptor',
            'company_name' :'mock_company',
            'product_name' : 'mock_product',
            'product_version':'1.0'
            }

options_two_page = {'max_pages':2}

options_negative_max_page = {'max_pages':-2}

options_api = { 'auth_url':'mock_auth_url',
                'events_url':'mock_items_url',
                'api_key':'mock_key',
                'client_id':'mock_client_id',
                'client_secret':'mock_client_secret'
                }

empty_page = []
first_page = {"size": 3,"nextPageToken": "eyJ","content": [{"eventId": "1"},{"eventId": "2"},{"eventId": "3"}]}
second_page = {"size": 3,"nextPageToken": "eyJ","content": [{"eventId": "4"},{"eventId": "5"},{"eventId": "6"}]}
third_page = {"size": 3,"nextPageToken": "eyJ","content": [{"eventId": "7"},{"eventId": "8"},{"eventId": "9"}]}
fourth_page = {"size": 3,"nextPageToken": "eyJ","content": [{"eventId": "10"},{"eventId": "11"},{"eventId": "12"}]}
empty_page = {"size": 0,"nextPageToken": "eyJ","content": []}

item_1 = json.loads('{"eventId":"flevent_9ab748ff5e42cf17677276a963495ca2","cloudService":"Salesforce","timestamp":"2020-06-29T18:31:01.867Z","resource":"Login Service","action":"Successful Login","userEmail":"obodner@proofpoint.com.cstdemoprime","requestIp":"18.205.99.60","geographicalContextCountry":"United States of America","geographicalContextState":"Virginia","geographicalContextCity":"Ashburn","userAgent":"akka-http/10.1.11","systemEvent":false,"additionalProperties":[{"key":"userIsVAP","value":"false"}]}')
item_2 = json.loads('{"eventId":"flevent_66f841926e9ce1960a97d161b3f13900","cloudService":"Salesforce","timestamp":"2020-06-29T22:03:36.603Z","resource":"Login Service","action":"Successful Login","userEmail":"obodner@proofpoint.com.cstdemoprime","requestIp":"34.237.114.124","geographicalContextCountry":"United States of America","geographicalContextState":"Virginia","geographicalContextCity":"Ashburn","userAgent":"akka-http/10.1.10","systemEvent":false,"additionalProperties":[{"key":"userIsVAP","value":"false"}]}')
items = [item_1,item_2]
sample_response_body = {"size":2,"nextPageToken":"eyJs","content":items}
partial_item = json.loads('{"eventId":"flevent_66f841926e9ce1960a97d161b3f13900","cloudService":"Salesforce","timestamp":"2020-06-29T22:03:36.603Z","resource":"Login Service","action":"Successful Login"}')

valid_header = 'LEEF:1.0|mock_company|mock_product|1.0|flevent_9ab748ff5e42cf17677276a963495ca2|'
valid_msg = 'LEEF:1.0|mock_company|mock_product|1.0|flevent_9ab748ff5e42cf17677276a963495ca2|devTime=2020-06-29T18:31:01.867Z\tdevTimeFormat=Milliseconds\tusrName=obodner@proofpoint.com.cstdemoprime\teventID=flevent_9ab748ff5e42cf17677276a963495ca2\tcloudService=Salesforce\tresource=Login Service\taction=Successful Login\trequestIp=18.205.99.60\tgeographicalContextCountry=United States of America\tgeographicalContextState=Virginia\tgeographicalContextCity=Ashburn\tuserAgent=akka-http/10.1.11\tsystemEvent=False\text.userIsVAP=false\t'
valid_partial_msg = 'LEEF:1.0|mock_company|mock_product|1.0|flevent_66f841926e9ce1960a97d161b3f13900|devTime=2020-06-29T22:03:36.603Z\tdevTimeFormat=Milliseconds\tusrName=USEREMAIL_EXTRACT_FAIL\teventID=flevent_66f841926e9ce1960a97d161b3f13900\tcloudService=Salesforce\tresource=Login Service\taction=Successful Login\trequestIp=REQUESTIP_EXTRACT_FAIL\tgeographicalContextCountry=GEOGRAPHICALCONTEXTCOUNTRY_EXTRACT_FAIL\tgeographicalContextState=GEOGRAPHICALCONTEXTSTATE_EXTRACT_FAIL\tgeographicalContextCity=GEOGRAPHICALCONTEXTCITY_EXTRACT_FAIL\tuserAgent=USERAGENT_EXTRACT_FAIL\tsystemEvent=SYSTEMEVENT_EXTRACT_FAIL\t'
single_page = [first_page]
two_pages = [first_page,second_page]
three_pages = [first_page,second_page, third_page]