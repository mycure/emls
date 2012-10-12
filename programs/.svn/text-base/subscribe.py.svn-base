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
  sys.stdout.write("[ems::usage] subscribe.py [mailing-list]\n")
  sys.exit(0)

#
# this function performs a private subscription.
#
def                     Private(conf, queue, email):
  # just reject the registration.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateErrorPrivateMembershipPolicy,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.address,
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address })

#
# this function performs a moderated subscription.
#
# postpone the registration waiting from the manager's confirmation.
#
def                     Moderated(conf, queue, email):
  key = None
  id = None

  # generate an id.
  id = ems.Misc.Generate(32)

  # generate a key.
  key = ems.Misc.Generate(32)

  # add the subscription to the pending registrations.
  queue.tokens[id] = { "action": ems.ActionSubscribe,
                       "member": { "address": email.issuer, "behaviour": ems.BehaviourContributor, "key": key },
                       "requirements": [ ems.RequirementManager, ems.RequirementMember ] }

  # notify both the user and the manager.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateSubscriptionConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ID>": id,
                  "<KEY>": key })
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplateSubscriptionAuthorisation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<USER>": email.issuer,
                  "<ID>": id,
                  "<KEY>": conf.manager["key"] })

#
# this function performs a public subscription.
#
def                     Public(conf, queue, email):
  key = None
  id = None

  # generate an id.
  id = ems.Misc.Generate(32)

  # generate a key.
  key = ems.Misc.Generate(32)

  # add the subscription to the queue, waiting user's confirmation.
  queue.tokens[id] = { "action": ems.ActionSubscribe,
                       "member": { "address": email.issuer, "behaviour": ems.BehaviourContributor, "key": key },
                       "requirements": [ ems.RequirementMember ] }

  # notify the user.
  ems.Misc.Send(conf.address,
                [ email.issuer ],
                ems.TemplateSubscriptionConfirmation,
                { "<DATE>": ems.Misc.Date(),
                  "<FROM>": conf.address,
                  "<TO>": email.issuer,
                  "<REPLY-TO>": conf.addresses["confirm"],
                  "<MAILING-LIST>": conf.id,

                  "<ADDRESS>": conf.address,
                  "<ID>": id,
                  "<KEY>": key })

#
# this function subscribes a user according to the mailing-list
# subscription policy.
#
def                     Subscribe(conf, queue, email):
  users = None

  # retrieve the complete list of users.
  users = conf.Users()

  # check if the subscriber is already registered.
  if email.issuer in users:
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorAlreadySubscribed,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ADDRESS:ADMIN>": conf.addresses["admin"] })
    return

  # look at the mailing-list's subscription policy.
  if conf.policies["membership"] == ems.PolicyMembershipPrivate:
    Private(conf, queue, email)
  elif conf.policies["membership"] == ems.PolicyMembershipModerated:
    Moderated(conf, queue, email)
  elif conf.policies["membership"] == ems.PolicyMembershipPublic:
    Public(conf, queue, email)
  else:
    # notify both the sender and manager that something went wrong.
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorUnexpected,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ACTION>": "your subscription from being processed" })
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
                                "'s subscription from being processed because " +
                                "of a unexpected membership policy '" +
                                conf.policies["membership"] + "'" })

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

  # try to subscribe the user to the given mailing-list.
  Subscribe(conf, queue, email)

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
