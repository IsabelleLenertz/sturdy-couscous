# Class that represents all the amassed SSL/TLS info about a given domain.

class domain_info():

	def __init__(self, domain):
		# Provided by Security Crawler
		self.domain = domain
		self.title = title # for "habitat classifier" purposes

		# To be filled in by SecurityCrawler + Checker
		self.tls_versions_supported = None
		self.ports_open = None
		self.ciphers_supported = None
		self.valid_cert = None


	def export_json(self):
		json_obj = {
			"domain": self.domain,
			"tls_versions_supported": self.tls_versions_supported,
			"open_ports": self.ports_open,
			"certificate_valid": self.valid_cert,
			"ciphers_supported": self.ciphers_supported
		}

		return json_obj