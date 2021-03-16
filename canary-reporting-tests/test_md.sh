#!/bin/bash

echo "------------STANDARD------------"
python3 reporter.py md test/test_results_dir/ -o out_1.md --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.4 --hub-platform=aws --import-platform=aws --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -iu=www.mygitissue.com
echo "------------IMPORT CLUSTER LIST------------"
python3 reporter.py md test/test_results_dir/ -o out_2.md --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --hub-platform=aws --import-cluster-details-file=test/test_import_cluster_details.json --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -iu=www.mygitissue.com
