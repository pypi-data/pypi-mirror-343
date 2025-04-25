import sys
import os
sys.path.insert(0, os.path.abspath(".."))
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from brg_certificate.cert_defines import DATA_REAL_TAGS, DATA_SIMULATION
import brg_certificate.brg_certificate as brg_certificate
TEST_LIST_DEFAULT_FILE = "certificate_test_list.txt"

class BrgCertificateCLI:
    """Bridge Certificate CLI."""
    def __init__(self):
        self.parser = ArgumentParser(
            description="Bridge Certificate CLI",
            epilog=
            "run examples:\n"
            "  Run command example with COM PORT connection:\n"
            "  wlt-cert-brg --gw SIM --brg <XXXXXXXXXXXX> --port <COM_PORT>\n"
            "  Run command example with remote GW connection:\n"
            "  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg <XXXXXXXXXXXX>\n"
            "  Run command example for running datapath module tests only:\n"
            "  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg <XXXXXXXXXXXX> --run datapath\n"
            "  Run command example with sanity test list:\n"
            "  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg <XXXXXXXXXXXX> --tl certificate_sanity_test_list.txt\n"
            "  Run command example with COM PORT connection for bridge with cloud connectivity:\n"
            "  wlt-cert-brg --gw SIM --brg_cloud_connectivity <XXXXXXXXXXXX> --tl certificate_bcc_test_list.txt --port <COM_PORT>\n"
            "  Run command example with remote GW connection for bridge with cloud connectivity:\n"
            "  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg_cloud_connectivity <XXXXXXXXXXXX> --tl certificate_bcc_test_list.txt\n",
            formatter_class=RawDescriptionHelpFormatter
        )
        self.parser.add_argument('--brg', '-b', default="", help='Bridge id to run on the tests')
        self.parser.add_argument('--brg_cloud_connectivity', '-bcc', default="", help='Bridge with cloud connectivity id to run on the tests')
        self.parser.add_argument('--brg1', '-b1', default="", help='Second bridge id to run on tests two bridges needed')
        self.parser.add_argument('--gw', '-g', type=str, required=True, help='GW id to run on the test, SIM prefix is used for Gateway simulation')
        self.parser.add_argument('--data', '-d', choices=[DATA_REAL_TAGS, DATA_SIMULATION], default=DATA_SIMULATION, help='Choose if data generated from real tags or by simulation')
        self.parser.add_argument('--port', '-p', default='', help='Enable UT using UART connection for Gateway Simulation or Data Simulation')
        self.parser.add_argument('--clean', default=False, action='store_true', help='Clean all logs')
        self.parser.add_argument('--tl', type=str, help='Test list file to use', default=TEST_LIST_DEFAULT_FILE)
        self.parser.add_argument('--run', type=str, help='String to filter tests to run')
        self.parser.add_argument('--drun', type=str, help='String to filter tests not to run')
        self.parser.add_argument('--exit_on_test_failure', default=False, action='store_true', help='Stop running the tests if a test failed')
        self.parser.add_argument('--exit_on_param_failure', default=False, action='store_true', help='Sets exit_on_param_failure mode to true in order to prevent \
                                 tests from continuing iteration over all possibilities in case of failure')
        self.parser.add_argument('--analyze_interference', '-ai', default=False, action='store_true', help='Analyze interference before tests start \
                        (relevant only for Gateway Simulator)')

    def parse_args(self, args=None):
        """Parse arguments and return them."""
        return self.parser.parse_args(args)

def main():
    cli = BrgCertificateCLI()
    args = cli.parse_args()
    # Set extra args to defaults
    args.server = "prod"
    args.lan = False
    args.latest = False
    args.rc = False
    args.private_setup = False
    args.skip_internal = False
    brg_certificate.main(args)

if __name__ == '__main__':
    main()
