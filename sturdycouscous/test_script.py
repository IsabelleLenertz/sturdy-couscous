import socket, ssl

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


def test_tls_version(context, domain):

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
	

def get_tls_version(domain="google.com"):

	tls_version = None
	for context in contexts:
		if test_tls_version(context, domain):
			tls_version = contexts_dict[context]
			break

	print("domain: " + domain + " tls_version: " + tls_version)


if __name__ == "__main__":
	domains = ["google.com", "netflix.com", "yahoo.com", "amazon.com"]
	for domain in domains:
		print(domain)
		get_tls_version(domain)
