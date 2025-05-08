# check-aws-resource-state-delete
This will check aws account help you on many this like 


This script checks the state of instances in your AWS account and outputs the IDs of instances that are stopped.

import boto3

def lambda_handler(event, context):
    # Create an EC2 client
    ec2 = boto3.client('ec2')
    
    # Describe instances
    response = ec2.describe_instances()
    
    # List to hold instance IDs
    instance_ids = []
    
    # Iterate over reservations and instances
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Check the state of the instance
            state = instance['State']['Name']
            # Add instance ID to the list if the instance is stopped
            if state == 'stopped':
                instance_ids.append(instance['InstanceId'])
    
    # Return the list of instance IDs
    return {
        'statusCode': 200,
        'body': instance_ids
    }


Check Orphaned Volumes and Snapshots

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get all volumes
    volumes_response = ec2.describe_volumes()
    # Get all snapshots
    snapshots_response = ec2.describe_snapshots(OwnerIds=['self'])
    
    # Lists to hold orphaned volumes and snapshots
    orphaned_volumes = []
    orphaned_snapshots = []
    
    # Check for orphaned volumes (volumes not attached to any instance)
    for volume in volumes_response['Volumes']:
        if not volume['Attachments']:
            orphaned_volumes.append(volume['VolumeId'])
    
    # Get all volume IDs to check against snapshots
    volume_ids = {volume['VolumeId'] for volume in volumes_response['Volumes']}
    
    # Check for orphaned snapshots (snapshots without a corresponding volume)
    for snapshot in snapshots_response['Snapshots']:
        if snapshot['VolumeId'] not in volume_ids:
            orphaned_snapshots.append(snapshot['SnapshotId'])
    
    # Return the list of orphaned volumes and snapshots
    return {
        'statusCode': 200,
        'body': {
            'orphaned_volumes': orphaned_volumes,
            'orphaned_snapshots': orphaned_snapshots
        }
    }

Delete Orphaned Volumes and Snapshots

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get all volumes
    volumes_response = ec2.describe_volumes()
    # Get all snapshots
    snapshots_response = ec2.describe_snapshots(OwnerIds=['self'])
    
    # Lists to hold orphaned volumes and snapshots
    orphaned_volumes = []
    orphaned_snapshots = []
    
    # Check for orphaned volumes (volumes not attached to any instance)
    for volume in volumes_response['Volumes']:
        if not volume['Attachments']:
            orphaned_volumes.append({
                'VolumeId': volume['VolumeId'],
                'VolumeName': next((tag['Value'] for tag in volume.get('Tags', []) if tag['Key'] == 'Name'), 'No Name')
            })
    
    # Get all volume IDs to check against snapshots
    volume_ids = {volume['VolumeId'] for volume in volumes_response['Volumes']}
    
    # Check for orphaned snapshots (snapshots without a corresponding volume)
    for snapshot in snapshots_response['Snapshots']:
        if snapshot['VolumeId'] not in volume_ids:
            orphaned_snapshots.append({
                'SnapshotId': snapshot['SnapshotId'],
                'SnapshotName': next((tag['Value'] for tag in snapshot.get('Tags', []) if tag['Key'] == 'Name'), 'No Name')
            })
    
    # Delete orphaned volumes
    for volume in orphaned_volumes:
        ec2.delete_volume(VolumeId=volume['VolumeId'])
    
    # Delete orphaned snapshots
    for snapshot in orphaned_snapshots:
        ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
    
    # Return the list of deleted volumes and snapshots
    return {
        'statusCode': 200,
        'body': {
            'deleted_volumes': orphaned_volumes,
            'deleted_snapshots': orphaned_snapshots
        }
    }
