import logging
import pkg_resources
import requests

import mapzen.whosonfirst.utils

import wof.validate

# things starting with 'check_' return True or False
# things starting with 'ensure_' return None if True or sys.exit(1)

def check_is_wofdata():

   root = os.getcwd()
   base = os.path.basename(root)

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

def ensure_is_wofdata():

   if not check_is_wofdata():
      sys.exit(1)

def ensure_hooks_cfg():
   pass

def ensure_pylibs():

   if not check_pylibs():
      sys.exit(1)

def ensure_valid_wof_documents(files):

   if not wof.validate.validate_files(repo, files):
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

   _modified, _created = wof.meta.update_metafiles(base, updated)

   for path in _modified:
      path = path.replace(base + "/", "")
      modified.append(path)

   for path in _created:
      path = path.replace(base + "/", "")
      created.append(path)

   _modified, _created = wof.concordances.update_concordances(base, updated)

   for path in _modified:
      path = path.replace(base + "/", "")
      modified.append(path)
      
   for path in _created:
      path = path.replace(base + "/", "")
      created.append(path)

   return modified, created
