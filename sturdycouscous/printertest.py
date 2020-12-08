from Printer import Printer
inputdict = {'URL': 'https://www.kqed.org/coronavirusliveupdates', 'Title': '', 'Domain': 'www.kqed.org', 'Checker': {'tls_versions_supported': ['TLSv1-2'], 'open_ports': [80], 'certificate_valid': True, 'ciphers_supported': ['TLSv1-2'], 'expiering_soon': False}, 'Classification': {'categories': ['news'], 'data': {'IT': 0.8360952094004219, 'government': 0.32389273877673996, 'education': 0.0, 'news': 6.029677613739079, 'other': 0.7519835291754545, 'commerce': 0.2937631816812293, 'social-media': 1.0997288339861404}}}

# Printer().mongo_query({'Checker.tls_versions_supported'})

# Printer().tally_top_domains()

# Printer().invalid_cert_stats()

# Printer().tally_tls_versions()

# Printer().tally_open_ports()

# Printer().tally_categories()

Printer().output_report()
