import socket
import os
import time
import datetime
import subprocess
import threading
from queue import Queue

version = "1.0"

connections_allowed = 20
connections = []
addresses = []
for i in range(connections_allowed):
    connections.append(0)
    addresses.append(0)
quit = False

admin_conn = ""
client_conn = ""
disconnect = False
transfering = False

THREADS = connections_allowed
JOB_NUMBER = connections_allowed
queue = Queue()

transfer_dir = os.getcwd()
printing = False

def thread_p(message):
    global printing
    while True:
        if printing == False:
            printing = True
            print(message)
            printing = False
            break

def socket_create():
    try:
        global host_list
        global port
        global s
        host_list = ["HOST IP GOES HERE"]
        port = int(HOST PORT GOES HERE)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Error while creating socket")


def socket_bind():
    try:
        for host in host_list:
            try:
                s.bind((host, port))
            except:
                continue
        s.listen(connections_allowed)
    except:
        print("Error while binding sockets")


def accept_connections():
    while True:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            for i in range(connections_allowed):
                if conn in connections:
                    continue
                if connections[i] == 0:
                    connections[i] = conn
                    addresses[i] = address
                    break
        except Exception as e:
            print(f"Error while accepting connections: {e}")
            break
    print("Program Terminated")

def list_connections(admin_n):
    results = ""
    for i in range(len(addresses)):
        if addresses[i] != 0 and addresses[i] != addresses[admin_n]:
            results += f"{str(i)}  {str(addresses[i][0])}  {str(addresses[i][1])}\n"
    connections[admin_n].send(f"\n----- Clients -----\n{results}".encode('utf-8'))
    thread_p(f"===== Admin Requested Client List =====\nRequest IP: {addresses[admin_n][0]}\nResult:\n----- Clients -----\n{results}\nStatus: Success\n")

# WORK ON ADMIN SHELL AND SEE IF THIS WORKS

def admin(thread):

    global disconnect

    try:
        while connections[thread] != 0 and addresses[thread] != 0:

            admin = connections[thread]
            cmd = admin.recv(128).decode('utf-8')

            if "select " in cmd:
                try:

                    target = cmd.replace("select ","")
                    if target == "":
                        admin.send("Invalid Connection Request".encode('utf-8'))
                        continue

                    try:
                        target = int(target)
                    except:
                        admin.send("You need to get a brain...".encode('utf-8'))
                        continue

                    if connections[target] != 0 and admin != connections[target] and target < connections_allowed and target >= 0:
                        try:
                            client = connections[target]
                        except:
                            admin.send("Invalid Connection Request".encode('utf-8'))
                            continue

                    else:
                        admin.send("Invalid Connection Request".encode('utf-8'))
                        continue

                    try:

                        connect_connections(thread, target)

                        while disconnect != True:
                            pass
                        disconnect = False
                        thread_p(f"===== Admin Requested Disconnection =====\nFrom: {addresses[thread][0]}\nTo: {addresses[target][0]}\nStatus: Success")

                    except Exception as e:
                        admin.send(f"Reroute to {addresses[target][0]} failed".encode('utf-8'))
                        thread_p(f"===== Admin Requested Connection =====\nFrom: {addresses[thread][0]}\nTo: {addresses[target][0]}\nStatus: Failed\nReason: {e}")
                        break

                except Exception as e:
                    thread_p(f"===== Admin Request Failed =====\nRequest IP: {addresses[thread][0]}\nRequested IP: {addresses[target][0]}\nReason: {e}")
                    break

            elif "list clients" == cmd:
                try:
                    list_connections(thread)
                except Exception as e:
                    thread_p(f"===== Admin Requested Client List =====\nRequest IP: {addresses[thread][0]}\nStatus: Failed\nReason: {e}")

            else:
                admin.send("Invalid Command".encode('utf-8'))
                continue


    except:
        thread_p(f"===== Admin Disconnected =====\nIP: {addresses[thread][0]}")
        connections[thread] = 0
        addresses[thread] = 0

