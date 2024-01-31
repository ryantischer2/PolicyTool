# Copyright (c) 2024, AMD
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
# Author: Ryan Tischer ryan.tischer@amd.com

# Note Some of are untested with DSS PSM

import json
import requests

def get_web_call(url, session, *payload):

    if not payload:
        data = {}
    else:
        data = payload[0]
    try:
        api_ref = session.get(url, data=json.dumps(data))

    except requests.exceptions.Timeout:
        print('Network Timeout')

    except requests.exceptions.TooManyRedirects:
        print('too Many Redirects')

    except requests.exceptions.RequestException as err:
        print('Something went wrong')

        raise SystemExit(err)

    print (api_ref)
    return api_ref

def post_web_call(url, session, data):

    try:
        api_ref = session.post(url, data)

    except requests.exceptions.Timeout:
        print('Network Timeout')

    except requests.exceptions.TooManyRedirects:
        print('too Many Redirects')

    except requests.exceptions.RequestException as err:
        print('Something went wrong')

        raise SystemExit(err)

    return api_ref


def get_psm_workloads(psm_ip, session):

    url = psm_ip + 'configs/workload/v1/workloads'
    return get_web_call(url, session).json()

def get_psm_cluster(psm_ip, session):

    url = psm_ip +'configs/cluster/v1/cluster'
    return get_web_call(url, session).json()

def get_flow_export_policy(psm_ip, session):

    url = psm_ip + 'configs/monitoring/v1/flowExportPolicy'
    return get_web_call(url, session).json()

def get_dss(psm_ip, session):

    url = psm_ip + '/configs/cluster/v1/distributedserviceentities'
    dsc = get_web_call(url, session).json()

    return dsc

def get_config_snapshot(psm_ip, session):
    url = psm_ip + '/configs/cluster/v1/config-snapshot'
    return get_web_call(url, session).json()

def get_node1(psm_ip, session):
    url = psm_ip + '/configs/cluster/v1/nodes/node1'
    return get_web_call(url, session).json()

def get_networksecuritypolicy(psm_ip, session,):
    url = psm_ip + '/configs/security/v1/networksecuritypolicies'
    return get_web_call(url, session).json()

def get_Specificpolicy(psm_ip, session, policyName):
    url = psm_ip + '/configs/security/v1/networksecuritypolicies/' + policyName
    return get_web_call(url, session).json()

def get_users(psm_ip, session, tenant):
    url = psm_ip + '/configs/auth/v1/tenant/{t}/users'.format(t=tenant)
    return get_web_call(url, session).json()

def get_psm_metrics(psm_ip, session, psm_tenant, st, et):

    data = {
    "queries": [
        {
            "Kind": "Node",
            "start-time": st,
            "end-time": et
        }
    ]
}

    url = psm_ip + 'telemetry/v1/metrics'

    return get_web_call(url, session, data).json()



def get_dsc_metrics(psm_ip, session, psm_tenant, interface, st, et):

    data = {
    "queries": [
        {
            "Kind": "DistributedServiceCard",
            "selector": {
                "requirements": [
                    {
                        "key": "reporterID",
                        "operator": "equals",
                        "values": [interface]
                    }
                ]
            },
            "start-time": st,
            "end-time": et
        }
                ]
            }

    url = psm_ip + 'telemetry/v1/metrics'

    return get_web_call(url, session, data).json()


def get_uplink_metrics(psm_ip, session, psm_tenant, st, et):

    data = {
    "queries": [
        {
            "Kind": "MacMetrics",
            "start-time": st,
            "end-time": et
        }
                ]
            }

    url = psm_ip + 'telemetry/v1/metrics'

    return get_web_call(url, session, data).json()

def get_pf_metrics(psm_ip, session, psm_tenant, st, et):

    data = {
    "queries": [
        {
            "Kind": "LifMetrics",
            "start-time": st,
            "end-time": et
        }
                ]
            }

    url = psm_ip + 'telemetry/v1/metrics'

    return get_web_call(url, session, data).json()

def get_cluster_metrics(psm_ip, session, psm_tenant, st, et):

    data = {
    "queries": [
        {
            "Kind": "Cluster",
            "start-time": st,
            "end-time": et
        }
                ]
            }

    url = psm_ip + 'telemetry/v1/metrics'

    return get_web_call(url, session, data).json()

def get_fw_logs(psm_ip, session, psm_tenant, interface, st, et):
    connector = '_'
    extension = '.csv.gzip'

    #generate the log first
    url1 = '{psm}objstore/v1/tenant/{tenant}/fwlogs/objects?field-selector=' \
        'start-time={start},end-time={end},dsc-id={int},vrf-name={tenant}'.format \
        (psm=psm_ip, int=interface, tenant=psm_tenant, start=st, end=et)
    t = get_web_call(url1, session)


    #pull the download link from the log generation response
    link = str(t.json()['items'][0]['meta']['name'])
    formatLink = link.replace("/", "_")

    #craft download url and download the data
    url = '{psm}objstore/v1/downloads/tenant/default/fwlogs/{link}'.format(psm=psm_ip, link=formatLink)

    w = get_web_call(url, session)

    return w.content

def get_alerts(psm_ip, session, tenant):

    data = {
    "kind": "AlertPolicy",
    "api-version": "v1",
    "meta": {
        "name": "alertPolicy1",
        "tenant": tenant,
        "namespace": "default"
            }
            }

    url = psm_ip + 'configs/monitoring/v1/alerts'

    return get_web_call(url, session, data).json()




