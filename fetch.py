#Michael Barnes


import boto3
import yaml



keypair = "server"

ec2 = boto3.client('ec2')
response = ec2.delete_key_pair(KeyName=keypair)
ec2.delete_key_pair(KeyName=keypair)


ec2 = boto3.resource('ec2')


# create key pair to log into instance
response = ec2.create_key_pair(KeyName=keypair)
with open('./' + keypair + '.pem', 'w') as file:
    file.write(response.key_material)


# read in yaml file with  ec2 instance information

with open("awsyaml2.yml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Read successful")


# extract data from yaml file isolate information
instance = ((data['server']['instance_type']))
ami = (data['server']['ami_type'])
low = (data['server']['min_count'])
high = (data['server']['min_count'])


# VOLUME CREATION
numofvolumes = 0
teststr = (data['server']['volumes'])
numofvolumes = len(teststr)


# user data informatio is ran during instance launch
userdata = '''#!/bin/bash
sudo adduser user1
sudo mkdir /home/user1/.ssh
sudo chmod 700 /home/user1/.ssh
sudo touch  /home/user1/.ssh/authorized_keys
sudo chmod 600  /home/user1/.ssh/authorized_keys
cat /home/ec2-user/.ssh/authorized_keys > /home/user1/.ssh/authorized_keys
sudo chown -R user1:user1 /home/user1/.ssh/
sudo adduser user2
sudo mkdir /home/user2/.ssh
sudo chmod 700 /home/user2/.ssh
sudo touch  /home/user2/.ssh/authorized_keys
sudo chmod 600  /home/user2/.ssh/authorized_keys
cat /home/ec2-user/.ssh/authorized_keys > /home/user2/.ssh/authorized_keys
sudo chown -R user2:user2 /home/user2/.ssh/
sudo yum install xfsprogs -y
sudo mkfs -t xfs /dev/xvdf
sudo mkdir /data
sudo mount /dev/xvdf /data'''


# Extract volume information
counter = 0
for x in range(numofvolumes):

    b = (teststr[counter])


    device = (str(b['device']))

    newdevice =(device[counter])


    gbsize = (str(b['size_gb']))
    voltype = (str(b['type']))
    mount = (str(b['mount']))
    newlist = [device, gbsize, voltype, mount]


    counter += 1
    newsize = int(gbsize)

    f = open("drives.txt", "a")
    f.write(device + ',' + gbsize + "\n")
    f.close()


f = open("drives.txt", "r")
lines = f.readlines()[-2:]
f.close()
split1 = lines[0].strip().split(' ')
split2 = lines[1].strip().split(' ')


driveb = str(split2).split(",")
mountb = str(driveb[0]).strip('[')
sizeb = str(driveb[1]).strip('[')
print(mountb[1:10])
print(sizeb[0:3])

intsizeb = int(sizeb[0:3])
strmountb = str(mountb[1:10])


# create ec2 instance with parameters
instnces = ec2.create_instances(
        InstanceType=instance,
        ImageId=ami,
        MinCount=low,
        MaxCount=high,
        UserData=userdata,
        KeyName=keypair,
        BlockDeviceMappings=[{

            "DeviceName": strmountb,
            "Ebs": {"VolumeSize": intsizeb}
             }

        ]
    )


