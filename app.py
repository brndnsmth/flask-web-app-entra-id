import os
import requests
import logging
from flask import Flask, render_template
from identity.flask import Auth
import app_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = "0.9.0"  # Application version for troubleshooting

# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object(app_config)

# Initialize authentication
auth = Auth(
    app,
    authority=os.getenv("AUTHORITY"),
    client_id=os.getenv("CLIENT_ID"),
    client_credential=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
)

# Microsoft Graph API endpoint and scope
GRAPH_API_URL = "https://graph.microsoft.com/v1.0/me?$select=displayName,givenName,surname,mail,userPrincipalName,id,employeeId"
GRAPH_SCOPES = ["https://graph.microsoft.com/User.Read"]

@app.route("/")
@auth.login_required(scopes=GRAPH_SCOPES)
def index(*, context):
    """Home route that fetches user details from Microsoft Graph API."""
    logger.info("Accessed index route")
    user_details = {}

    access_token = context.get("access_token")
    if access_token:
        logger.info("Access token found, making request to Microsoft Graph API")
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(GRAPH_API_URL, headers=headers, timeout=30)
            logger.info(f"Graph API response status: {response.status_code}")

            if response.status_code == 200:
                user_details = response.json()
                logger.info(f"User details retrieved: {user_details}")
            else:
                logger.error(
                    f"Failed to fetch user details: {response.status_code} - {response.text}"
                )
        except requests.RequestException as e:
            logger.exception(f"Error while fetching user details: {e}")
    else:
        logger.warning("No access token found in context")

    return render_template(
        "index.html",
        user=user_details,
        edit_profile_url=auth.get_edit_profile_url(),
        api_endpoint=os.getenv("ENDPOINT"),
        title=f"Flask Web App Sample v{__version__}",
    )

@app.route("/call_api")
@auth.login_required(scopes=os.getenv("SCOPE", "").split())
def call_downstream_api(*, context):
    """Route to call a downstream API."""
    logger.info("Accessed call_api route")
    api_result = {}

    access_token = context.get("access_token")
    if access_token:
        endpoint = os.getenv("ENDPOINT")
        if not endpoint:
            logger.error("ENDPOINT environment variable is not set")
            return render_template(
                "display.html",
                title="API Response",
                result="Error: ENDPOINT environment variable is not set",
            )

        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(endpoint, headers=headers, timeout=30)
            logger.info(f"Downstream API response status: {response.status_code}")

            if response.status_code == 200:
                api_result = response.json()
            else:
                logger.error(
                    f"Failed to call downstream API: {response.status_code} - {response.text}"
                )
                api_result = {
                    "error": f"API call failed with status {response.status_code}"
                }
        except requests.RequestException as e:
            logger.exception(f"Error while calling downstream API: {e}")
            api_result = {"error": str(e)}
    else:
        logger.warning("No access token available for API call")
        api_result = {"error": "Access token is missing"}

    return render_template("display.html", title="API Response", result=api_result)

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)
