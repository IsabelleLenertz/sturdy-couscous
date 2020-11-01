import socket, ssl

# Testing through the versions of TLS and SSL

def get_tls_version(domain="google.com"):
	
	# tlsv1_3 context:
	tlsv1_3_context = ssl.create_default_context()
	tlsv1_3_context.options |= (ssl.PROTOCOL_TLS | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2)

	# tlsv1_2 context:
	tlsv1_2_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

	# tlsv1_1 context
	tlsv1_1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)

	tlsv1_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sslSocket = tlsv1_context.wrap_socket(s, server_hostname = domain)
	sslSocket.connect((domain, 443))
	print(sslSocket.version())

if __name__ == "__main__":
	domains = ["google.com", "netflix.com", "yahoo.com", "amazon.com"]
	for domain in domains:
		print(domain)
		get_tls_version(domain)
