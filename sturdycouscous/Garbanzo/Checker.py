# Class with methods defined that `
# 1) Check certificate validity 
# 2) Check TLS versions supported
# 3) Look for open ports
# 4) Get all ciphers supported (?)
import socket, ssl
from datetime import datetime

class connection_checker():

	# Returns a boolean checking whether a specified port for a given domain is open.
	def port_checker(self, domain, port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		
		result = s.connect_ex((domain, port))
		return (result == 0)

	# Checks whether the certificate obtained using the default_context is still valid.
	# Returns True if certificate is still valid.
	def certificate_checker(self, domain):
		context = ssl.create_default_context()
		sslSocket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = domain)
		sslSocket.connect((domain, 443))
		
		cert = sslSocket.getpeercert()
		expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")

		return datetime.now() < expiry_date


	# Returns the list of all tls contexts
	def get_all_tls_contexts(self):
		# Contexts for each TLS version
		tlsv1_3_context = ssl.create_default_context()
		tlsv1_3_context.options |= (ssl.PROTOCOL_TLS | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)

		tlsv1_2_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		tlsv1_1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
		tlsv1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

		contexts_dict = {
			tlsv1_context: "tlsv1",
			tlsv1_1_context: "tlsv1_1",
			tlsv1_2_context: "tlsv1_2",
			tlsv1_3_context: "tlsv1_3",
		}

		contexts = [tlsv1_3_context, tlsv1_2_context, tlsv1_1_context, tlsv1_context]

		return contexts_dict, contexts		

	# Returns a list of all TLS verions supported for the given domain. 
	def tls_versions_checker(self, domain):
		# Contexts for each TLS version
		# tlsv1_3_context = ssl.create_default_context()
		# tlsv1_3_context.options |= (ssl.PROTOCOL_TLS | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)

		# tlsv1_2_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		# tlsv1_1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
		# tlsv1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

		# contexts_dict = {
		# 	tlsv1_context: "tlsv1",
		# 	tlsv1_1_context: "tlsv1_1",
		# 	tlsv1_2_context: "tlsv1_2",
		# 	tlsv1_3_context: "tlsv1_3",
		# }

		# contexts = [tlsv1_3_context, tlsv1_2_context, tlsv1_1_context, tlsv1_context]
		
		contexts_dict, contexts = self.get_all_tls_contexts()
		versions_supported = []

		for context in contexts:
			if self.test_tls_version(context, domain):
				versions_supported.append(contexts_dict[context])

		return {domain: versions_supported}


	def test_tls_version(self, context, domain):
		success = True
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
			sslSocket = context.wrap_socket(s, server_hostname = domain)
			sslSocket.connect((domain, 443))
			print(sslSocket.version())
		except:
			success = False
		finally:
			return success
	

	# Returns a list of all ciphers supported by... context...? 
	# Need more clarification on this one.
	def get_all_ciphers(self, domain):

		context = ssl.create_default_context()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		sslSocket = context.wrap_socket(s, server_hostname = domain)

		sslSocket.connect((domain, 443))
		all_ciphers = sslSocket.shared_ciphers()

		return all_ciphers




