aws ec2 run-instances --image-id ami-abcd1234 --count 1 --instance-type t2.2xlarge \
--key-name key --subnet-id subnet-ce8911ef --security-group-ids sg-0f39f828b810c7bb0 \
--user-data file://python_configure.txt --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=feat_extract1}],ResourceType=volume,Tags=[{Key=Name,Value=feat_extract1-disk1}]'
