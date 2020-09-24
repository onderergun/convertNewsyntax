import csv
from jsonrpclib import Server
import ssl
from getpass import getpass
import argparse

ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser()
parser.add_argument('--username', required=True)
parser.add_argument('--inventoryname', required=True)


args = parser.parse_args()
switchuser = args.username
inventory = args.inventoryname
switchpass = getpass()

with open(inventory) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for iter,row in enumerate(csv_reader):
        if iter == 0 :
            for num,column in enumerate(row):
                if column == "IP Address" or column == "IPAddress":
                    hostIndex=num
        else:
            ssh_host=row[hostIndex]
            print ssh_host
            hostname=row[0]
            print hostname
            mgmtIP=row[5]
            urlString = "https://{}:{}@{}/command-api".format(switchuser, switchpass, ssh_host)
            switchReq = Server(urlString)
            response = switchReq.runCmds( 1, [{"cmd": "enable", "input": ""},{ "cmd": "configure convert new-syntax", "input": "y" }],"text" )
            print response