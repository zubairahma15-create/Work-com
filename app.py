from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to Work.com!"
