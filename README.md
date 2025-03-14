# Flask Web Application with Microsoft Entra ID Integration

This project is a simplified version of the original Microsoft Entra ID with a Python web application sample. It demonstrates how to integrate Microsoft Entra ID with a Python web application built using Flask. All configurations and features unrelated to Microsoft Entra ID have been removed to streamline the application.

## Features

This application supports the following scenarios:

| Feature                     | Supported |
|-----------------------------|-----------|
| Web App Sign-In & Sign-Out  | ✓         |
| Web App Calling a Web API   | ✓         |
| Retrieve Employee ID        | ✓         |

## Getting Started

### Prerequisites

1. **Python**: Ensure you have Python 3.8+ installed.
2. **Clone the Repository**: Clone this repository or download the zip file.

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
flask run -h localhost
```

By default, the app runs on `http://localhost:5000`. Update the port if needed to match your `REDIRECT_URI` configuration.

---

## Configuration

### App Registration

Before running the application, you need to register it in the Microsoft Entra ID portal. Follow these steps:

1. Complete steps 1–3 of the [Quickstart: Add sign-in with Microsoft to a Python web app](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-v2-python-webapp).
2. Note down the **Client ID**, **Tenant ID**, and **Client Secret** from the app registration.

### Environment Variables

1. Copy the `.env.sample.entra-id` file and rename it to `.env`.
2. Update the `.env` file with your app's settings:
   - `CLIENT_ID`: Your app's client ID.
   - `CLIENT_SECRET`: Your app's client secret.
   - `TENANT_ID`: Your tenant ID.
   - `REDIRECT_URI`: The redirect URI configured in the app registration.

> **Important**: Avoid committing sensitive information (like credentials) to version control.

---

## Using the Application

### Sign-In and Sign-Out

Once configured, navigate to the app's homepage to test the sign-in and sign-out functionality.

### Calling a Web API

To enable the app to call a web API (e.g., Microsoft Graph), update the `.env` file with the API's endpoint and required scopes. For example:

```env
ENDPOINT=https://graph.microsoft.com/v1.0/me
SCOPE=User.Read
```

Restart the application and test the "Call API" feature.

### Retrieve Employee ID

The application now retrieves the `employeeId` property from Microsoft Graph API (if available). Ensure the following:

1. The `SCOPE` environment variable includes `User.Read` or `User.Read.All`.
2. The user has an `employeeId` set in Azure AD.

The `employeeId` will be displayed on the homepage after sign-in.

---

## Logging and Debugging

The application includes enhanced logging to help diagnose issues:

- Logs are written to the console, including details about API requests, responses, and errors.
- If the `employeeId` is not available, a warning will be logged, and "Not Available" will be displayed on the homepage.

To enable debug mode, run the application with:

```bash
flask run --debug
```

---

## Deployment

To deploy this application to Azure App Service:

1. Follow the [Quickstart: Deploy a Python web app to Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python), replacing the sample app with this project.
2. Configure the app's settings in Azure to include the environment variables from your `.env` file.
3. If `SESSION_TYPE = "filesystem"` is set in `app_config.py`, enable "session affinity" (ARR affinity) in the Azure App Service settings.

---

## Troubleshooting

1. **Access Token Issues**: If the application cannot retrieve an access token, ensure the `SCOPE` environment variable is set correctly (e.g., `User.Read`).
2. **Missing Employee ID**: If the `employeeId` is not displayed:
   - Verify the user has an `employeeId` set in Azure AD.
   - Ensure the app has the correct permissions (`User.Read` or `User.Read.All`).
3. **Logging**: Check the console logs for detailed error messages and debugging information.