from Decoding import Decoder


f = open('/Users/shoe/xecrypt.data', 'r')
d = Decoder(f.read())
d.decode()
