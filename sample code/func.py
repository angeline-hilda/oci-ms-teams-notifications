import io
import oci
import json
import logging
import requests         # for making http requests

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# This function processes the incoming event data and constructs an Adaptive Card message in JSON format, which Microsoft Teams can understand.
# Data Extraction: Retrieves relevant fields from the event body, including compartment ID, resource ID, and additional details.
# Adaptive Card Construction: Builds a message in Adaptive Card format, including text, facts, and an image.
# Sending Notification: Converts the notification to JSON and calls make_post to send it to Microsoft Teams.

def parse_message(body):
    logging.debug("Entering parse_message function")

    # Extracting data from the body
    event_type = body.get("eventType", "")
    description = body.get("eventType", "")
    compartment_id = body["data"].get("compartmentId", "")
    compartment_name = body["data"].get("compartmentName", "")
    resource_id = body["data"].get("resourceId", "")
    availability_domain = body["data"].get("availabilityDomain", "")
    action_type = body["data"]["additionalDetails"].get("instanceActionType", "")
    shape = body["data"]["additionalDetails"].get("shape", "")
    image_id = body["data"]["additionalDetails"].get("imageId", "")

    # Constructing the Adaptive Card message without private IP
    notification = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"Instance Action Notification: {description}",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {"title": "Compartment Name", "value": compartment_name},
                                {"title": "Compartment ID", "value": compartment_id},
                                {"title": "Resource ID", "value": resource_id},
                                {"title": "Availability Domain", "value": availability_domain},
                                {"title": "Action Type", "value": action_type},
                                {"title": "Shape", "value": shape},
                                {"title": "Image ID", "value": image_id}
                            ]
                        },
                        {
                            "type": "Image",
                            "url": "https://adaptivecards.io/content/cats/3.png",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": "For Samples and Templates, see [https://adaptivecards.io/samples](https://adaptivecards.io/samples)",
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }

    # Convert the notification message to JSON
    notification_json = json.dumps(notification)
    logging.debug(f"Constructed notification JSON: {notification_json}")

    # Sending the notification
    make_post(notification_json)

# Sends the constructed notification to a Microsoft Teams webhook URL.
# HTTP POST Request: Sends the JSON payload to the specified URL
# Error Handling: Logs the response status and any errors encountered during the POST request.

def make_post(post_text):
    url = ""
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        post_response = requests.post(url=url, data=post_text, headers=headers)
        logging.debug(f"POST response status: {post_response.status_code}")
        logging.debug(f"POST response body: {post_response.text}")
    except Exception as e:
        logging.error(e)
        return

    # Check if response body is not empty and in JSON format
    if post_response.text:
        try:
            response_dict = json.loads(post_response.text)
            code = response_dict.get("StatusCode", -1)
            if code != 0:
                logging.error(f"Error sending post text, code: {code}")
        except json.JSONDecodeError:
            logging.error("Response is not in JSON format")
    else:
        logging.debug("Empty response body")


#Converts string representations of boolean values ("True" or "False") to actual Python boolean values.

def to_bool(a):
    return True if a == "True" else False

# Entry point for the function, responsible for handling the incoming request, parsing the data, and invoking the parse_message function.
# OCI Signer: Uses the Resource Principals signer for authentication.
# Configuration Handling: Parses configuration if provided.
# Data Parsing: Extracts and processes the event data from the request.

def handler(ctx, data: io.BytesIO = None):
    logging.debug("Entering handler function")
    signer = oci.auth.signers.get_resource_principals_signer()
    # Skip the configuration handling when running locally
    try:
        if ctx:
            cfg = dict(ctx.Config())
            for a in cfg:
                cfg[a] = to_bool(cfg[a])
            logging.debug(f"Config: {cfg}")
        else:
            logging.debug("No context provided, skipping configuration parsing.")
    except Exception as e:
        logging.error(f"ERROR: Missing configuration keys: {e}")
        return f'error parsing config keys: {e}'

    try:
        raw_body = data.getvalue()
        body = json.loads(raw_body)
        logging.debug(f"Received body: {body}")
        parse_message(body)
    except (Exception, ValueError) as ex:
        logging.error(f'Error parsing JSON payload: {ex}')
        return f'error parsing json payload: {ex}'

# Read the sample JSON payload from file and test the handler function
# Allows local testing of the function by reading a sample JSON payload from a file and invoking the handler function with it.
if __name__ == "__main__":
    with open('sample_payload.json', 'r') as file:
        sample_payload = file.read()
        data_stream = io.BytesIO(sample_payload.encode('utf-8'))
        handler(None, data_stream)

