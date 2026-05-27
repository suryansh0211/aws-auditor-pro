import boto3

print("=" * 50)
print("AWS AUDITOR PRO REPORT")
print("=" * 50)

# -------------------------
# AWS Clients
# -------------------------

ec2 = boto3.client(
    "ec2",
    region_name="ap-south-1"
)

s3 = boto3.client("s3")

# -------------------------
# EC2 ANALYSIS
# -------------------------

response = ec2.describe_instances()

running = 0
stopped = 0

instance_details = []

for reservation in response["Reservations"]:

    for instance in reservation["Instances"]:

        state = instance["State"]["Name"]

        instance_id = instance["InstanceId"]

        instance_name = "No Name"

        if "Tags" in instance:

            for tag in instance["Tags"]:

                if tag["Key"] == "Name":

                    instance_name = tag["Value"]

        instance_details.append(
            {
                "id": instance_id,
                "name": instance_name,
                "state": state
            }
        )

        if state == "running":
            running += 1

        elif state == "stopped":
            stopped += 1

print("\nEC2 SUMMARY")
print("-" * 20)

print("Running:", running)
print("Stopped:", stopped)

print("\nEC2 DETAILS")

for item in instance_details:

    print(
        f"Name: {item['name']}"
    )

    print(
        f"ID: {item['id']}"
    )

    print(
        f"State: {item['state']}"
    )

    print("-" * 20)

# -------------------------
# EBS ANALYSIS
# -------------------------

volumes_response = ec2.describe_volumes()

volumes = volumes_response["Volumes"]

total_volumes = len(volumes)

unattached_volumes = 0

for volume in volumes:

    if len(volume["Attachments"]) == 0:

        unattached_volumes += 1

print("\nEBS SUMMARY")
print("-" * 20)

print("Total Volumes:", total_volumes)

print(
    "Unattached Volumes:",
    unattached_volumes
)

# -------------------------
# S3 ANALYSIS
# -------------------------

buckets = s3.list_buckets()["Buckets"]

print("\nS3 SUMMARY")
print("-" * 20)

print("Total Buckets:", len(buckets))

for bucket in buckets:

    bucket_name = bucket["Name"]

    print("Bucket:", bucket_name)

# -------------------------
# FINDINGS
# -------------------------

print("\nFINDINGS")
print("-" * 20)

if stopped > 0:

    print(
        f"{stopped} stopped EC2 instance(s) found."
    )

    print(
        "Review whether these servers are still required."
    )

else:

    print(
        "No stopped EC2 instances found."
    )

if unattached_volumes > 0:

    print(
        f"{unattached_volumes} unattached volume(s) found."
    )

    print(
        "These may generate unnecessary storage costs."
    )

else:

    print(
        "No unattached volumes found."
    )

if len(buckets) == 0:

    print(
        "No S3 buckets detected."
    )

# -------------------------
# ESTIMATED SAVINGS
# -------------------------

estimated_savings = 0

estimated_savings += stopped * 5

estimated_savings += unattached_volumes * 1

print("\nESTIMATED SAVINGS")
print("-" * 20)

print(
    f"Potential Monthly Savings: ${estimated_savings}"
)

# -------------------------
# FINAL RECOMMENDATIONS
# -------------------------

print("\nRECOMMENDATIONS")
print("-" * 20)

print(
    "1. Review stopped EC2 instances."
)

print(
    "2. Remove unused storage volumes after backup."
)

print(
    "3. Verify S3 buckets are still actively used."
)

print("\nEND OF REPORT")