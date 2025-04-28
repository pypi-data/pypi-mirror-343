from ansible_aap_api_client.ansible_aap_api_client_cli import cli_argument_parser


def test_cli_argument_parser_run_job_template():
    arg_parser = cli_argument_parser()
    args = arg_parser.parse_args(
        [
            "-b",
            "https://fake.com",
            "-u",
            "fake-username",
            "-p",
            "fake-password",
            "run-job-template",
            "-t",
            "fake-template",
            "-i",
            "fake-inventory",
        ]
    )

    assert args.which_sub == "run-job-template"
    assert args.base_url == "https://fake.com"
    assert args.username == "fake-username"
    assert args.password == "fake-password"
    assert args.template_name == "fake-template"
    assert args.inventory_name == "fake-inventory"
