import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, Blueprint
import boto3
from botocore.exceptions import ClientError
import requests
import os
import botocore


APP_CLIENT_ID = "1rfl5n6j4su0mgmgkfh43fqbov"

cognito_client = boto3.client('cognito-idp', region_name='us-east-1')


cognitoRoute = Blueprint('cognitoRoute', __name__)

@cognitoRoute.route('/auth/signup', methods=['GET'])
def create_account():
    return render_template("login.html")

@cognitoRoute.route('/', methods=['GET'])
def login_page():
    return render_template("login.html")

@cognitoRoute.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

@cognitoRoute.route('/auth/signup/', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_email = request.form['Email']
        user_password = request.form['Password']
        user_name = request.form['Username']
        usertype = request.form['usertype']
    
        try:
            cognito_client.sign_up(ClientId=APP_CLIENT_ID,
                            Username=user_email,
                            Password=user_password,
                            UserAttributes=[{'Name': 'name', 'Value': user_name}])
        except ClientError as e:
            if e.response['Error']['Code'] == 'UsernameExistsException':
                
                print("User already exists")
                return redirect(url_for('cognitoRoute.create_account'))
            if e.response['Error']['Code'] == 'ParamValidationError':
                
                print("Param Validate Error")
                return redirect(url_for('cognitoRoute.create_account'))
            print(e)



        return redirect(url_for('cognitoRoute.login'))


    return redirect(url_for('cognitoRoute.create_account'))


@cognitoRoute.route('/auth/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['Email']
        password = request.form['Password']
        try:
            response =  cognito_client.initiate_auth(ClientId=APP_CLIENT_ID,
                                        AuthFlow='USER_PASSWORD_AUTH',
                                        AuthParameters={
                                        'USERNAME': user_email,
                                        'PASSWORD': password
                                        }
            )
        

        except ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                print("Can't Find user by Email")
                return render_template("login.html", error = "Can't find user by email")
            if e.response['Error']['Code'] == 'ParamValidationError':
                print("Param Validate Error")
                return render_template("login.html", error = "Param Validate Error")

            if e.response['Error']['Code'] == 'NotAuthorizedException':
                print("Not Valid")
                return render_template("login.html", error = "Wrong Email or Password")
        
        return redirect(url_for('cognitoRoute.home'))

    return redirect(url_for('cognitoRoute.login_page'))


