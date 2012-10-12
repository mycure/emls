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
# this function tries to confirm a subscription.
#
def                     Subscribe(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  elif (ems.RequirementMember in token["requirements"]) and             \
       (token["member"]["address"] == email.issuer) and                 \
       (token["member"]["key"] == key.argument):
    token["requirements"].remove(ems.RequirementMember)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # add the user to the list of members.
    conf.members[token["member"]["address"]] = { "type": ems.TypeUser,
                                                 "behaviour": token["member"]["behaviour"],
                                                 "key": token["member"]["key"] }

    # delete the queue token.
    del queue.tokens[id.argument]

    # finally, tell the user that her subscription went through.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateSubscription,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<DESCRIPTION>": conf.description,
                    "<ADDRESS:SUBSCRIBE>": conf.addresses["subscribe"],
                    "<ADDRESS:ADMIN>": conf.addresses["admin"],
                    "<ADDRESS:CONFIRM>": conf.addresses["confirm"] })

#
# this function tries to confirm a post.
#
def                     Post(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # post the message.
    ems.Misc.Send(token["message"]["address"],
                  conf.Listeners().keys(),
                  ems.TemplateRaw,
                  { "<CONTENTS>": token["message"]["contents"] })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a add operation.
#
def                     Add(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # add the user to the list of members.
    conf.members[token["member"]["address"]] = { "type": ems.TypeUser,
                                                 "behaviour": token["member"]["behaviour"],
                                                 "key": token["member"]["key"] }

    # finally, tell the user to her subscription went through.
    ems.Misc.Send(conf.address,
                  [ token["member"]["address"] ],
                  ems.TemplateSubscription,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": token["member"]["address"],
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<DESCRIPTION>": conf.description,
                    "<ADDRESS:SUBSCRIBE>": conf.addresses["subscribe"],
                    "<ADDRESS:ADMIN>": conf.addresses["admin"],
                    "<ADDRESS:CONFIRM>": conf.addresses["confirm"] })

    # but also to the manager who added the user.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The member '" + token["member"]["address"] +
                                  "' has been added to the following mailing-list:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a insert operation.
#
def                     Insert(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # add the user to the list of members.
    conf.members[token["member"]] = { "type": ems.TypeList }

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The list '" + token["member"] +
                                  "' has been added to the following mailing-list:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a edit operation.
#
def                     Edit(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # edit the user.
    if token["member"]["address"] in conf.members:
      conf.members[token["member"]["address"]]["behaviour"] = token["member"]["behaviour"]

    # notify the mananger.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The member '" + token["member"]["address"] +
                                  "' from the following mailing-list has been edited successfully:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a remove operation.
#
def                     Remove(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # remove the user.
    if token["member"] in conf.members:
      del conf.members[token["member"]]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The member '" + token["member"] +
                                  "' has been removed from the following mailing-list:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a description operation.
#
def                     Description(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # edit the description.
    conf.description = token["description"]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The description of the following mailing-list has been modified:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a tag operation.
#
def                     Tag(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # edit the description.
    conf.tag = token["tag"]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The tag of the following mailing-list has been modified:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a membership operation.
#
def                     Membership(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # edit the description.
    conf.policies["membership"] = token["policy"]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The membership policy of the following mailing-list has been modified:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a control operation.
#
def                     Control(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementManager in token["requirements"]) and              \
     (conf.manager["address"] == email.issuer) and                      \
     (conf.manager["key"] == key.argument):
    token["requirements"].remove(ems.RequirementManager)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # edit the description.
    conf.policies["control"] = token["policy"]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "The control policy of the following mailing-list has been modified:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm an unsubscription.
#
def                     Unsubscribe(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementMember in token["requirements"]) and               \
     (token["member"] == email.issuer) and                              \
     (conf.members[token["member"]]["key"] == key.argument):
    token["requirements"].remove(ems.RequirementMember)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # remove the user.
    if token["member"] in conf.members:
      del conf.members[token["member"]]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "You have been unsubscribed from the following mailing-list with success:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function tries to confirm a behaviour operation.
#
def                     Behaviour(conf, queue, email, id, key):
  token = None

  # retrive the token.
  token = queue.tokens[id.argument]

  # try to reduce the requirements by updating the list of
  # reqirements every time a confirmation comes in.
  if (ems.RequirementMember in token["requirements"]) and               \
     (token["member"]["address"] == email.issuer) and                   \
     (conf.members[token["member"]["address"]]["key"] == key.argument):
    token["requirements"].remove(ems.RequirementMember)
  else:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownConfirmation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ID>": id.argument,
                    "<ADDRESS>": conf.address })
    return

  # then, if all the requirements have been met, perform the operation.
  if ems.RequirementNone == token["requirements"]:
    # edit the user's behaviour.
    if token["member"]["address"] in conf.members:
      conf.members[token["member"]["address"]]["behaviour"] = token["member"]["behaviour"]

    # notify the manager.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateAdminApplication,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<CONTENTS>": "Your behaviour have been modified on the following mailing-list:\n\n" +
                                  "  " + conf.address + "\n" })

    # delete the queue token.
    del queue.tokens[id.argument]

#
# this function confirms an action according to the received email.
#
def                     Confirm(conf, queue, email):
  id = None
  key = None

  # check if the subscriber is already registered.
# XXX[does not make sense since the one of the confirmation is for users to confirm
#     their registration]
#  if (conf.manager["address"] != email.issuer) and (not email.issuer in conf.members):
#    ems.Misc.Send(conf.address,
#                  [ email.issuer ],
#                  ems.TemplateErrorNotSubscribed,
#                  { "<DATE>": ems.Misc.Date(),
#                    "<FROM>": conf.address,
#                    "<TO>": email.issuer,
#                    "<REPLY-TO>": conf.address,
#                    "<MAILING-LIST>": conf.id,

#                    "<ADDRESS>": conf.address,
#                    "<ADDRESS:SUBSCRIBE>": conf.addresses["subscribe"] })
#    return

  # retrieve the tokens from the email.
  id = ems.Id(email)
  key = ems.Key(email)

  id.Locate()
  key.Locate()

  if (not id.argument) or (not key.argument):
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorMissingTokens,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address })
    return

  # check if this operation is registered in the queue.
  if not id.argument in queue.tokens:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnknownToken,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ID>": id.argument })
    return

  # according to the type of action.
  if queue.tokens[id.argument]["action"] == ems.ActionSubscribe:
    Subscribe(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionPost:
    Post(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionAdd:
    Add(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionInsert:
    Insert(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionEdit:
    Edit(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionRemove:
    Remove(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionDescription:
    Description(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionTag:
    Tag(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionMembership:
    Membership(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionControl:
    Control(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionUnsubscribe:
    Unsubscribe(conf, queue, email, id, key)
  elif queue.tokens[id.argument]["action"] == ems.ActionBehaviour:
    Behaviour(conf, queue, email, id, key)
  else:
    # notify both the sender and manager than something was wrong.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnexpected,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ACTION>": "your action from being confirmed" })
    ems.Misc.Send(conf.address,
                  [ conf.manager["address"] ],
                  ems.TemplateErrorConfiguration,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ACTION>": email.issuer +
                                "'s action from being confirmed because " +
                                "of a unexpected action's type '" +
                                queue.tokens[id.argument]["action"] + "'" })
    return

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

  # try to confirm an action.
  Confirm(conf, queue, email)

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

