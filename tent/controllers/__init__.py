from flask import Blueprint, current_app

from tent.controllers.base_controller import hello

base_bp = Blueprint('', 'api', url_prefix='')

base_url_rules = [('/', hello, ['GET'])]


for (rule, func, methods) in base_url_rules:
    base_bp.add_url_rule(rule, view_func=func, methods=methods)
