import os
import sys
import subprocess

# define GRASS Database
# add your path to grassdata (GRASS GIS database) directory
gisdb = os.path.join(os.path.expanduser("~"), "grassdata")
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")

# specify (existing) Location and Mapset
location = "idaho_idtm83"
mapset   = "IDlandcover"


# path to the GRASS GIS launch script
# we assume that the GRASS GIS start script is available and on PATH
# query GRASS itself for its GISBASE
# (with fixes for specific platforms)
# needs to be edited by the user
grass7bin = 'grass72'
if sys.platform.startswith('win'):
    # MS Windows
    grass7bin = r'D:\OSGeo4W64\bin\grass72.bat'
    # uncomment when using standalone WinGRASS installer
    # grass7bin = r'C:\Program Files (x86)\GRASS GIS 7.0.0\grass70.bat'
    # this can be avoided if GRASS executable is added to PATH
elif sys.platform == 'darwin':
    # Mac OS X
    # TODO: this have to be checked, maybe unix way is good enough
    grass7bin = '/Applications/GRASS/GRASS-7.0.app/'

# query GRASS GIS itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']
try:
    p = subprocess.Popen(startcmd, shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except OSError as error:
    sys.exit("ERROR: Cannot find GRASS GIS start script"
             " {cmd}: {error}".format(cmd=startcmd[0], error=error))
if p.returncode != 0:
    sys.exit("ERROR: Issues running GRASS GIS start script"
             " {cmd}: {error}"
             .format(cmd=' '.join(startcmd), error=err))
gisbase = out.strip(os.linesep)

# set GISBASE environment variable
os.environ['GISBASE'] = gisbase

# define GRASS-Python environment
grass_pydir = os.path.join(gisbase, "etc", "python")
sys.path.append(grass_pydir)

# import (some) GRASS Python bindings
import grass.script as gscript
import grass.script.setup as gsetup

# launch session
rcfile = gsetup.init(gisbase, gisdb, location, mapset)

# example calls
gscript.message('Current GRASS GIS 7 environment:')
print gscript.gisenv()

gscript.message('Available raster maps:')
for rast in gscript.list_strings(type='raster'):
    print rast

gscript.message('Available vector maps:')
for vect in gscript.list_strings(type='vector'):
    print vect

# delete the rcfile
os.remove(rcfile)