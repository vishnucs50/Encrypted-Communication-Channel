import random
import socket
from time import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
start = time()

host = "127.0.0.1"
port = 56739                                                    #port number of UDP server

message = "Hey Bob! Let's start the Key Exchange?"
q = 17707
a = 3                                                         #Alpha
sec_alice = 91

ClientSocketA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket object
ClientSocketA.sendto(message, (host, port))                      ##First Msg

def val_dh(sec_alice, q, a):
    y_alice = (a**x_alice) % q                                  #Calculate value to be shared publicly over the internet
    return y_alice

y_alice = val_dh(91,17707,3)
my_msg= str(a)+','+str(q)+','+str(y_alice)
ClientSocketA.sendto(my_msg, (host, port))                ##Msg to Bob

rec_msg = ClientSocketA.recvfrom(4096)       #Msg from Bob 1
rec_msg = ClientSocketA.recvfrom(4096)       #Msg from Bob 2
y_bob = rec_msg[0]
print ("Y_Bob:", y_bob)
y_bob = int(y_bob[0])

def dh_key(y_bob):      #AES 192 Key
    val = (y_bob**sec_alice)%q
    keyvalue = bin(val)[2:].zfill(24)
    return keyvalue

def randomnumber():
    y = random.getrandbits(32)
    convert = "{0:b}".format(y)

    return y

nounce = randomnumber()
message = str(nounce)

key = bin(3750)[2:].zfill(24)      #192 AES format


class AESCipher:         #AES 128, 192, 256
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        if len(message)%16 == 0:
            plaintext = message.encode('utf-8')
            cipher = AES.new(key, AES.MODE_ECB)
            msg = cipher.encrypt(plaintext)
        else:
            length = len(message)
            plaintext = (message + ((16 - length % 16) * str(0)))
            plaintext = plaintext.encode('utf-8')
            cipher = AES.new(key, AES.MODE_ECB)
            msg = cipher.encrypt(plaintext)
        return msg

    def decrypt(self, msg):

        decipher = AES.new(self.key, AES.MODE_ECB)
        plaintext = decipher.decrypt(msg)
        plaintext = plaintext.decode('utf-8')
        plaintext = plaintext.rstrip('0')
        return plaintext

aliceclass = AESCipher(key)
cipher_alice = aliceclass.encrypt(message)
print("Nounce is sent: ", message)
print("sent encrypted nounce: ", cipher_alice)

ClientSocketA.sendto(cipher_alice, (host, port))     #Msg to Bob 3

data = ClientSocketA.recvfrom(4096)            #Msg from Bob 3

print (data)
data = data[0]
alice_decrypt = aliceclass.decrypt(data)
print("Nounce generated: ", alice_decrypt)

idx_val = alice_decrypt.index(',')
alice_decrypt = int(alice_decrypt[0:idx_val])
alice_decrypt = alice_decrypt - 1
message = str(alice_decrypt)
data = aliceclass.encrypt(message)
print("Final challenge : ", alice_decrypt, data)
ClientSocketA.sendto(data, (host, port))

data = ClientSocketA.recvfrom(4096)                            ###FINAL AUTHENTICATION
data = data[0]
print("Final received message is: ", str(data))                      #success or failure

end = time()
print("The duration of execution is: ",end - start)