# Integrate OCI Notifications with Microsoft Teams
Oracle Notification Service (ONS) is a robust cloud-native tool that allows you to route notifications from Oracle Topics to various destinations like email, Slack channels, or custom HTTP webhooks with ease. 
However, Microsoft Teams is not natively supported as a direct destination for these notifications. When trying to use Custom HTTP URLs to integrate with Microsoft Teams, there are two significant constraints that need to be addressed : 
1.	Custom HTTPs URLs in Oracle Subscriptions do not support URL parameters. The URL must be encoded in ASCII. This poses a problem when integrating with services like Microsoft Teams, where the webhook URLs typically include parameters.
2.	When you declare an HTTPS Custom URL subscription, Oracle requires you to confirm the subscription by sending an HTTP GET request to a specific URL sent to your custom URL.

This process is incompatible with Microsoft Teams via webhook, as it requires the JSON payload to be specific format.
	Handling Payload Format: 
To send a message using workflow, you must post a JSON payload to the webhook URL. This payload should be in the form of Adaptive Card Format. 
Payload of any other format is not acceptable in Teams with workflow. Here is an Example Connector card that you can post. Please check the docs here.
OCI Functions can be used to format the payload correctly, ensuring it complies with Microsoft Team’s requirements. OCI Functions also provide flexibility to include additional logic, such as logging, and even routing messages based on content. 

