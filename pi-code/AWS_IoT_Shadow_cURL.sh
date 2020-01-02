# curl --tlsv1.2 \
# # --cacert root-CA.crt \
# # --cert 4b7828d2e5-certificate.pem.crt \
# --key 4b7828d2e5-private.pem.key \
# -X POST \
# -d "{ \"message\": \"Hello, world\" }" \
# "https://a1pn10j0v8htvw.iot.us-east-1.amazonaws.com:8443/topics/my/topic"

base_dir=/Users/moose/Documents/IoT-stuff/AWS/test-pi/client
#echo "base dir: $base_dir"

curl --tlsv1.2 \
--cacert $base_dir/AmazonRootCA1.pem \
--cert $base_dir/b3e88e24a4-certificate.pem.crt \
--key $base_dir/b3e88e24a4-private.pem.key \
-X POST \
-d "{\"request\": \"temperature\"}" \
"https://a2vbde4oiektna-ats.iot.us-east-2.amazonaws.com:8443/topics/SmartThermalController-Test/request?qos=1"

echo "The following is an attempt to get from a topic.  It doesn't work at this time."

curl --tlsv1.2 \
--cacert $base_dir/AmazonRootCA1.pem \
--cert $base_dir/b3e88e24a4-certificate.pem.crt \
--key $base_dir/b3e88e24a4-private.pem.key \
"https://a2vbde4oiektna-ats.iot.us-east-2.amazonaws.com:8443/things/SmartThermalController-Test/shadow"
