#/bin/bash

echo "#####################"
echo "# Summary"
echo "#####################"

echo "# of mail events:"; cat ../output/mail_logs.json | wc -l
echo "# of accepted email objects"; cat ../output/mail_logs.json | grep -i accepted | wc -l
echo "# of email objects:"; ls -l ../output/emails/ | grep -v total | wc -l
echo "# of outbound web events:"; cat ../output/outbound_proxy_traffic.txt | wc -l
echo -e "\n"

echo "#####################"
echo "# Answers"
echo "#####################"
echo -e "\n"

EMAIL_ADDR=$(cat ../output/prompt.txt | grep -oE 'from (.+)\.' | cut -d " " -f 2 | cut -d \. -f -2)

echo "Here are all the users that were sent an email from $EMAIL_ADDR"
cat ../output/mail_logs.json | grep $EMAIL_ADDR | jq -rc '[.recipient, .result] | join("~")' | sort -u | tabulate -s "~" 

echo -e "\n"
echo "These are the employees that actually received the email from $EMAIL_ADDR"
cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -rc '[.recipient, .result] | join("~")' | sort -u | tabulate -s "~" 

echo -e "\n"
echo "Here are all the malicious links in emails from $EMAIL_ADDR"
for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u

echo -e "\n"
echo "The users that clicked on a link containing the malicious domain are:"
#grep -i -f <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u | cut -d \/ -f 3 | sed 's/www\.//g') ../output/outbound_proxy_traffic.txt | cut -d ' ' -f 4 | sort -u
grep -f <(grep -f  <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | cut -d \/ -f 3 | sort -u | sed 's/www\.//g') ../output/outbound_proxy_traffic.txt | cut -d " " -f 4 | sort -u) <(cat ../output/employees.json | jq -c .[])  | jq -r .name


echo -e "\n"
echo "Here are the other email senders that sent links containing these domains:"
for email in $(grep -irlf <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u | cut -d \/ -f 3 | sed 's/www\.//g')  ../output/emails/); do cat $email; done | grep -i "from\:" | cut -d ' ' -f 2 | sort -u | grep -v $EMAIL_ADDR 

echo -e "\n"
echo "Recipients of emails from new senders"
cat  ../output/mail_logs.json | grep -v $EMAIL_ADDR | grep -if <(for email in $(grep -irlf <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u | cut -d \/ -f 3 | sed 's/www\.//g')  ../output/emails/); do cat $email; done | grep -i "from\:" | cut -d ' ' -f 2 | sort -u) | jq -r '[.sender, .recipient, .result] | join("~")' | sort -t "~" -k3 | tabulate -s "~"

echo -e "\n"
echo "Additional Domains:"
for i in $(cat ../output/mail_logs.json | grep -i -f <(for email in $(grep -irlf <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u | cut -d \/ -f 3 | sed 's/www\.//g')  ../output/emails/); do cat $email; done | grep -i "from\:" | cut -d ' ' -f 2 | sort -u) | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u



echo -e "\n"
echo "Here are the IPs associated with these domains:"
grep -i -f <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | sort -u | cut -d \/ -f 3 | sed 's/www\.//g') ../output/outbound_proxy_traffic.txt | cut -d ' ' -f 5-7 | sort -u

#grep -f  <(for i in $(cat ../output/mail_logs.json | grep $EMAIL_ADDR | grep -i accepted | jq -r .filename); do cat ../output/emails/$i; done  | grep \/ | cut -d \/ -f 3 | sort -u) ../output/outbound_proxy_traffic.txt | cut -d " " -f 5,7 | sort -u