def connect_connections(admin_n, client_n):

    global admin_conn
    global client_conn

    global admin_num
    global client_num

    admin_conn = connections[admin_n]
    client_conn = connections[client_n]

    admin_num = admin_n
    client_num = client_n

    admin_conn.send(f"{addresses[client_n][0]}".encode('utf-8'))
    thread_p(f"===== Admin Requested Connection =====\nFrom: {addresses[admin_n][0]}\nTo: {addresses[client_n][0]}\nStatus: Success")

def brain(): # THIS IS FOR ADMIN COMMANDS

    global disconnect
    global transfering

    global admin_conn
    global client_conn

    admin_conn = ""
    client_conn = ""

    while True:
        if admin_conn != "" and client_conn != "":
            try:
                # This checks for incoming commands from the admin.
                transfering = False
                # If program crashes for admin, this will time out the connection
                s.settimeout(60)
                while True:
                    try:
                        cmd = admin_conn.recv(128).decode('utf-8')
                        s.settimeout(None)
                        break
                    except:
                        thread_p(f"===== Scanning Admin Presence =====\nConnection: {addresses[admin_num][0]} -> {addresses[client_num][0]}")
                        try:
                            admin_conn.send("".encode('utf-8'))
                            continue
                        except:
                            cmd = "disconnect"
                            connections[admin_num] = 0
                            addresses[admin_num] = 0
                            break

                transfering = True
                if cmd == "":
                    pass

                if cmd == "disconnect":
                    disconnect = True
                    s.settimeout(None)
                    transfering = False
                    admin_conn = ""
                    client_conn = ""
                    continue

                # This if-elif-else statement processes custom keywords and forwards to client.
                if "file transfer " in cmd:

                    thread_p(f"==+== HEAVY ADMIN COMMAND ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {addresses[client_num][0]}\nCommand: File Transfer\nStatus: Starting")

                    client_conn.send(cmd.encode('utf-8'))

                    file_conns = []
                    file_addrs = []

                    try:

                        for host in host_list:
                            try:
                                f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                f.bind((host, TRANSFER PORT GOES HERE))
                            except:
                                continue
                        f.listen(2)

                    except Exception as e:
                        thread_p(f"==+== HEAVY COMMAND ERROR ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {addresses[client_num][0]}\nCommand: File Transfer\nException: {e}")
                        f.close()

                    for i in range(2):
                        conn_f, addr_f = f.accept()
                        file_conns.append(conn_f)
                        file_addrs.append(addr_f)

                    # auth_f is overwritten because both admin and client have
                    # to send a string for conn and this stops those strings
                    # from interfering with the file transfer protocol.
                    auth_f = file_conns[1].recv(32).decode('utf-8')
                    auth_f = file_conns[0].recv(32).decode('utf-8')

                    # defining which conn belongs to admin and vice-verse
                    if auth_f == "admin-client":
                        admin = file_conns[0]
                        client = file_conns[1]
                        admin_a = file_addrs[0]
                        client_a = file_addrs[1]
                    elif auth_f == "-client-":
                        client = file_conns[0]
                        admin = file_conns[1]
                        client_a = file_addrs[0]
                        admin_a = file_addrs[1]
                    else:
                        thread_p("Sockets Not Differenciated.")

                    # Forwarding the file byte length to client from admin

                    try:
                        data_len = admin.recv(64).decode('utf-8')
                        client.send(data_len.encode('utf-8'))

                    except Exception as e:
                        thread_p(f"==+== HEAVY COMMAND ERROR ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {addresses[client_num][0]}\nCommand: File Transfer\nException: {e}")
                        f.close()

                    time.sleep(1)

                    # Forwarding the bytes from admin to client
                    byte_string = []
                    data_len = int(data_len)
                    if data_len < 819200:
                        bytes = admin.recv(data_len)
                        byte_string.append(bytes)
                    else:
                        n = round(data_len / 40960)
                        if str(n) in str(data_len / 40960):
                            n += 1
                        for i in range(n):
                            bytes = admin.recv(40960)
                            byte_string.append(bytes)

                    load = b"".join(byte_string)
                    client.send(load)

                    filename = cmd.replace("file transfer ", "")

                    thread_p(f"==+== HEAVY ADMIN COMMAND ==+==\nSource IP: {admin_a}\nDestination IP: {client_a}\nCommand: File Transfer\nFilename: {filename}\nByte Length: {data_len}\nStatus: Success")

                    f.close()

                elif "file collect " in cmd:

                    thread_p(f"==+== HEAVY ADMIN COMMAND ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {addresses[client_num][0]}\nCommand: File Collect\nStatus: Starting")

                    client_conn.send(cmd.encode('utf-8'))

                    file_conns = []
                    file_addrs = []

                    try:

                        for host in host_list:
                            try:
                                f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                f.bind((host, TRANSFER PORT GOES HERE))
                            except:
                                continue
                        f.listen(2)

                    except Exception as e:
                        thread_p(f"==+== HEAVY COMMAND ERROR ==+==\nSource IP: {addresses[admin_n][0]}\nDestination IP: {addresses[client_num][0]}\nCommand: File Collect\nException: {e}")
                        f.close()

                    for i in range(2):
                        conn_f, addr_f = f.accept()
                        file_conns.append(conn_f)
                        file_addrs.append(addr_f)

                    # auth_f is overwritten because both admin and client have
                    # to send a string for conn and this stops those strings
                    # from interfering with the file transfer protocol.
                    auth_f = file_conns[1].recv(32).decode('utf-8')
                    auth_f = file_conns[0].recv(32).decode('utf-8')

                    # defining which conn belongs to admin and vice-verse
                    if auth_f == "admin-client":
                        admin = file_conns[0]
                        client = file_conns[1]
                        admin_a = file_addrs[0]
                        client_a = file_addrs[1]
                    elif auth_f == "-client-":
                        client_a = file_addrs[0]
                        admin_a = file_addrs[1]
                        client = file_conns[0]
                        admin = file_conns[1]
                    else:
                        thread_p("Sockets Not Differenciated.")

                    print(admin_a, client_a)

                    # Forwarding the file byte length to admin from client
                    try:
                        data_len = client.recv(64).decode('utf-8')
                        admin.send(data_len.encode('utf-8'))
                    except Exception as e:
                        thread_p(f"==+== HEAVY COMMAND ERROR ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {addresses[client_num][0]}\nCommand: File Collect\nException: {e}")
                        f.close()

                    time.sleep(1)

                    # Forwarding the bytes from client to admin
                    byte_string = []
                    if data_len != "":
                        data_len = int(data_len)
                        if data_len < 819200:
                            bytes = client.recv(data_len)
                            byte_string.append(bytes)
                        else:
                            n = round(data_len / 40960)
                            if str(n) in str(data_len / 40960):
                                n += 1
                            for i in range(n):
                                bytes = client.recv(40960)
                                byte_string.append(bytes)

                        load = b"".join(byte_string)
                        admin.send(load)

                    filename = cmd.replace("file collect ","")

                    if data_len != 0:
                        thread_p(f"==+== HEAVY ADMIN COMMAND ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {client_num}\nCommand: File Collect\nFilename: {filename}\nByte Length: {data_len}\nStatus: Success")
                    else:
                        thread_p(f"==+== HEAVY ADMIN COMMAND ==+==\nSource IP: {addresses[admin_num][0]}\nDestination IP: {client_num}\nCommand: File Collect\nFilename: {filename}\nByte Length: {data_len}\nStatus: Failed\nError Handled Successfully")
                    f.close()

                else:
                    client_conn.send(f"{cmd}".encode('utf-8'))
                    recievement = client_conn.recv(819200)
                    admin_conn.send(recievement)

            except BrokenPipeError:
                disconnect = True
                break



