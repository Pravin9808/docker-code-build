import boto3

codepipeline = boto3.client("codepipeline")
####

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
