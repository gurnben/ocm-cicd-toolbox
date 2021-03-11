#!/bin/bash

python3 reporter.py sl test/test_results_dir/ -o slack-message.json --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.4 --hub-platform=aws --import-platform=aws --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdownurl.com -iu=www.mygitissue.com
# python3 reporter.py sl test/squad-tests-min/ -o slack-message.json --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
#     --hub-platform=aws --import-platform=aws -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH
curl -X POST -H 'Content-type: application/json' --data @slack-message.json $SLACK_URL