import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")

from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser, Classifier
from Mongo_Client import Client
import pandas as pd 
from threading import Thread
from Printer import Printer

import logging


# Driver for Checker & Classifier interface.
MONGO_COLLECTION = "domain_info"

class security_crawler(Thread):

	def __init__(self):
		
		self.raw_history = set()
		self.sites_to_visit = set()	
		self.domain_infos = set()
		self.red_list = set()
		self.db_client = None
		self.checker = Checker.connection_checker()
		logging.basicConfig(
			format='%(asctime)s %(message)s',
			level=logging.INFO,
                        datefmt='%H:%M:%S')
		logging.info('***crawler started')
		self.classifier_errorcount = 0

	def get_history(self, filename):
		unique_history = set()
		df = pd.read_csv(filename)
		
		for indx, row in df.iterrows():
			url = row['url']
			if url not in self.raw_history and type(url) == str:
				self.raw_history.add(url)
				self.sites_to_visit.add(url)

	def add_children_to_visit(self):
		# create "parser" objects for each of the urls.

		for link in self.raw_history:
			p = parser.Parser(link)
			children = p.get_links_from_child_pages()

		for child in children:
			logging.info("Adding child to visit--" + child)
			if "http" in child: 
				self.sites_to_visit.add(child)

	# The thread function.
	def crawl_url(self, url):
		logging.info("Crawling URL --" + url)
		if 'http' not in url:
			pass
		c = self.checker
		d = DomainInfo.domain_info(url)

		logging.info("Running checker analysis.")
		try:
			domain, valid_cert, expiering_soon, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)
			logging.info("Checker analysis complete.")
			if red_list:
				self.red_list.add(url)
		
			d.domain = domain
			d.valid_cert = valid_cert
			d.ports_open = ports_open
			d.tls_versions_supported = tls_versions_supported
			d.ciphers_supported = ciphers_supported
			d.expiering_soon = expiering_soon

			# get results from classifier..
			logging.info("Running classifier.")
			try:
				d.classification = Classifier.Classifier(url).classification
			except:
				logging.info("Broke during classification")
				self.classifier_errorcount += 1
				pass
			logging.info("Classifier complete.")

			self.domain_infos.add(d)

			# output to mongo
			mongo = Client(MONGO_COLLECTION)
			while(mongo.connect()):
				mongo.insert(d.export_json())
				mongo.close()
				print('db updated with ', url)
				break
		except:
			logging.info("Broke during checker analysis.")
			pass

			
	def sample_run(self):
		running_threads = []		
		urls = ["github.com", "https://www.kqed.org/coronavirusliveupdates"]
		for url in urls:
			t = Thread(target=self.crawl_url, args=(url,))
			t.start()
			running_threads.append(t)

		# joining threads
		for t in running_threads:
			t.join()

	def run(self):
		# obtain first level of history
		# then add children to visit from first level of history.
		#self.get_txt_history("sturdycouscous/resources/children-2.txt")
		self.get_history(filename="sturdycouscous/history/embarrassing_history.csv")
		self.get_history(filename="sturdycouscous/history/history_large.csv")
		# self.add_children_to_visit()
		print("about to scan %s websites", len(self.sites_to_visit))
		pass
		running_threads = []
		# start each thread
		for url in self.sites_to_visit:
			self.crawl_url(url)
#			print("Starting thread for " + str(url))
#			if len(url) > 1:
#				t = Thread(target=self.crawl_url, args=(url,))
#				t.start()
#				print("Thread %s started to evaluate %s" ,  str(t) , url)
#				running_threads.append(t)
		# joining threads
#		for t in running_threads:
#			t.join()  
		print("Classifier error count: " + str(self.classifier_errorcount))

if __name__ == "__main__":
	sc = security_crawler()
#	sc.sample_run()
	sc.run()
	Printer().output_report()
