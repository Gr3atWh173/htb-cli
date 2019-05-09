HTB_CLI - Interact with HTB through a terminal.
Copyleft: Gr3atWh173

based upon https://github.com/kulinacs/htb

SETUP:
1. get your API key from HackTheBox (profile settings)
2. set the HTB_API_KEY environment variable to your api key

USAGE:
LIST MACHINES:          python hackthebox.py list machines [active/retired]
GET A SPECIFIC MACHINE: python hackthebox.py get machine (machine id)
SWITCH VPN:             python hackthebox.py switch (lab)
SUBMIT FLAG:            python hackthebox.py submit (root/user) (mid) (hash) (difficulty [10-100])
