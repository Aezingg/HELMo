# coding: utf8
import socket
from datetime import datetime
import sys
buffersize = 16777216

time = datetime.now()

if sys.argv[1] == "fail":
    subject = "Tentatives de connexion"
    message = f"Le LogHost a report un nombre anormal de tentatives de connexion\nDate : {time.strftime('%a, %d %b %y %H:%M')}\nUser : {sys.argv[2]}\n" \
              f"Machine : {sys.argv[3]}"

elif sys.argv[1] == "double":
    subject = "Tentative de DoS"
    message = f"Le LogHost a report une potentielle tentaitve DoS\nDate : {time.strftime('%a, %d %b %y %H:%M')}\nUser : {sys.argv[2]}\n"

elif sys.argv[1] == "sudo":
    subject = "Faille SUDO"
    message = f"Le LogHost a report une tentative de l'utilisation de la faille sudo\nDate : {time.strftime('%a, %d %b %y %H:%M')}\nUser : {sys.argv[2]}\n"

elif sys.argv[1] == "cascade":
    subject = "Connexion en cascade"
    message = f"Le LogHost a report une tentative de connexion en cascade\nDate : {time.strftime('%a, %d %b %y %H:%M')}\nUser : {sys.argv[2]}\n"

sender_mail = "loghost@helmo.be"
sender_name = "LogHost"

# create socket
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# connect to server
ipv4 = socket.gethostbyname("relay.proximus.be")
port = 25
client.connect((ipv4, port))

print(f"You are connected to '{ipv4}:25'")


# send message
data = client.recv(buffersize)
print(data.decode())

if data[0:3].decode() == "220":
    client.sendto(str.encode("EHLO mail_server_helmo.home\n"), (ipv4, 25))
    print("EHLO mail_server_helmo.home")

    data = client.recv(buffersize)
    print(data.decode())

    if data[0:3].decode() == "250":
        client.sendto(str.encode(f"MAIL FROM:<{sender_mail}>\n"), (ipv4, 25))
        print(f"MAIL FROM:<{sender_mail}>")

        data = client.recv(buffersize)
        print(data.decode())

        if data[0:3].decode() == "250":
            client.sendto(str.encode(f"RCPT TO:<a.valente@student.helmo.be>\n"), (ipv4, 25))
            print(f"RCPT TO:<a.valente@student.helmo.be>")

            data = client.recv(buffersize)
            print(data.decode())

            if data[0:3].decode() == "250":
                client.sendto(str.encode(f"RCPT TO:<al.dupret@student.helmo.be>\n"), (ipv4, 25))
                print(f"RCPT TO:<al.dupret@student.helmo.be>")

                data = client.recv(buffersize)
                print(data.decode())

                if data[0:3].decode() == "250":
                    client.sendto(str.encode(f"RCPT TO:<l.thiteux@student.helmo.be>\n"), (ipv4, 25))
                    print(f"RCPT TO:<l.thiteux@student.helmo.be>")

                    data = client.recv(buffersize)
                    print(data.decode())

                    if data[0:3].decode() == "250":
                        client.sendto(str.encode("DATA\n"), (ipv4, 25))
                        print("DATA")

                        data = client.recv(buffersize)
                        print(data.decode())

                        if data[0:3].decode() == "354":
                            client.sendto(str.encode(f"Date: {time.strftime('%a, %d %b %y %H:%M')}\n"), (ipv4, 25))
                            print(f"Date: {time.strftime('%a, %d %b %y %H:%M')}")

                            client.sendto(str.encode(f"From: {sender_name} <{sender_mail}>\n"), (ipv4, 25))
                            print(f"From: {sender_name} <{sender_mail}>")

                            client.sendto(str.encode(f"To: Antoine Valente <a.valente@student.helmo.be>\n"), (ipv4, 25))
                            print(f"To: Antoine Valente <a.valente@student.helmo.be>")

                            client.sendto(str.encode(f"Cc: Alexis Dupret <al.dupret@student.helmo.be>, Lucas Thiteux <l.thiteux@student.helmo.be>\n"), (ipv4, 25))
                            print(f"Cc: Alexis Dupret <al.dupret@student.helmo.be>, Lucas Thiteux <l.thiteux@student.helmo.be>")

                            client.sendto(str.encode(f"Subject: {subject}\n",encoding='UTF-8'), (ipv4, 25))
                            print(f"Subject: {subject}")

                            client.sendto(str.encode(f"{message}\n", encoding='UTF-8'), (ipv4, 25))
                            print(f"{message}")

                            client.sendto(str.encode(".\n"), (ipv4, 25))
                            print(".")

                            data = client.recv(buffersize)
                            if data[0:3].decode() == "250":
                                client.sendto(str.encode("quit\n"), (ipv4, 25))
                                print("quit")

# close connection
client.close()
print('Connection closed')
