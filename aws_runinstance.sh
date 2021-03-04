#!/bin/sh
bucket="b_03"
count=$(aws s3 ls s3://uob-miniproject/$bucket/json/ | wc -l)
echo $count

for((i=1;i<=$count;i=i+10));

do
end=$[ $i + 10 ]

sed 's/$1/'$i'/g' ./user_data/python_configure.txt|sed 's/$2/'$end'/g'|sed 's/$3/'$bucket'/g' > ./user_data/python_configure_${i}_${end}.txt
user_data=./user_data/python_configure_${i}_${end}.txt
echo "node $i data execuate from day $i to day $end"
echo $user_data

aws ec2 run-instances --image-id ami-0915bcb5fa77e4892  --count 1 --instance-type t2.2xlarge \
--key-name key --subnet-id subnet-ce8911ef --security-group-ids sg-0f39f828b810c7bb0 \
--user-data file://$user_data --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=feat_extract_from$i}]" \
"ResourceType=volume,Tags=[{Key=Name,Value=feat_extract1-disk-$i}]" --iam-instance-profile "Arn=arn:aws:iam::292935198470:instance-profile/admin" --region us-east-1
done

