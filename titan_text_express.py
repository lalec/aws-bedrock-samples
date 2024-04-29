import json
import boto3
import botocore
import subprocess

def get_profile_session(profile, retry=True):
    try:
        print('info: get session for profile: {0}'.format(profile))
        session = boto3.session.Session(profile_name=profile)
        sts = session.client('sts')
        try:
            identity = sts.get_caller_identity()
            print(f"info: authorized role: {identity['Arn']}")
            return session
        except (botocore.exceptions.SSOTokenLoadError, botocore.exceptions.UnauthorizedSSOTokenError):          
            if retry:
                subprocess.run(['aws','sso', 'login', '--profile', profile])
                return get_profile_session(profile, False)
            else:
                raise
    except botocore.exceptions.ProfileNotFound as e:
        print('error: profile: {0} does not exist in configured profiles'.format(profile))
        print('error: check your aws configuration under: C:\\Users\\<user_name>\\.aws\\config')
        exit(1) 

# https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html
model_id = 'amazon.titan-text-express-v1'

# Define the API request body. Input/prompts and configuration depends on the model
body = {
    "inputText": "User: Meeting transcript: \nMiguel: Hi Brant, I want to discuss the workstream  for our new product launch \nBrant: Sure Miguel, is there anything in particular you want to discuss? \nMiguel: Yes, I want to talk about how users enter into the product. \nBrant: Ok, in that case let me add in Namita. \nNamita: Hey everyone \nBrant: Hi Namita, Miguel wants to discuss how users enter into the product. \nMiguel: its too complicated and we should remove friction.  for example, why do I need to fill out additional forms?  I also find it difficult to find where to access the product when I first land on the landing page. \nBrant: I would also add that I think there are too many steps. \nNamita: Ok, I can work on the landing page to make the product more discoverable but brant can you work on the additonal forms? \nBrant: Yes but I would need to work with James from another team as he needs to unblock the sign up workflow.  Miguel can you document any other concerns so that I can discuss with James only once? \nMiguel: Sure. \nFrom the meeting transcript above, Create a list of action items for each person.",
    "textGenerationConfig": {
        "temperature": 0,  
        "topP": 1,
        "maxTokenCount": 512,
        "stopSequences": ["User:"]
    }
}

profile = '<profile_name>'
session = get_profile_session(profile)

client = session.client('bedrock-runtime', region_name='eu-west-3')

try:
  response = client.invoke_model(
      modelId=model_id,
      contentType="application/json",
      accept="*/*",     
      body=json.dumps(body)
  )
  # Parse the response body and inspect the different outputs and completions
  payload = json.loads(response['body'].read())
  for result in payload['results']:
    print('completionReason: {}, tokenCount: {}'.format(result['completionReason'], result['tokenCount'])) 
    print('outputText: {}'.format(result['outputText'])) 

except Exception as error:
  if isinstance(error, botocore.exceptions.ClientError):
    print('Client error: {}: {}'.format(error.response['Error']['Code'], error.response['Error']['Message']))
  else:
    print(f"Unexpected error: {error}")
else:
    print(f"Finished generating text with model: {model_id}.")  
