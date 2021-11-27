from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from numpy import integer
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()
ma = Marshmallow()