def monitor(n):
    while True:
        try:

            while True:
                if connections[n] != 0:
                    conn = connections[n]
                    break
            thread_p(f"===== Connection Established =====\nConnection: {addresses[n][0]}\nPort: {addresses[n][1]}")

            try:
                s.settimeout(5)
                data = conn.recv(64).decode('utf-8')
            except socket.timeout:
                thread_p(f"===== Connection Closed =====\nConnection: {addresses[n][0]}\nPort: {addresses[n][1]}\nReason: Unwanted Connection Recieved - Connection Timed Out")
                conn.close()
                connections[n] = 0
                addresses[n] = 0
                continue

            if data == "admin-client":
                s.settimeout(10)
                try:

                    conn.send("password:".encode('utf-8'))
                    password = conn.recv(64).decode('utf-8')
                    date = datetime.datetime.now()
                    local_time = date.time()

                    s.settimeout(None)

                    if password == str((local_time.minute + 348)/((3 + date.month)/date.day * 4)):
                        thread_p(f"===== Admin Authentication Succeeded =====\nRequest IP: {addresses[n][0]}\nPort: {addresses[n][1]}")
                        conn.send("Authentication Succeeded".encode('utf-8'))
                        admin(n)
                    else:
                        thread_p(f"===== Admin Authentication Failed =====\nRequest IP: {addresses[n][0]}\nPort: {addresses[n][1]}\nReason: Incorrect Password")
                        connections[n] = 0
                        addresses[n] = 0
                        conn.send("Authentication Failed".encode('utf-8'))
                        conn.close()



                except socket.timeout:
                    thread_p(f"===== Admin Request Closed =====\nConnection: {addresses[n][0]}\nPort: {addresses[n][1]}\nReason: Connection Timed Out - Password")
                    conn.close()
                    connections[n] = 0
                    addresses[n] = 0

            elif data == "-client-":
                s.settimeout(None)
                thread_p(f"===== Client Authentication Succeeded =====\nRequest IP: {addresses[n][0]}\nPort: {addresses[n][1]}")
                try:
                    while connections[n] != 0 and addresses[n] != 0:
                        if transfering == False:
                            conn.send("".encode('utf-8'))
                        else:
                            pass
                except:
                    thread_p(f"===== Client Connection Lost =====\nRequest IP: {addresses[n][0]}\nPort: {addresses[n][1]}")
                    connections[n] = 0
                    addresses[n] = 0

            else:
                s.settimeout(None)
                thread_p(f"===== Connection Closed =====\nConnection: {addresses[n][0]}\nPort: {addresses[n][1]}\nReason: Unwanted Connection Recieved - Incorrect Key")
                conn.close()
                connections[n] = 0
                addresses[n] = 0
            continue



        except BrokenPipeError:
            thread_p(f"===== Connection Lost =====\nConnection: {addresses[n][0]}\nPort: {addresses[n][1]}\nReason: Client Closed Connection.")
            connections[n] = 0
            addresses[n] = 0
            continue

        except Exception as e:
            print(f"Unexpected Error took place in thread {n}: {e}")


def check_time():

    date = datetime.datetime.now()
    time = date.time()
    min = time.minute

    thread_p(f"===== Program Started =====\nDate: {date.month}-{date.day}-{date.year}\nTime: {time.hour}:{time.minute}")

    while True:
        date = datetime.datetime.now()
        time = date.time()
        if time.minute % 10 == 0 and time.minute != int(min):
            min = time.minute
            hour = time.hour
            if len(str(min)) == 1:
                min = "0" + str(min)
            if len(str(hour)) == 1:
                hour = "0" + str(hour)
            thread_p(f"===== TIMESTAMP: =====\nDate: {date.month}-{date.day}-{date.year}\nTime: {hour}:{min}")

# Threading is done below

def create_workers():
    for _ in range(THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    x = queue.get()
    if x == -3:
        brain() # This is the main task that forwards data between clients
    if x == -2:
        check_time() # Prints TIMESTAMP every 10 minutes
    if x == -1:
        # Processes that set up the basis for the socket connections
        socket_create()
        socket_bind()
        accept_connections()
    if x >= 0:
        monitor(x) # Identifies conn as ADMIN, CLIENT or UNKNOWN
    queue.task_done()



def create_jobs():
    for x in range(-3, connections_allowed):
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
