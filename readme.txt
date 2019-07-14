HTB_CLI - Interact with HTB through a terminal.
Copyleft: Gr3atWh173
based upon https://github.com/kulinacs/htb

INSTALL: pip install htb_cli

SETUP:
1. get your API key from HackTheBox (profile settings)
2. set the HTB_API_KEY environment variable to your api key

USAGE:
LIST MACHINES:          hackthebox.py list machines [active/retired]
GET A SPECIFIC MACHINE: hackthebox.py get machine (machine id)
SWITCH VPN:             hackthebox.py switch (lab)
SUBMIT FLAG:            hackthebox.py submit (root/user) (mid) (hash) (difficulty [10-100])
