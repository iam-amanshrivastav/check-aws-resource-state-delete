## Here I have convered how to get the stale resources( unattached Volumes and Snapshots ) which are on your aws accounts. 
## This will help you to get idea of stale resoures and identifying those resources which are increasing cost unnessarily for your account.
## This will show you the volumes and snapshots which are not attached to any of the EC2 instances

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
