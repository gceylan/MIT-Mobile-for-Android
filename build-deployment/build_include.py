import os
import shutil
import commands
import sys
import build_settings
import time

VERSION_NUMBER = 6
VERSION_NAME = "2.1"

# a wrapper to make it harder to silently ignore errors
def shell(command, silent=False):
   print command
   #DEBUG
   import subprocess as sub
   p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
   output = p.communicate()
   print "output = " + str(output)
   #DEBUG
   
   return output[0].strip()
   
   #ret = os.system(command)
   #print "ret = " + ret
   #statusoutput = commands.getstatusoutput(command)
   #print statusoutput
   #if not silent:
   #    print statusoutput[1]


   #if statusoutput[0] != 0:
   #   raise Exception("Error executing shell commmand")

   return statusoutput[1]



# generate a source code file that contains
# constants which are build compile time settings
def write_build_settings(build_settings_dictionary):

    build_class_source = """
         package edu.mit.mitmobile2.about;
         
         

         public class BuildSettings {
              public final static String BUILD_ID = "%(build_id)s";
              public final static String BUILDER = "%(builder)s";
              public final static String BUILD_SOURCE = "%(build_source)s";
              public final static String TAG = %(tag_literal)s;
              public final static long BUILD_TIME = %(build_time)iL;
              public final static String MOBILE_WEB_DOMAIN = "%(mobile_web_domain)s";
              public final static String VERSION_NAME = "%(version_name)s";
              public final static String NEWS_OFFICE_PATH = "%(news_office_path)s";
              public final static boolean VERBOSE_LOGGING = %(verbose_logging)s;
              public final static String BUILD_TAG = "%(build_tag)s";
         }
	""" % build_settings_dictionary
    build_settings_file = open("src/edu/mit/mitmobile2/about/BuildSettings.java", "w")
    build_settings_file.write(build_class_source)
    build_settings_file.close()
    build_settings_resource_source = """<?xml version="1.0" encoding="utf-8"?><resources>
               <string name="googleMapsApiKey">%(google_maps_api_key)s</string>
               <integer name="versionNumber">%(version_number)i</integer>
               <string name="versionName">%(version_name)s</string>
    </resources>
    """ % build_settings_dictionary

    build_settings_resource_file = open("res/values/build_settings_resource.xml", "w")
    build_settings_resource_file.write(build_settings_resource_source)
    build_settings_resource_file.close()

    

# generate the local.settings build file
def write_local_properties(android_sdk_path):
    local_properties_text = """
       # This file is automatically generated
       # Do not modify this file -- YOUR CHANGES WILL BE ERASED!
       # 
       # This file must *NOT* be checked in Version Control Systems,
       # as it contains information specific to your local configuration.

       # location of the SDK. This is only used by Ant
       # For customization when using a Version Control System, please read the
       # header note.
       sdk.dir=%s\n""" % android_sdk_path

    local_properties_file = open("local.properties", "w")
    local_properties_file.write(local_properties_text)
    local_properties_file.close()

def build_source(builder, tag, fresh_repository):
   inital_cwd = os.getcwd()
   print inital_cwd
   if not tag:
      build_id = shell("git rev-parse HEAD", True)     
      build_source = "local code"
   else:
      if fresh_repository:
         tmp_tag_path = '/tmp/MIT-Mobile-%s' % tag

         if os.path.exists(tmp_tag_path):
            shutil.rmtree(tmp_tag_path)

         os.system('git clone %s %s/' % (git_repository, tmp_tag_path))

         # make the android project folder the current working directory
         os.chdir(tmp_tag_path)
         shell("git checkout " + tag)
         build_id = shell("git rev-parse HEAD", True)
         build_source = "repository"
      else:
         # shell("git pull", False)
         shell("git checkout %s" % tag, False)
         build_id = shell("git rev-parse HEAD", True)     
         build_source = "local code"
      
   if tag:
       tag_literal = '"' + tag + '"'
   else:
       tag_literal = 'null'

   if build_settings.verbose_logging:
       verbose_logging_literal = 'true'
   else:
       verbose_logging_literal = 'false'

   write_local_properties(build_settings.android_sdk_path)
   write_build_settings({
       "build_id" : build_id,
       "build_source" : build_source,
       "builder" : builder,
       "tag_literal" : tag_literal,
       "build_time" : (int) (time.time() * 1000),  # unixtime in miliseconds
       "mobile_web_domain" : build_settings.mobile_web_domain,
       "google_maps_api_key" : build_settings.google_maps_api_key,
       "version_number" : VERSION_NUMBER,
       "version_name" : VERSION_NAME,
       "news_office_path" : build_settings.news_office_path,
       "verbose_logging" : verbose_logging_literal,
       "build_tag" : build_settings.build_tag,
   })

   project_path = os.getcwd()
   os.chdir(inital_cwd)
   return project_path

def build_apk(tag, fresh_repository):
   initial_cwd = os.getcwd()

   project_path = build_source("ant", tag, fresh_repository)

   os.chdir(project_path)

   if os.path.exists("bin"):
      shutil.rmtree("bin")

   os.system("ant debug")

   os.chdir(initial_cwd)
   return project_path

    



    

