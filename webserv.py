import random
import string
import os
from cherrypy.lib.static import serve_file
from mako.template import Template
from mako.lookup import TemplateLookup
import cherrypy.process.plugins
import cherrypy

class Main(object):



    @cherrypy.expose
    def index(self):
        mylookup = TemplateLookup(directories=['/'])
        t = Template(filename='index.mako',lookup=mylookup)

        return t.render().replace("\n","")

    @cherrypy.expose
    def img(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return serve_file(os.getcwd()+'/bg.jpg')



def update():
   os.system("C:\Python27\python.exe ifs_db_magic.py")
   print "updating table"


if __name__ == '__main__':

    wd = cherrypy.process.plugins.BackgroundTask(30,update)
    wd.start()
    cherrypy.quickstart(Main(),'/', 'c.conf')