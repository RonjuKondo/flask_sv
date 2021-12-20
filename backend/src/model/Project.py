from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.type_api import STRINGTYPE
from model import Status
import sqlalchemy
from model.common import strftime
from model.common import strptime
import time
import model.Status
#from sqlalch

import datetime
#from datetime import datetime

from model.db import engine
from model.db import Base

# model class
class Project(Base):
    """
    accountモデル
    flask_svシステムにログインするアカウントを管理するモデル

    Parameters
    ----------
    Base : データベース接続子
    """
    __tablename__ = 'project'

    title = Column(String(), primary_key=True)
    description = Column(String())
    status = Column(Integer)
    created_by = Column(Integer, nullable=True)
    created_at = Column(Timestamp, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(Timestamp, nullable=True)

    # get Dict data
    def toDict(self):
        """
        ディクショナリ形式でクラスの全メンバを返却する

        Parameters
        ----------
        self : 自クラス

        Returns
        -------
        クラスの全メンバのディクショナリ
        """
        return {
            'title' : str(self.title),
            'description' : str(self.description),
            'status' : int(self.status),
            'created_by' : int(self.created_by),
            'created_at' : strptime(self.created_at), 
            'updated_by' : int(self.updated_by),
            'updated_at' : strptime(self.updated_at),
        }
    # datetime.strptime(str(self.start_on), "%Y-%m-%d %H:%M:%S")

    def toJson(self):
        return {
            "name": "project",
            "title" : str(self.title),
            "description" : str(self.description),
            "status" : int(self.status),
            "created_by" : int(self.created_by),
            "created_at" : strftime(self.created_at), 
            "updated_by" : int(self.updated_by),
            "updated_at" : strftime(self.updated_at),
        }
    
# get List data    
def getByList(arr):
    res = []
    for item in arr:
        res.append(item.toDict())
    return res

# get all mydata record
def getAll():
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = ses.query(Project).all()
    ses.close()
    return res


def getByTitle(title, operation_account_id):
    """
    アカウントidでaccountテーブルを検索をし、該当したAccountオブジェクト群を取得する

    Parameters
    ----------
    title : 検索対象のアカウントid
    operation_account_id : 操作ユーザーのアカウントid

    Returns
    -------
    Accountオブジェクトのリスト
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = ses.query(Project).get(title)
    ses.close()
    return res

def search(project_dict, operation_account_id):
    """
    dictアカウントからaccountテーブルを検索し、該当したAccountオブジェクト群を取得する

    Parameters
    ----------
    {
        'description' : 文字列str(self.description),
        'start_on' : 文字列 '2020-05-01 00:00:00',
        'end_on' : 文字列 '2020-12-31 00:00:00',
        'created_by' : title,
        'created_at' : 文字列 '2020-12-31 00:00:00',
        'updated_by' : title,
        'updated_at' : 文字列 '2020-12-31 00:00:00',
        'status' : statusの数値
    }

    Returns
    -------
    Accountオブジェクトのリスト
    """
    print(f"project_dict={project_dict}")
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = None
    rs = ses.query(Project)
    v = project_dict.get('description')
    if (v != None):
        rs = rs.filter(Project.description==v)
    if (v != None):
        rs = rs.filter(Project.status==v)
    v = project_dict.get('created_by')
    if (v != None):
        rs = rs.filter(Project.created_by==v)
    v = project_dict.get('created_at')
    if (v != None):
        rs = rs.filter(Project.created_at==v)
    v = project_dict.get('updated_by')
    if (v != None):
        rs = rs.filter(Project.updated_by==v)
    v = project_dict.get('updated_at')
    if (v != None):
        rs = rs.filter(Project.updated_at==v)
    rs = rs.filter(Project.status!=Status.getStatusKey("DELETE"))

    res = rs.all()
    lambda r: print(f"r={r}"),res
    ses.close()
    return res
            
def create(project_dict, operation_account_id):
    project = Project()
    project.title = project_dict['title']
    project.description = project_dict['description']
    project.status = project_dict['status']
    project.created_by = project_dict['created_by']
    project.created_at = project_dict['created_at']
    project.updated_by = project_dict['updated_by']
    project.updated_at = project_dict['updated_at']
    Session = sessionmaker(bind=engine)
    ses = Session()
    ses.begin()
    try:
        ses.add(project)
        ses.commit()
        res = True
    except:
        ses.rollback()
        res = False
    finally:
        ses.close()
    return res

def update(project_dict, operation_account_id):
    title = project_dict.get('title')
    Session = scoped_session(sessionmaker(bind=engine, autocommit=False))
    res=False
    ses = Session()
    project_record = ses.query(Project).with_for_update().get(title)
    print(f"Project#update project_record={project_record}")
    message = ""
    try:
        v = project_dict.get('description')
        if (v != None):
            project_record.description=v
        project_record.updated_by=operation_account_id
        ses.add(project_record)
        #他のプロセスによるロックを待つ
        #time.sleep(1)
        ses.commit()
        res = True
    except Exception as e:
        message = str(e)
        print(f"Project#update error:{message}")
        ses.rollback()
        res = False
    finally:
        ses.close()
    return (res, message)    


def delete(title, operation_account_id):
    Session = scoped_session(sessionmaker(bind=engine, autocommit=False))
    ses = Session()
    project_record = ses.query(Project).with_for_update().get(title)
    try:
        project_record.status=Status.getStatusKey("DELETE")
        ses.add(project_record)
        #他のプロセスによるロックを待つ
        #time.sleep(1)
        ses.commit()
        message = ""
        res = True
    except Exception as e:
        message = str(e)
        print(f"Project#update error:{message}")
        ses.rollback()
        res = False
    finally:
        ses.close()
    return (res, message)    

