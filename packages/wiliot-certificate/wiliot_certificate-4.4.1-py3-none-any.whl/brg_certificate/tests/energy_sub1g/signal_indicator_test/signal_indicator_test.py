from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config


def run(test):

    fields = [BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP]
    sub1g_module = test.active_brg.energy_sub1g

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)
    for param in test.params:
        param_name = f"{param.name}"
        test = cert_config.brg_configure(test, fields=fields, values=param.value, module=sub1g_module)[0]
        field_functionality_pass_fail_print(test, fields[0] + "_sub1g", value=param_name)
        generate_log_file(test, param_name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED:
            if test.exit_on_param_failure:
                break  # break the whole for loop and keep the test as failed
        test.reset_result()  # reset result and continue to next param

    return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])
