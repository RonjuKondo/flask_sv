from model import db
from model import Project
from model import Status
import pprint
import datetime

def test_getByTitle():
    """
    """
    user_id = 1
    
    project = {
        'title' : "test_project",
        'description' : 'flask_sv',
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now()
    }

    Project.create(project, 999) == True

    project_dict = {
        '' : "flask_sv",
    }
    results = Project.search(project_dict, 1)
    project_title = results[0].title
    result = Project.getByTitle(project_title, 999)

    assert result.title == project_dict['title'] 
    assert result.created_by == 999
    assert result.status == Status.getStatusKey("NEW")

    assert results[0].title == project_dict['title'] 
    assert results[0].created_by == 999
    assert results[0].status == Status.getStatusKey("NEW")

               
def test_create():
    """
    """
    project = {
        'title' : 'test_project2',
        'description' : 'flask_sv2',
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now()
    }

    assert Project.create(project, 999) == True
    project_dict = {
        'title' : 'test_project2',
        'description' : "flask_sv2",
        'end_on' : "2030-12-31 00:00:00"
    }
    results = Project.search(project_dict, 1)
    assert results[0].title == project_dict['title'] 
    assert results[0].created_by == 999
    

def test_update():
    """
    """
    project = {
        'title' : 'test_project3',
        'description' : 'flask_sv3',
        'status' : 1,
        'created_by' : 999,
        'created_at' : datetime.datetime.now(),
        'updated_by' : 999,
        'updated_at' : datetime.datetime.now()
    }

    assert Project.create(project, 999) == True
    project_dict = {
        'title' : 'test_project3',
        'description' : "flask_sv3"
    }
    results = Project.search(project_dict, 1)
    project_title = results[0].title
    result = Project.getByTitle(project_title, 999)
    project_update = {
        'title' : project_title,
        'description' : 'flask_sv4',
        'status' : results[0].status + 1
    }
    assert Project.update(project_update, 999)[0] == True
    result = Project.getByTitle(project_title, 999)
    assert result.title == project_update['title']
    assert result.created_by == 999
    assert result.status == project_update['status']
    
    
