from Garbanzo import Checker, DomainInfo
from bouneschlupp import Parser
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
		
		self.sites_visited = set()	#do we need this?
		self.domain_infos = set()
		self.red_list = set()
		self.db_client = None


	def get_history(self, filename):
		unique_history = set()
		df = pd.read_csv(filename)
		
		for indx, row in df.iterrows():
			url = row['url']
			if url not in unique_history:
				unique_history.add(url)

		return unique_history

	def get_children_from_history(self, unique_history):
		# create "parser" objects for each of the urls.

		super_set = unique_history.union(unique_history)

		for link in unique_history:
			p = Parser.parser(link)
			super_set = super_set.union(p.get_links_from_child_pages())

		return super_set


	def parse_all_links(self, history):
		filtered_set = set()
		for link in history:
			domain_name = self.grab_domain_name(link)
			filtered_set.add(domain_name)

		return filtered_set

	def tls_analysis(self, domain_list):

		c = connection_checker()

		for domain in domain_list:
			print(domain)
			d = DomainInfo.domain_info(domain)
			
			d.valid_cert = c.certificate_checker(domain)
			d.ports_open = c.port_checker(domain)
			d.tls_versions_supported = c.tls_versions_checker(domain)
			d.ciphers_supported = c.get_supported_ciphers(domain)
			
			domain_infos.add(d)

			# redlist websites supporting tls v1 and v1.1
			if ('TLSv1.1' in dl.tls_versions_supported) or ('TLSv1.0' in dl.tls_versions_supported):
				red_list.add(domain)




	# def read_csv(self, filename):
	# 	df = pd.read_csv(filename)
		
	# 	checker = Checker.connection_checker()		
	# 	for indx, row in df.iterrows():
	# 		url = row['url']
	# 		domain = self.grab_tld(url)
			

	# 		# if top-level domain is not in site visited, mark it as visited, then perform checks.
	# 		if domain not in self.sites_visited:
	# 			print(domain)
	# 			self.sites_visited.add(domain)

	# 			# checking_time:
		

	def grab_domain_name(self, url):
		
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


	def crawl(self):
		history = self.get_history(filename="history_small.csv")
		all_history = self.get_children_from_history(history)
		filtered_set = self.parse_all_links(all_history)

		self.tls_analysis(filtered_set)


if __name__ == "__main__":
	sc = security_crawler()
	sc.crawl()



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
