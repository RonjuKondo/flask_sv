from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from restapi import AccountApi

system_account_id=999

account_bp = Blueprint('account_app', __name__, url_prefix='/api/account')

@account_bp.route('/get/<id>', methods=['GET'])
def getAccount(id):
    account_json = AccountApi.getById(id, system_account_id)
    return jsonify(account_json)

@account_bp.route('/lock/<id>', methods=['GET'])
def lockAccount(id):
    account_json = AccountApi.getByIdWithLock(id, system_account_id)
    return jsonify(account_json)
    # TODO lockする場合はロックするユーザーidも渡す必要がある。POSTへの変更が望ましい。

@account_bp.route('/create', methods=['POST'])
def createAccount():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = AccountApi.create(payload, system_account_id)
    return jsonify(response_json)

@account_bp.route('/search', methods=['POST'])
def searchAccount():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = AccountApi.search(payload, system_account_id)
    return jsonify(response_json)

@account_bp.route('/update', methods=['POST'])
def updateAccount():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = AccountApi.update(payload, system_account_id)
    return jsonify(response_json)

@account_bp.route('/update_for_lock', methods=['POST'])
def updateAccountWithLock():
    #payload = request.data.decode('utf-8')
    payload = request.json
    print(f"payload={payload}")
    response_json = AccountApi.updateWithLock(payload, system_account_id)
    return jsonify(response_json)

@account_bp.route('/delete/<id>', methods=['GET'])
def deleteAccount(id):
    account_json = AccountApi.delete(id, system_account_id)
    return jsonify(account_json)

class Spam(Resource):
    def get(self):
        return {'id': 42, 'name': 'Name'}

api = Api(account_bp)
api.add_resource(Spam, '/spam')

