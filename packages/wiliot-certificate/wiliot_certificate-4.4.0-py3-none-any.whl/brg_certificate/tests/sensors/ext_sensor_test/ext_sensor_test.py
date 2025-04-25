from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_mqtt as cert_mqtt
import csv
# test MACROS definitions #
DEFAULT_SENSOR_PAYLOAD_DATA = "0200002929B0FFF98DB104FA68BD5491456B55CC18AADB"
DEFAULT_ADVA0 = "112233445566"
DEFAULT_ADVA1 = "778899AABBCC"
ERM_SMART_MS_PAYLOAD = "0201060303374C17FFAE0421EF9DE99CE7AE7C5EB13B744D401CC6CFCF0107"
ZEBRA_PRINTER_PAYLOAD = "0201020F0958585A564A323331363038333435030279FEA5A5A5A5A5A5A5A5"
DEFAULT_SPECIAL_PAYLOAD = ZEBRA_PRINTER_PAYLOAD
DEFAULT_PACKET_LENGTH = "1E"

SCAN_TIMEOUT = 60

# UUID defines for logs review #
ERM_SMART_MS_UUID = 0xFFAE04
ZEBRA_PRINTER_UUID = 0x0279FE
UUID_0 = ZEBRA_PRINTER_UUID
UUID_1 = 0x987654
SCRAMBLE_ON = 0x01
SCRAMBLE_OFF = 0x00


def uuid_scramble_cfg_add(uuid, scramble):
    return uuid << 8 | scramble


def unscramble(packet):
    unscrambled_packet_id = int(hex(packet[RSSI])[2:] + packet[SENSOR_ID][-6:], 16)  # transforming parameters string to hex format
    for idx in range(6, 60, 8):
        current_word = int(packet[PAYLOAD][idx: idx + 8], 16)
        unscrambled_packet_id ^= current_word
    return packet[PAYLOAD][8:-8] + hex(unscrambled_packet_id)[2:]


