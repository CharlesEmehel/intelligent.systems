
from ontoML import db

from ontoML import app

with app.app_context():
    db.drop_all()

with app.app_context():
    db.create_all()

from ontoML.models import Item

item1 =Item(entity="meter", type="equipmentContainer", locatedat='substation:rdnsubstation001', datecreated="2017-05-04T12:30:00Z", modifiedat= "2022-05-18T13:45:30Z", entityversion=2, devicecategory='grid-related')

with app.app_context():
    db.session.add(item1)
    db.session.commit()

###            OR if any mistake
with app.app_context():
    db.session.rollback()
###

with app.app_context():
    items = Item.query.all()
    users = User.query.all()

with app.app_context():
    for item in Item.query.all():
        item.entity
        item.type
        item.locatedat
        item.datecreated
        item.modifiedat
        item.entityversion
        item.devicecategory
        item.id




    D:\Users\cem\data\git\namespace3\venv\Scripts\python.exe "C:\Users\cem\AppData\Local\JetBrains\PyCharm Community Edition 2022.1.2\plugins\python-ce\helpers\pydev\pydevconsole.py" --mode=client --port=61120
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['D:\\Users\\cem\\data\\git\\namespace3', 'D:/Users/cem/data/git/namespace3'])
Python 3.9.0 (tags/v3.9.0:9cf6752, Oct  5 2020, 15:34:40) [MSC v.1927 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.5.0 -- An enhanced Interactive Python. Type '?' for help.
PyDev console: using IPython 8.5.0
Python 3.9.0 (tags/v3.9.0:9cf6752, Oct  5 2020, 15:34:40) [MSC v.1927 64 bit (AMD64)] on win32
from ontoML import db
from ontoML import app
with app.app_context():
    db.drop_all()    
        
with app.app_context():
    db.create_all()    
        
from ontoML.models import Item
item1 =Item(entity="meter", type="equipmentContainer", locatedat='substation:rdnsubstation001', datecreated="2017-05-04T12:30:00Z", modifiedat= "2022-05-18T13:45:30Z", entityversion=2, devicecategory='grid-related')
with app.app_context():
    db.session.add(item1)
    db.session.commit()
with app.app_context():
    itemde = Item.query.all()
itemde
Out[10]: [Item meter]
item2 =Item(entity="pmu", type="equipmentContainer", locatedat='substation:rdnsubstation002', datecreated="2017-05-05T12:30:00Z", modifiedat= "2022-05-19T13:45:30Z", entityversion=3, devicecategory='grid-related')
with app.app_context():
    db.session.add(item2)
    db.session.commit()
item3 =Item(entity="stringbox", type="equipmentContainer", locatedat='substation:rdnsubstation003', datecreated="2017-05-06T12:30:00Z", modifiedat= "2022-05-20T13:45:30Z", entityversion=4, devicecategory='grid-related')
with app.app_context():
    db.session.add(item3)
    db.session.commit()
item4 =Item(entity="inverter", type="equipmentContainer", locatedat='substation:rdnsubstation004', datecreated="2017-05-07T12:30:00Z", modifiedat= "2022-05-21T13:45:30Z", entityversion=5, devicecategory='grid-related')
with app.app_context():
    db.session.add(item4)
    db.session.commit()
with app.app_context():
    itemde = Item.query.all()
itemde
Out[18]: [Item meter, Item pmu, Item stringbox, Item inverter]
with app.app_context():
    for item in Item.query.all():
        item.entity
        item.type
        item.locatedat
        item.datecreated
        item.modifiedat
        item.entityversion
        item.devicecategory
        item.id
    
item.entity
Out[20]: 'inverter'
item.type
Out[21]: 'equipmentContainer'
import os
os.system('cls')
Out[23]: 0
Item.query.filter_by(entityversion=2)


#################### Database Creation Batch commands##################
from ontoML import db
from ontoML import app
with app.app_context():
    db.drop_all()
with app.app_context():
    db.create_all()
from ontoML.models import Item
item1 = Item(entity="meter", type="equipmentContainer", locatedat='substation:rdnsubstation001',
             datecreated="2017-05-04T12:30:00Z", modifiedat="2022-05-18T13:45:30Z", entityversion=2,
             devicecategory='grid-related')
with app.app_context():
    db.session.add(item1)
    db.session.commit()
item2 = Item(entity="pmu", type="equipmentContainer", locatedat='substation:rdnsubstation002',
             datecreated="2017-05-05T12:30:00Z", modifiedat="2022-05-19T13:45:30Z", entityversion=3,
             devicecategory='grid-related')
with app.app_context():
    db.session.add(item2)
    db.session.commit()
    
item3 = Item(entity="stringbox", type="equipmentContainer", locatedat='substation:rdnsubstation003',
             datecreated="2017-05-06T12:30:00Z", modifiedat="2022-05-20T13:45:30Z", entityversion=4,
             devicecategory='grid-related')
with app.app_context():
    db.session.add(item3)
    db.session.commit()
item4 = Item(entity="inverter", type="equipmentContainer", locatedat='substation:rdnsubstation004',
             datecreated="2017-05-07T12:30:00Z", modifiedat="2022-05-21T13:45:30Z", entityversion=5,
             devicecategory='grid-related')
with app.app_context():
    db.session.add(item4)
    db.session.commit()

from ontoML.models import User
user1 = User(username='Charles', password_hash='123456', email_address='cemehel@gmail.com')
user2 = User(username='Alex', password_hash='123456', email_address='alex@gmail.com')
user3 = User(username='Amaris', password_hash='123456', email_address='amaris@gmail.com')
user4 = User(username='Ariel', password_hash='123456', email_address='ariel@gmail.com')
user5 = User(username='Elon', password_hash='123456', email_address='elon@gmail.com')
with app.app_context():
    db.session.add(user1)
    db.session.commit()
with app.app_context():
    db.session.add(user2)
    db.session.commit()
with app.app_context():
    db.session.add(user3)
    db.session.commit()
with app.app_context():
    db.session.add(user4)
    db.session.commit()
with app.app_context():
    db.session.add(user5)
    db.session.commit()

with app.app_context():
    items = Item.query.all()
    users = User.query.all()



with app.app_context():
    item1 = Item.query.filter_by(entity='meter')

import os
os.urandom(12).hex()
Out[3]: 'aa6c3448b51c3c8030952387'


pip install email_validator
Collecting email_validator
  Downloading email_validator-1.3.0-py2.py3-none-any.whl (22 kB)
Requirement already satisfied: idna>=2.0.0 in c:\users\cem\appdata\local\programs\python\python39\lib\site-packages (from email_validator) (3.4)
Collecting dnspython>=1.15.0
  Downloading dnspython-2.3.0-py3-none-any.whl (283 kB)
Installing collected packages: dnspython, email-validator
Successfully installed dnspython-2.3.0 email-validator-1.3.0
WARNING: You are using pip version 21.3.1; however, version 22.3.1 is available.
You should consider upgrading via the 'D:\Users\cem\data\git\namespace3\venv\Scripts\python.exe -m pip install --upgrade pip' command.
Note: you may need to restart the kernel to use updated packages.
