# Discord BOT Infrastructure

AWS Cloud has been used to deploy the bot. With the help of github actions CI/CD has been
achieved.

All the infrastructure setup has been done using AWS Cloudformation.

Following are the files and their short description:

1. **VPC-setup.yml** -> Used to setup the VPC, which includes 2 public subnets routing table association and IAM role creation.

2. **ECS-cluster.yml** -> Setting up the cluster

3. **EC2-setup.yml** -> Creates AWS EC2 on-demand instance.

4. **ECS-service.yml** -> Setting up the service and task definitions for the bot using ECS
(Elastic Container Services)




