"""
CLI for ansible_aap_api_client
"""

from argparse import ArgumentParser
from ansible_aap_api_client.job_management import JobManagement


def cli_argument_parser() -> ArgumentParser:
    """Function to create the argument parser

    :rtype: ArgumentParser
    :returns: The argument parser
    """
    arg_parser = ArgumentParser(description="ansible-aap-api-client-cli")

    arg_parser.add_argument("-b", "--base-url", required=True, help="Base URL for the Tower/AAP")
    arg_parser.add_argument("-u", "--username", required=True, help="The username")
    arg_parser.add_argument("-p", "--password", required=True, help="The password")

    subparsers = arg_parser.add_subparsers(
        title="commands",
        description="Valid commands: a single command is required",
        help="CLI Help",
        dest="a single command please see the -h option",
    )
    subparsers.required = True

    # This is the sub parser to jon a job template
    arg_parser_run_job_template = subparsers.add_parser("run-job-template", help="Run a job template in Tower/AAP")
    arg_parser_run_job_template.set_defaults(which_sub="run-job-template")
    arg_parser_run_job_template.add_argument(
        "-t", "--template-name", required=True, help="The name of the Job Template"
    )
    arg_parser_run_job_template.add_argument("-i", "--inventory-name", required=True, help="The name of Inventory")

    return arg_parser


def cli() -> None:  # pragma: no cover
    """Function to run the command line
    :rtype: None
    :returns: Nothing it is the CLI
    """
    arg_parser = None

    try:
        arg_parser = cli_argument_parser()
        args = arg_parser.parse_args()

        if args.which_sub == "run-job-template":
            job_mgmnt_obj = JobManagement(
                base_url=args.base_url,
                username=args.username,
                password=args.password,
                ssl_verify=False,
                job_template_name=args.template_name,
                inventory_name=args.inventory_name,
            )

            job_mgmnt_obj.poll_completion(print_status=True)

            print(job_mgmnt_obj.get_job_stdout(job_mgmnt_obj.job_id, "txt"))

    except AttributeError as error:
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()

    except FileNotFoundError as error:
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()

    except FileExistsError as error:
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"\n !!! {error} !!! \n")
        arg_parser.print_help()
