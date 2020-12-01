from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser
import pandas as pd 
import re
# Driver for Checker interface.

# More random notes -- need to check certificate first.
# The connections will all fail if the certificate isn't trusted or valid.
# And I'm too lazy to put in try/catch blocks.

# another big note: domain names should NOT include the http or the www part.

class security_crawler():

	def __init__(self):
		
		self.sites_to_visit = set()	
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
				self.sites_to_visit.add(self.grab_domain_name(url))

		return unique_history

	def add_children_to_visit(self, unique_history):
		# create "parser" objects for each of the urls.

		for link in unique_history:
			p = parser.Parser(link)
			children = p.get_links_from_child_pages()

			for child in children:
				self.sites_to_visit.add(self.grab_domain_name(child))


	def tls_analysis(self):

		c = Checker.connection_checker()

		for domain in self.sites_to_visit:
			# print(domain)
			d = DomainInfo.domain_info(domain)
			
			d.valid_cert = c.certificate_checker(domain)

			# d.ports_open = c.port_checker(domain)
			# print("got ports open")

			d.tls_versions_supported = c.tls_versions_checker(domain)
		
			d.ciphers_supported = c.get_supported_ciphers(domain, d.tls_versions_supported)
			
			self.domain_infos.add(d)

			# redlist websites supporting tls v1 and v1.1
			if ('TLSv1.1' in d.tls_versions_supported) or ('TLSv1.0' in d.tls_versions_supported):
				self.red_list.add(domain)


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
		history = self.get_history(filename="embarrassing_history.csv")
		print(history)
		self.add_children_to_visit(history)	# passing history in just in case there are more links to other sites on these pages.
		print(self.sites_to_visit)	# full list of top-level domains to get info on.

		self.tls_analysis()

		for domain in self.domain_infos:
			print(domain.export_json())


if __name__ == "__main__":
	sc = security_crawler()
	sc.crawl()


