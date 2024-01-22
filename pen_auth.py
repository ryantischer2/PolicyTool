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
# Author: Ryan Tischer ryan@pensando.io


import requests
import json
import pen_auth, pen

#get rid of insecure warnings -
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def psm_login (psm_ip, username, password, tenant):

    auth_data = {
        "username": username,
        "password": password,
        "tenant": tenant
    }
    data_to_send = json.dumps(auth_data).encode("utf-8")

    #Create session for PSM

    session = requests.Session()
    session.verify = False

    #working
    URL = psm_ip + 'v1/login'

    auth = session.post(URL, data_to_send)

    return session

#static PSM vars.  Uncomment to use

PSM_IP = 'https://10.29.75.21/'
PSM_TENANT = 'default'
PSM_USERNAME = "admin"
PSM_PASSWD = 'admin'


session = pen_auth.psm_login(PSM_IP, PSM_USERNAME, PSM_PASSWD, PSM_TENANT)
#session is used to authenicate future API calls to PSM.

# Get PSM security policies 
print(pen.get_networksecuritypolicy(PSM_IP, session))