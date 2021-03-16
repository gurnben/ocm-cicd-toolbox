#!/bin/bash

echo "------------IMPORT CLUSTER DETAILS (IMPORT PLATFORM AND VERSION IGNORED)------------"
python3 reporter.py js 219500322/ -o out.json --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --hub-platform=aws --import-platform=gcp --import-version=4.6.8 --import-cluster-details-file=test/test_import_cluster_details.json --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -iu=www.mygitissue.com