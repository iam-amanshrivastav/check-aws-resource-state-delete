## Here, I have covered how to get the instances which are currently present in your aws account.
## It'll provide the output of instances which are present in aws account like instance (id, state, type, public and private ip address).

import boto3

def list_ec2_instances():
    ec2 = boto3.client("ec2")

    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running", "stopped"]}]
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append({
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "InstanceType": instance["InstanceType"],
                "PublicIP": instance.get("PublicIpAddress", "N/A"),
                "PrivateIP": instance["PrivateIpAddress"]
            })

    return instances

if __name__ == "__main__":
    ec2_instances = list_ec2_instances()
    if ec2_instances:
        for instance in ec2_instances:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']}, Type: {instance['InstanceType']}, Public IP: {instance['PublicIP']}, Private IP: {instance['PrivateIP']}")
    else:
        print("No running or stopped instances found.")
