import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")

from Garbanzo import Checker, DomainInfo
from bouneschlupp import parser, Classifier
from Mongo_Client import Client
import pandas as pd 
from threading import Thread
import csv

# Driver for Checker & Classifier interface.
MONGO_COLLECTION = "domain_info"

class security_crawler(Thread):

	def __init__(self):
		
		self.raw_history = set()
		self.sites_to_visit = set()	
		self.domain_infos = set()
		self.red_list = set()
		self.db_client = None
	
	def get_history(self, filename):
		df = pd.read_csv(filename)
		
		for indx, row in df.iterrows():
			url = row['url']
			if url not in self.raw_history:
				self.raw_history.add(url)
				self.sites_to_visit.add(url)

	def get_txt_history(self, filename):
		with open(filename) as file:
			lines = file.readlines()
			for line in lines:
				self.sites_to_visit.add(line.strip())

	def add_children_to_visit(self):
		# create "parser" objects for each of the urls.
		for link in self.raw_history:
			print("processing children of ", link)
			self.sites_to_visit.update(parser.Parser(link).get_link_from_descendent(1))
		with open("sturdycouscous/resources/children-2.txt", "w") as out:
			out.write("\n".join(str(i) for i in self.sites_to_visit))

	def get_traing_set(self):
		with open("sturdycouscous/resources/keyword_training.csv") as csvfile:
			training_sample = csv.reader(csvfile, delimiter=',')
			for row in training_sample:
				self.sites_to_visit.add(row[0])

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
		# obtain first level of history
		# then add children to visit from first level of history.
		#self.get_txt_history("sturdycouscous/resources/children-2.txt")
		#self.get_history(filename="sturdycouscous/history/embarrassing_history.csv")
		self.get_traing_set()
		#self.add_children_to_visit()
		print("about to scan %s websites", len(self.sites_to_visit))

		running_threads = []

		# start each thread
		for url in self.sites_to_visit:
			print("**********  ", url, " **********")
			print("checker runnin")
			#c = Checker.connection_checker()
			d = DomainInfo.domain_info(url)
			#try:			
			'''domain, valid_cert, expiering_soon, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)
			if red_list:
				self.red_list.add(url)
			d.domain = domain
			d.valid_cert = valid_cert
			d.ports_open = ports_open
			d.tls_versions_supported = tls_versions_supported
			d.ciphers_supported = ciphers_supported
			d.expiering_soon = expiering_soon
			# get results from classifier..'''
			print("Classifier Runnin")
			d.classification = Classifier.Classifier(url).classification
			print("done classifying")
			self.domain_infos.add(d)
			# output to mongo
			mongo = Client(MONGO_COLLECTION)
			while(mongo.connect()):
				mongo.insert(d.export_json())
				mongo.close()
				print('db updated with ', url)
				break 
 
if __name__ == "__main__":
	sc = security_crawler()
#	sc.sample_run()
	sc.run()
