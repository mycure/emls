#
# ---------- definitions ------------------------------------------------------
#

EMSLocation = "/etc/ems/"

ListsLocation = EMSLocation + "lists/"
LogsLocation = EMSLocation + "logs/"
TemplatesLocation = EMSLocation + "templates/"

#
# ---------- packages ---------------------------------------------------------
#

import os
import re
import sys
import tempfile
import shutil
import time
import yaml
import random
import string
import email
import smtplib

#
# ---------- status -----------------------------------------------------------
#

StatusOk = 1
StatusError = 2

#
# ---------- type -------------------------------------------------------------
#

TypeUser = "user"
TypeList = "list"

#
# ---------- actions ----------------------------------------------------------
#

ActionSubscribe = "subscribe"
ActionPost = "post"

ActionHelp = "help"
ActionDump = "dump"
ActionAdd = "add"
ActionInsert = "insert"
ActionEdit = "edit"
ActionRemove = "remove"
ActionDescription = "description"
ActionTag = "tag"
ActionMembership = "membership"
ActionControl = "control"

ActionShow = "show"
ActionUnsubscribe = "unsubscribe"
ActionBehaviour = "behaviour"

#
# ---------- arguments --------------------------------------------------------
#

ArgumentsHelp = 0
ArgumentsDump = 0
ArgumentsAdd = 2
ArgumentsInsert = 1
ArgumentsEdit = 2
ArgumentsRemove = 1
ArgumentsDescription = 1
ArgumentsTag = 1
ArgumentsMembership = 1
ArgumentsControl = 1

ArgumentsUnsubscribe = 0
ArgumentsShow = 0
ArgumentsBehaviour = 1

#
# ---------- behaviours -------------------------------------------------------
#

BehaviourListener = "listener"
BehaviourSpeaker = "speaker"
BehaviourContributor = "contributor"

#
# ---------- policies ---------------------------------------------------------
#

PolicyMembershipPublic = "public"
PolicyMembershipModerated = "moderated"
PolicyMembershipPrivate = "private"

PolicyControlOpen = "open"
PolicyControlFiltered = "filtered"

#
# ---------- requirements -----------------------------------------------------
#

RequirementNone = []
RequirementManager = "manager"
RequirementMember = "member"

#
# ---------- templates --------------------------------------------------------
#

TemplateErrorAlreadySubscribed = TemplatesLocation + "ErrorAlreadySubscribed.txt"
TemplateErrorPrivateMembershipPolicy = TemplatesLocation + "ErrorPrivateMembershipPolicy.txt"
TemplateErrorNotAllowedToPost = TemplatesLocation + "ErrorNotAllowedToPost.txt"
TemplateErrorConfiguration = TemplatesLocation + "ErrorConfiguration.txt"
TemplateErrorUnexpected = TemplatesLocation + "ErrorUnexpected.txt"
TemplateErrorMissingTokens = TemplatesLocation + "ErrorMissingTokens.txt"
TemplateErrorUnknownToken = TemplatesLocation + "ErrorUnknownToken.txt"
TemplateErrorUnknownConfirmation = TemplatesLocation + "ErrorUnknownConfirmation.txt"
TemplateErrorNotSubscribed = TemplatesLocation + "ErrorNotSubscribed.txt"
TemplateErrorBadCommand = TemplatesLocation + "ErrorBadCommand.txt"
TemplateErrorUnallowedCommand = TemplatesLocation + "ErrorUnallowedCommand.txt"

TemplatePostAuthorisation = TemplatesLocation + "PostAuthorisation.txt"

TemplateRaw = TemplatesLocation + "Raw.txt"

TemplateSubscriptionConfirmation = TemplatesLocation + "SubscriptionConfirmation.txt"
TemplateSubscriptionAuthorisation = TemplatesLocation + "SubscriptionAuthorisation.txt"
TemplateSubscriptionNotification = TemplatesLocation + "SubscriptionNotification.txt"
TemplateSubscription = TemplatesLocation + "Subscription.txt"

TemplateUnsubscriptionConfirmation = TemplatesLocation + "UnsubscriptionConfirmation.txt"
TemplateUnsubscription = TemplatesLocation + "Unsubscription.txt"

