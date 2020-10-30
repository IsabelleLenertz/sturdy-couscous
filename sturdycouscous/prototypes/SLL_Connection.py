#Connection.bind(address)
#Connection.connect(address)
#Connection.get_peer_certificate()
#Connection.get_cipher_list()
#Connection.context()
#connection.close()

# Installing pip
# python get-pip.py
# pip -V # checking version
# python -m pip install --upgrade pip #upgrading

# Installing pyOpenSSL
# pip install pyopenssl

# pyOpenSSL Documentation: https://www.pyopenssl.org/en/stable/index.html
# python networking interface: https://docs.python.org/3/library/ipc.html
from OpenSSL import SSL, crypto
import socket

# Callback method to verify the certificat
# callback should take five arguments: A Connection object, an X509 object, and three integer variables, which are in turn potential error number, error depth and return code. callback should return true if verification passes and false otherwise.
def verify_cb(conn, cert, errnum, depth, ok):
    # This obviously has to be updated
    print('Got certificate: %s' % cert.get_subject())
    #don't ever do this in production.
    #this force verifies all certs.
    return 1

# Initialize context
context = SSL.Context(SSL.TLSv1_2_METHOD);
context.set_verify(SSL.VERIFY_PEER, verify_cb); # when receiving a certificate, call the callback method defeind above

# Set up connection client
connection = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
connection.connect(("google.com", 443))

# Sends a simple get request
connection.send("""GET / HTTP/1.0
Host: www.google.com
""".replace("\n","\r\n"))

# Look at the response
# socket.recv(bufsiz{,flags])
# Receive data from the socket. The return value is a bytes object representing the data received. The maximum amount of data to be received at once is specified by bufsize. See the Unix manual page recv(2) for the meaning of the optional argument flags; it defaults to zero.
# Note For best match with hardware and network realities, the value of bufsize should be a relatively small power of 2, for example, 4096.
while True:
    try:
        buf = connection.recv(4096)
    except SSL.SysCallError:
        break
    if not buf:
        break
connection.close()