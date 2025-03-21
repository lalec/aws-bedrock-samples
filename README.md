# aws-bedrock-samples

This guide focuses on Windows but the only difference compared to macOS and Linux are the paths.

## Configure AWS CLI

(If you haven't installed the AWS CLI already: `https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html` and complete initial configuration)

1. Open the AWS CLI config file located in folder: `C:\Users\<USERPROFILE>\.aws\config`
2. Create a profile for the AWS account with an alias `[profile <profile_name>]` and the required parameters below:

```
[profile <profile_name>]
sso_start_url = https://weforum.awsapps.com/start
sso_region = eu-west-1
sso_account_id = <12DigitAccountNr>
sso_role_name = <RoleNameAlreayProvided>
region = eu-west-1
output = json
```

## Run Python Script

1. Clone the [anthropic_claude_3_5_sonnet.py](anthropic_claude_3_5_sonnet.py), [titan_text_express.py](titan_text_express.py) or [mixtral_8x7b.py](mixtral_8x7b.py) sample files and open in your favourite IDE, preferibly one with a console attached, like VSCode.
2. Replace `<profile_name>` in the code with the profile you speficied in the AWS Config.

```
profile = '<profile_name>'
session = get_profile_session(profile)
```

3. Run [anthropic_claude_3_5_sonnet.py](anthropic_claude_3_5_sonnet.py),[titan_text_express.py](titan_text_express.py) or [mixtral_8x7b.py](mixtral_8x7b.py) in the IDE and the browser will open a new tab where you need to authorize the code you specified above to use your AWS sign-in

![aws-sso](https://user-images.githubusercontent.com/22824001/223488357-d512cea5-a1c6-4d65-b9e6-972c665d3c7c.PNG)

4. Click Allow and the code will continue executing with your credentials

5. The bedrock-runtime API will be executed and your model invoked.

## Region and Model Availability

While `eu-west-1` is our preferred region, model access can vary between AWS regions. We currently have the following models enabled in specific regions:

| Region         | Model                         |
|----------------|-------------------------------|
| eu-west-1      | Claude 3.5 Sonnet             |
| eu-west-3      | Claude 3.5 Sonnet             |
| eu-west-3      | Titan Text G1 - Lite          |
| eu-west-3      | Titan Text G1 - Express       |
| eu-west-3      | Mistral 7B Instruct           |
| eu-west-3      | Mistral 8x7B Instruct         |

To use a different region, simply change the `region_name` parameter in the client configuration for each code example.

# Note on Cloud Models

For cloud models, you'll also need to adjust the `modelId` when changing regions. This is because these models utilize cross-region inference.

Example:
```
client = boto3.client('bedrock-runtime', region_name='eu-west-1')
```