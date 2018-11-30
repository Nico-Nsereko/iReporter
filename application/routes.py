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
        @app.route('/api/v1')
        def home():
            return jsonify({"message":"Welcome to iReporter"}), 200

        @app.route('/api/v1/red-flags', methods = ['GET'])
        def getredflags():
            if len(redflags)>0:
                return jsonify({"data": redflags }), 200
            return jsonify({"message": "No red flags detected"}), 400

        @app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['GET'])
        def getredflag(red_flag_id):
            for redflag in redflags:
                if redflag["id"] == red_flag_id:
                    return jsonify({"data": redflags[red_flag_id]}), 200
            return jsonify({"message": "Red-flag does not exist."}), 400

        @app.route('/api/v1/red-flags', methods=['POST'])
        def createredflag():
            data_request = request.get_json()
            id = len(redflags)
            createdOn = datetime.datetime.utcnow()
            createdBy = data_request.get('createdBy')
            incident_type = data_request.get("incident_type")
            location = data_request.get("location")
            status = data_request.get("status")
            comment = data_request.get("comment")

            new_incident = Incident(id, createdOn, createdBy, incident_type, location, status, comment)

            if new_incident.createdBy is str or new_incident.createdBy == '':
                return jsonify({"message": "Incident creator cannot be empty and must be a "}), 400
            if incident_type is str or incident_type == '':
                return jsonify({"message": "Incident type cannot be empty and must be a string"}), 400
            if location == '':
                return jsonify({"message": "Incident location should not be empty"}), 400
            if status is str or status not in statuses:
                return jsonify({
                                   "message": "Incident status should either be Draft, Rejected, Under investigation, or Resolved"}), 400
            if comment is str or comment == '':
                return jsonify({"message": "Incident comment can not be empty and should be a string."}), 400

            incident_dict = dict(
                id=new_incident.id,
                createdOn=new_incident.createdOn,
                createdBy=new_incident.createdBy,
                incident_type=new_incident.incident_type,
                location=new_incident.location,
                status=new_incident.status,
                comment=new_incident.comment
            )
            redflags.append(incident_dict)

            return jsonify({
                "data": incident_dict["id"],
                "message": "Created red-flag record"
            }), 200

        @app.route('/api/v1/red-flags/<int:red_flag_id>/location', methods=['PATCH'])
        def editlocation(red_flag_id):
            data_request = request.get_json()
            for redflag in redflags:
                if redflag["id"] == red_flag_id:
                    redflag["location"] = data_request.get("location")
                    return jsonify({
                        "data": red_flag_id,
                        "message": "Updated red-flag record's location",
                        "status": 200
                    }), 200
            return jsonify({"message": "Red-flag record's location not updated"}), 400

        @app.route('/api/v1/red-flags/<int:red_flag_id>/comment', methods=['PATCH'])
        def editcomment(red_flag_id):
            data_request = request.get_json()
            for redflag in redflags:
                if redflag["id"] == red_flag_id:
                    redflag['comment'] = data_request.get("comment")
                    return jsonify({
                        "data": red_flag_id,
                        "message": "Updated red-flag record's comment."
                    }), 200
            return jsonify({"message": "Red-flag not updated"}), 400

        @app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['DELETE'])
        def deleteredflag(red_flag_id):
            for i, redflag in enumerate(redflags):
                if redflag["id"] == red_flag_id:
                    redflags.pop(i)
                    return jsonify({
                        "data": redflag["id"],
                        "message": "Red-flag record deleted"
                    }), 200
            return jsonify({"message": "Red-flag record not deleted"}), 400
