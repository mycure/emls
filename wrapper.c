#include <stdio.h>
#include <stdarg.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <pwd.h>

int			command(char*		command)
{
  const char*		commands[] =
    {
      "subscribe",
      "unsubscribe",
      "admin",
      "post",
      "confirm",
      NULL
    };
  unsigned int		i;

  for (i = 0; commands[i] != NULL; i++)
    if (strcmp(commands[i], command) == 0)
      return (0);

  return (-1);
}

int			identity(void)
{
  struct passwd*	password;

  password = getpwuid(getuid());

  if (strcmp(password->pw_name, "nobody") != 0)
    return (-1);

  setreuid(0, -1);

  return (0);
}

int			launch(char*		program,
			       char*		list,
			       char**		env)
{
#define VARIABLES_KEEP		4
#define VARIABLES_ADD		1
#define VARIABLES_NULL		1

#define ARGUMENTS		4

#define PACKAGES_DIRECTORY	"/etc/ems/packages/"
#define PROGRAMS_DIRECTORY	"/etc/ems/programs/"

#define PYTHON			"/usr/bin/python2"

  const char*		variables[VARIABLES_KEEP + VARIABLES_NULL] =
    {
      "USER",
      "PATH",
      "PWD",
      "SHLVL",
      NULL
    };
  char*			environment[VARIABLES_KEEP + VARIABLES_ADD + VARIABLES_NULL];
  char*			value;
  char*			arguments[ARGUMENTS];
  unsigned int		i;
  unsigned int		j;

  for (i = 0, j = 0; variables[i]; i++)
    if ((value = getenv(variables[i])) != NULL)
      environment[j++] = value - 1 - strlen(variables[i]);

  environment[j] = malloc(strlen("PYTHONPATH=") + strlen(PACKAGES_DIRECTORY) + 1);

  strcpy(environment[j], "PYTHONPATH=");
  strcat(environment[j++], PACKAGES_DIRECTORY);

  environment[j] = NULL;

  arguments[0] = PYTHON;

  arguments[1] = malloc(strlen(PROGRAMS_DIRECTORY) + strlen(program) + strlen(".py") + 1);
  strcpy(arguments[1], PROGRAMS_DIRECTORY);
  strcat(arguments[1], program);
  strcat(arguments[1], ".py");

  arguments[2] = list;

  arguments[3] = NULL;

  execve(PYTHON, arguments, env);

  return (-1);
}

int			main(int		argc,
			     char**		argv,
			     char**		env)
{
  if (argc != 3)
    {
      fprintf(stderr, "[wrapper::usage] %s program [mailing-list]\n",
	      argv[0]);
      exit(EXIT_FAILURE);
    }

  if (command(argv[1]) != 0)
    {
      fprintf(stderr, "[wrapper::error] illegal '%s' command\n", argv[1]);
      exit(EXIT_FAILURE);
    }

  if (identity() != 0)
    {
      fprintf(stderr, "[wrapper::error] this wrapper is supposed to be run by the 'nobody' user\n");
      exit(EXIT_FAILURE);
    }

  if (launch(argv[1], argv[2], env) != 0)
    {
      fprintf(stderr, "[wrapper::error] unable to launch the given command\n");
      exit(EXIT_FAILURE);
    }

  return (EXIT_SUCCESS);
}