TemplateAdminManagerHelp = TemplatesLocation + "AdminManagerHelp.txt"
TemplateAdminMemberHelp = TemplatesLocation + "AdminMemberHelp.txt"
TemplateAdminDump = TemplatesLocation + "AdminDump.txt"
TemplateAdminShow = TemplatesLocation + "AdminShow.txt"
TemplateAdminConfirmation = TemplatesLocation + "AdminConfirmation.txt"
TemplateAdminApplication = TemplatesLocation + "AdminApplication.txt"

#
# ---------- configuration ----------------------------------------------------
#

class Configuration:
  #
  # constructor
  #
  def           __init__(self, id):
    self.id = id

    self.address = None
    self.addresses = {}

    self.description = None
    self.policies = None
    self.tag = ""
    self.manager = None
    self.members = {}

  #
  # this method loads a mailing-list configuration file.
  #
  def           Load(self):
    stream = None
    address = None

    # check the configuration file.
    if not os.path.exists(ListsLocation + self.id + "/configuration"):
      return StatusError

    # read the configuration file.
    try:
      stream = yaml.load(Misc.Pull(ListsLocation + self.id + "/configuration"))
      if not stream:
        return StatusError
    except:
      return StatusError

    # build the object.
    self.address = stream["address"]

    address = self.address.split("@")

    self.addresses["subscribe"] = address[0] + "+subscribe@" + address[1]
    self.addresses["confirm"] = address[0] + "+confirm@" + address[1]
    self.addresses["admin"] = address[0] + "+admin@" + address[1]

    self.description = stream["description"]

    try:
      self.tag = stream["tag"]
    except:
      pass

    self.policies = stream["policies"]
    self.manager = stream["manager"]

    try:
      self.members = stream["members"]
    except:
      pass

    return StatusOk

  #
  # this method serialises a mailing-list object.
  #
  def           Store(self):
    stream = {}
    descriptor = None

    # open the output file.
    descriptor = file(ListsLocation + self.id + "/configuration", 'w')

    # initialise the stream
    if self.address:
      stream["address"] = self.address
    if self.description:
      stream["description"] = self.description
    if self.tag:
      stream["tag"] = self.tag
    if self.policies:
      stream["policies"] = self.policies
    if self.manager:
      stream["manager"] = self.manager
    if self.members:
      stream["members"] = self.members

    # store the stream.
    yaml.dump(stream, descriptor)

    # close the file.
    descriptor.close()

    return StatusOk

  #
  # this method returns the complete list of users.
  #
  def           Users(self):
    users = {}
    list = None
    member = None

    if self.members:
      for member in self.members:
        if self.members[member]["type"] == TypeUser:
          try:
            users[member]["behaviour"] = users[member]["behaviour"] |         \
                                         self.members[member]["behaviour"]
          except:
            users[member] = self.members[member]
        elif self.members[member]["type"] == TypeList:
          conf = Configuration(member)

          conf.Load()
          list = conf.Users()

          if list:
            for member in list:
              try:
                users[member]["behaviour"] = users[member]["behaviour"] |     \
                                             list["behaviour"]
              except:
                users[member] = list[member]

    return users

  #
  # this method returns the list's listeners.
  #
  def           Listeners(self):
    listeners = {}
    users = None
    user = None

    # retrieve the complete list of users.
    users = self.Users()

    # filter the listeners.
    for user in users:
      if (users[user]["behaviour"] == BehaviourListener) or (users[user]["behaviour"] == BehaviourContributor):
        listeners[user] = users[user]

    return listeners

  #
  # this method returns the list's speakers.
  #
  def           Speakers(self):
    speakers = {}
    users = None
    user = None

    # retrieve the complete list of users.
    users = self.Users()

    # filter the speakers.
    for user in users:
      if (users[user]["behaviour"] == BehaviourSpeaker) or (users[user]["behaviour"] == BehaviourContributor):
        speakers[user] = users[user]

    return speakers

#
# ---------- queue ------------------------------------------------------------
#

