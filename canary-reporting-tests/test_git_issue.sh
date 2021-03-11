#!/bin/bash

echo "------------STANDARD------------"
python3 reporter.py gh test/test_results_dir/ -o out.github --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.9 --hub-platform=aws --import-platform=gcp --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdown.com -mg www.must-gather.com -ru www.results-bucket.com --repo "cicd-staging" -t "blocker (P0)" -t "canary-failure" \
    -t "Severity 1 - Urgent" -t "bug"
echo "------------INVALID REPO------------"
python3 reporter.py gh test/test_results_dir/ -o out.github --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.9 --hub-platform=aws --import-platform=gcp --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdown.com -mg www.must-gather.com -ru www.results-bucket.com --repo "a-super-secret-totally-invalid-repo-007" -t "blocker (P0)" -t "canary-failure" \
    -t "Severity 1 - Urgent" -t "bug" 
echo "------------INVALID ORG------------"
python3 reporter.py gh test/test_results_dir/ -o out.github --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.9 --hub-platform=aws --import-platform=gcp --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdown.com -mg www.must-gather.com -ru www.results-bucket.com --repo "a-super-secret-totally-invalid-org-007" -t "blocker (P0)" -t "canary-failure" \
    -t "Severity 1 - Urgent" -t "bug" 
echo "------------INVALID TAG------------"
python3 reporter.py gh test/test_results_dir/ -o out.github --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.9 --hub-platform=aws --import-platform=gcp --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdown.com -mg www.must-gather.com -ru www.results-bucket.com --repo "cicd-staging" -t "blocker (P0)" -t "canary-failure" \
    -t "Severity 1 - Urgent" -t "an-invalid-tag" --repo "cicd-staging"
echo "------------DRY RUN------------"
python3 reporter.py gh test/test_results_dir/ -o out.github --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.9 --hub-platform=aws --import-platform=gcp --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdown.com -mg www.must-gather.com -ru www.results-bucket.com --dry-run --repo "cicd-staging"
echo "------------DRY RUN WITH TAGS------------"
python3 reporter.py gh test/test_results_dir/ -o out.github --ignore-list=test/ignorelist.json -eg=100 -pg=100 --snapshot=TEST_SNAPSHOT\
    --hub-version=4.6.4 --import-version=4.6.9 --hub-platform=aws --import-platform=gcp --job-url=www.test-url.com -id=BUILD_ID --stage=TEST_STAGE --branch=TEST_BRANCH \
    -sd=www.myshapshotdiffurl.com -md=www.mymarkdown.com -mg www.must-gather.com -ru www.results-bucket.com --dry-run -t "blocker (P0)" -t "canary-failure" \
    -t "Severity 1 - Urgent" -t "bug" --repo "cicd-staging"
