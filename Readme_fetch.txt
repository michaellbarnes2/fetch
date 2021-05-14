1. You will need to have acess to an aws account and create an aws acess key
2. Log into AWS and open IAM.
3. Once IAM is open click add user
	-> Provide a user name and click programatic acess
	-> click next permissions select AmazonEC2FullAccess
	-> click next -> click review -> click create user
	-> donwload the csv file.

4. Ensure aws cli is installed and configured.
Install and config document:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html




1. For server acess download putty and putty gen
2. open putty gen click load and locate the server.pem key
3. click  save private key and save as server.ppk.

4. open putty under category click ssh click Auth and on the righ hand side navigate to 
the key create in step 4
5. click open
6. enter the user name ec2-user, user1 or user2