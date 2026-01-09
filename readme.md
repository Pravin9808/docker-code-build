Option 1: Lambda triggered by CodeBuild EventBridge rule
Event Pattern (EventBridge)
{
  "source": ["aws.codebuild"],
  "detail-type": ["CodeBuild Build State Change"],
  "detail": {
    "build-status": ["FAILED"]
  }
}

Lambda (Python) – Fail on Build Failure
def lambda_handler(event, context):
    build_status = event["detail"]["build-status"]
    build_id = event["detail"]["build-id"]

    if build_status == "FAILED":
        raise Exception(f"Build failed: {build_id}")

    return {
        "statusCode": 200,
        "body": "Build succeeded"
    }


✅ Raising an exception fails the Lambda
✅ EventBridge + Lambda failure can:

Stop downstream automation

Trigger alerts (SNS, Slack, etc.)

Option 2: Lambda used inside CodePipeline (Most Common)
Lambda triggered as a CodePipeline action
Lambda (Python)
import boto3

codepipeline = boto3.client("codepipeline")

def lambda_handler(event, context):
    job_id = event["CodePipeline.job"]["id"]

    try:
        # Example validation logic
        build_status = event["CodePipeline.job"]["data"]["actionConfiguration"]["configuration"].get("BuildStatus")

        if build_status == "FAILED":
            raise Exception("Build failed")

        codepipeline.put_job_success_result(jobId=job_id)

    except Exception as e:
        codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                "type": "JobFailed",
                "message": str(e)
            }
        )
