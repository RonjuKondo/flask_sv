from model import db
from model import Project
from model import Status
from restapi import ProjectApi
import json
import pprint
import datetime
import ujson
import requests
import pytest
from model.common import strftime
from model.common import strptime

def test_project_get():
    """
    restapi/getById
    """
    project = {
        'description' : 'flask_sv',
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now(),
    }

    Project.create(project, 999) == True

    project_dict = {
        'description' : "flask_sv",
    }
    result = Project.search(project_dict, 1)
    title = result[0].id

    # APIから確認
    url = f"http://localhost:5000/api/project/get/{title}"
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'flask_sv/0.0.1',
               'Content-type': 'application/json; charset=utf-8',
               }
    response = requests.get(url, headers=headers)

    assert response.status_code == 200

    data = json.loads(response.text)
    assert data['body']['name'] == "project"
    assert data['body']['description'] == "flask_sv"
    assert data['status']['code'] == "I0001"
    assert data['status']['message'] == ""
    

def test_projectt_create():
    """
    """
    # modelから試験データ登録
    test_description= 'api_project_get'
    payload = {
        'description' : test_description
    }

    # createのテスト
    # APIの実行
    url = f"http://localhost:5000/api/project/create"
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'flask_sv/0.0.1',
               'Content-type': 'application/json; charset=utf-8',
               }
    response = requests.post(url, headers=headers, json=payload)

    assert response.status_code == 200
    data = json.loads(response.text)
    assert data['body'] == ""
    assert data['status']['code'] == "I0001" 
    assert data['status']['message'] == "Created Project Succesfuly." 

    # 作成されたデータの確認
    project_dict = {
        'description' : test_description
    }
    result = Project.search(project_dict, 999)
    title = result[0].title

    result_json = ProjectApi.getById(title, 100)

    assert result_json['body']['name'] == "project"
    assert result_json['body']['description'] == test_description
    assert result_json['status']['code'] == "I0001"
    assert result_json['status']['message'] == ""


def test_project_search():
    """
    """
    project = {
        'description' : "search_project",
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now(),
    }

    # createのテスト
    assert Project.create(project, 999) == True

    payload = {
        "description":"search_project"
        }
    #result = Project.search(query, 999)

    # APIから確認
    url = f"http://localhost:5000/api/project/search"
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'flask_sv/0.0.1',
               'Content-type': 'application/json; charset=utf-8',
               }
    response = requests.post(url, headers=headers, json=payload)

    # HTTP Statusコードが200であること
    assert response.status_code == 200

    print(f"test_project_search():json response.text={response.text}")
    # BODYをjsonでパースできること
    data = json.loads(response.text)
    print(f"test_project_search():json data={data}")
    assert data['body'][0]['description'] == payload["description"]
    assert data['body'][0]['created_by'] == 999
    assert data['status']['code'] == 'I0001'
    assert data['status']['message'] == 'Found (1) records.'

def test_project_update():
    """
    """
    project = {
        'description' : "update_project",
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now(),
    }

    # create
    Project.create(project, 999) == True

    search_query = {
        "description":"update_project"
    }
    result = Project.search(search_query, 999)
    assert result[0].description == project['description']
    title = result[0].title
    payload = {
        "title": title,
        "description":"update_account_modified",
        "status":"1"
    }

    # APIから確認
    url = f"http://localhost:5000/api/project/update"
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'flask_sv/0.0.1',
               'Content-type': 'application/json; charset=utf-8',
               }
    response = requests.post(url, headers=headers, json=payload)

    # HTTP Statusコードが200であること
    assert response.status_code == 200
    data = json.loads(response.text)
    assert data['body'] == ""
    assert data['status']['code'] == "I0001"
    assert data['status']['message'] == "Updated Project Succesfuly."

    search_query = {
        "description":"update_project_modified",
    }
    result = Project.search(search_query, 999)
    assert result[0].created_by == 999
    assert result[0].status == 1


def test_project_delete():
    """
    """
    project = {
        'description' : "delete_project",
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now(),
    }

    # create
    Project.create(project, 999) == True

    search_query = {
        "description":"delete_project",
    }
    result = Project.search(search_query, 999)
    assert result[0].description == project['description']
    account_title = result[0].title

    # APIから確認
    url = f"http://localhost:5000/api/project/delete/{title}"
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'flask_sv/0.0.1',
               'Content-type': 'application/json; charset=utf-8',
               }
    response = requests.get(url, headers=headers)

    # HTTP Statusコードが200であること
    assert response.status_code == 200

    data = json.loads(response.text)
    print(f"test_ProjectApi#test_project_delete data={data} code={data['status']['code']} message={data['status']['message']}")
    assert data['body'] == ""
    assert data['status']['code'] == "I0001"
    assert data['status']['message'] == "deleted Project Succesfuly."

    