def find_packet_in_csv(unscrambled_payload):
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(f'{base_path}/out_sensor_data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        next(csv_reader)                        # stepping over the header line
        for line in csv_reader:
            raw_data_payload = line['raw packet'][20:]
            if raw_data_payload[:8] == unscrambled_payload[:8]:
                return True
        return False


# Test functions description #
def create_csv_file_in(test, length=500):
    if test.data != DATA_SIMULATION:
        return []
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    pkts = []
    payload_0 = DEFAULT_ADVA0 + DEFAULT_SPECIAL_PAYLOAD
    payload_1 = DEFAULT_ADVA1 + DEFAULT_PACKET_LENGTH + cert_common.int2mac_get(UUID_1)[6:] + DEFAULT_SENSOR_PAYLOAD_DATA
    with open(f"{base_path}/in_sensor_data.csv", "w+") as f:
        f.write("raw packet,output power,delay,duplicates,channel,COM\n")
        for i in range(length):
            f.write(payload_0 + ",8,200,6,37,COM3\n")
            f.write(payload_1 + "{:08X}".format(i) + ",8,200,6,37,COM3\n")
            pkts.append(payload_0)
            pkts.append(payload_1 + "{:08X}".format(i))
    return pkts


def create_csv_file_out(test):
    if test.data != DATA_SIMULATION:
        return
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    uuid_0 = cert_common.int2mac_get(UUID_0)[6:]
    with (open(f"{base_path}/in_sensor_data.csv", "r") as csv_in,
          open(f"{base_path}/out_sensor_data.csv", "w") as csv_out):
        csv_out.write("raw packet,output power,delay,duplicates,channel,COM\n")
        csv_in = csv.DictReader(csv_in)
        next(csv_in)                        # stepping over the header line
        for line in csv_in:
            input_payload = line['raw packet'][12:]
            if uuid_0 in input_payload:
                csv_out.write(DEFAULT_ADVA0 + process_sensor_payload(input_payload, uuid_0) + ",8,200,6,37,COM3\n")
            else:
                csv_out.write(line['raw packet'] + ",8,200,6,37,COM3\n")


def process_sensor_payload(payload, uuid):
    uuid_idx = payload.find(uuid)
    if uuid_idx == -1:
        raise ValueError(f"Pattern {uuid_idx} not found in the packet")

    len = int(payload[uuid_idx - 2:uuid_idx], 16)
    segment_start_idx = uuid_idx - 2
    segment_end_idx = uuid_idx + len * 2
    segment = payload[segment_start_idx:segment_end_idx]
    output = segment + payload[:segment_start_idx] + payload[segment_end_idx:]
    return output


def pkts_get(test, phase):
    test.mqttc.flush_pkts()
    mqtt_scan_wait(test, duration=SCAN_TIMEOUT)
    sensor_pkts = cert_mqtt.get_all_sensor_pkts(test)
    generate_log_file(test, phase)

    if len(sensor_pkts) == 0:
        if phase != "tag_data_only" and phase != "rssi_threshold":
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - didn't find any sensor packets")
    else:
        if phase == "tag_data_only":
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - found sensor packets")
        sensor0_pkts = [p[SENSOR_UUID] == f"{UUID_0:06X}" for p in sensor_pkts]
        if phase == "snsr0_scrmbl_snsr1_no_scrmbl" or phase == "snsr0_scrmbl_snsr1_scrmbl" or phase == "snsr0_no_scrmbl":
            if not any(sensor0_pkts):
                test.rc = TEST_FAILED
                test.add_reason(f"Phase {phase} failed - didn't find any sensor0 packets")
        sensor1_pkts = [p[SENSOR_UUID] == f"{UUID_1:06X}" for p in sensor_pkts]
        if phase == "snsr0_scrmbl_snsr1_no_scrmbl" or phase == "snsr0_scrmbl_snsr1_scrmbl" or phase == "snsr1_scrmbl":
            if not any(sensor1_pkts):
                test.rc = TEST_FAILED
                test.add_reason(f"Phase {phase} failed - didn't find any sensor1 packets")

    return sensor_pkts


def test_tag_data_only(test, phase, _):
    pkts_get(test, phase)
    return test


def test_rssi_threshold(test, phase, ext_sensors_module):
    rssi_threshold = -25
    # Config
    utPrint(f"UUID_0 only without scrambling, RSSI Threshold = {rssi_threshold}\n", "BLUE")
    sensor0 = uuid_scramble_cfg_add(UUID_0, SCRAMBLE_OFF)
    test = cert_config.brg_configure(test=test, module=ext_sensors_module,
                                     fields=[BRG_SENSOR0, BRG_RSSI_THRESHOLD], values=[sensor0, rssi_threshold])[0]
    # Analyze
    sensor_pkts = pkts_get(test, phase)
    if test.rc == TEST_FAILED:
        return test
    rssi_threshold_viloation_pkts = [p for p in sensor_pkts if p[RSSI] >= -1 * rssi_threshold]
    if rssi_threshold_viloation_pkts:
        test.rc = TEST_FAILED
        test.add_reason("rssi_threshold phase failed - received"
                        f" {len(rssi_threshold_viloation_pkts)} sensor packets\n with RSSI weaker than {rssi_threshold}")
        return test
    return test


def test_snsr0_no_scrmbl(test, phase, ext_sensors_module):
    # Config
    utPrint("UUID_0 only without scrambling - UUID is 0x{:06X}".format(UUID_0), "BLUE")
    sensor0 = uuid_scramble_cfg_add(UUID_0, SCRAMBLE_OFF)
    test = cert_config.brg_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[sensor0])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Configuration for phase {phase} failed")
        return test
    # Analyze
    sensor_pkts = pkts_get(test, phase)
    if test.rc == TEST_FAILED:
        return test
    for p in sensor_pkts:
        if p[SENSOR_UUID] != "{:06X}".format(UUID_0):
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - received packets from an un-registered sensor")
            return test
        unscrambled_payload = p[PAYLOAD][8:]
        if find_packet_in_csv(unscrambled_payload) is False:
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - couldn't find unscrambled payload")
            return test
    return test


def test_snsr1_scrmbl(test, phase, ext_sensors_module):
    # Config
    utPrint("UUID_1 only with scrambling - UUID is 0x{:06X}".format(UUID_1), "BLUE")
    sensor1 = uuid_scramble_cfg_add(UUID_1, SCRAMBLE_ON)
    test = cert_config.brg_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR1], values=[sensor1])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Configuration for phase {phase} failed")
        return test
    # Analyze
    sensor_pkts = pkts_get(test, phase)
    if test.rc == TEST_FAILED:
        return test
    for p in sensor_pkts:
        if p[SENSOR_UUID] != "{:06X}".format(UUID_1):
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - received packets from an un-registered sensor")
            return test
        unscrambled_payload = unscramble(p)
        if find_packet_in_csv(unscrambled_payload) is False:
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - scrambling algorithm error")
            return test
    return test


