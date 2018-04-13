#!/bin/sh
url=http://$1:6188/ws/v1/timeline/metrics
while [ 1 ]
do
millon_time=$(( $(date +%s%N) / 1000000 ))
random=`expr $RANDOM % 10`
json="{
 \"metrics\": [
 {
 \"metricname\": \"$2\",
 \"appid\": \"$3\",
 \"hostname\": \"single\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${random}
 }
 }
 ]
}"
  
echo $json |tee -a /root/my_metric.log
curl -i -X POST -H "Content-Type: application/json" -d "${json}" ${url}
sleep 5
done
