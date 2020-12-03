from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser
import pandas as pd 
import re
from threading import Thread
# Driver for Checker & Classifier interface.

class security_crawler(Thread):

	def __init__(self):
		
		self.raw_history = set()
		self.sites_to_visit = set()	
		self.domain_infos = set()
		self.red_list = set()
		self.db_client = None


	def get_history(self, filename):
		unique_history = set()
		df = pd.read_csv(filename)
		
		for indx, row in df.iterrows():
			url = row['url']
			if url not in self.raw_history:
				self.raw_history.add(url)
				self.sites_to_visit.add(url)

	def add_children_to_visit(self):
		# create "parser" objects for each of the urls.

		for link in self.raw_history:
			p = parser.Parser(link)
			children = p.get_links_from_child_pages()

			for child in children:
				self.sites_to_visit.add(url)


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


	# Return the "Checker" json part.
	def checker_analysis(self, url):

		c = Checker.connection_checker()
		domain = self.grab_domain_name(url)

		valid_cert = c.certificate_checker(domain)
		ports_open = c.port_checker(domain)
		tls_versions_supported = c.tls_versions_checker(domain)
		ciphers_supported = c.get_supported_ciphers(domain, d.tls_versions_supported)

		# redlist websites supporting tls v1 and v1.1
		if ('TLSv1.1' in tls_versions_supported) or ('TLSv1.0' in tls_versions_supported):
			self.red_list.add(url)

		# redlist insecure requests..?
		if "https" not in url:
			self.red_list.add(url)

		return valid_cert, ports_open, tls_versions_supported, ciphers_supported			


	# The thread function.
	def crawl_url(self, url):

		c = Checker.connection_checker()
		d = DomainInfo.domain_info(url)

		domain, valid_cert, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)
		print(domain)

		if red_list:
			self.sites_to_visit.add(url)
		
		print("done!")
		# d = DomainInfo(url, self.grab_domain_name(url))

		# call results from connection checker
		# valid_cert, ports_open, tls_versions_supported, ciphers_supported = self.checker_analysis(url)
		# d.valid_cert = valid_cert
		# d.ports_open = ports_open
		# d.tls_versions_supported = tls_versions_supported
		# d.ciphers_supported = ciphers_supported

		# get results from classifier..
		# << don't know how that will work yet >>

		# output to mongo -- look at robby's code.
		# print(d.export_json())
		# self.domain_infos.add(d)

	def run(self):
		# obtain first level of history
		# then add children to visit from first level of history.
		self.get_history(filename="history/embarrassing_history.csv")
		self.add_children_to_visit()

		threads = len(self.sites_to_visit)
		running_threads = []		

		# start each thread
		for url in self.sites_to_visit:
			t = Thread(target=self.crawl_url, args=(url,))
			t.start()
			print("Thread " + str(t) + " started")
			running_threads.append(t)

		# joining threads
		for t in running_threads:
			t.join()


	# def crawl(self):
	# 	history = self.get_history(filename="embarrassing_history.csv")
	# 	print(history)
	# 	self.add_children_to_visit(history)	# passing history in just in case there are more links to other sites on these pages.
	# 	print(self.sites_to_visit)	# full list of top-level domains to get info on.

	# 	self.tls_analysis()

	# 	for domain in self.domain_infos:
	# 		print(domain.export_json())


if __name__ == "__main__":
	sc = security_crawler()
	sc.run()


