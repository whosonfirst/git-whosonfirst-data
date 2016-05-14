import os
import sys
import logging

import pkg_resources
import requests

import ConfigParser

import mapzen.whosonfirst.utils

import validate
import meta
import concordances

# things starting with 'check_' return True or False
# things starting with 'ensure_' will invoke sys.exit(1) if False

def check_is_wof_repo(repo=None):

   if not repo:
      repo = os.getcwd()

   base = os.path.basename(repo)

   if not base.startswith("whosonfirst-data"):
      return False

   return True

def check_pylibs():

   pymz = pkg_resources.get_distribution("mapzen.whosonfirst").version
   pymz = pymz.rstrip("-")

   current = None

   try:
      logging.info("I am going to try and see whether you are using the most recent version of py-mapzen-whosonfirst...")

      rsp = requests.get("https://raw.githubusercontent.com/whosonfirst/py-mapzen-whosonfirst/master/VERSION")
      current = rsp.content
      current = current.strip()

   except Exception, e:
      logging.warning("Failed to determine ACTUAL current version of py-mapzen-whosonfirst, because %s (setting current to %s for now but don't be surprised if HILARITY ensues...)" % (e, pymz))
      current = pymz

   if pymz != current:
      logging.warning("You are running version %s of py-mapzen-whosonfirst but the current version is %s - you should update because HILARITY may ensue if you don't" % (pymz, current))
      return False

   return True

def ensure_is_wof_repo(repo=None):

   if not check_is_wof_repo(repo=None):
      sys.exit(1)

def ensure_hooks_cfg(whoami, options_config):

   if not options_config:

      hooks = os.path.dirname(whoami)
      path_config = os.path.join(hooks, 'hooks.cfg')

   else:
      path_config = os.path.abspath(options_config)

   if not os.path.exists(path_config):
      logging.error("INVISIBLE CONFIG FILE %s" % path_config)
      sys.exit(1)

   cfg = ConfigParser.ConfigParser()
   cfg.read(path_config)

   return cfg

def ensure_pylibs():

   if not check_pylibs():
      sys.exit(1)

def ensure_valid_wof_documents(base, files):

   if not validate.validate_files(base, files):
      logging.error("one or more files failed validation")
      sys.exit(1)

def filter_for_wof_documents(files):

   docs = []

   for fname in files:

      parsed = mapzen.whosonfirst.utils.parse_filename(fname)

      if not parsed:
         continue

      id, suffix = parsed

      if suffix:
         logging.info("%s has a suffix (%s) so skipping" % (fname, suffix))
         continue
            
      docs.append(fname)

   return docs

def update_ancillary_files(base, updated):

   modified = []
   created = []

   _modified, _created = meta.update_metafiles(base, updated)

   for path in _modified:
      path = path.replace(base + "/", "")
      modified.append(path)

   for path in _created:
      path = path.replace(base + "/", "")
      created.append(path)

   _modified, _created = concordances.update_concordances(base, updated)

   for path in _modified:
      path = path.replace(base + "/", "")
      modified.append(path)
      
   for path in _created:
      path = path.replace(base + "/", "")
      created.append(path)

   return modified, created
