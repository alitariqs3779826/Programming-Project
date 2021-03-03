
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import boto3
from botocore.exceptions import ClientError
import requests
import os
import botocore
from cognito import cognitoRoute


app = Flask(__name__)
APP_CLIENT_ID = "1rfl5n6j4su0mgmgkfh43fqbov"

app.register_blueprint(cognitoRoute)

if __name__ == '__main__':
   
    app.run(host='0.0.0.0',debug=True)
