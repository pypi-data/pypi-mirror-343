from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

# Test Description:
#   This test is to verify the functionality of both signal indicator tx (tx_brg) and rx (rx_brg) at BRG level.
#   We will configure several signal indicator params during the test, and check the functionality of the signal indicator logic
#   for each of them.
#   It is important to execute the test with several setups: 2 Fanstel BRG's, 2 Minew BRG's and 1 Fanstel and 1 Minew BRG.
#   At first, we will configure several tx signal indicator params and check for ack's, to verify all indicated params were
#   received at the cloud.
#   Then, we will examine the signal indicator end-2-end logic with both transmitter and receiver:
#   phase 1 - One BRG will be configured as signal indicator tx, and the other as signal indicator rx, and we expect to see
#   signal indicator packets only from the tx BRG, and according to the tx params (to check the repetition and cycle params).
#   phase 2 - Same as phase 1, but with different tx params configured.
#   phase 3 - One rx BRG without any tx BRG. We don't expect to see any signal indicator packets. This phase is to verify the
#   brg module logic is working properly, and no tag packet is accidentally being treated as signal indicator packet.
#   phase 4 - Both BRG's will be configured to be transmitters and receivers, with different tx params for each one. we expect
#   to see signal indicator packets from both BRG's, according to the tx params.
#   phase 5 - One BRG will be configured as signal indicator tx, but no rx, so we don't expect to receive signal indicatopr packets.
#   that way we can assure the logic within the receiver is not confused by the signal indicator uuid as external sensor.


# Test MACROS #
NUM_OF_SCANNING_CYCLE = 5
DEFAULT_SCAN_TIME = 30
SCAN_DELAY_TIME = 3
BLE4_BROADCAST_DURATION = ag.BLE5_PARAM_PRIMARY_CHANNEL_SCAN_CYCLE // 1000 + 1


def test_rssi_threshold(test):
    cycle, rep = 5, 4
    rx_brg_ = test.brg1  # when internal_brg test this is the internal_brg
    tx_brg_ = test.brg0
    rssi_threshold = -25

    utPrint(f"TX BRG with RX- cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # configuring receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver with RSSI Threshold of {rssi_threshold}", "BOLD")
    is_ble5 = not test.internal_brg
    test = cert_config.brg1_configure(test=test, module=rx_brg_.sensors, fields=[BRG_SENSOR0, BRG_RSSI_THRESHOLD],
                                      values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR, rssi_threshold], ble5=is_ble5, wait=True)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    wait = not test.internal_brg
    test = cert_config.brg_configure(test=test, module=tx_brg_.energy2400, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP],
                                     values=[cycle, rep], ble5=True, wait=wait)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {cycle},"
            f"repetition = {rep}", "BOLD")
    # phase analysis #
    print_update_wait(BLE4_BROADCAST_DURATION)  # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE * cycle) + SCAN_DELAY_TIME, "rssi_threshold")
    received_signal_ind_pkts = cert_common.get_all_sig_ind_pkts(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    for p in received_signal_ind_pkts:
        print(f"rssi value: {p[RSSI]}")
    rssi_threshold_viloation_pkts = [p for p in received_signal_ind_pkts if p[RSSI] >= -1 * rssi_threshold]
    if rssi_threshold_viloation_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"rssi_threshold phase failed - BRG {rx_brg_.id_str} echoed"
                        f" {len(rssi_threshold_viloation_pkts)} signal indicator packets\n with RSSI weaker than {rssi_threshold}")
    return test


def test_brg0_tx_brg1_rx(test):

    tx_brg_ = test.brg0
    rx_brg_ = test.brg1   # when internal_brg test this is the internal_brg
    cycle, rep = 8, 4

    utPrint(f"TX BRG with RX- cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # configuring receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    is_ble5 = not test.internal_brg
    test = cert_config.brg1_configure(test=test, module=rx_brg_.sensors, fields=[BRG_SENSOR0],
                                      values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR], ble5=is_ble5, wait=True)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    # configuring transmitter #
    wait = not test.internal_brg
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test = cert_config.brg_configure(test=test, module=tx_brg_.energy2400,
                                     fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP],
                                     values=[cycle, rep], ble5=True, wait=wait)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle = {cycle},"
            f"repetition = {rep}", "BOLD")
    # phase analysis #
    print_update_wait(BLE4_BROADCAST_DURATION)  # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE * cycle) + SCAN_DELAY_TIME, f"brg0_rx_brg1_tx_{cycle}_{rep}")
    received_signal_ind_pkts = cert_common.get_all_sig_ind_pkts(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)

    if cert_common.sig_ind_pkts_fail_analysis(tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE, received_signal_ind_pkts):
        test.rc = TEST_FAILED
        expected_signal_ind_pkts = cert_common.exp_sig_ind_pkts2(tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE)
        test.add_reason(f"brg0_rx_brg1_tx phase failed - BRG {rx_brg_.id_str} received wrong number of "
                        f"signal indicator packets\nreceived {len(received_signal_ind_pkts)} packets, "
                        f"expected {expected_signal_ind_pkts} packets")
        print(received_signal_ind_pkts)  # TODO: logging print(debug)
        print([[p[TIMESTAMP], p[SENSOR_PKT].pkt.rx_antenna] for p in received_signal_ind_pkts])

    test = cert_common.rx_tx_antenna_check(test, received_signal_ind_pkts, tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE)
    test = cert_common.output_power_check(test, received_signal_ind_pkts, tx_brg_)
    test = cert_common.rssi_check(test, received_signal_ind_pkts)

    return test


