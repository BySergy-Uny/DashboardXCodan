from flask import Flask
from dotenv import dotenv_values

config = dotenv_values("./.env")
app = Flask(__name__)