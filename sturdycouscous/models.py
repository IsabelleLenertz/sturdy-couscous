class TLS_Record(object):

    def __init__(self, URL='', Title='', Domain='', Checker={}, Classification={}):
        self.URL = URL
        self.Title = Title
        self.Domain = Domain
        self.Checker = Checker
        self.Classification = Classification

    def parse_record(self, input_dict):
        output_record = TLS_Record()

        if type(input_dict) != dict:
            print("Error: input must be a dict mapped to TLS_Record attributes")
            return 0
        self.URL = input_dict['URL']
        self.Title = input_dict['Title']
        self.Domain = input_dict['Domain']
        self.Checker = input_dict['Checker']
        self.Classification = input_dict['Classification']
        return self

    def getattrs(self):
        return list(filter(lambda x: x[0] != '_', dir(TLS_Record())))
    
    def dump_dict(self):
        output = {}
        for attr in self.getattrs():
            val = eval('self.' + attr)
            if not callable(val):
                output[attr] = val
        return output


#################NEED A WORKING OBJECT MODEL HERE
            
