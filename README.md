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

## Pre-requisites:
1. Create a Workflow in Microsoft Teams. This allows posting to a channel or chat when a webhook request is received. You can follow the steps in the [official documentation](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498#:~:text=An%20Incoming%20webhook%20lets%20external,a%20webhook%20request%20is%20received.&text=next%20to%20the%20channel%20or,for%2C%20and%20then%20select%20Workflows) to create an incoming webhook.

2. Custom Functions Code: Available [here](https://github.com/angeline-hilda/OCI-Notifications/tree/9007f51a4a3a94e9b7b71e33064d3f3cdeaa7308/sample%20code).
   
The following are the steps to get notified on MS Team when an instance is stopped.<br/>

## Documentation:

Step by step guide to integrate OCI Notifications service with Microsoft Teams can be found [here]()




