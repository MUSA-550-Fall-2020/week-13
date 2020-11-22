from flask import Flask

# initialize your application
app = Flask(__name__)


@app.route("/")
def hello_world():
    """
    This function runs when the "/" route (the home page of 
    your application) is requested by a browser
    """
    return "My name is Nick"


@app.route("/test")
def hello_test():
    """
    This function runs when the "/" route (the home page of 
    your application) is requested by a browser
    """
    return "Hello, this is a test"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

