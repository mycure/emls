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
  sys.stdout.write("[ems::usage] insert _id_ _file_\n")
  sys.exit(1)

#
# this function takes a list of emails and insert them in the
# given mailing-list configuration.
#
def                     Insert(conf, emails):
  email = None

  # for every email.
  for email in emails:
    key = None

    # generate a key.
    key = ems.Misc.Generate(32)

    # add the user to the list of members.
    conf.members[email] = { "type": ems.TypeUser,
                            "behaviour": ems.BehaviourContributor,
                            "key": key }

    try:
      # finally, tell the user that her subscription went through.
      ems.Misc.Send(conf.address,
                    [ email ],
                    ems.TemplateSubscription,
                    { "<DATE>": ems.Misc.Date(),
                      "<FROM>": conf.address,
                      "<TO>": email,
                      "<REPLY-TO>": conf.addresses["confirm"],
                      "<MAILING-LIST>": conf.id,

                      "<ADDRESS>": conf.address,
                      "<DESCRIPTION>": conf.description,
                      "<ADDRESS:SUBSCRIBE>": conf.addresses["subscribe"],
                      "<ADDRESS:ADMIN>": conf.addresses["admin"],
                      "<ADDRESS:CONFIRM>": conf.addresses["confirm"] })

      # print a message.
      print "[success] " + email
    except:
      # print a message.
      print "[failure] " + email

#
# this function extracts emails from the given file.
#
def                     Extract(file):
  contents = None
  emails = None

  # read the file.
  contents = ems.Misc.Pull(file).strip(" \n")

  # split the contents according to the line delimiter.
  emails = contents.split("\n")

  return emails

#
# this is the main function.
#
def                     Main():
  conf = None
  file = None
  id = None
  emails = None

  # retrieve the argument.
  if len(sys.argv) != 3:
    Usage()

  id = sys.argv[1]
  file = sys.argv[2]

  # check if the mailing-list already exist and create it if not.
  if os.path.exists(ems.ListsLocation + id) == False:
    sys.stderr.write("[ems::error] the mailing-list does not seem to exist\n")
    sys.exit(1)

  # create a configuration object.
  conf = ems.Configuration(id)

  # load the configuration object.
  if conf.Load() == ems.StatusError:
    sys.stderr.write("[ems::error] an error occured while loading the conf file\n")
    sys.exit(1)

  # extract the emails from the given file.
  emails = Extract(file)

  # insert the emails.
  Insert(conf, emails)

  # finally store the modifications applied on to the configuration.
  if conf.Store() == ems.StatusError:
    ems.Misc.Log("[ems::error] an error occured while storing the queue file")
    sys.exit(0)

#
# ---------- entry point ------------------------------------------------------
#
if __name__ == "__main__":
  Main()
