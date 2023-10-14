from flask import Flask, request, render_template
import sys
import logging
import requests
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from google.oauth2 import service_account

# Flask app
app = Flask(__name__)  

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logs = []

credentials = service_account.Credentials.from_service_account_file(
    'maximal-emitter-401822-371705b00b77.json', scopes=['https://www.googleapis.com/auth/analytics.readonly']
)

@app.route("/")
def hello_world():
    # Adding a google tag for google analysis
    prefix_google = """
  <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-286538006-2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-286538006-2');
</script>
    """
    # Return the tag and a print "Hello world"
    return prefix_google + "Hello World !!"

# Route to logger page
@app.route("/logger", methods=['GET', 'POST'])
def log():

    # Print a message in Python
    log_msg = "<br>Welcome to the Logger page "
    app.logger.info(log_msg)

    if request.method == 'POST':

        # Retreiived the text in the text box
        text_from_textbox = request.form['textbox']

        # Print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Web browser console : You are in the logger page');
            console.log('Text sent by the textbox : {text_from_textbox}');
        </script>
        """
    else:
        # Print a message in the browser console
        browser_log = """
        <script>
            console.log('Web browser console : You are in the logger page');
        </script>
        """

    # Text box
    textbox_value = """
    <form method="POST">
        <label for="textbox"><br><br>Write something you want to display in the console :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="send">
    </form>
    """

    # Buttons for google request, google analytics request and cookies request
    button_msg = "<br>Google Requests :<br><br>"
    google_button = """
    Google search :
    <form method="GET" action="/google-request">
        <input type="submit" value="Google">
    </form>"""
    google_analytics_button = """Google Analytics : <form method="GET" action="/google-analytics-request">
        <input type="submit" value="Google Analytics Dashboard">
    </form>
        """
    google_cookies_button = """Get the cookies informations from google analytics : <form method="GET" action="/google-cookies-request">
        <input type="submit" value="Google cookies">
    </form>
    """
    google_analytics_api = """Get the visitors number on this website from Google Analytics API : <form method="GET" action="/api-google-analytics-data">
        <input type="submit" value="Google Analytics API">
    </form>
        """

    return log_msg + browser_log + textbox_value  + button_msg +google_analytics_button + google_button  + google_cookies_button + google_analytics_api

# Google request
@app.route('/google-request', methods=['GET'])
def google_request():
    # Question
    google_url = "https://www.google.com/"
    
    try:
        response = requests.get(google_url)
        response.raise_for_status()  
        return response.text
    # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return f"Error making Google request: {str(e)}"
    
# Google analytics request
@app.route('/google-analytics-request', methods=['GET'])
def google_analytics_request():
    # Question
    google_analytics_url = "https://analytics.google.com/analytics/web/?authuser=6#/report-home/a286538006w411474576p296626512"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        # Return response from get request
        return response.text
   
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics request: {str(e)}"

# Google cookies request
@app.route('/google-cookies-request', methods=['GET'])
def google_cookies_request():

    google_analytics_url = "https://analytics.google.com/analytics/web/?authuser=6#/report-home/a286538006w411474576p296626512"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status() # Raise an exception for HTTP errors

        # Retrieve cookies of the response
        cookies = response.cookies

        # Send cookies to the template for display
        return render_template('cookies.html', cookies=cookies)
    
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics Cookies request: {str(e)}"

# Fetch data from Google analytics api
@app.route('/api-google-analytics-data', methods=['GET'])
def api_google_analytics_data():

    # Set the path to the Google Cloud credentials file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'maximal-emitter-401822-371705b00b77.json'
    # Define Google Analytics property ID, and a period of time with starting date and ending date
    GA_property_ID = "286538006"
    start_date = "2023-10-01"
    end_date = "today"

    # Initialize a client for the Google Analytics Data API
    client = BetaAnalyticsDataClient(credentials=credentials)
    
    # Function that gets the number of visitors
    def get_visitors_number(client, property_id):
        # Define the request to retrieve active users metric
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": start_date, "end_date": end_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)
        # return active_users_metric
        return response

    # Get the visitor number using the function
    response = get_visitors_number(client, GA_property_ID)

    # Check if there's a valid response with data
    if response and response.row_count > 0:
        # Extract the value of the active users metric from the response
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  # Handle the case where there is no data

    return f'Number of visitors: {metric_value}'
        
if __name__ == '__main__':
    app.run(debug=True)