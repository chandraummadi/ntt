#!/bin/bash

rm -rf package
mkdir package
cd package
pip3 install charset-normalizer requests -t .

cp ../lambda_function.py .
zip -r9 lambda_function.zip *

aws s3 mb s3://gettimeinfolambda
aws s3 cp lambda_function.zip s3://gettimeinfolambda/
