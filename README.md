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
region = eu-west-3
output = json
```

## Run Python Script

1. Clone the [titan_text_express.py](titan_text_express.py) and/or [mixtral_8x7b.py](mixtral_8x7b.py) sample files and open in your favourite IDE, preferibly one with a console attached, like VSCode.
2. Replace `<profile_name>` with the profile you speficied in the AWS Config.

```
profile = '<profile_name>'
session = get_profile_session(profile)
```

3. Run [titan_text_express.py](titan_text_express.py) or [mixtral_8x7b.py](mixtral_8x7b.py) in the IDE and the browser will open a new tab where you need to authorize the code you specified above to use your AWS sign-in

![aws-sso](https://user-images.githubusercontent.com/22824001/223488357-d512cea5-a1c6-4d65-b9e6-972c665d3c7c.PNG)

4. Click Allow and the code will continue executing with your credentials

5. The bedrock-runtime API will be executed and your model invoked.
