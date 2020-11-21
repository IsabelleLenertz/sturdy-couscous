# Class with methods defined that `
# 1) Check certificate validity 
# 2) Check TLS versions supported
# 3) Look for open ports
# 4) Get all ciphers supported 
import socket, ssl
import copy
from datetime import datetime

class connection_checker():

	# Returns list of open ports.
	def port_checker(self, domain):

		port_list = [20, 21, 22, 23, 25, 53, 69, 67, 80, 110, 119, 123, 143, 161, 162, 389, 443, 445, 514, 554, 636, 1720, 3389, 5060, 5061]
		ports_open = []

		for port in port_list:

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(1)
		
			result = s.connect_ex((domain, port))
			if (result == 0):
				ports_open.append(port)
			s.close()

		return ports_open

	# Checks whether the certificate obtained using the default_context is still valid.
	# Returns True if certificate is still valid.
	# Tabling the discussion for revoked certificates for later, since it's a bit complicated.
	def certificate_checker(self, domain, port=443):
		context = ssl.create_default_context()
		sslSocket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = domain)
		
		# sslSocket.connect can throw an error
		valid_cert = False
		try:
			sslSocket.connect((domain, port))
			cert = sslSocket.getpeercert()
			expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
			valid_cert = datetime.now() < expiry_date
		except:
			pass
		finally:
			sslSocket.close()
			return valid_cert


	# Returns the list of all tls contexts
	def get_all_tls_contexts(self):
		# Contexts for each TLS version
		tlsv1_3_context = ssl.create_default_context()
		tlsv1_3_context.options |= (ssl.PROTOCOL_TLS | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)

		tlsv1_2_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		tlsv1_1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
		tlsv1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

		contexts_dict = {
			tlsv1_context: "TLSv1.0",
			tlsv1_1_context: "TLSv1.1",
			tlsv1_2_context: "TLSv1.2",
			tlsv1_3_context: "TLSv1.3",
		}

		contexts = [tlsv1_3_context, tlsv1_2_context, tlsv1_1_context, tlsv1_context]

		return contexts_dict, contexts		

	# Returns a list of all TLS verions supported for the given domain. 
	def tls_versions_checker(self, domain):
		# Contexts for each TLS version		
		contexts_dict, contexts = self.get_all_tls_contexts()
		versions_supported = []

		for context in contexts:
			if self.test_tls_version(context, domain):
				versions_supported.append(contexts_dict[context])

		return versions_supported


	def test_tls_version(self, context, domain, port=443):
		success = True
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
			sslSocket = context.wrap_socket(s, server_hostname = domain)
			sslSocket.connect((domain, port))
			# print(sslSocket.version())
		except:
			success = False
		finally:
			sslSocket.close()
			return success
	

	# Returns a dictionary mapping tls version -> ciphers supported on the client side.
	# socket.shared_ciphers returns only the client-side ciphers.
	# therefore, need to test one by one.
	def get_all_ciphers(self):
		domain = "www.google.com"
		context = ssl.create_default_context()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		sslSocket = context.wrap_socket(s, server_hostname = domain)
		sslSocket.connect((domain, 443))

		all_ciphers = sslSocket.shared_ciphers()

		cipher_dict = {
			"TLSv1.0": [],
			"TLSv1.1": [],
			"TLSv1.2": [],
			"TLSv1.3": []
		}

		for cipher in all_ciphers:
			if cipher[1] in ["TLSv1.3", "TLSv1.2", "TLSv1.1", "TLSv1.0"]:
				cipher_dict[cipher[1]].append(cipher[0])				

		sslSocket.close()
		return cipher_dict

	# Returns a context for a given TLS version.
	def get_context_by_version(self, tls_version):
		if tls_version == "TLSv1.3":
			tlsv1_3_context = ssl.create_default_context()
			tlsv1_3_context.options |= (ssl.PROTOCOL_TLS | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)
			return tlsv1_3_context
		elif tls_version == "TLSv1.2":
			return ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		elif tls_version == "TLSv1.1":
			return ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
		elif tls_version == "TLSv1.0":
			return ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

	# Returns a list of all ciphers supported by the domain's context 
	def get_supported_ciphers(self, domain, tls_versions_supported, port=443):

		# actually so we have to make a list of all the ciphers the client supports sorted out by TLS version
		# and force a connection for each of those using that particular cipher, and see if it works or not.
		supported_cipher_dict = {version: [] for version in tls_versions_supported}
		all_ciphers = self.get_all_ciphers()
		
		for tls_version in tls_versions_supported:

			if tls_version == "TLSv1.3":
				# cannot disable any of the TLS1.3 ciphers. 
				# can only get the shared cipher at the time being.
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sslSocket = self.get_context_by_version("TLSv1.3").wrap_socket(s, server_hostname=domain)
				sslSocket.connect((domain, port))
				supported_cipher_dict["TLSv1.3"].append(sslSocket.cipher()[0])
				sslSocket.close()

			else:
				for cipher in all_ciphers[tls_version]:
					# create context for that tls version and force the one cipher.
					cipher_context = self.get_context_by_version(tls_version)
					cipher_context.set_ciphers(cipher)

					# set timeout to 1 second.
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					socket.setdefaulttimeout(1)
					sslSocket = cipher_context.wrap_socket(s, server_hostname = domain)

					# If the cipher doesn't work, we get a ssl.SSLError HANDSHAKE failure.
					try:		
						result = sslSocket.connect_ex((domain, port))
						if (result == 0):
							supported_cipher_dict[tls_version].append(cipher)
					except ssl.SSLError:
						pass
					finally:
						sslSocket.close()

		return supported_cipher_dict


