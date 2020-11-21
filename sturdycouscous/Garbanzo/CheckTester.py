from Checker import *
import unittest

# The four main functions to test are:
# 1) port_checker
# 2) tls_versions_checker
# 3) certificate_checker
# 4) get_supported_ciphers

class check_tester(unittest.TestCase):

	# These methods are called before every test.
	def setUp(self):
		pass

	def tearDown(self):
		pass

	# Sanity check that "bad" ports are closed.
	def test_ports(self):
		checker = connection_checker()
		domain = "amazon.com"
		ports_open = checker.port_checker(domain)

		# There should at least be 443 open.
		self.assertTrue(len(ports_open) > 0)
		self.assertTrue(443 in ports_open)

		# Ports 3389 (Remote Desktop Protocol) and 514 (Remote Shell) should NOT be open.
		self.assertFalse(3389 in ports_open)
		self.assertFalse(514 in ports_open)

	# Test against known bad certificates.
	def test_certs(self):
		# Sanity check for good cert.
		checker = connection_checker()
		self.assertTrue(checker.certificate_checker(domain="docs.google.com"))

		# Bad certs -- wrong.host.badssl.com, expired.badssl.com, untrusted-root.badssl.com
		# Can't check for revoked yet. 
		self.assertFalse(checker.certificate_checker(domain="wrong.host.badssl.com"))
		self.assertFalse(checker.certificate_checker(domain="expired.badssl.com"))
		self.assertFalse(checker.certificate_checker(domain="untrusted-root.badssl.com"))

	# Test supported TLS versions.
	def test_tls_versions(self):

		conn_checker = connection_checker()
		tls_contexts = {item[1]: item[0] for item in conn_checker.get_all_tls_contexts()[0].items()}

		# Testing TLS 1.2 thru 1.0 on badssl.
		self.assertTrue(conn_checker.test_tls_version(context=tls_contexts['TLSv1.0'], domain="tls-v1-0.badssl.com", port=1010))
		self.assertTrue(conn_checker.test_tls_version(context=tls_contexts['TLSv1.1'], domain="tls-v1-1.badssl.com", port=1011))
		self.assertTrue(conn_checker.test_tls_version(context=tls_contexts['TLSv1.2'], domain="tls-v1-2.badssl.com", port=1012))
	
		# Testing to make sure that you can't connect to a TLS v1.0 site with a TLS v1.2 context.
		self.assertFalse(conn_checker.test_tls_version(context=tls_contexts['TLSv1.2'], domain="tls-v1-1.badssl.com", port=1011))

		# Testing to make sure that you can't connect to a TLS v1.3 site with a TLSv1.2 context.
		self.assertFalse(conn_checker.test_tls_version(context=tls_contexts['TLSv1.2'], domain="tls13.1d.pw"))
		
		# Testing the same domain to ensure that TLS v1.3 context works.
		self.assertTrue(conn_checker.test_tls_version(context=tls_contexts['TLSv1.3'], domain="tls13.1d.pw"))

	# Test ciphers.
	def test_ciphers(self):
		# Can test against tls 1.1 to make sure no tls 1.3 ciphers are there
		# same with SSLv2/3 ciphers...?
		
		# found this site: https://null.badssl.com/
		pass



if __name__ == "__main__":
	unittest.main()