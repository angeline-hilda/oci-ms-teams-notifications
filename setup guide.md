# Setup Instructions for OCI Notifications with Microsoft Teams
## Step 1: Create Dynamic Group

Dynamic groups allow you to group OCI compute instances as “principal” actors (similar to user groups). In this step, we will create a Dynamic Group for the functions that will interact with the notification system.
> **Note**: You must have Administrator privileges to create dynamic groups.
1. Sign in to the OCI tenancy.
2. From the services menu, select **Identity & Security -> Dynamic Groups**.
3. Click **Create Dynamic Group**.
4. Enter a meaningful Name and Description.
5. In Rule 1, use the following rule to target the function resource:
   
   ```plaintext
   ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1', instance.compartment.id = 'ocid1.compartment.XXXXX'}
This rule grants access to all functions within the specified compartment.

## Step 2: Create Dynamic Group OCI IAM Policy

To enable the function to interact with necessary OCI services (like compute, networking, object storage, etc.), we will create a policy that grants permissions to the Dynamic Group.

1. In the OCI console, go to **Identity & Security -> Identity ->Policies**.
2. Click **Create Policy**.
3. Enter a suitable **Name** and **Description**, and select the appropriate **Compartment**.
4. Enable the **Show manual editor** option to write custom policies. 
5. Copy and paste the following policy statements adjusting the <dynamic_group_name> and <compartment_name_path> placeholders with your values:

   ```plaintext
   # Core permissions for function access to instances and network resources
   Allow dynamic-group <dynamic_group_name>/<domain> to read instances in compartment <compartment_name_path>
   Allow dynamic-group <dynamic_group_name>/<domain> to read vnics in compartment <compartment_name_path>
   Allow dynamic-group <dynamic_group_name>/<domain> to read vnic-attachments in compartment <compartment_name_path>
   Allow dynamic-group <dynamic_group_name>/<domain> to use virtual-network-family in compartment <compartment_name_path>

   # Permissions for accessing object storage and logging resources
   Allow dynamic-group <dynamic_group_name>/<domain> to read objectstorage-namespaces in compartment <compartment_name_path>
   Allow dynamic-group <dynamic_group_name>/<domain> to manage logging-family in compartment <compartment_name_path>

   # Permissions for using APM domains and accessing repositories for function container images
   Allow service faas to use apm-domains in compartment <compartment_name_path>
   Allow service faas to read repos in compartment <compartment_name_path> where request.operation='ListContainerImageSignatures'

   # Permissions for using keys and vaults for secure data handling
   Allow dynamic-group <dynamic_group_name>/<domain> to read vaults in compartment <compartment_name_path>
   Allow dynamic-group <dynamic_group_name>/<domain> to use keys in compartment <compartment_name_path>
   Allow service faas to {KEY_READ} in compartment <compartment_name_path> where request.operation='GetKeyVersion'
   Allow service faas to {KEY_VERIFY} in compartment <compartment_name_path> where request.operation='Verify'

   # Permission to manage function resources in the compartment
   Allow dynamic-group <dynamic_group_name>/<domain> to manage functions-family in compartment <compartment_name_path>

  ## Step 3: Create a Repository to Store the Custom OCI Function
Oracle Container Registry (OCIR) is used to store container images securely. This step involves creating a repository to store the custom OCI function image.

1. In the OCI console, Go to **Developer services -> Containers -> Container Registry -> Create Repository**.
2. In the **Create Repository** dialog box:
   - **Compartment**: Select the compartment where you want to store the repository.
   - **Repository Name**: Enter a name for your repository.
   - **Visibility**: Set the repository as **Private** to maintain security.
3. Click **Create Repository**. Your repository should now be created successfully. 


> **Note**: The repository must remain private for security reasons unless there's a specific need for public access.
## Step 4: Create a VCN with Subnet for the Function Application

A Virtual Cloud Network (VCN) allows you to manage networking resources within OCI. For this tutorial, we will create a VCN and subnet for hosting the function application.

> **Note**: If you already have an existing VCN and subnet, you can skip this step.
1. In the OCI Console, Go to **Networking -> Virtual Cloud Network -> Create VCN**.
2. In the **Create VCN** dialog box:
   - **Name**: Enter a descriptive name for your VCN.
   - **Compartment**: Choose the compartment where you want to create the VCN.
   - **VCN Configuration**: You can select **Create VCN with Internet Connectivity** or **Custom** based on your requirements.
   - **CIDR Block**: Specify the CIDR block for your VCN (e.g., `10.0.0.0/16`).
