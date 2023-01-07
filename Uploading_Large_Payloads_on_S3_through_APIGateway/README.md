
# Uploading large Payload on S3 bucket AWS CDk Python Project

## Project Description:
This project uses the `AWS CDK` in Python to create an S3 bucket, an API Gateway REST API with a POST method, and two Lambda functions. The first Lambda function generates a `presigned URL` for the client to use to upload a file to S3, while the second Lambda function sends an `SES notification` to the user once the file has been uploaded. The S3 bucket is configured to trigger the second Lambda function whenever a new object is created. The project can be tested by using the POST method to request a presigned URL and then uploading a file to S3, and can be deployed to AWS once it is complete.

## Architecture Diagram:

<div align="center">
   <div align="center">
    <img src="Architecture_Diagram/Uploading Large Payloads on S3 ArchitectureDiagram.jpg" width='700'/>
  </div>
</div>
</br>


The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.



To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
