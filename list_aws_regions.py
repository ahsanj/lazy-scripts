import boto
import boto.ec2
from boto.ec2.regioninfo import RegionInfo
count = 0
regions = boto.ec2.regions()
for aws_region in regions:
    count +=1
    region = str(aws_region)
    print count,":",region[11:]
