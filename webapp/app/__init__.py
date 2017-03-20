from flask import Flask
import libhoney

app = Flask(__name__)
libhoney.init(writekey='abcabc123123', dataset='my flask app')


from app import views
