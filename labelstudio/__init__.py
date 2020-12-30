from jinja2 import Template

from .TaskList import *

def generate_configuration(entities):
    #todo env defining where giacore is located?
    return Template(open('giacore/labelstudio/entity-choise.xml').read()).render(labels=entities)