def test_brg0_none_brg1_rx(test):
    cycle, rep = ag.BRG_DEFAULT_SIGNAL_INDICATOR_CYCLE, ag.BRG_DEFAULT_SIGNAL_INDICATOR_REP
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1  # when internal_brg test this is the internal_brg
    utPrint(f"RX BRG without TX- cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # configuring receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    is_ble5 = not test.internal_brg
    test = cert_config.brg1_configure(test=test, module=rx_brg_.sensors, fields=[BRG_SENSOR0],
                                      values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR], ble5=is_ble5, wait=True)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    utPrint(f"BRG {rx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")

    # phase analysis #
    print_update_wait(BLE4_BROADCAST_DURATION)  # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    mqtt_scan_n_create_log_file(test, DEFAULT_SCAN_TIME, "brg0_none_brg1_rx")
    expected_signal_ind_pkts = [0]
    received_signal_ind_pkts = cert_common.get_all_sig_ind_pkts(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"brg0_rx_brg1_tx phase failed - BRG {rx_brg_.id_str} received wrong number of "
                        f"signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                        f"expected {expected_signal_ind_pkts} packets")

    return test


def test_brg0_rxtx_brg1_rxtx(test):

    if test.internal_brg:
        # Can't scan on ble5 with internal brg because config won't be received
        test.add_reason("skip for internal BRG")
        test.rc = TEST_SKIPPED
        return test

    tx_cycle, tx_rep = 5, 4
    rx_cycle, rx_rep = 5, 4
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1
    utPrint("Both BRG's are transmitter and receivers, with different values\n", "BLUE")
    # configuring first brg (tx_brg_) as receiver
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    test = cert_config.brg_configure(test=test, module=tx_brg_.sensors, fields=[BRG_SENSOR0],
                                     values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR], ble5=True)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")
    # configuring first brg (tx_brg_) as transmitter
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test = cert_config.brg_configure(test=test, module=tx_brg_.energy2400, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP],
                                     values=[tx_cycle, tx_rep], ble5=True)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {tx_brg_.id_str} configured to be transmitter - cycle={tx_cycle}, repetition={tx_rep}", "BOLD")

    # configuring second brg (rx_brg_) as receiver
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    test = cert_config.brg1_configure(test=test, module=rx_brg_.sensors, fields=[BRG_SENSOR0],
                                      values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR], ble5=True)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return test
    utPrint(f"BRG {rx_brg_.id_str} successfully configured as Signal Indicator Receiver\n", "BOLD")

    # configuring second brg (rx_brg_) as transmitter (already configured as rx)
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    test = cert_config.brg1_configure(test=test, module=rx_brg_.energy2400, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP],
                                      values=[rx_cycle, rx_rep], ble5=True)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test
    utPrint(f"BRG {rx_brg_.id_str} configured to be transmitter - cycle={rx_cycle}, repetition={rx_rep}")

    # phase analysis #
    print_update_wait(BLE4_BROADCAST_DURATION)  # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    mqtt_scan_n_create_log_file(test, NUM_OF_SCANNING_CYCLE * max(tx_cycle, rx_cycle) + SCAN_DELAY_TIME, "brg0_rxtx_brg1_rxtx")

    # Analyzing tx_brg_ performance as receiver
    utPrint(f"Analyzing tx_brg {tx_brg_.id_str} performance as a Receiver\n", "BOLD")
    received_signal_ind_pkts = cert_common.get_all_sig_ind_pkts(test=test, rx_brg=tx_brg_, tx_brg=rx_brg_)
    if cert_common.sig_ind_pkts_fail_analysis(tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE, received_signal_ind_pkts):
        test.rc = TEST_FAILED
        expected_signal_ind_pkts = cert_common.exp_sig_ind_pkts2(tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE)
        test.add_reason(f"brg0_rxtx_brg1_rxtx phase failed - BRG {tx_brg_.id_str} received wrong number of "
                        f"signal indicator packets\nreceived {len(received_signal_ind_pkts)} packets, "
                        f"expected {expected_signal_ind_pkts} packets")
        print(received_signal_ind_pkts)  # TODO: logging print(debug)

    # Analyzing rx_brg_ performance as receiver
    utPrint(f"Analyzing rx_brg {rx_brg_.id_str} performance as a Receiver\n", "BOLD")
    received_signal_ind_pkts = cert_common.get_all_sig_ind_pkts(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if cert_common.sig_ind_pkts_fail_analysis(tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE, received_signal_ind_pkts):
        test.rc = TEST_FAILED
        expected_signal_ind_pkts = cert_common.exp_sig_ind_pkts2(tx_brg_, rx_brg_, NUM_OF_SCANNING_CYCLE)
        test.add_reason(f"brg0_rxtx_brg1_rxtx phase failed - BRG {rx_brg_.id_str} received wrong number of "
                        f"signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                        f"expected {expected_signal_ind_pkts} packets")
        print(received_signal_ind_pkts)  # TODO: logging print(debug)
    # NOTE: We skipped the antenna and output power checks for this phase
    return test


def test_brg0_tx_brg1_none(test):
    # Tx BRG without rx. just waiting for packets to be sent from the transmitter and verify
    # The receiver isn't receiving any signal indicator packets.
    cycle, rep = 4, 3
    tx_brg_ = test.brg0
    rx_brg_ = test.brg1  # when internal_brg test this is the internal_brg
    utPrint(f"TX BRG without RX - cycle = {cycle}, repetition = {rep}\n", "BLUE")
    # configuring transmitter #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator Transmitter", "BOLD")
    wait = not test.internal_brg
    test = cert_config.brg_configure(test=test, module=tx_brg_.energy2400, fields=[BRG_SIGNAL_INDICATOR_CYCLE, BRG_SIGNAL_INDICATOR_REP],
                                     values=[cycle, rep], ble5=True, wait=wait)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator transmitter configuration!")
        return test

    # phase analysis #
    print_update_wait(BLE4_BROADCAST_DURATION)  # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE * cycle) + SCAN_DELAY_TIME, "brg0_tx_brg1_none")
    expected_signal_ind_pkts = [0]
    received_signal_ind_pkts = cert_common.get_all_sig_ind_pkts(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    if len(received_signal_ind_pkts) not in expected_signal_ind_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"brg0_tx_brg1_none phase failed - received signal indicator packet from BRG"
                        f"{rx_brg_.id_str}")
    test = cert_common.output_power_check(test, received_signal_ind_pkts, tx_brg_)

    return test


SIGNAL_INDICATOR_TEST_MAP = {"rssi_threshold": test_rssi_threshold, "brg0_tx_brg1_rx": test_brg0_tx_brg1_rx,
                             "brg0_none_brg1_rx": test_brg0_none_brg1_rx, "brg0_rxtx_brg1_rxtx": test_brg0_rxtx_brg1_rxtx,
                             "brg0_tx_brg1_none": test_brg0_tx_brg1_none}


def run(test):
    # Test prolog
    test = cert_common.test_prolog(test)

    # Configure to scan ble5 channel during all the test
    test = cert_config.brg_configure(test, fields=[BRG_RX_CHANNEL], values=[ag.RX_CHANNEL_10_500K],
                                     module=test.brg0.datapath, ble5=True)[0]
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[test.brg0.datapath], ble5=True)
    test = cert_config.brg1_configure(test, fields=[BRG_RX_CHANNEL], values=[ag.RX_CHANNEL_10_500K], module=test.brg1.datapath)[0]
    if test.rc == TEST_FAILED:
        is_ble5 = not test.internal_brg
        return cert_common.test_epilog(test, revert_brgs=True, modules=[test.brg0.datapath],
                                       brg1_modules=[test.brg1.datapath], ble5=is_ble5)

    for param in test.params:
        phase_run_print(param.name)
        test = SIGNAL_INDICATOR_TEST_MAP[param.value](test)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

        # Reset to defaults after every phase (don't fail the phase on that)
        test = cert_config.config_brg_defaults(test, modules=[test.brg0.energy2400, test.brg0.sensors], ble5=True, wait=False)[0]
        # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec, we configured 2 modules here
        print_update_wait(2 * BLE4_BROADCAST_DURATION)
        if test.rc == TEST_FAILED:
            test.add_reason("Failed to restore brg0 to defaults")
        else:
            is_ble5 = not test.internal_brg
            wait = test.internal_brg
            test = cert_config.config_brg1_defaults(test, modules=[test.brg1.energy2400, test.brg1.sensors], ble5=is_ble5, wait=wait)[0]
            # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec, we configured 2 modules here
            print_update_wait(2 * BLE4_BROADCAST_DURATION)
            if test.rc == TEST_FAILED:
                test.add_reason("Failed to restore brg0 to defaults")
        if test.rc == TEST_FAILED:
            test.set_phase_rc(param.name, test.rc)
            test.add_phase_reason(param.name, test.reason)
            if test.exit_on_param_failure:
                break
        else:
            test.reset_result()

    # Revert to defaults here and not in epilog
    test = cert_config.config_brg_defaults(test, modules=[test.brg0.datapath], ble5=True, wait=False)[0]
    if test.rc == TEST_FAILED:
        test.add_reason("Failed to revert brg0 datapath to defaults")
    else:
        is_ble5 = not test.internal_brg
        wait = test.internal_brg
        test = cert_config.config_brg1_defaults(test, modules=[test.brg1.datapath], ble5=is_ble5, wait=wait)[0]
        if test.rc == TEST_FAILED:
            test.add_reason("Failed to revert brg1 datapath to defaults")
    print_update_wait(BLE4_BROADCAST_DURATION)  # BLE5 configuration can take up to BLE4_BROADCAST_DURATION sec

    return cert_common.test_epilog(test, revert_brgs=False)
