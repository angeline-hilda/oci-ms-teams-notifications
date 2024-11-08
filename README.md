# Integrate OCI Notifications with Microsoft Teams
Oracle Notification Service (ONS) is a robust cloud-native tool that allows you to route notifications from Oracle Topics to various destinations like email, Slack channels, custom HTTP webhooks or OCI Functions with ease.
Support of OCI Functions as Notification target allows to invoke cusotm function during Notification event and send updated notification details to communication channels that support API invocation. 
In this article, I'm going to show the integration between OCI and Microsoft Teams, ensuring that critical OCI events are communicated effectively to your team.

## Approach: ##

![ONS and MS Teams drawio_1](https://github.com/user-attachments/assets/e241e0d3-c255-4101-8d32-4e89a465d41b)

- **Resources in Oracle Cloud Infrastructure (OCI)** emit events, which are structured messages indicating the state of change of resources throughout the tenancy. For example, an event can be emitted when an instance starts, a backup completes or fails, or a file in an Object Storage bucket is added, updated, or deleted.
- **OCI Notifications** route these events to the appropriate destinations.
- **OCI Functions** reformat the event data (JSON Payload) to the Adaptive Card format required by Microsoft Teams.
- The restructured message is then published to Microsoft Teams via a webhook, ensuring that the notification is displayed correctly in the Teams channel.

## Prerequisites

### 1. Create a Workflow in Microsoft Teams

To receive notifications from OCI in Microsoft Teams, set up a workflow in Microsoft Teams to handle incoming webhook requests and post to a channel or chat. Follow the steps in the [Microsoft Teams Incoming Webhook Documentation](https://docs.microsoft.com/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) to create an incoming webhook.

### 2. Custom Functions Code

The function code is provided in the [sample code folder](https://github.com/angeline-hilda/OCI-Notifications/tree/9007f51a4a3a94e9b7b71e33064d3f3cdeaa7308/sample%20code) with the following files:

- **`func.py`**: Main function file, which processes incoming OCI event data and formats it for Microsoft Teams.
- **`requirements.txt`**: Lists the dependencies needed to run the function.
- **`func.yaml`**: Metadata file containing configuration details for deploying the function in OCI.

Ensure these files are available and accessible for deployment.

## Setup

The detailed, step-by-step setup guide can be found in the [setup.md](https://github.com/angeline-hilda/OCI-Notifications/blob/912b9de7b995c35d606780f3148e2e67334496a4/setup%20guide.md) file. It includes instructions to:

1. Create a dynamic group and policy to grant necessary permissions.
2. Create a repository and deploy the function in OCI.
3. Set up OCI Notifications and subscribe to a topic.
4. Test and validate the function by triggering OCI events.

## Usage

After deployment, any specified OCI events (e.g., instance stopped or Object Storage file upload) will trigger the notification function, which sends a message to the configured Microsoft Teams channel. You can update the function to customize the message format or to include additional event details.

### Triggering an Event

To test the integration, you can trigger an event by stopping or starting an instance, or by creating a file in Object Storage (if these events are configured as triggers). Verify that the notification appears in the designated Teams channel.

## Troubleshooting

Here are some common issues and tips to help resolve them:

- **Webhook Delivery Issues**: Verify that the webhook URL in the function code matches the Microsoft Teams webhook URL.
- **Permission Denied Errors**: Ensure that the IAM policies and dynamic group settings are correctly configured for the function.
- **Function Deployment Errors**: Check the `func.yaml` file for accurate configuration, and verify that all required dependencies are listed in `requirements.txt`.

## Resources

- [Oracle Cloud Infrastructure Notification Service](https://docs.oracle.com/en-us/iaas/Content/Notification/Concepts/notificationoverview.htm)
- [Oracle Cloud Infrastructure Events](https://docs.oracle.com/en-us/iaas/Content/Events/Concepts/eventsoverview.htm)
- [Oracle Functions](https://docs.oracle.com/en-us/iaas/Content/Functions/Concepts/functionsoverview.htm)
- [Microsoft Connectors](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL%2Ctext1)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/angeline-hilda/OCI-Notifications/tree/main?tab=MIT-1-ov-file) file for details.

---

This setup enables seamless integration between OCI and Microsoft Teams, ensuring that critical OCI events are effectively communicated in real time to your team, improving visibility and operational efficiency.

   



