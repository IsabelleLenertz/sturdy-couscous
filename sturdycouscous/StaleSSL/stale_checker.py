import ssl, socket

sites = [["tls-v1-1.badssl.com:1101"], ["tls-v1-0.badssl.com:1010"]]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
contexts = [ssl.SSLContext(ssl.PROTOCOL_TLSv1_1), ssl.SSLContext(ssl.PROTOCOL_TLSv1)]

def check_tls(domain, port):
    for context in contexts:
        result = check_protocol(domain, port, context)
        if result:
            print("TLS Version for " + domain + ": " + str(result))
        else:
            print("****FAILURE FOR " + domain + " " + str(context))

def check_protocol(domain, port, context):
    sock = context.wrap_socket(s, server_hostname=domain)
    try:
        sock.connect((domain, port))
    except:
        return False
    return sock.version()

def custom_port(site):
    info = site.split(":") if len(site.split(":")) > 1 else site
    return info

for site in sites:
    print("checking site: " + str(site))
    if isinstance(custom_port(site), list):
        print(site)
        print(check_tls(site[0], site[1]))
    else:
        print(check_tls(site, 443))
