from Mongo_Client import Client

class Printer():
    def __init__(self):
        self.client = Client('domain_info')
        self.outputfile = open('output.txt', "w")
    def write_to_file(self, output):
        pass
        self.outputfile.writelines(output)
        self.outputfile.close()

    def mongo_query(self, fields):
        self.client.connect()
        output = []
        for row in self.client.collection.find({}, fields):
            output.append(row)
        return output

    def dump_db(self):
        for row in self.client.collection.find({}):
            print(row)
            pass
            # record = tls_record().parse_record(row)
            # write_to_file(record.dump_dict())

    def print_record_count(self):
        return len(self.mongo_query({'_id'}))

    def tally_open_ports(self):
        tally = {}
        query_filter = {'Checker.open_ports'}

        # Retrieve data and tally results
        for row in self.mongo_query(query_filter):
            ports = row['Checker']['open_ports']
            for port in ports:
                if port not in tally:
                    tally[port] = 1
                else:
                    tally[port] += 1

        # Build output string
        tally_output = "Open Port Tally:\n"
        for port in tally:
            tally_output += "{0:8} {1}\n".format(str(port), str(tally[port]))

        return(tally_output)

    def tally_tls_versions(self):
        tally = {}
        query_filter = {'Checker.tls_versions_supported', 'Checker.ciphers_supported'}

        # Retrieve data and tally results
        for row in self.mongo_query(query_filter):
            versionlist = row['Checker']['tls_versions_supported']
            for version in versionlist:
                if version not in tally:
                    tally[version] = {'count': 1}
                else:
                    tally[version]['count'] += 1
                cipherlist = row['Checker']['ciphers_supported']
                for ver in cipherlist:
                    if len(cipherlist[version]) != 0:
                        for cipher in cipherlist[ver]:
                            if 'ciphers_supported' not in tally[version]:
                                tally[version]['ciphers_supported'] = {cipher: 0}
                            else:
                                if cipher not in tally[version]['ciphers_supported']:
                                    tally[version]['ciphers_supported'][cipher] = 0
                                else:
                                    tally[version]['ciphers_supported'][cipher] += 1

        # Build output string
        tally_output = 'SSL Version Tally:\n'
        for result in tally:
            tally_output += "{0:35} {1}\n".format(result + ":", str(tally[result]['count']))
            if 'ciphers_supported' in tally[result]:
                tally_output += "--Ciphers: \n"
                for cipher in tally[result]['ciphers_supported']:
                    if cipher in tally[result]['ciphers_supported']:
                        tally_output += "--{0:33} {1}\n".format("--" + cipher + ":", str(tally[result]['ciphers_supported'][cipher]))
        
        return(tally_output)


    def tally_top_domains(self, count=10):
        tally = {}
        query_filter = {'Domain'}
        
        # Retrieve data and tally results
        for row in self.mongo_query(query_filter):
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
            tally_output += "{0:25} {1}\n".format(row[0] + ":", row[1])
        return tally_output

    def tally_categories(self):
        tally = {}
        query_filter = {'Classification.categories'}

        # Query and tally data
        for row in self.mongo_query(query_filter):
            if 'Classification' not in row:
                continue
            categories = row['Classification']
            if 'categories' not in row['Classification']:
                continue
            for category in row['Classification']['categories']:
                if category not in tally:
                    tally[category] = 1
                else:
                    tally[category] += 1

        
        # Build output string
        tally_output = "Category Tally:\n"
        for result in tally:
            tally_output += "{0:20} {1}\n".format(result + ":",  str(tally[result]))

        return tally_output
        

    
    def invalid_cert_stats(self):
        query_filter = {'Checker.certificate_valid'}
        results = self.mongo_query(query_filter)

        invalid_count = 0
        total =  len(results)
        for row in results:
            if not row['Checker']['certificate_valid']:
                invalid_count += 1
        return("Percentage of invalid certs: " + str(round(invalid_count/max(total,1)*100, 2)) + "%\n")
            

    def output_report(self):
        padding = '\n' * 1
        domain_tally = self.tally_top_domains()
        outfile = self.outputfile
        outfile.writelines(Printer.header())
        outfile.writelines(padding)
        outfile.writelines("Record count: " + str(self.print_record_count()) + '\n')
        outfile.writelines(padding)
        outfile.writelines(self.tally_tls_versions())
        outfile.writelines(padding)
        outfile.writelines(self.tally_top_domains())
        outfile.writelines(padding)
        outfile.writelines(self.invalid_cert_stats())
        outfile.writelines(padding)
        outfile.writelines(self.tally_open_ports())
        outfile.writelines(padding)
        outfile.writelines(self.tally_categories())
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
