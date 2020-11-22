from Garbanzo import Checker
import pandas as pd 
import re
# Driver for Checker interface.
'''
NOTE: This is code copied over from CheckTester.py when CheckTester used to be the driver.
Now CheckTester is gonna be used for unit testing.
'''

# More random notes -- need to check certificate first.
# The connections will all fail if the certificate isn't trusted or valid.
# And I'm too lazy to put in try/catch blocks.

# another big note: domain names should NOT include the http or the www part.

class security_crawler():

	def __init__(self):
		
		self.sites_visited = set()
		self.red_list = set()
		self.db_client = None


	def read_csv(self, filename):
		df = pd.read_csv(filename)
		
		checker = Checker.connection_checker()		
		for indx, row in df.iterrows():
			url = row['url']
			domain = self.grab_tld(url)
			

			# if top-level domain is not in site visited, mark it as visited, then perform checks.
			if domain not in self.sites_visited:
				print(domain)
				self.sites_visited.add(domain)
		

	def grab_tld(self, url):
		
		common_tlds = ['com', 'net', 'org', 'edu', 'gov']
		url_split = re.split('\.|/', url)
		
		tld_indx = 0
		domain_name = ""

		for i in range(len(url_split)):
			if url_split[i] in common_tlds:
				tld_indx = i
				break

		domain_name = url_split[tld_indx-1] + "." + url_split[tld_indx]
		return domain_name


if __name__ == "__main__":
	sc = security_crawler()
	sc.read_csv(filename="history_small.csv")



# from Checker import *

# def test_given_domains(domain_list=['amazon.com', 'google.com', 'facebook.com', 'badssl.com', 'python.org']):
# 	checker = connection_checker()
# 	# domain_list = ['badssl.com']
# 	for domain in domain_list:
# 		certificate_valid = checker.certificate_checker(domain)
# 		versions_supported = checker.tls_versions_checker(domain)
# 		all_ciphers = checker.get_all_ciphers(domain)

# 		print(all_ciphers)
		
# 		common_ports = [80, 443]
# 		for port in common_ports:
# 			print(checker.port_checker(domain, port))


# if __name__ == "__main__":
# 	test_given_domains()
