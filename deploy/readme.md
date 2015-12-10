This setup guide was ran on a clean ubuntu 14.04 LTS image. For best results,
use the same. You can use a VM, an existing machine, or any other method you're
comfortable with.

This setup guide refers to the AWS UI as it was in December 2015. For best
results, go back in time or interpret the instructions to the best of your
ability given the changes in the UI.

##Creating an AWS Account

[Sign up for an AWS account](https://aws.amazon.com/)
Fill out the requisite information, with a personal account and basic support plan.

When that is complete, [sign into the
console.](https://us-west-2.console.aws.amazon.com/console/home?region=us-west-2#). Then navigate to the [IAM console](https://console.aws.amazon.com/iam/home?#home). This will show the Security Status, which prompts you to take some actions to increase security. Do the first three: delete root access keys, activate MFA on the account, then begin to create an IAM user and follow the instructions in the next section.


##Creating an IAM user
IAM is the AWS service that gives different "Users" which have different permissions to use the AWS account. We need to make an User that we can use to build and deploy the server.

1. Navigate to the [IAM User
   view](https://console.aws.amazon.com/iam/home?#users)
2. Create a new user named "rank-deploy"
4. Save the access key id and secret access key for later
5. Click on the new rank-deploy user
6. Tab over to "Permissions"
7. Click "Attach Policy" and attach the "AdministratorAccess" policy.

##Configuration of your (ubuntu) machine

###AWS keys
Add the AWS IAM access key id and secret access key to your environment:

```
cat <<EOI >> ~/.bashrc
export AWS_ACCESS_KEY_ID=<your access key id here>
export AWS_SECRET_ACCESS_KEY=<your secret access key here>
EOI
source ~/.bashrc
```

###Update software
Update installed software and install requirements:

```
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git unzip python-dev python-pip postfix libpq-dev
```

###Clone the code

```
git clone https://github.com/Rdbaker/Rank.git ~/rank/
```

###Install python dependencies

```
sudo pip install -r ~/rank/requirements/dev.txt
```

###Install terraform and packer

Terraform is the tool we use to deploy the resources.

Find the 64bit linux download on [their downloads
page](https://terraform.io/downloads.html), copy the download link.

Then run:

```
sh ~/rank/deploy/install_helper.sh terraform <download link>
```

Packer is the tool we use to build machine images of the servers.

Find the 64bit linux download on [their downloads
page](http://www.packer.io/downloads.html), copy the download link.

Then run:

```
sh ~/rank/deploy/install_helper.sh packer <download link>
```

That script added terraform and packer to the PATH in `~/.bashrc`, so source it:

```
source ~/.bashrc
```

Finally verify that terraform and packer are installed:
```
terraform --version
packer --version
```

##Create the Hosted Zone

Since MyDomain.com manages the tmwild.com domain, we have to find out which Name
Servers to tell MyDomain should be able to create DNS recors for the domain.

```
cd ~/rank/deploy/hostedzone/
terraform apply
```

It will briefly output something like:

```
...
  hosted_zone_id = Z3365SB34A7V5E
  name_servers   = ns-107.awsdns-13.com,ns-1230.awsdns-25.org,ns-1798.awsdns-32.co.uk,ns-917.awsdns-50.net
```

Grab the hosted zone id and edit the file `~/rank/deploy/conf.sh`

```
# change this line:
export TF_VAR_hostedzoneid=""
# to (your hosted zone id):
export TF_VAR_hostedzoneid="Z3365SB34A7V5E"
```

Then take the list of name servers and go to MyDomain's DNS management and make
those name servers the authority on tmwild.com records.


##Set up the database

We need to spin up the database and configure/migrate it to be ready to be used
by the server.

###Deploy database

First we need to create a database password since we can't store that in git. Edit
the databse config file at `~/rank/deploy/conf.sh` and add a password to the line:

```
export PGPASSWORD=""
```

Then source that file so the environment variables are set for terraform to
read:

```
source ~/rank/deploy/conf.sh
```

Then use terraform to deploy a partially preconfigured AWS database:

```
cd ~/rank/deploy/db/
terraform apply
```

This may take about 10 minutes.  It will output the database host
name, something like:

```
PGHOST = rankdb.ckiwv8uixoq5.us-west-2.rds.amazonaws.com
```

Copy the host name, and paste it to the line in `~/rank/deploy/conf.sh`:

```
export PGHOST=
```

Then source that file so the environment variables are set for python to read:

```
source ~/rank/deploy/conf.sh
```


###Configure database
Next we migrate the database and initiate admin users.

Edit the file `~/rank/.admin.yml` to set the username and password to something
you'll remember. This corresponds to the credentials for the first admin.

Then run these commands:

```
cd ~/rank/
python manage.py db upgrade
python manage.py seed_database
```


##Build the server image

Packer will create an AWS server instance, configure it to act as a rank server,
then kill the instance but save a machine image. Do this by running:

```
cd ~/rank/
packer build deploy/build/packer.json
```

It will take maybe 5 minutes to build the machine image. When it is done it will
output something like:

```
...
--> amazon-ebs: AMIs were created:

us-west-2: ami-f7bba696
```

Take the ami id (ami-f7bba696 in this case) and edit the file
`~/rank/deploy/conf.sh`

```
# change this line:
export TF_VAR_amiid=""
# to (your ami id):
export TF_VAR_amiid="ami-f7bba696"
```


##Deploy Server+

Just as we used terraform to deploy the database, we will use it to deploy the
server (and load balancer, auto-scale groups, etc...).

The only other thing we need the vpc-id for the VPC that was created by AWS by default.
Find the id
[here](https://us-west-2.console.aws.amazon.com/vpc/home?region=us-west-2#vpcs:).


Grab the vpc id and edit the file `~/rank/deploy/conf.sh`

```
# change this line:
export TF_VAR_vpcid=""
# to (your vpc id):
export TF_VAR_vpcid="vpc-e4182e81"
```

```
source ~/rank/deploy/conf.sh
cd ~/rank/deploy/
terraform apply
```

DONE, it may take a minute or so for the DNS record for tmwild to catch up, but
then everything should be set up.
