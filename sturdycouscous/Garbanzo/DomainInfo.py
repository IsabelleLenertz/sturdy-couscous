# Class that represents all the amassed SSL/TLS info about a given domain.

class domain_info():

	def __init__(self, url, domain):
		# Provided by Security Crawler
		self.domain = domain
		self.url = url

		self.title = "" # for "habitat classifier" purposes

		# Checker fields
		self.tls_versions_supported = []
		self.ports_open = []
		self.ciphers_supported = {}
		self.valid_cert = False

		# Classification fields
		self.categories = []
		self.keywords = []
		self.extension = ""


	def export_json(self):
		json_obj = 
		{
			"URL": self.url,
			"Title": self.title,
			"Domain": self.domain,
			"Checker": {
				"tls_versions_supported": self.tls_versions_supported,
				"open_ports": self.ports_open,
				"certificate_valid": self.valid_cert,
				"ciphers_supported": self.ciphers_supported
			},
			"Classification": {
				"categories": self.categories,
				"data": {
					"keywords": self.keywords,
					"extension": self.extension
				}

			}

		}


		return json_obj