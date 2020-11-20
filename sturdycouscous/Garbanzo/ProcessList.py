import Checker, DBWriter

f = open('sites.txt', 'r')
sitelist = f.read().splitlines()
checker = Checker.connection_checker()
results = []
for site in sitelist[:2]:
    result = checker.tls_versions_checker(site)
    results.append(result)
    print(result)

