from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser
import pandas as pd 
from threading import Thread
from Mongo_Client import DBClient
from Printer import Printer

# Driver for Checker & Classifier interface.

class security_crawler(Thread):

	def __init__(self):
		
		self.raw_history = set()
		self.sites_to_visit = set()	
		self.domain_infos = set()
		self.red_list = set()
		self.db_client = DBClient()

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
			print(link)
			children = p.get_links_from_child_pages()


			for child in children:
				if "http" in child: 
					self.sites_to_visit.add(child)

	# The thread function.
	def crawl_url(self, url):

		c = Checker.connection_checker()
		d = DomainInfo.domain_info(url)

		domain, valid_cert, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)
		print(domain)

		if red_list:
			self.red_list.add(url)
		
		d.domain = domain
		d.valid_cert = valid_cert
		d.ports_open = ports_open
		d.tls_versions_supported = tls_versions_supported
		d.ciphers_supported = ciphers_supported

		url_dict = d.export_json()
		# get results from classifier..
		# << don't know how that will work yet >>

		# output to mongo
		client = DBClient()
		client.column.insert(url_dict)

		self.domain_infos.add(d)

	def stupid_add(self, num):
		print(str(num + num))

	def sample_run(self):
		nums = range(5)
		threads = 1 
		running_threads = []		
		
		for num in nums:
			t = Thread(target=self.stupid_add, args=(num,))
			t.start()
			print("Thread " + str(t) + " started")
			running_threads.append(t)

		# joining threads
		for t in running_threads:
			t.join()


	def run(self):
		# obtain first level of history
		# then add children to visit from first level of history.
		#self.get_history(filename="sturdycouscous/history/embarrassing_history.csv")
		#self.get_history(filename="sturdycouscous/history/history_medium.csv")
		self.get_history(filename="sturdycouscous/history/history_small.csv")
		#self.get_history(filename="sturdycouscous/history/history_large.csv")
		self.add_children_to_visit()

		# making the set much smaller.
		small_set = set()
		i = 0
		for item in self.sites_to_visit:
			if (i >= 4):
				break
			small_set.add(item)
			i += 1	

		self.sites_to_visit = small_set
		# end the making smaller part.

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
#	sc.sample_run()
	sc.run()
	Printer().output_report()