class Queue:
  #
  # constructor
  #
  def           __init__(self, id):
    self.id = id

    self.tokens = {}

  #
  # this method loads a mailing-list queue file.
  #
  def           Load(self):
    stream = None

    # check the queue file.
    if not os.path.exists(ListsLocation + self.id + "/queue"):
      return StatusError

    # read the configuration file.
    try:
      stream = yaml.load(Misc.Pull(ListsLocation + self.id + "/queue"))
    except:
      return StatusError

    # build the object.
    if stream:
      self.tokens = stream

    return StatusOk

  #
  # this method serialises a mailing-list object.
  #
  def           Store(self):
    stream = {}
    descriptor = None

    # open the output file.
    descriptor = file(ListsLocation + self.id + "/queue", 'w')

    # initialise the stream
    if self.tokens:
      stream = self.tokens

    # store the stream.
    yaml.dump(stream, descriptor)

    # close the file.
    descriptor.close()

#
# ---------- email ------------------------------------------------------------
#

class Email:
  #
  # constructor
  #
  def           __init__(self):
    self.raw = None

    self.message = None
    self.issuer = None

  #
  # this method builds an email object.
  #
  def           Catch(self):
    stream = None
    index = None

    # retrieve the email.
    stream = Misc.Input()
    if not stream:
      return StatusError

    # XXX
    Misc.Log("<Received>\n" + stream)

    # build the email object.
    self.raw = stream
    self.message = email.message_from_string(self.raw)

    self.issuer = email.Utils.getaddresses([self.message["from"]])[0][1]

    return StatusOk

  #
  # this method modifies a given attribute.
  #
  def           Set(self, attribute, value):
    if attribute in self.message:
      del self.message[attribute]

    self.message[attribute] = value

  #
  # this method returns a header element
  #
  def           Get(self, attribute):
    return self.message[attribute]

  #
  # return the email text
  #
  def           Text(self):
    return self.message.as_string()

#
# ---------- id ---------------------------------------------------------------
#

class Id:
  #
  # constructor
  #
  def           __init__(self, email):
    self.contents = email.Text()

    self.argument = None

  #
  # this method builds an id object.
  #
  def           Locate(self):
    match = None

    # locate the instance.
    match = re.search("\[id:" + "((?:(?:\\\\])|(?:[^\]]))+)", self.contents, re.IGNORECASE | re.DOTALL)
    if not match:
      return

    # set the string.
    self.argument = match.group(1).strip(" \n")

#
# ---------- key --------------------------------------------------------------
#

class Key:
  #
  # constructor
  #
  def           __init__(self, email):
    self.contents = email.Text()

    self.argument = None

  #
  # this method builds an key object.
  #
  def           Locate(self):
    match = None

    # locate the instance.
    match = re.search("\[key:" + "((?:(?:\\\\])|(?:[^\]]))+)", self.contents, re.IGNORECASE | re.DOTALL)
    if not match:
      return

    # set the string.
    self.argument = match.group(1).strip(" \n")

#
# ---------- command ----------------------------------------------------------
#

