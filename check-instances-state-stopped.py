## Check the instance state which are stopped in your accont and get the output of those instaces ID's.
## We ( Devops Engineer ) always we get the client request to check the instances which are in stopped state and provide them the instance id's.

import boto3
def lambda_handler(event, context): # Create an EC2 client ec2 = boto3.client('ec2')

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
