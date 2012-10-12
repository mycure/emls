#! /usr/bin/python

#
# ---------- packages ---------------------------------------------------------
#

import ems

import sys
import re
import os

#
# ---------- functions --------------------------------------------------------
#

#
# this function displays the usage.
#
def                     Usage():
  sys.stdout.write("[ems::usage] create.py\n")
  sys.exit(1)

#
# this function inform the user of the general information
# and the next steps he/she has to go through.
#
def                     Inform(conf, queue):
  address = None

  sys.stdout.write("\n\n\n")

  sys.stdout.write("Below are summarised the mailing-list informations:\n")
  sys.stdout.write("  [id] " + conf.id + "\n")
  sys.stdout.write("  [address] " + conf.address + "\n")
  sys.stdout.write("  [description] " + conf.description + "\n")
  sys.stdout.write("  [tag] " + conf.description + "\n")
  sys.stdout.write("  [manager] " + conf.manager["address"] + "\n")

  sys.stdout.write("\n\n\n")

  address = conf.address.split("@")

  sys.stdout.write("Now, you need to add the following piece of code to\n")
  sys.stdout.write("the 'regexp:' file specified in the 'virtual_alias_map'\n")
  sys.stdout.write("of your Postfix 'main.cf' configuration file:\n")

  sys.stdout.write("\n")

  sys.stdout.write("#\n# " + conf.address + "\n#\n")
  sys.stdout.write("/^" + address[0] + "\\+(subscribe|confirm|admin)@" +
                   address[1] + "$/   ems_$1+" + conf.id + "\n")
  sys.stdout.write("/^" + conf.address + "$/   ems_post+" + conf.id + "\n")
  sys.stdout.write("/^" + address[0] + "\\+.*@" + address[1] +
                   "$/   ems_post+" + conf.id + "\n")

#
# this function asks the user information about the
# mailing-list he/she wants to create.
#
def                     Ask():
  address = None
  id = None
  description = None
  membership = None
  control = None
  tag = None
  manager = None
  key = None

  # mailing-list address.
  sys.stdout.write("mailing-list address []: ")
  address = sys.stdin.readline().strip("\n")
  if (len(address) == 0) or (address.find("@") == -1):
    sys.stderr.write("[ems::error] incorrect mailing-list email address")
    sys.exit(1)

  # mailing-list identifier.
  id = address.replace("@", ".")

  # description.
  sys.stdout.write("description []: ")
  description = sys.stdin.readline().strip("\n")

  # membership policy.
  sys.stdout.write("membership policy (public, moderated or private) [public]: ")
  membership = sys.stdin.readline().strip("\n")
  if (membership != "public") and (membership != "moderated") and (membership != "private"):
    membership = "public"

  # control policy.
  sys.stdout.write("control policy (open, filtered) [open]: ")
  control = sys.stdin.readline().strip("\n")
  if (control != "open") and (control != "filtered"):
    control = "open"

  # tag.
  sys.stdout.write("tag []: ")
  tag = sys.stdin.readline().strip("\n")

  # manager email address.
  sys.stdout.write("manager email address []: ")
  manager = sys.stdin.readline().strip("\n")
  if (len(manager) == 0) or (manager.find("@") == -1):
    sys.stderr.write("[ems::error] incorrect manager's email address")
    sys.exit(1)

  # generate a key for the manager.
  key = ems.Misc.Generate(32)

  return (address, id, description, membership, control, tag, manager, key)

#
# this is the main function.
#
def                     Main():
  conf = None
  queue = None
  email = None

  address = None
  id = None
  description = None
  membership = None
  control = None
  tag = None
  manager = None
  key = None

  # ask the user for the mailing-list informations.
  (address, id, description, membership, control, tag, manager, key) = Ask()

  # check if the mailing-list already exist and create it if not.
  if os.path.exists(ems.ListsLocation + id):
    sys.stderr.write("[ems::error] the mailing-list seems to exist already\n")
    sys.exit(1)

  os.mkdir(ems.ListsLocation + id)

  # create a configuration object.
  conf = ems.Configuration(id)

  conf.id = id
  conf.address = address
  conf.description = description
  conf.policies = { "membership": membership, "control": control }
  conf.tag = tag
  conf.manager = { "address": manager, "key": key }
  conf.members = {}

  # create the queue object.
  queue = ems.Queue(id)

  queue.id = id
  queue.tokens = {}

  # serialise the configuration object.
  if conf.Store() == ems.StatusError:
    sys.stderr.write("[ems::error] an error occured while storing the configuration file\n")
    sys.exit(1)

  # serialise the queue object.
  if queue.Store() == ems.StatusError:
    sys.stderr.write("[ems::error] an error occured while storing the queue file\n")
    sys.exit(1)

  # inform the user of the next steps.
  Inform(conf, queue)

#
# ---------- entry point ------------------------------------------------------
#
if __name__ == "__main__":
  Main()
