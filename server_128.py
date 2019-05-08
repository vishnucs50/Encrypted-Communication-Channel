import random
from Crypto.Cipher import AES
import socket
from Crypto.Random import get_random_bytes
from time import time

host = '127.0.0.1'
port = 56739                                                        #UDP server port number
buffersize = 4096
x_bob = 253

ServerSocketB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ServerSocketB.bind((host, port))

while True:                                         #Listen to the convo until terminated
    data, addr = ServerSocketB.recvfrom(buffersize)    #Msg from Alice 1
    print ("The message is:", data)
    message = "Hey! Got your Message"
    ServerSocketB.sendto(message, addr)
    data = ServerSocketB.recvfrom(4096)
    print("The value of alpha, q and Y_a is given as:", data)
    string = data[0]
    a = int(string[0])
    q = int(string[2:7])
    y_alice = int(string[8:12])
    def val_dh(sec_bob, q, a):
        y_bob = (a ** sec_bob) % q

        return y_bob


    y_bob = val_dh(sec_bob, q, a)
    y_bob = str(y_bob)
    print ("Print Y_bob", y_bob)
    ServerSocketB.sendto(y_bob, addr)

    def dh_key(y_alice):
        val_dh(x_bob, q, a)
        k = (y_alice ** sec_bob) % q
        keyvalue = bin(k)[2:].zfill(16)
        return keyvalue

    Alice_key = dh_key(y_alice)
    key = bin(3750)[2:].zfill(16)
    start = time()
    class AESCipher:
        def __init__(self, key):
            self.key = key

        def encrypt(self, message):
            if len(message) % 16 == 0:
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

    data = ServerSocketB.recvfrom(4096)
    bobclass = AESCipher(key)
    data = data[0]
    bob_decrypt = bobclass.decrypt(data)
    print("Initial challenge received from Alice: ", int(bob_decrypt))

    def randomnumber():
        y = random.getrandbits(32)
        convert = "{0:b}".format(y)

        return y

    nounce = randomnumber()
    bob_decrypt = int(bob_decrypt) - 1
    message = str(nounce)+','+str(bob_decrypt)

    cipher_bob = bobclass.encrypt(message)
    print("The first challenge message: ", nounce, cipher_bob)
    ServerSocketB.sendto(cipher_bob, addr)
    data = ServerSocketB.recvfrom(4096)
    data = data[0]
    bob_decrypt = bobclass.decrypt(data)

    fin_challenge = int(bob_decrypt)
    print("The final challenge: ", fin_challenge)
    if fin_challenge == (nounce - 1):
        print("The nonce and 1 less are:", nounce, fin_challenge)
        message = "authentication successful" \
                  "authentication successful" \
                  "authentication successful" \
                  "authentication successful" \
                  "authentication successful" \
                  "authentication successful" \

        cipher_bob = bobclass.encrypt(message)

        end = time()
        print("The duration of AES 192 encryption: ", end - start)
        ServerSocketB.sendto(cipher_bob, addr)                                 ##MESSAGE AUTHENTICATION

    else:
        message = "Authentication failure"
        ServerSocketB.sendto(message, addr)                                     ##MESSAGE FAILURE
        break


ServerSocketB.close()