Overview:

template.yml: cloudformation template

cfn_lambda.py: lambda python code

resources/buildLambda.sh: shell script to build lambda zip file and upload to s3


**Workflow:**

1. resources/buildLambda.sh
    any time the lambda contents need to be updated
    
2. aws cloudformation deploy --stack-name nttdata --template-file template.yml --capabilities CAPABILITY_NAMED_IAM --parameter- overrides TimeZone=America/Boise
    deploy stack
    specify the timezone from here: http://worldtimeapi.org/api/timezone
    
3. aws cloudformation delete-stack --stack-name nttdata
    destroy stack
    
4. aws cloudformation describe-stacks --stack-name nttdata
    get stack info
    
    
Techinical overview:

1. cloudformation:**
    Resources
      GetTimeInfo lambda function
      GetTimeInfoRole role for lambda function
      Custom resource to interact with lambda and customer
  Outputs
    Time zone, current information
    Unix time, current information
  Parameters
    Time zone, full string
2. cloudformation passes information to lambda by setting an environment variable in the lambda function
