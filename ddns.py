#coding:utf-8

import dns.resolver
import json, jsonpath
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest

#替换以下参数
ID="************"
Secret="********************"
RegionId="cn-hangzhou"

client = AcsClient(ID,Secret,RegionId)

def dns_des(RecordId):
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(RecordId)
    response = client.do_action_with_exception(request)
    data = json.loads(response)
    data = json.dumps(data, sort_keys=True, indent=2)
    #print(data)

def dns_del(DomainName, RR):
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(DomainName)
    request.set_RRKeyWord(RR)
    response = client.do_action_with_exception(request)
    data = json.loads(response)
    for record in data["DomainRecords"]["Record"]:
        if RR == record["RR"]:
            RecordId = record["RecordId"]
            print("WARNING: Delete the existing records: %s" % record["Value"])
            dns_des(RecordId)
            request = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
            request.set_RecordId(RecordId)
            response = client.do_action_with_exception(request)

def dns_add(DomainName, RR, Type, Value):
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_DomainName(DomainName)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)
    data = json.loads(response)
    print("INFO: Record adding success")
    RecordId = (data['RecordId'])
    dns_des(RecordId)

def GetIpFromDomain(domain):
    result = []
    A = dns.resolver.query(domain, 'A')
    for i in A.response.answer:
        for j in i.items:
            result.append(j.address)
    return result

def lambda_handler(event, context):
    RR = "@"
    Type = "A"
    domain = os.environ["domain"]
    albdomain = os.environ["alb"]
    
    dns_del(domain, RR)
    loadblancer = albdomain
    values = GetIpFromDomain(loadblancer)
    for value in values:
        #print(value)
        dns_add(domain, RR, Type, value)

