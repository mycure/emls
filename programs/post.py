#
# ---------- packages ---------------------------------------------------------
#

import ems

import sys
import re

#
# ---------- functions --------------------------------------------------------
#

#
# this function displays the usage.
#
def                     Usage():
  sys.stdout.write("[ems::usage] post.py [mailing-list]\n")
  sys.exit(0)

#
# this function posts a message to an open mailing-list
#
def                     Open(conf, queue, email):
  match = None
  contents = None

  # modify some fields.
  email.Set("To", conf.address)
  email.Set("Reply-To", conf.address)
  email.Set("Errors-To", email.issuer)
  email.Set("Mailing-List", "list " + conf.id)

  # add the tag.
  if email.Get("Subject").find(conf.tag) == -1:
    email.Set("Subject", conf.tag + email.Get("Subject"))

  # build the contents.
  contents = email.Text()

  # forward the message.
  ems.Misc.Send(email.issuer,
                conf.Listeners().keys(),
                ems.TemplateRaw,
                { "<CONTENTS>": contents })

#
# this function posts a message to a controlled mailing-list.
#
def                     Filtered(conf, queue, email):
  id = None
  contents = None

  # generate an identifier.
  id = ems.Misc.Generate(32)

  # modify some fields.
  email.Set("To", conf.address)
  email.Set("Reply-To", conf.address)
  email.Set("Errors-To", email.issuer)
  email.Set("Mailing-List", "list " + conf.id)

  # add the tag.
  if email.Get("Subject").find(conf.tag) == -1:
    email.Set("Subject", conf.tag + email.Get("Subject"))

  # build the contents.
  contents = email.Text()

  # add the post to the queue.
  queue.tokens[id] = { "action": ems.ActionPost,
                       "message": { "address": email.issuer, "contents": contents },
                       "requirements": [ ems.RequirementManager ] }

  # notify the manager of the required confirmation.
  ems.Misc.Send(conf.address,
                [ conf.manager["address"] ],
                ems.TemplatePostAuthorisation,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": conf.manager["address"],
                    "<REPLY-TO>": conf.addresses["confirm"],
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<USER>": email.issuer,
                    "<SUBJECT>": email.Get("Subject"),
                    "<CONTENTS>": email.Text(),
                    "<ID>": id,
                    "<KEY>": conf.manager["key"] })

#
# this function posts a message to the mailing-list.
#
def                     Post(conf, queue, email):
  # check if the user is subscribed and has the right to post.
  if not email.issuer in conf.Speakers():
    ems.Misc.Send(conf.address,
                  [ email.issuer ],
                  ems.TemplateErrorNotAllowedToPost,
                  { "<DATE>": ems.Misc.Date(),
                    "<FROM>": conf.address,
                    "<TO>": email.issuer,
                    "<REPLY-TO>": conf.address,
                    "<MAILING-LIST>": conf.id,

                    "<ADDRESS>": conf.address,
                    "<ADDRESS:SUBSCRIBE>": conf.addresses["subscribe"] })
    return

  # handle the request according to the post policy.
  if conf.policies["control"] == ems.PolicyControlOpen:
    Open(conf, queue, email)
  elif conf.policies["control"] == ems.PolicyControlFiltered:
    Filtered(conf, queue, email)
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
                    "<ACTION>": "your message from being posted" })
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
                                "'s message from being posted because " +
                                "of a unexpected post policy '" +
                                conf.policies["control"] + "'" })

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

  # post the message.
  Post(conf, queue, email)

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
