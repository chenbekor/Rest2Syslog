options = { 'max_pages':10,
            'extension_name.formatter_module':'r2s.extensions.proofpoint.pcasb.alerts_formatter',
            'extension_name.formatter_class':'PCASBAlertsFormatter',
            'extension_name.api_adaptor_module':'r2s.extensions.proofpoint.pcasb.alerts_api_adaptor',
            'extension_name.api_adaptor_class':'PCASBAlertsAPIAdaptor',
            'company_name' :'mock_company',
            'product_name' : 'mock_product',
            'product_version':'1.0'
            }

options_two_page = {'max_pages':2}

options_negative_max_page = {'max_pages':-2}

options_api = { 'auth_url':'mock_auth_url',
                'alerts_url':'mock_items_url',
                'api_key':'mock_key',
                'client_id':'mock_client_id',
                'client_secret':'mock_client_secret'
                }

empty_page = []
first_page = [{'id':'1'},{'id':'2'},{'id':'3'}]
second_page = [{'id':'4'},{'id':'5'},{'id':'6'}]
third_page = [{'id':'7'},{'id':'8'},{'id':'9'}]
fourth_page = [{'id':'10'},{'id':'11'},{'id':'12'}]

item_1 = {"id":"d04c8","timestamp":1557045242740,"severity":"MID","title":"Mock Title","description":"Mock Description","type":"Footprint","sub_type":"Suspicious Activity","related_events":[{"event_id":"b4cc","cloud_service":"Google Apps","timestamp":1557045242462,"user_email":"mock@mock.com","event_classification":{"id":"22","category":"Authorize","sub_category":"Authorize 3rd Party App Access","threat":"Authorization"},"meta_data":{"extracted_fields":[{"128042":"[\"ZIP Extractor\"]"}]}}]}
item_2 = {"id":"afaf7","timestamp":1557043844539,"severity":"MID","title":"Mock Title","description":"Mock Description","type":"Footprint","sub_type":"Suspicious Activity","related_events":[{"event_id":"df0f3","cloud_service":"Google Apps","timestamp":1557043844214,"user_email":"mock1@mock.com","event_classification":{"id":"29","category":"Authorize","sub_category":"Authorize 3rd Party App Access","threat":"Authorization"},"meta_data":{"extracted_fields":[{"128042":"[\"WhatsApp Messenger\"]"}]}}]}
items = [item_1,item_2]
sample_response_body = {'alerts':items}
partial_item = {"id":"d04c8","timestamp":1557045242740,"severity":"MID","title":"Mock Title","description":"Mock Description","type":"Footprint","sub_type":"Suspicious Activity"}

valid_header = 'LEEF:1.0|mock_company|mock_product|1.0|Footprint|'
valid_msg = 'LEEF:1.0|mock_company|mock_product|1.0|Footprint|cat=Suspicious Activity\tdevTime=1557045242740\tdevTimeFormat=Milliseconds\tsev=5\tusrName=USER_NAME_EXTRACT_FAIL\talertID=d04c8\tdescription=Mock Description\ttitle=Mock Title\tcloudService=CLOUD_SERVICE_EXTRACT_FAIL\talertClassification=CLASSIFICATION_EXTRACT_FAIL\talertSubClassification=SUB_CLASSIFICATION_EXTRACT_FAIL\tthreat=THREAT_EXTRACT_FAIL\tdateTimeString=2019-05-05T08:34:02.740000+0000\t'

single_page = [first_page]
two_pages = [first_page,second_page]
three_pages = [first_page,second_page, third_page]