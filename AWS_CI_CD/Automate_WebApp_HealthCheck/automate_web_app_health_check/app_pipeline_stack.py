from aws_cdk import (
    Stack,
    pipelines as pipelines_,
    SecretValue as secret_,
    aws_codepipeline_actions as codepipeline_actions_,    
)

from automate_web_app_health_check.app_pipeline_stage import AppPipelineStage
from constructs import Construct


class AppPipelineStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines.html
       
        # Access the GitHub repository
        source = pipelines_.CodePipelineSource.git_hub("ahmedtariq01/AWS_Projects", "main",
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/SecretValue.html#aws_cdk.core.SecretValue
                                                       authentication=secret_.secrets_manager("My-Token", json_field="Key-name"),
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codepipeline_actions/GitHubTrigger.html#aws_cdk.aws_codepipeline_actions.GitHubTrigger
                                                       trigger=codepipeline_actions_.GitHubTrigger('POLL')
                                                       )
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
        # Add shell step to synthesized the code
        synth = pipelines_.ShellStep("Synth", input=source,
                                     
                                     commands=['cd AWS_CI_CD/Automate_WebApp_HealthCheck/',
                                               'npm install -g aws-cdk',
                                               "pip install -r requirements.txt",
                                               'cdk synth'
                                               ],
                                     primary_output_directory="AWS_CI_CD/Automate_WebApp_HealthCheck/cdk.out",
                                     
                                     )
        # create pipeline
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        pipeline = pipelines_.CodePipeline(self, "Pipeline",
                                           synth=synth
                                           )
        
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        # beta testing stage for pipeline
        beta_testing_stage = AppPipelineStage(self, "Beta")
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/AddStageOpts.html
        # adding beta testing stage to pipeline
        pipeline.add_stage(beta_testing_stage, pre =[
                                pipelines_.ShellStep("Synth", input=source, 
                                commands=[  'cd AWS_CI_CD/Automate_WebApp_HealthCheck/',
                                            'npm install -g aws-cdk',
                                            "pip install -r requirements.txt",
                                            "pip install -r requirements-dev.txt",
                                            'pytest'],
                                # primary_output_directory="AWS_CI_CD/Automate_WebApp_HealthCheck/cdk.out",
                                )
                            ]
                        )
        

       
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        # prod stage for pipeline
        prod_stage = AppPipelineStage(self, "Prod")
        
        # adding prod stage to pipeline and manual Approval Step
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/AddStageOpts.html
        pipeline.add_stage(prod_stage, pre =[
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ManualApprovalStep.html
        
            pipelines_.ManualApprovalStep("ApproveProd")
                                ]
                    )
                                              
                                                       
    