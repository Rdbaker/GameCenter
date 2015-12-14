#Destruction
If you'd like to destroy all the resources, start up the instance that you
stopped, the one you first used to set up and [deploy](readme.md) the service.
[It should be listed
here.](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:instanceState=stopped;sort=instanceState)
Start it by selected the correct instance, then click Actions > Instance State > Start.
It will take maybe a minute to start up again. Then ssh into it.


Destroy the server, load balancer, etc:

```
cd ~/rank/deploy
source ~/rank/conf.sh
terraform destroy #type 'yes' when it prompts you
```

Destroy the hosted zone:

```
cd ~/rank/deploy/hostedzone/
terraform destroy #type 'yes' when it prompts you
```

Destroy the database:

```
cd ~/rank/deploy/db/
terraform destroy #type 'yes' when it prompts you
```

If those were all successful, then everything should be gone. Check the [billing
page](https://console.aws.amazon.com/billing/home?region=us-west-2#/) for a full
detail of the account usage.

#Inspection/debugging

If you need to inspect a running server, find it's IP address in the [EC2
dashboard](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2),
then run

```
ssh -i ~/.ssh/rank_key_pair.pem ubunutu@<ip address>
```

(this assumes the ssh key you created from the [deploy
stage](readme.md#create-a-ubuntu-server) is in the directory `~/.ssh/`)
