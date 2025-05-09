## Here I have covered how to delete the unattached/stale resources like volumes & snapshots. which are increasing the cost of your aws account.
## This code will check the volumes and snapshots which are not attached to any of the ec2 instances and it'll delete those resources.
## Delete Orphaned Volumes and Snapshots

import boto3

def lambda_handler(event, context): ec2 = boto3.client('ec2')

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
