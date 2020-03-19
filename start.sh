#/bin/bash

echo "Running modules....."
python run_modules.py
sleep 5
echo "Making malware....."
./malware/make_malware.sh

zip "cyber_challenge.zip" output
