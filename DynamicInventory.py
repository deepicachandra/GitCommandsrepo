#!/bin/python
# Shebang Line Should Point Python Installation Path
"""
Author Mithun Technologies
Fetech List of Servers from AWS and group based on EC2
instance tag name and value.
"""
import pprint
import boto3
import json


def getgroupofhosts(ec2):
    allgroups = {}

    for each_in in ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):
        for tag in each_in.tags:
            if tag["Key"] in allgroups:
                hosts = allgroups.get(tag["Key"])
                hosts.append(each_in.public_ip_address)
                allgroups[tag["Key"]] = hosts
            else:
                hosts = [each_in.public_ip_address]
                allgroups[tag["Key"]] = hosts

            if tag["Value"] in allgroups:
                hosts = allgroups.get(tag["Value"])
                hosts.append(each_in.public_ip_address)
                allgroups[tag["Value"]] = hosts
            else:
                hosts = [each_in.public_ip_address]
                allgroups[tag["Value"]] = hosts

    return allgroups


def main():
    ec2 = boto3.resource("ec2",region_name='us-west-2',
    aws_access_key_id='AKIATAZMLDHUXLLK7VG6', 
    aws_secret_access_key='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')
    all_groups = getgroupofhosts(ec2)
    inventory = {}
    for key, value in all_groups.items():
        hostsobj = {'hosts': value}
        inventory[key] = hostsobj
    print(json.dumps(inventory))


if __name__ == "__main__":
    main()