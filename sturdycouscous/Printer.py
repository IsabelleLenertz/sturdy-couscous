from Mongo_Client import DBClient
from models import TLS_Record

class Printer():
    def __init__(self):
        self.client = DBClient()
        self.outputfile = open('output.txt', "w")

    def write_to_file(self, output):
        self.outputfile.writelines(output)
        self.outputfile.close()

    def dump_fields(self, fields):
        output = []
        for row in self.client.column.find({}, fields):
            output.append(row)
        return output

    def dump_db(self):
        for row in self.client.column.find({}, {'URL', 'Title'}):
            record = TLS_Record().parse_record(row)
            write_to_file(record.dump_dict())

    def print_record_count(self):
        pass


    def tally_tls_versions(self):
        tally = {}
        query_filter = {'Checker.tls_versions_supported', 'Checker.ciphers_supported'}
        for row in self.dump_fields(query_filter):
            print(row)
            versionlist = row['Checker']['tls_versions_supported']
            for version in versionlist:
                if version not in tally:
                    tally[version] = {'count': 1}
                else:
                    tally[version]['count'] += 1
        return(tally)

    def tally_top_domains(self, count=10):
        tally = {}
        query_filter = {'Domain'}
        print(self.dump_fields(query_filter))
        for row in self.dump_fields(query_filter):
            domain = row['Domain']
            if domain not in tally:
                tally[domain] = 1
            else:
                tally[domain] += 1
        print(tally)

    def output_report(self):
        tls_tally = str(self.tally_tls_versions())

        self.outputfile.writelines(Printer.header())
        self.outputfile.writelines(tls_tally)
        self.outputfile.write('\n')
        self.outputfile.close()
        print("************************ REPORT WRITTEN TO output.txt *************************")


    def header():
        figlet = '''
            ***************************************************************************    
            /  ___| |               | |     /  __ \                                    
            \ `--.| |_ _   _ _ __ __| |_   _| /  \/ ___  _   _ ___  ___ ___  _   _ ___ 
             `--. \ __| | | | '__/ _` | | | | |    / _ \| | | / __|/ __/ _ \| | | / __|
            /\__/ / |_| |_| | | | (_| | |_| | \__/\ (_) | |_| \__ \ (_| (_) | |_| \__ \\
            \____/ \__|\__,_|_|  \__,_|\__, |\____/\___/ \__,_|___/\___\___/ \__,_|___/
                                        __/ |                                          
                                       |___/
            ***************************************************************************
            '''
        return figlet
