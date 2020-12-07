from Mongo_Client import DBClient
from models import TLS_Record
import collections

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
        return len(self.dump_fields({'_id'}))


    def tally_tls_versions(self):
        tally = {}
        query_filter = {'Checker.tls_versions_supported', 'Checker.ciphers_supported'}

        # Retrieve data and tally results
        for row in self.dump_fields(query_filter):
            versionlist = row['Checker']['tls_versions_supported']
            for version in versionlist:
                if version not in tally:
                    tally[version] = {'count': 1}
                else:
                    tally[version]['count'] += 1

        # Build output string
        tally_output = 'SSL Version Tally:\n'
        for result in tally:
            tally_output += "{0:8} {1}\n".format(result + ":", str(tally[result]['count']))
        return(tally_output)

    def tally_top_domains(self, count=10):
        tally = {}
        query_filter = {'Domain'}
        
        # Retrieve data and tally results
        for row in self.dump_fields(query_filter):
            domain = row['Domain']
            if domain not in tally:
                tally[domain] = 1
            else:
                tally[domain] += 1
        sorted_tally = sorted(tally.items(), key=lambda x:x[1], reverse=True)

        # Build output string
        tally_output = 'Top 10 visited Domains:\n'
        for rank in range(0, min(len(sorted_tally), 10)):
            row = sorted_tally[rank]
            tally_output += "{0:20} {1}\n".format(row[0] + ":", row[1])
        return tally_output


    def output_report(self):
        padding = '\n' * 1
        tls_tally = self.tally_tls_versions()
        domain_tally = self.tally_top_domains()
        outfile = self.outputfile
        outfile.writelines(Printer.header())
        outfile.writelines(padding)
        outfile.writelines("Record count: " + str(self.print_record_count()) + '\n')
        outfile.writelines(padding)
        outfile.writelines(tls_tally)
        outfile.writelines(padding)
        outfile.writelines(domain_tally)
        outfile.write('\n')
        outfile.close()
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