class Command:
  #
  # constructor
  #
  def           __init__(self, email):
    self.contents = email.Text()

    self.string = None
    self.arguments = {}

  #
  # this method builds an key object.
  #
  def           Locate(self):
    arguments = None
    match = None
    rest = None

    # locate the instance.
    match = re.search("\[cmd:" + "((?:(?:\\\\])|(?:[^\]]))+)\]", self.contents, re.IGNORECASE | re.DOTALL)
    if not match:
      return

    # set the string.
    self.string = match.group(1)

    # locate the instance.
    match = re.search("^((?:(?:\\\\])|(?:[^\] \n]))+)", self.string.lstrip(" \n"), re.IGNORECASE | re.DOTALL)
    if not match:
      return

    # set the action in the argument list.
    self.arguments["action"] = match.group(1)

    # prepare the next step.
    rest = self.string.lstrip(" \n")[len(match.group(1)):].lstrip(" \n").replace("\\[", "[").replace("\\]", "]")

    # according to the action.
    if match.group(1) == ActionHelp:
      # no argument, nothing to do.
      pass
    elif match.group(1) == ActionDump:
      # no argument, nothing to do.
      pass
    elif match.group(1) == ActionAdd:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsAdd:
        self.arguments = None
        return

      self.arguments["address"] = arguments[0]
      self.arguments["behaviour"] = arguments[1]
    elif match.group(1) == ActionInsert:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsInsert:
        self.arguments = None
        return

      self.arguments["id"] = arguments[0]
    elif match.group(1) == ActionEdit:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsEdit:
        self.arguments = None
        return

      self.arguments["address"] = arguments[0]
      self.arguments["behaviour"] = arguments[1]
    elif match.group(1) == ActionRemove:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsRemove:
        self.arguments = None
        return

      self.arguments["member"] = arguments[0]
    elif match.group(1) == ActionDescription:
      self.arguments["description"] = rest
    elif match.group(1) == ActionTag:
      self.arguments["tag"] = rest
    elif match.group(1) == ActionMembership:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsMembership:
        self.arguments = None
        return

      self.arguments["policy"] = arguments[0]
    elif match.group(1) == ActionControl:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsControl:
        self.arguments = None
        return

      self.arguments["policy"] = arguments[0]
    elif match.group(1) == ActionShow:
      pass
    elif match.group(1) == ActionUnsubscribe:
      pass
    elif match.group(1) == ActionBehaviour:
      arguments = re.split("[ \n]+", rest.rstrip(" \n"), re.DOTALL)

      if len(arguments) != ArgumentsBehaviour:
        self.arguments = None
        return

      self.arguments["behaviour"] = arguments[0]

#
# ---------- misc -------------------------------------------------------------
#

class Misc:
  #
  # this method read the standard input.
  #
  def           Input():
    handle = None
    line = None
    contents = ""

    for line in sys.stdin.readlines():
      contents += line

    return contents

  #
  # this method reads the contents of a single file.
  #
  def           Pull(file):
    handle = None
    line = None
    contents = ""

    if not os.path.exists(file):
      return None

    try:
      handle = open(file, "r")
    except IOError:
      return None

    for line in handle.readlines():
      contents += line

    handle.close()

    return contents

  #
  # this method writes the contents of a single file.
  #
  def           Push(file, contents):
    handle = None

    try:
      handle = open(file, "w")
    except:
      return StatusError

    handle.write(contents)

    handle.close()

    return StatusOk

  #
  # this method generates a key.
  #
  def           Generate(length):
    key = ""
    i = None

    # generate the key.
    for i in range(0, length):
      key += random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

    return key

  #
  # this method generates a date.
  #
  def           Date():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0100", time.gmtime())

  #
  # this method logs error messages.
  #
  def           Log(message):
    contents = None
    d = None
    t = None

    # get the current date.
    d = time.strftime("%Y-%m-%d")

    # read the log file
    contents = Misc.Pull(LogsLocation + d + ".log")
    if not contents:
      contents = ""

    # get the current time.
    t = time.strftime("%H:%M:%S")

    # add the message.
    contents = contents + "[" + t + "]\n" + message + "[/" + t + "]\n\n\n"

    # write the file back.
    Misc.Push(LogsLocation + d + ".log", contents)

  #
  # this method sends a template-based message to
  # the given addresses.
  #
  def           Send(sender, receivers, template, substitutions):
    contents = None
    tag = None

    # check if the receivers list is empty.
    if len(receivers) == 0:
      return

    # retrieve the template.
    contents = Misc.Pull(template)

    # perform the substitutions.
    for tag in substitutions:
      if tag == "<CONTENTS>":
        continue

      contents = contents.replace(tag, substitutions[tag])

    # finally, if there is a <CONTENTS> substitution, perform it.
    try:
      contents = contents.replace("<CONTENTS>", substitutions["<CONTENTS>"])
    except:
      pass

    # XXX
    Misc.Log("<Sending...>\n" + contents)

    # send the email.
    server = smtplib.SMTP()
    server.connect("localhost")

    for receiver in receivers:
      server.sendmail(sender, receiver, contents)

    server.quit()

  #
  # initialisation
  #
  Input = staticmethod(Input)
  Pull = staticmethod(Pull)
  Push = staticmethod(Push)
  Generate = staticmethod(Generate)
  Date = staticmethod(Date)
  Log = staticmethod(Log)
  Send = staticmethod(Send)
