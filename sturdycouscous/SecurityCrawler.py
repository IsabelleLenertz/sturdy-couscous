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


	def check_domain_exist(self, url):

		domain = Checker.connection_checker().grab_domain_name(url)

		for d in self.domain_infos:
			if d.domain == domain:
				new = DomainInfo.domain_info(url)
				
				new.domain = d.domain
				new.title = d.title
				new.tls_versions_supported = d.tls_versions_supported
				new.ports_open = d.ports_open
				new.ciphers_supported = d.ciphers_supported
				new.valid_cert = d.valid_cert
				new.expiering_soon = d.expiering_soon

				return new

		return None

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

		self.get_txt_history("sturdycouscous/resources/children-med.txt")

		print("about to scan %s websites", len(self.sites_to_visit))

		# removing threads.
		for url in self.sites_to_visit:
			print("**********  ", url, " **********")
			c = Checker.connection_checker()
			
			# checking if the domain has already been examined.
			d = self.check_domain_exist(url)

			# if domain has not already been examined, perform TLS checks.
			if d is None:
				
				d = DomainInfo.domain_info(url)
				
				# putting try/catch block in here for the time being
				try:
					print("checker runnin")			
					domain, valid_cert, expiering_soon, ports_open, tls_versions_supported, ciphers_supported, red_list = c.checker_analysis(url)

					d.domain = domain
					d.valid_cert = valid_cert
					d.ports_open = ports_open
					d.tls_versions_supported = tls_versions_supported
					d.ciphers_supported = ciphers_supported
					d.expiering_soon = expiering_soon

					if red_list:
						self.red_list.add(url)

				except Exception as e:
					print(e)

			# Classifier will be run on the url, not on the domain. 
			# Therefore, it should be run for every URL.
			print("Classifier Runnin")
			d.classification = Classifier.Classifier(url).classification
			print("done classifying")

			self.domain_infos.add(d)
		# endfor

		print("final results: " + str(len(self.domain_infos)) + " sites visited")

		# write to mongo
		mongo = Client(MONGO_COLLECTION)
		for info in self.domain_infos:
			while(mongo.connect()):
				mongo.insert(info.export_json())
		mongo.close()

 
if __name__ == "__main__":
	sc = security_crawler()
	sc.run()
