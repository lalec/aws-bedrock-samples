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
        print('error: check your aws configuration under: C:\\Users\\<user_name>\\.aws\\config or ~/.aws/config')
        exit(1) 

# https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html
model_id='arn:aws:bedrock:eu-west-1:867352477168:inference-profile/eu.anthropic.claude-3-5-sonnet-20240620-v1:0'

prompt = """<transcript> Miguel: Hi Brant, I want to discuss the workstream  for our new product launch 
            Brant: Sure Miguel, is there anything in particular you want to discuss? 
            Miguel: Yes, I want to talk about how users enter into the product. 
            Brant: Ok, in that case let me add in Namita. 
            Namita: Hey everyone 
            Brant: Hi Namita, Miguel wants to discuss how users enter into the product. 
            Miguel: its too complicated and we should remove friction.  for example, why do I need to fill out additional forms?  I also find it difficult to find where to access the product when I first land on the landing page.
            Brant: I would also add that I think there are too many steps. 
            Namita: Ok, I can work on the landing page to make the product more discoverable but brant can you work on the additonal forms? 
            Brant: Yes but I would need to work with James from another team as he needs to unblock the sign up workflow.  Miguel can you document any other concerns so that I can discuss with James only once?
            Miguel: Sure. 
            From the meeting transcript above, Create a list of action items for each person.</transcript>
            """

# Define the API request body. Input/prompts and configuration depends on the model
body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 500,
    "temperature": 0.5,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          }
        ]
      }
    ]
  }

profile = '<profile_name>'
session = get_profile_session(profile)

client = session.client('bedrock-runtime', region_name='eu-west-1')

try:
  response = client.invoke_model(
      modelId=model_id,
      contentType="application/json",
      accept="application/json",     
      body=json.dumps(body)
  )
  # Parse the response body and print the text inside the content
  model_response = json.loads(response['body'].read())
  response_text = model_response["content"][0]["text"]
  print(response_text)

except Exception as error:
  if isinstance(error, botocore.exceptions.ClientError):
    print('Client error: {}: {}'.format(error.response['Error']['Code'], error.response['Error']['Message']))
  else:
    print(f"Unexpected error: {error}")
else:
  print(f"Finished generating text with model: {model_id}.")
