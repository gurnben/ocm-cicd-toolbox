#!/bin/bash

python3 reporter.py md test/test_results_dir/ -o out.md --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.4 --hub-platform=aws --import-platform=aws --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -iu=www.mygitissue.com
# python3 reporter.py md test/test_results_dir/ -o out.md --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
#     --stage=TEST_STAGE --branch=TEST_BRANCH
