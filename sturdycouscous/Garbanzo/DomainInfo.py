# Class that represents all the amassed SSL/TLS info about a given domain.

class domain_info():

	def __init__(self, url):
		# Provided by Security Crawler
		self.domain = ""
		self.url = url
		self.title = "" # for "habits classifier" purposes

		# Checker fields
		self.tls_versions_supported = []
		self.ports_open = []
		self.ciphers_supported = {}
		self.valid_cert = False
		self.expiering_soon = False

		# Classification fields
		self.classification = {}

	def export_json(self):
		return {
				"URL": self.url,
				"Title": self.title,
				"Domain": self.domain,
				"Checker": {
					"tls_versions_supported": [str.replace(".", "-") for str in self.tls_versions_supported],
					"open_ports": self.ports_open,
					"certificate_valid": self.valid_cert,
					"ciphers_supported": self.ciphers_supported,
					"expiering_soon": self.expiering_soon
				},
				"Classification": self.classification
			}