def test_snsr0_scrmbl_snsr1_no_scrmbl(test, phase, ext_sensors_module):
    # Config
    print(f"UUID_0 with scrambling, UUID_1 without scrambling, {SCAN_TIMEOUT} sec\n")
    sensor0 = uuid_scramble_cfg_add(UUID_0, SCRAMBLE_ON)
    sensor1 = uuid_scramble_cfg_add(UUID_1, SCRAMBLE_OFF)
    test = cert_config.brg_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0, BRG_SENSOR1], values=[sensor0, sensor1])[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Configuration for phase {phase} failed")
        return test
    # Analyze
    sensor_pkts = pkts_get(test, phase)
    if test.rc == TEST_FAILED:
        return test
    for p in sensor_pkts:
        if p[SENSOR_UUID] == "{:06X}".format(UUID_0):
            unscrambled_payload = unscramble(p)
            if find_packet_in_csv(unscrambled_payload) is False:
                test.rc = TEST_FAILED
                test.add_reason(f"Phase {phase} failed - scrambling algorithm error")
                return test
        if p[SENSOR_UUID] == "{:06X}".format(UUID_1):
            unscrambled_payload = p[PAYLOAD][8:]
            if find_packet_in_csv(unscrambled_payload) is False:
                test.rc = TEST_FAILED
                test.add_reason(f"Phase {phase} failed - couldn't find unscrambled payload")
                return test
    return test


def test_snsr0_scrmbl_snsr1_scrmbl(test, phase, ext_sensors_module):
    # Config
    utPrint(f"UUID_0 with scrambling, UUID_1 with scrambling, {SCAN_TIMEOUT} sec\n", "BLUE")
    sensor0 = uuid_scramble_cfg_add(UUID_0, SCRAMBLE_ON)
    sensor1 = uuid_scramble_cfg_add(UUID_1, SCRAMBLE_ON)
    test = cert_config.brg_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0, BRG_SENSOR1], values=[sensor0, sensor1])[0]
    if test.rc == TEST_FAILED:
        return test
    # Analyze
    sensor_pkts = pkts_get(test, phase)
    if test.rc == TEST_FAILED:
        return test
    for p in sensor_pkts:
        unscrambled_payload = unscramble(p)
        if find_packet_in_csv(unscrambled_payload) is False:
            test.rc = TEST_FAILED
            test.add_reason(f"Phase {phase} failed - scrambling algorithm error")
            return test
    return test


EXT_SENSOR_TEST_MAP = {"tag_data_only": test_tag_data_only,
                       "rssi_threshold": test_rssi_threshold,
                       "snsr0_no_scrmbl": test_snsr0_no_scrmbl,
                       "snsr1_scrmbl": test_snsr1_scrmbl,
                       "snsr0_scrmbl_snsr1_no_scrmbl": test_snsr0_scrmbl_snsr1_no_scrmbl,
                       "snsr0_scrmbl_snsr1_scrmbl": test_snsr0_scrmbl_snsr1_scrmbl}


def run(test):
    datapath_module = test.active_brg.datapath
    ext_sensors_module = test.active_brg.sensors
    test = cert_common.test_prolog(test)
    # check for problems in prolog
    if test.rc == TEST_FAILED:
        test = cert_common.test_epilog(test)
        return test

    # Adaptation of GW configuration for internal BRG test
    if test.internal_brg:
        test = cert_config.brg_configure(test, fields=[BRG_RX_CHANNEL], values=[ag.RX_CHANNEL_37], module=datapath_module, wait=True)[0]
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            return cert_common.test_epilog(test, revert_gws=True)

    # create csv file for the test
    in_pkts = create_csv_file_in(test)
    create_csv_file_out(test)

    if test.data == DATA_SIMULATION:
        # start generating sensor pkts and send them using data simulator
        pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=len(in_pkts), duplicates=6, delay=200,
                                                       pkt_types=[0], pixels_type=RAW_DATA, pkts=in_pkts)
        pixel_sim_thread.start()
        ble_sim_thread = pixel_sim_thread

    for param in test.params:
        functionality_run_print(param.name)
        test = EXT_SENSOR_TEST_MAP[param.value](test, param.name, ext_sensors_module)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED:
            if test.exit_on_param_failure:
                break  # break the whole for loop and keep the test as failed
        test.reset_result()  # reset result and continue to next param

    # Kill the ble simulator
    if test.data == DATA_SIMULATION:
        ble_sim_thread.stop()

    return cert_common.test_epilog(test, revert_brgs=True, modules=[ext_sensors_module, datapath_module])
