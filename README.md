# Don't Mock Me

## LocalStack vs Native unit testing

### Premise

Often in serverless development, there is a focus on local execution for tests. The premise of this repository and the [companion blog post](), is to show that testing directly against AWS is generally lower TCO than using LocalStack or equivalents.

The repository shows that from a code ownership and complexity perspective when running the test suite they are approximately the same.

## Prerequisites

1. Python v3.9 installed
2. Pipenv installed
3. Terraform installed
4. An AWS account
   1. The resources created _should_ not exceed the free tier for DynamoDB

### Running Native Tests

1. Run `pipenv install --dev` to install all the required python packages
2. Run `pipenv shell` to activate the python virtual environment
3. Assume an AWS role in your current terminal session

#### With Fresh Infrastructure (Expected CI Usage)

1. Run `pytest native_tests`

#### To Run With Persistent Infrastructure (Expected Local Usage)

1. Run `export ENVIRONMENT=local`
2. Run `cd native_tests && terraform init && terraform apply -auto-approve && cd ..` to create the infrastructure
   1. This is only required on the first test run
3. Run `pytest native_tests`

##### End of Work Clean Up

1. Run `cd native_tests && terraform destroy -auto-approve && cd ..` to tear down the infrastructure

### To Run LocalStack Tests

1. Run `pipenv install --dev` to install all the required python packages
2. Run `pipenv shell` to activate the python virtual environment
3. Run `docker run -d --name localstack --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack`

#### With Fresh Infrastructure (Expected CI Usage)

1. Run `pytest localstack_tests`

#### To Run With Persistent Infrastructure (Expected Local Usage)

1. Run `export ENVIRONMENT=local`
2. Run `cd native_tests && terraform init && terraform apply -auto-approve && cd ..` to create the infrastructure
   1. This is only required on the first test run
3. Run `pytest localstack_tests`

##### End of Work Clean Up

1. Run `docker kill localstack` to kill the running container
