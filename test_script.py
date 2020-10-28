import socket, ssl
def get_tls_version(domain="google.com"):
	context = ssl.create_default_context()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sslSocket = context.wrap_socket(s, server_hostname = domain)
	sslSocket.connect((domain, 443))
	print(sslSocket.version())
if __name__ == "__main__":
	domains = ["google.com", "netflix.com", "yahoo.com", "amazon.com"]
	for domain in domains:
		print(domain)
		get_tls_version(domain)
