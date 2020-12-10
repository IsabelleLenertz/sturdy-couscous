import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")

from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser, Classifier
from Mongo_Client import Client
import pandas as pd 
from threading import Thread
import csv
import Utils

# Driver for Checker & Classifier interface.
MONGO_COLLECTION = "domain_info"

class security_crawler(Thread):

	def __init__(self, urls):
		
		self.raw_history = set()
		self.sites_to_visit = urls	
		self.domain_infos = set()
		self.red_list = set()
		self.db_client = None
		self.visited_domains = {}

	# The thread function.
	def crawl_url(self, url):
		c = Checker.connection_checker()
		d = DomainInfo.domain_info(url)
		#try:			
		domain, valid_cert, expiering_soon, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)
		if red_list:
			self.red_list.add(url)
		d.domain = domain
		d.valid_cert = valid_cert
		d.ports_open = ports_open
		d.tls_versions_supported = tls_versions_supported
		d.ciphers_supported = ciphers_supported
		d.expiering_soon = expiering_soon
		# get results from classifier..
		d.classification = Classifier.Classifier(url).classification
		self.domain_infos.add(d)
		# output to mongo
		mongo = Client(MONGO_COLLECTION)
		while(mongo.connect()):
			mongo.insert(d.export_json())
			mongo.close()
			print('db updated with ', url)
			break
		#except Exception as e:
		#	print(e)
			
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
		print("about to scan %s websites", len(self.sites_to_visit))
		mongo = Client(MONGO_COLLECTION)
		c = Checker.connection_checker()

		for url in self.sites_to_visit:
			print("**********  ", url, " **********")
			domain = Utils.grab_domain_name(url)
			d = self.visited_domains.get(domain)
			if(d is None):
				d = DomainInfo.domain_info(url)
				print("Checker running")			
				d.domain, d.valid_cert, d.expiering_soon, d.ports_open, d.tls_versions_supported, d.ciphers_supported, red_list = c.checker_analysis(domain)
				if red_list:
					self.red_list.add(url)
			else:
				d.url = url
			print("Classifier unning")
			d.classification = Classifier.Classifier(url).classification
			print("Analysis complete")
			self.visited_domains[domain] = d
			mongo = Client(Utils.DOMAIN_COLLECTION)
			mongo.connect()
			mongo.insert(d.export_json())

		print("Analysis Done")
