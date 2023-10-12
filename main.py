from flask import Flask, request
import logging,sys



app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logs = []


@app.route('/')
def hello_world():
    prefix_google = """  
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-286538006-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-286538006-1');
</script>
     """
    return prefix_google+ "Hello, World!"
  
# @app.route('/logger')
# def logger():
#     print("this is a Python log message")
#     return """
#   <script>
#   console.log("This is a browser log message");
#   </script>
#   """ + "logger page"

# @app.route('/logger')
# def logger():  
#   app.logger.info('%s you are in the logger page')
#   logging.basicConfig(filename='record.log', level=logging.DEBUG)
#   return """
#    <script>
#    console.log("This is a browser log message");
#    </script>
#    """ + "hello logger from python"


@app.route("/logger", methods=['GET', 'POST'])
def log():
    # Print a message in Python
    log_msg = "test page"
    app.logger.info(log_msg)

    if request.method == 'POST':
        # Retreiived the text in the text box
        text_from_textbox = request.form['textbox']

        # Print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
            console.log('Texte de la boîte de texte : {text_from_textbox}');
        </script>
        """
    else:
        # Print a message in the browser console
        browser_log = """
        <script>
            console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
        </script>
        """

    # Formulaire HTML avec une boîte de texte
    textbox_form = """
    <form method="POST">
        <label for="textbox">Html logging :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Submit">
    </form>
    """

    return log_msg + browser_log + textbox_form


   

if __name__ == '__main__':
    app.run(debug=True)
    
