# Driver for Checker interface.
from Checker import *

def test_given_domains(domain_list=['amazon.com', 'google.com', 'facebook.com', 'badssl.com', 'python.org']):
	checker = connection_checker()
	for domain in domain_list:
		certificate_valid = checker.certificate_checker(domain)
		versions_supported = checker.tls_versions_checker(domain)
		all_ciphers = checker.get_all_ciphers(domain)

		common_ports = [80, 443]
		for port in common_ports:
			print(checker.port_checker(domain, port))


if __name__ == "__main__":
	test_given_domains()

