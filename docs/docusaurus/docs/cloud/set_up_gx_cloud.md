---
sidebar_label: 'Set up GX Cloud'
title: 'Set up GX Cloud'
description: Set up GX Cloud.
---

To get the most out of GX Cloud, you'll need to request a GX Cloud Beta account, generate and record access tokens, set environment variables, and then install and start the GX Agent.

Currently, the GX Cloud user interface is configured for Snowflake. If you don't have a Snowflake Data Source, you won't be able to connect to Data Assets, create Expectation Suites and Expectations, run Validations, or create Checkpoints. 

If you're using Snowflake and are ready to create Expectations and run Validations, see [Quickstart for GX Cloud and Snowflake](/docs/cloud/quickstarts/snowflake_quickstart).

## Request a GX Cloud Beta account

1. Go to the GX Cloud Beta [sign-up page](https://greatexpectations.io/cloud).

2. Complete the sign-up form and then click **Submit**.

3. If you're invited to view a GX Cloud demonstration, click **Schedule a time to connect here** in the confirmation email to schedule a time to meet with a Great Expectations (GX) representative. After your meeting you'll be sent an email invitation to join your GX Cloud organization.

4. In your GX Cloud email invitation, click **click here** to set your password and sign in.

5. Enter your email address and password, and then click **Continue to GX Cloud**. Alternatively, click **Log in with Google** and use your Google credentials to access GX Cloud.


## Prepare your environment

1. Download and install Python. See [Active Python Releases](https://www.python.org/downloads/).

2. Download and install pip. See the [pip documentation](https://pip.pypa.io/en/stable/cli/pip/).

3. Download and install Docker. See [Get Docker](https://docs.docker.com/get-docker/).

## Get your user access token and organization ID

You'll need your user access token and organization ID to set your environment variables. Don't commit your access tokens to your version control software.

1. In GX Cloud, click **Settings** > **Tokens**.

2. In the **User access tokens** pane, click **Create user access token**.

3. Complete the following fields:

    - **Token name** - Enter a name for the token that will help you quickly identify it.

    - **Role** - Select **Admin**. For more information about the available roles, click **Information** (?) .

4. Click **Create**.

5. Copy and then paste the user access token into a temporary file. The token can't be retrieved after you close the dialog.

6. Click **Close**.

7. Copy the value in the **Organization ID** field into the temporary file with your user access token and then save the file. 

    GX recommends deleting the temporary file after you set the environment variables.

## Set the environment variables and start the GX Agent

Environment variables securely store your GX Cloud access credentials. The GX Agent runs open source GX code in GX Cloud, and it allows you to securely access your data without connecting to it or interacting with it directly. 

Currently, the GX Cloud user interface is configured for Snowflake and this procedure assumes you have a Snowflake Data Source. If you don't have a Snowflake Data Source, you won't be able to connect to Data Assets, create Expectation Suites and Expectations, run Validations, or create Checkpoints. 

1. Start the Docker Engine.

2. Run the following code to set the `GX_CLOUD_ACCESS_TOKEN` and `GX_CLOUD_ORGANIZATION_ID` environment variables, install GX Cloud and its dependencies, and start the GX Agent:

    ```bash title="Terminal input"
    docker run --rm --pull=always -e GX_CLOUD_ACCESS_TOKEN="<user_access_token>" -e GX_CLOUD_ORGANIZATION_ID="<organization_id>" greatexpectations/agent
    ```      
    Replace `user_access_token` and `organization_id` with the values you copied previously.

3. Optional. To use GX Cloud in Python scripts, save your `GX_CLOUD_ACCESS_TOKEN` and `GX_CLOUD_ORGANIZATION_ID` as environment variables outside the Docker Engine by entering `export ENV_VAR_NAME=env_var_value` in the terminal or adding the commands to your `~/.bashrc` or `~/.zshrc` file. For example:

    ```bash title="Terminal input"
    export GX_CLOUD_ACCESS_TOKEN=<user_access_token>
    export GX_CLOUD_ORGANIZATION_ID=<organization_id>
    ```
4. Optional. If you created a temporary file to record your user access token and Organization ID, delete it.

5. Optional. Run `docker ps` or open Docker Desktop to confirm the agent is running.

    If you stop the GX Agent, close the terminal, and open a new terminal you'll need to set the environment variables again.

    To edit an environment variable, stop the GX Agent, edit the environment variable, save the change, and then restart the GX Agent.

## Next steps

 - [Create a Data Asset](/docs/cloud/data_assets/manage_data_assets#create-a-data-asset)