4. Click **Create VCN**.
5. After creating the VCN, you will need to create a **Subnet** within this VCN:
   - Select **Subnets** under your newly created VCN.
   - Click **Create Subnet**.
   - Enter a **Name** and **CIDR Block** for your subnet (e.g., `10.0.1.0/24`).
   - **Availability Domain**: Choose an availability domain or leave it as **Regional** if you want the subnet to span across multiple availability domains.
   - **Subnet Access**: Choose **Public** or **Private** based on your needs.
6. Click **Create Subnet**, and your subnet should be created successfully.
   
## Step 5: Create an Application to Store the Functions
An application in OCI serves as a container for deploying and managing functions. 

1. In OCI Console, Go to **Developer Services -> Functions -> Applications -> Create Application**.
2. In the **Create Application** window:
   - **Name**: Enter a name for the application, such as `fun-app`.
   - **VCN**: Select the VCN and the Public subnet created earlier. 
3. Click **Create**, and your function application should be created successfully.

## Step 6: Deploy the Function

We will now deploy the function code to OCI using the OCI Functions platform. This will leverage the code mentioned in the pre-requisite.

1. Launch the **Cloud Shell** from the OCI console. 
2. Upload the function code 
3. 'func.py' file contains the following key functions:
     - `parse_message`: Processes the incoming event data and foramts it for Microsoft Teams.
     - `make_post`: Sends the notification as an Adaptive card to the Microsoft TeamsL.
     - `handler`: The entry point for the function, responsible for handling the request, parsing the data, and invoking `parse_message`.

4. Use the following commands to deploy the function:

     ```bash
     fn -v deploy --app <app-name>
     fn -v deploy --app fun-app
     ```
This will build the function’s Docker image, push it to the repository, and deploy it to OCI Functions.

## Step 7: Subscribe the Function to a Topic

To trigger the function upon receiving events, we must subscribe the function to a notification topic.

1. In the OCI console, go to **Developer Services -> Application Integration -> Notifications**.
   
2. Click **Create Topic**, enter an appropriate name for the topic, and click **Create***.

3. After the topic is created, find and select it from the list of topics.

4. On the topic’s details page, under **Resources**, click **Subscriptions -> Create Subscription**.

5. In the **Create Subscription** window, set the following:
   - **Protocol**: Choose **Functions**.
   - **Compartment**: Select the compartment where the function is located.
   - **Application**: Choose the application created in **Step 5**.
   - **Function**: Select the function deployed in **Step 6**.
6. Click **Create** to finalize the subscription.<br/>

<img width="800" alt="subscription" src="https://github.com/user-attachments/assets/9fe8be3c-0800-4a0b-8eb1-e1aa5980b92e">

## Step 8: Create an Instance and the Notification Event Rule

To validate the function, we’ll create a compute instance and associate it with the event notification rule.

1. In the OCI console, go to **Compute ->Instances -> create instance**

2. Provide the required details:
   - Instance Name, Compartment, Availability Domain
   - Select the VCN and Public Subnet
   - Copy-paste the SSH public key
   - Click **Create** and wait for the instance to become running. 

3. Log into the instance using SSH:
   ```bash
   ssh opc@<public ip> -i <private key>
4. In Instance Details page, go to the **Notification** tab, create a notification event.

5. Select a **QuickStart template**, such as **Instance Status Change to Stopped**, and associate it with the topic created earlier in Step 7.

6. Click **Create Notification**
<img width="900" alt="notification" src="https://github.com/user-attachments/assets/54080ff9-03a7-4c25-9e2f-be4c917cc70e">

## Step 9: Validate Notification Event Rule

Now we’ll validate that the event rule triggers the function upon stopping the instance. You can also include your email address to receive the notification payload.

1. Stop the instance from the OCI Console or using the following command:
   ```bash
   oci compute instance action --instance-id <instance_ocid> --action STOP

3. Once the instance is stopped, you should receive an email through the subscribed notification topic, and the function should be triggered.

4. Confirm that you have received the email with the notification details.

5. Check the Microsoft Teams channel for the alert.
<img width="900" alt="MS Teams" src="https://github.com/user-attachments/assets/b23781d5-1667-49ad-b207-ce56c1995e1e">

The custom function should post a notification with the relevant message to the Teams Channel, verifying the entire flow.

# Conclusion 

By following these steps, you have successfully set up an integration between OCI Notifications and Microsoft Teams, ensuring that critical OCI events are communicated effectively to your team. This setup allows for real-time alerts and event-driven notifications, enhancing the team's ability to monitor and respond swiftly to important infrastructure changes and incidents in your OCI environment. 
  


















