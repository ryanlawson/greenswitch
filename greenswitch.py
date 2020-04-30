from datetime import datetime
import boto3
import os

client = boto3.client('ec2')

def get_instances(instance_list, turn_on):
    response = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': instance_list}])
    instances = response['Reservations'][0]['Instances']
    ids = []
    for i in instances:
        instance_id = i['InstanceId']
        instance_is_running = i['State']['Name'] == 'running'
        if turn_on:
            if instance_is_running:
                print(f'Instance {instance_id} is already running')
            else:
                ids.append(instance_id)
        else:
            if instance_is_running:
                ids.append(instance_id)
            else:
                print(f'Instance {instance_id} is already stopped')
    print(f'Instances: {str(ids)}')
    return ids

def turn_on_instances(ids):
    response = client.start_instances(InstanceIds=ids)
    print(f'Start Instance Response: {str(response)}')

def turn_off_instances(ids):
    response = client.stop_instances(InstanceIds=ids)
    print(f'Stop Instance Response: {str(response)}')

def handler(event, context):
    if 'InstanceNames' not in event:
        print('Key InstanceNames must be in Lambda input.')
        return
    instance_list = event['InstanceNames'].split(',')
    print(f'Instance List: {instance_list}')
    if len(instance_list) <= 0:
        print('No instances listed in InstanceNames.')
        return
    if 'Action' not in event:
        print('Key Action must be in Lambda input.')
        return
    action = event['Action']
    print(f'Action: {action}')
    if action not in ['ON', 'OFF']:
        print('Action must be ON or OFF.')
    turn_on = action == 'ON'
    instances = get_instances(instance_list, turn_on)
    if len(instances) <= 0:
        print('No instances meet the Action criteria.')
        return
    if turn_on:
        turn_on_instances(instances)
    else:
        turn_off_instances(instances)
