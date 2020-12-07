from models import TLS_Record
from Printer import Printer

inputdict = {'URL': 'https://www.soompi.com/article/1346713wpp/13-actors-and-actresses-who-always-pick-good-roles', 'Title': '', 'Domain': 'soompi.com', 'Checker': {'tls_versions_supported': ['TLSv1_3', 'TLSv1_2', 'TLSv1_1', 'TLSv1_0'], 'open_ports': [80], 'certificate_valid': True, 'ciphers_supported': {'TLSv1_3': ['TLS_AES_256_GCM_SHA384'], 'TLSv1_2': [], 'TLSv1_1': [], 'TLSv1_0': []}}, 'Classification': {'categories': [], 'data': {'keywords': [], 'extension': ''}}}

r = TLS_Record().parse_record(inputdict)

# print(r.dump_dict())

# Printer().dump_fields({'Checker.tls_versions_supported'})

# Printer().tally_tls_versions()

# Printer().tally_top_domains()

Printer().output_report()


