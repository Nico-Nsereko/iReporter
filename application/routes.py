from flask import Flask, jsonify, abort, request
from .model import Incident
import datetime

statuses =('Draft', 'Rejected', 'Under investigation', 'Resolved')
type = ('red-flag', 'intervention')
redflags=[
    {
        "id": 0,
        "createdOn": datetime.datetime.utcnow(),
        "createdBy" : 1,
        "type" : 1,
        "location" : "lat 0.00333 long 1.3456",
        "status" : "Draft",
        "images" : ['img1.gif','img2.jpg'],
        "videos" : ['vid1.mp4', 'vid2.mkv'],
        "comment" : "This is my comment."

    }
]

class Views:
    app = Flask(__name__)

    @staticmethod
    def get_views(app):
        @app.route('/')
        def home():
            return jsonify({"message":"Welcome to iReporter"}), 200

        @app.route('/api/v1/red-flags', methods = ['GET'])
        def getredflags():
            if len(redflags)>0:
                return jsonify({"data": redflags }), 200
            return jsonify({"message": "No red flags detected"}), 400
