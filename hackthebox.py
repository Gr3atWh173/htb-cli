#!/usr/bin/env python3
# Gr3atWh173 (github.com/gr3atwh173)
from sys import argv, exit
from os import environ
from htb import HTB
from prettytable import PrettyTable

try:
    htb = HTB(environ["HTB_API_KEY"])
except:
    print("Setup the HTB_API_KEY first!")
    exit(1)

def print_machine(argv):
    global htb
    mid = int(argv.pop())
    machine = htb.get_machine(mid)

    for key, value in machine.items():
        if key == "avatar" or key == "avatar_thumb":
            continue
        print(key.upper() + ": ", end="")
        if type(value) is dict:
            print()
            for k, v in value.items():
                print("\t" + k.upper() + ": " + str(v))
        else:
            print(str(value))

def print_machines(argv):
    global htb

    if len(argv) == 0:
        argv.append("all")
    
    machines = htb.get_machines()
    t = PrettyTable(['ID', 'Name', 'OS', 'Points', 'Maker'])
    
    fltr = argv.pop()
    for machine in machines:
        if fltr == "retired" and (machine.get("retired_date") != None):
            t.add_row([machine["id"], machine["name"], machine["os"], machine["points"], machine["maker"]["name"]])
        elif fltr == "active" and (machine.get("retired_date") == None):
            t.add_row([machine["id"], machine["name"], machine["os"], machine["points"], machine["maker"]["name"]])
        elif fltr == "all":
            t.add_row([machine["id"], machine["name"], machine["os"], machine["points"], machine["maker"]["name"]])

    print(t)
    
def print_usage():
    print("USAGE:")
    print("LIST MACHINES:          python hackthebox.py list machines [active/retired]")
    print("GET A SPECIFIC MACHINE: python hackthebox.py get machine (machine id)")
    print("SWITCH VPN:             python hackthebox.py switch (lab)")
    print("SUBMIT FLAG:            python hackthebox.py submit (root/user) (mid) (hash) (difficulty[10-100])")

def ls(argv):
    global htb
    t = argv.pop()
    if t == "machines":
        print_machines(argv)
    elif t == "vpns":
        print("eufree, usfree, euvip, usvip")
    else:
        print(t + ": I can't list that")

def get(argv):
    global htb
    t = argv.pop()
    if t == "machine":
        print_machine(argv)

def switch_vpn(argv):
    global htb
    htb.switch_vpn(argv.pop())

def submit_flag(argv):
    diff, flag, mid, lvl = argv
    diff = int(diff)
    mid = int(mid)
    if diff not in range(10, 100):
        print("Difficulty should be between 10 and 100")
        return
    elif lvl not in ["root", "user"]:
        print("Flag type should be root or user")
        return
    if lvl == "root":
        a = htb.own_machine_root(mid, flag, diff)
    else:
        a = htb.own_machine_user(mid, flag, diff)
    if not a:
        print("Submit failed!")
    
def main():
    if len(argv) < 2:
        print("type 'hackthebox.py usage' for usage")
        exit()
        
    argv.reverse()
    argv.pop()

    t = argv.pop()
    if t == "list":
        ls(argv)
    elif t == "get":
        get(argv)
    elif t == "switch":
        switch_vpn(argv)
    elif t == "usage":
        print_usage()
        exit()
    elif t == "submit":
        submit_flag(argv)
    else:
        print("I don't understand")
        exit()

main()


