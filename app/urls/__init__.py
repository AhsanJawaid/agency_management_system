from app.urls import index
from app.urls import reports
from app.urls import tasks

from flask import render_template

render_template('/tasks/new_tasks.html')