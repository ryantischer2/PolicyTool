# Copyright (c) 2020, Pensando Systems
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# Author: Ryan Tischer - ryan@pensando.io

import keyring
import getpass
import json

#Run this program first or anytime the username/password changes

print ("Init program for pypen Python Library.")
print ("This init program securly stores Pensando PSM connection details in OS keyring services ")
print ("tenant and PSM IP address are stored in clear text")
print ("---------------------------------------------------------")
psm_temp_ip = input("Enter PSM IP address, for example 10.29.75.21: = ")
psm_ip = f"https://{psm_temp_ip}/"

psm_tenant = input("Enter PSM tenant, for example default:  ")
psm_admin = input("Enter PSM admin account: ")
print ("---------------------------------------------------------")
print ("")
print ("Data Entered is ")
print (f"IP address = {psm_ip}")
print (f"Tenant = {psm_tenant}")
print (f"Username = {psm_admin}")
print ("password is a secert")
print ("---------------------------------------------------------")

if input("Is this correct y/n: " ) == "y" or "Y" or "yes" or "Yes":
    keyring.set_password('penando', psm_admin, getpass.getpass("Enter PSM Password: "))
    data = {"ip":psm_ip, "tenant":psm_tenant}
    with open('pypen_init_data.json', 'w') as outfile:
        json.dump(data, outfile)
else:
    exit()
