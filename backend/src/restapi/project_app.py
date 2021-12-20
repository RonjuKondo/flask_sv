# 近藤君割り当て
from os import system
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from restapi import ProjectApi

system_account_id=999

project_bp = Blueprint('project_app', __name__, url_prefix='/api/project')

@project_bp.route('/get/<title>', methods=['GET'])
def getProject(title):
    project_json = ProjectApi.getByTitle(title, system_account_id)
    return jsonify(project_json)

@project_bp.route('/lock', methods=['POST'])
def lockProject():
    payload = request.json
    print(f"project_app#lockProject() payload={payload}")
    project_json = ProjectApi.getByIdWithLock(payload, system_account_id)
    return jsonify(project_json)
    # TODO lockする場合はロックするユーザーidも渡す必要がある。POSTへの変更が望ましい。

@project_bp.route('/create', methods=['POST'])
def createProject():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = ProjectApi.create(payload, system_account_id)
    return jsonify(response_json)

@project_bp.route('/search', methods=['POST'])
def searchProject():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = ProjectApi.search(payload, system_account_id)
    return jsonify(response_json)

@project_bp.route('/search_range', methods=['POST'])
def searchRangeProject():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = ProjectApi.search_range(payload, system_account_id)
    return jsonify(response_json)

@project_bp.route('/update', methods=['POST'])
def updateProject():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = ProjectApi.update(payload, system_account_id)
    return jsonify(response_json)

@project_bp.route('/update_for_lock', methods=['POST'])
def updateProjectWithLock():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = ProjectApi.updateWithLock(payload, system_account_id)
    return jsonify(response_json)

@project_bp.route('/delete/<title>', methods=['GET'])
def deleteProject(title):
    project_json = ProjectApi.delete(title, system_account_id)
    return jsonify(project_json)

class Spam(Resource):
    def get(self):
        return {'title': 42, 'name': 'Name'}

api = Api(project_bp)
api.add_resource(Spam, '/spam')

