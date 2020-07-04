from r2s.utils import _print,_print_error
from r2s.extensions.abstract import R2SItemFormatter
from datetime import datetime
from datetime import timezone

class PCASBEventsFormatter(R2SItemFormatter):
    def __init__(self, item):
        _print("About to initialize PCASBEventsFormatter...")
        self.company_name = self.options['company_name']
        self.product_name = self.options['product_name']
        self.product_version = self.options['product_version']
        super().__init__(item)
    
    @staticmethod
    def wrapItems(items_as_json_array):
        formatters = []
        for item in items_as_json_array:
            formatters.append(PCASBEventsFormatter(item))
        return formatters

    def buildHeader(self):
        return 'LEEF:1.0|' + self.company_name + '|' + self.product_name + '|' + self.product_version + '|' + self.item['type'] + '|'
    
    def buildBody(self, leef_attributes):
        try:
            leef_body = ''
            for (key,val) in leef_attributes.items(): leef_body += (key + '=' + val + '\t')
            return leef_body
        except Exception as ex:
            _print_error(ex)
            return ''

    
    def getTime(self):
        return str(self.item['timestamp'])
    
    def getDateTimeAsString(self):
        try:
            _t = self.item['timestamp']
            _print('about to parse this epoch: {}'.format(_t))
            return datetime.fromtimestamp(_t/1000.0,timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        except Exception as e: 
            _print('Error occured while trying to parse DateTimeAsString:{}'.format(e))
            return 'N/A'
    
    def getTimeFormat(self):
        return 'Milliseconds'

    def extractAttribute(self, attr_name):
        try:
            return self.item[attr_name]
        except:
            _print_error('could not extract ' + attr_name + ' from event with id: ' + self.item['eventId'])
            return attr_name.upper() + '_EXTRACT_FAIL'
        
    
    def buildMessage(self):
        leef_header = self.buildHeader()
        
        #standard LEEF Attributes
        leef_attributes = {}
        leef_attributes['devTime'] = self.getTime()
        leef_attributes['devTimeFormat'] = self.getTimeFormat()
        leef_attributes['usrName'] = self.extractAttribute('userEmail')
        
        #extended LEEF Attributes
        leef_attributes['eventID'] = self.extractAttribute('eventId')
        leef_attributes['cloudService'] = self.extractAttribute('cloudService')
        leef_attributes['resource'] = self.extractAttribute('resource')
        leef_attributes['action'] = self.extractAttribute('action')
        leef_attributes['requestIp'] = self.extractAttribute('requestIp')
        leef_attributes['geographicalContextCountry'] = self.extractAttribute('geographicalContextCountry')
        leef_attributes['geographicalContextState'] = self.extractAttribute('geographicalContextState')
        leef_attributes['geographicalContextCity'] = self.extractAttribute('geographicalContextCity')
        leef_attributes['userAgent'] = self.extractAttribute('userAgent')
        leef_attributes['systemEvent'] = self.extractAttribute('systemEvent')
        

        for (key,val) in self.item['additionalProperties']: leef_attributes['ext.' + key] = val

        leef_body = self.buildBody(leef_attributes)
        
        leef_msg = leef_header + leef_body
        return leef_msg
