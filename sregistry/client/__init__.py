#!/usr/bin/env python

'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from sregistry.client.singularity import Singularity
import sregistry
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="Singularity Registry tools")

    # Customize parser depending on client
    from sregistry.main import Client as cli

    # Global Variables
    parser.add_argument("--version", dest='version', 
                        help="show software version", 
                        default=False, action='store_true')


    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')


    description = 'actions for Singularity Registry Global Client'
    subparsers = parser.add_subparsers(help='sregistry actions',
                                       title='actions',
                                       description=description,
                                       dest="command")
 
    # Local shell with client loaded
    shell = subparsers.add_parser("shell",
                                  help="shell into a session a client.")

    # List local containers and collections
    images = subparsers.add_parser("images",
                                   help="list local images, optionally with query")

    images.add_argument("query", nargs='*', 
                        help="container search query", 
                        type=str, default="*")


    # List local containers and collections
    inspect = subparsers.add_parser("inspect",
                                    help="inspect a container in your database")

    inspect.add_argument("query", nargs='*', 
                          help="container search query to inspect", 
                          type=str, default="*")

    # Get path to an image
    get = subparsers.add_parser("get",
                                    help="get a container path from your storage")

    get.add_argument("query", nargs='*', 
                     help="container search query to inspect", 
                     type=str, default="*")


    # List local containers and collections
    ls = subparsers.add_parser("list",
                               help="list local containers")

    ls.add_argument("query", nargs='*',
                     help="container list filter", 
                     type=str, default="*")


    # Add/copy local containers to storage, if client has it
    if hasattr(cli,'storage'):
        add = subparsers.add_parser("add",
                                    help="add a container to local storage")

        add.add_argument("image", nargs=1,
                         help="full path to image file", 
                         type=str)

        add.add_argument("--name", dest='name', 
                         help='name of image, in format "library/image"', 
                         type=str)

        add.add_argument('--copy', dest="copy", 
                         help="copy the container instead of moving it.", 
                         default=False, action='store_true')

        rm = subparsers.add_parser("rm",
                                   help="remove a container from the database")

        rm.add_argument("image", nargs=1,
                        help='name of image, in format "library/image"', 
                        type=str)

        rmi = subparsers.add_parser("rmi",
                                    help="remove a container from the database AND storage")

        rmi.add_argument("image", nargs=1,
                         help='name of image, in format "library/image"', 
                         type=str)


    # List or search containers and collections
    if hasattr(cli,'search'):

        search = subparsers.add_parser("search",
                                   help="search remote containers")

        search.add_argument("query", nargs='*', 
                         help="container search query, don't specify for all", 
                         type=str, default="*")


    # A more specific search, implemented by sregistry
    if hasattr(cli,'container_search'):

        search.add_argument('--runscript','-r', dest="runscript", 
                            help="show the runscript for each container", 
                            default=False, action='store_true')

        search.add_argument('--def','-df', dest="deffile", 
                            help="show the deffile for each container.", 
                            default=False, action='store_true')

        search.add_argument('--env','-e', dest="environ", 
                            help="show the environment for each container.", 
                            default=False, action='store_true')

        search.add_argument('--test','-t', dest="test", 
                            help="show the test for each container.", 
                            default=False, action='store_true')

    # Push an image
    if hasattr(cli,'push'):

        push = subparsers.add_parser("push",
                                     help="push one or more images to a registry")


        push.add_argument("image", nargs=1,
                           help="full path to image file", 
                           type=str)

        push.add_argument("--tag", dest='tag', 
                           help="tag for image. If not provided, defaults to latest", 
                           type=str, default=None)

        push.add_argument("--name", dest='name', 
                           help='name of image, in format "library/image"', 
                           type=str, required=True)


    # Pull an image
    if hasattr(cli,'pull'):

        pull = subparsers.add_parser("pull",
                                     help="pull an image from a registry")

        pull.add_argument("image", nargs=1,
                           help="full uri of image", 
                           type=str)

        pull.add_argument("--name", dest='name', 
                           help='custom name for image', 
                           type=str, default=None)

        pull.add_argument('--no-cache', dest="nocache", 
                           help="if storage active, don't add the image to it", 
                           default=False, action='store_true')


    # List or search labels
    if hasattr(cli,'label_search'):

        labels = subparsers.add_parser("labels",
                                    help="query for labels")

        labels.add_argument("--key", "-k", dest='key', 
                            help="A label key to search for", 
                            type=str, default=None)

        labels.add_argument("--value", "-v", dest='value', 
                            help="A value to search for", 
                            type=str, default=None)

    # List or search labels
    if hasattr(cli,'remove'):

        # Remove
        delete = subparsers.add_parser("delete",
                                        help="delete an image from the registry.")

        delete.add_argument('--force','-f', dest="force", 
                            help="don't prompt before deletion", 
                            default=False, action='store_true')

        delete.add_argument("image", nargs=1,
                            help="full path to image file", 
                            type=str)


    return parser


def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers



def main():
    '''main is the entrypoint to the sregistry client. The flow works to first
    to determine the subparser in use based on the command. The command then
    imports the correct main (files imported in this folder) associated with
    the action of choice. When the client is imported, it is actually importing
    a return of the function get_client() under sregistry/main, which plays
    the job of "sniffing" the environment to determine what flavor of client
    the user wants to activate. Installed within a singularity image, this
    start up style maps well to Standard Container Integration Format (SCIF)
    apps, where each client is a different entrypoint activated based on the
    environment variables.
    '''

    from sregistry.main import Client as cli
    parser = get_parser()
    subparsers = get_subparsers(parser)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # if environment logging variable not set, make silent
    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "INFO"

    # The client will announce itself (backend/database) unless it's get
    if args.command not in ["get"]:
        cli.speak()
    
    if args.version is True:
        print(sregistry.__version__)
        sys.exit(0)

    # Does the user want a shell?
    if args.command == "add": from .add import main
    if args.command == "get": from .get import main
    if args.command == "delete": from .delete import main
    if args.command == "inspect": from .inspect import main
    if args.command == "images": from .images import main
    if args.command == "labels": from .labels import main
    if args.command == "list": from .list import main
    if args.command == "push": from .push import main
    if args.command == "pull": from .pull import main
    if args.command == "rm": from .rm import main
    if args.command == "rmi": from .rmi import main
    if args.command == "search": from .search import main
    if args.command == "shell": from .shell import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args,
             parser=parser,
             subparser=subparsers[args.command])
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    # If we get down here are the user didn't 
    parser.print_help()    
    sys.exit(return_code)

if __name__ == '__main__':
    main()
