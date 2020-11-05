# Class with methods defined that `
# 1) Check certificate validity 
# 2) Check TLS versions supported
# 3) Look for open ports
# 4) Get all ciphers supported (?)
import socket, ssl

class connection_checker():

	# Returns a boolean checking whether a specified port for a given domain is open.
	def port_checker(domain, port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		
		result = s.connect_ex((domain, port))
		return (result == 0)

	# Checks whether the certificate obtained using the default_context is still valid.
	def certificate_checker(domain):
		pass

	# Returns a list of all TLS verions supported for the given domain. 
	def tls_versions_checker(domain):
		pass

	# Returns a list of all ciphers supported by... context...? 
	# Need more clarification on this one.
	def get_all_ciphers(domain):
		pass
