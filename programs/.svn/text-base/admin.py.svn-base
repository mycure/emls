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
  sys.stdout.write("[ems::usage] confirm.py [mailing-list]\n")
  sys.exit(0)

#
# this function returns the help to the sender.
#
def                     Help(conf, queue, email, command):
  # send the help according to the type of user: member or manager.
  if email.issuer == conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminManagerHelp,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminMemberHelp,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })

#
# this function returns a human-readable dump of the mailing-list
# configuration and queue.
#
def                     Dump(conf, queue, email, command):
  contents = None
  token = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # build the configuration dump.
  contents = "---[ Configuration\n"
  contents += "\n"
  contents += "[id] " + conf.id + "\n"
  contents += "[address] " + conf.address + "\n"
  contents += "\n"
  contents += "[description] " + conf.description + "\n"
  contents += "\n"
  contents += "[tag] " + conf.tag + "\n"
  contents += "\n"
  contents += "[policies]\n"
  contents += "  [membership] " + conf.policies["membership"] + "\n"
  contents += "  [control] " + conf.policies["control"] + "\n"
  contents += "\n"
  contents += "[manager]\n"
  contents += "  [address] " + conf.manager["address"] + "\n"
  contents += "  [key] " + conf.manager["key"] + "\n"

  if conf.members:
    contents += "\n"
    contents += "[members]\n"

    for member in conf.members:

      if conf.members[member]["type"] == ems.TypeUser:
        contents += "  [user]\n"
        contents += "    [address] " + member + "\n"
        contents += "    [behaviour] " + conf.members[member]["behaviour"] + "\n"
        contents += "    [key] " + conf.members[member]["key"] + "\n"
      elif conf.members[member]["type"] == ems.TypeList:
        contents += "  [list]\n"
        contents += "    [id] " + member + "\n"
      else:
        contents += "  [error::undefined]\n"
        contents += "    " + member + " :: " + str(conf.members[member]) + "\n"

  contents += "\n"

  # build the queue dump.
  contents += "---[ Queue\n"
  contents += "\n"

  if queue.tokens:
    contents += "[tokens]\n"
    for token in queue.tokens:
      contents += "  [id] " + token + "\n"
      contents += "    " + str(queue.tokens[token]) + "\n"

  # finally send the dump.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateAdminDump,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["admin"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<CONTENTS>": contents })

