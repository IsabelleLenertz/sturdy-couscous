from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser
import pandas as pd 
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

	# The thread function.
	def crawl_url(self, url):

		c = Checker.connection_checker()
		d = DomainInfo.domain_info(url)

		domain, valid_cert, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)
		print(domain)

		if red_list:
			self.sites_to_visit.add(url)
		
		d.domain = domain
		d.valid_cert = valid_cert
		d.ports_open = ports_open
		d.tls_versions_supported = tls_versions_supported
		d.ciphers_supported = ciphers_supported

		url_dict = d.export_json()
		print(url_dict)
		self.domain_infos.add(d)

		# get results from classifier..
		# << don't know how that will work yet >>

		# output to mongo

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

if __name__ == "__main__":
	sc = security_crawler()
	sc.connect_client()
	sc.run()