#
# this function adds a member to the list.
#
def                     Add(conf, queue, email, command):
  key = None
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # check the arguments.
  if not command.arguments["behaviour"] in [ ems.BehaviourListener, ems.BehaviourSpeaker, ems.BehaviourContributor ]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # generate a key.
  key = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionAdd,
                       "member": { "address": command.arguments["address"], "behaviour": command.arguments["behaviour"], "key": key },
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to add the user '" + command.arguments["address"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function adds a list to the list.
#
def                     Insert(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionInsert,
                       "member": command.arguments["id"],
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to insert the list '" + command.arguments["id"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function edits a member.
#
def                     Edit(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # check the arguments.
  if not command.arguments["behaviour"] in [ ems.BehaviourListener, ems.BehaviourSpeaker, ems.BehaviourContributor ]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionEdit,
                       "member": { "address": command.arguments["address"], "behaviour": command.arguments["behaviour"] },
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to edit the user '" + command.arguments["address"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function removes an entry.
#
def                     Remove(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # check if the entry exists.
  if (command.arguments["member"] in conf.members) and                  \
     (conf.members[command.arguments["member"]]["type"] != ems.TypeUser):
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionRemove,
                       "member": command.arguments["member"],
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to remove member '" + command.arguments["member"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function edits the description.
#
def                     Description(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionDescription,
                       "description": command.arguments["description"],
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to set the description to '" + command.arguments["description"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function edits the tag.
#
def                     Tag(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionTag,
                       "tag": command.arguments["tag"],
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to set the tag to '" + command.arguments["tag"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function changes the membership policy.
#
def                     Membership(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # check the arguments.
  if not command.arguments["policy"] in [ ems.PolicyMembershipPublic, ems.PolicyMembershipModerated, ems.PolicyMembershipPrivate ]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionMembership,
                       "policy": command.arguments["policy"],
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to set the membership policy to '" + command.arguments["policy"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function changes the control policy.
#
def                     Control(conf, queue, email, command):
  id = None

  # if the email does not come from the manager, return an error.
  if email.issuer != conf.manager["address"]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnallowedCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # check the arguments.
  if not command.arguments["policy"] in [ ems.PolicyControlOpen, ems.PolicyControlFiltered ]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionControl,
                       "policy": command.arguments["policy"],
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to set the control policy to '" + command.arguments["policy"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function returns a human-readable dump of the subscription.
#
def                     Show(conf, queue, email, command):
  contents = None

  # build the contents.
  contents = "    [address] " + email.issuer + "\n"
  contents += "    [behaviour] " + conf.members[email.issuer]["behaviour"] + "\n"
  contents += "    [key] " + conf.members[email.issuer]["key"] + "\n"

  # finally send the dump.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateAdminShow,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["admin"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<CONTENTS>": contents })

#
# this function unsubscribes a user.
#
def                     Unsubscribe(conf, queue, email, command):
  id = None

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionUnsubscribe,
                       "member": email.issuer,
                       "requirements": [ ems.RequirementMember ] }

  # notify the user.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to unsubscribe from the mailing-list",
                  "<ID>": id,
                  "<KEY>": conf.members[email.issuer]["key"] })

#
# this function modifies the behaviour of the calling user.
#
def                     Behaviour(conf, queue, email, command):
  id = None

  # check the arguments.
  if not command.arguments["behaviour"] in [ ems.BehaviourListener, ems.BehaviourSpeaker, ems.BehaviourContributor ]:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # generate an id.
  id = ems.Misc.Generate(32)

  # create an entry in the queue file.
  queue.tokens[id] = { "action": ems.ActionBehaviour,
                       "member": { "address": email.issuer, "behaviour": command.arguments["behaviour"] },
                       "requirements": [ ems.RequirementMember ] }

  # notify the user.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateAdminConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ACTION>": "Trying to change your behaviour to '" + command.arguments["behaviour"] + "'",
                  "<ID>": id,
                  "<KEY>": conf.members[email.issuer]["key"] })

#
# this function admins the mailing-list according to the given command.
#
def                     Admin(conf, queue, email):
  users = None
  command = None
  arguments = None

  # check if the subscriber is already registered.
  if (conf.manager["address"] != email.issuer) and (not email.issuer in conf.members):
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorNotSubscribed,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ADDRESS:SUBSCRIBE>": conf.addresses["subscribe"] })
    return

  # retrieve the operation from the email.
  command = ems.Command(email)
  command.Locate()

  if not command.arguments:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorBadCommand,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["admin"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # dispatch.
  if command.arguments["action"] == ems.ActionHelp:
    Help(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionDump:
    Dump(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionAdd:
    Add(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionAdd:
    Add(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionInsert:
    Insert(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionEdit:
    Edit(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionRemove:
    Remove(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionDescription:
    Description(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionTag:
    Tag(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionMembership:
    Membership(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionControl:
    Control(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionShow:
    Show(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionUnsubscribe:
    Unsubscribe(conf, queue, email, command)
  elif command.arguments["action"] == ems.ActionBehaviour:
    Behaviour(conf, queue, email, command)

#
# this is the main function.
#
def                     Main():
  conf = None
  queue = None
  email = None
  user = None
  id = None

  # retrieve the argument.
  if len(sys.argv) != 2:
    Usage()

  # set the id.
  id = sys.argv[1]

  # retrieve a configuration object.
  conf = ems.Configuration(id)
  if conf.Load() == ems.StatusError:
    ems.Misc.Log("[ems::error] unable to load the configuration file '" +
                 id + "'")
    sys.exit(0)

  # retrive the queue object.
  queue = ems.Queue(id)
  if queue.Load() == ems.StatusError:
    ems.Misc.Log("[ems::error] unable to load the queue file '" + id + "'")
    sys.exit(0)

  # retrieve the email.
  email = ems.Email()
  if email.Catch() == ems.StatusError:
    ems.Misc.Log("[ems::error] unable to catch the incoming email")
    sys.exit(0)

  # try to perform the requested action.
  Admin(conf, queue, email)

  # update both the configuration and the queue.
  if queue.Store() == ems.StatusError:
    ems.Misc.Log("[ems::error] an error occured while storing the queue file")
    sys.exit(0)

  if conf.Store() == ems.StatusError:
    ems.Misc.Log("[ems::error] an error occured while storing the queue file")
    sys.exit(0)

#
# ---------- entry point ------------------------------------------------------
#
if __name__ == "__main__":
  Main()
