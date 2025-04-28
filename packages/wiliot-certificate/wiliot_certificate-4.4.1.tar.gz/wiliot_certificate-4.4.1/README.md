# wiliot-certificate Version 4.4.0

<!-- Description -->
wiliot-certificate is a Python library that provides tools for testing and certifying boards for compatibility with Wiliot’s ecosystem.
This python package includes the following CLI utilities:
 - Gateway Certificate (`wlt-cert-gw`)
 - Bridge Certificate (`wlt-cert-brg`)

# Version: 
wiliot-certificate versions 4.4.0 are compatible with firmware version 4.4.6 (ESP: 4.4.44, BLE: 4.4.93)

## Installing wiliot-certificate
Uninstall wiliot-deployment-tools if installed (relevant for old wlt-gw-certificate users):
````commandline
pip uninstall wiliot-deployment-tools
````

Install wiliot-certificate:
````commandline
pip install wiliot-certificate
````

## Using wiliot-certificate
### Gateway Certificate
Test Wiliot Gateway capabilities.
The Gateway Certificate includes different test that run sequentially to test each capability reported by the Gateway.
To run the Gateway Certificate the Gateway needs to use a public MQTT Broker (Eclipse):

Host:	mqtt.eclipseprojects.io
TLS TCP Port:	8883
TLS Websocket Port:	443
TCP Port:	1883
Websocket Port:	80

More information can be found at https://mqtt.eclipseprojects.io/.

#### Gateway Certificate Release Notes:
Release:
 - Standalone wiliot-certificate package
 - Python 3.13 support
 - Gateway API version 205 support
 - Registration test added
 - Bridge OTA stage added under actions
 - Aggregation flag supported by StressTest
 - -update flag compatibility fix. Upgrades bootloader if needed
 - -actions flag to select specific actions to test
 - ACL (Access control list) test for gateways reporting API version 205 in the connection test

#### The following capabilities are not tested in this version
 - Access control list stress stress
 - Validation schema verification
 - Board type registered within the Board Type Management system
 - Bridge OTA progress reporting


```
Usage: wlt-cert-gw [-h] -owner OWNER -gw GW [-suffix SUFFIX] [-tests {connection,uplink,downlink,stress}]

Gateway Certificate - CLI Tool to test Wiliot GWs

Required arguments:
  -gw GW        Gateway ID

Optional arguments:
  -owner OWNER  Owner ID (Required for non-registration tests)
  -tests        Pick specific tests to run
  -actions      Pick specific actions to test during the ActionsTest
  -update       Update the firmware of the test board
  -pps          Pick specific PPS rate for the stress test
  -agg          Duration uplink stages wait before processing packets
  -suffix       Allow for different suffixes after the Gateway ID in MQTT topics
  -env          Wiliot environment for registration and bridgeOTA tests
  -h, --help    show this help message and exit
  ```

### Bridge Certificate
Test Wiliot Bridge capabilities.
The Bridge Certificate includes different tests that run sequentially to test each capability reported by the bridge.


# update Gateway sim version :
- Update your gateway and bridge using Wiliot's platform. (https://platform.wiliot.com/) 
- Transfer the gateway to dev mode - run the following command: py ut\dev_mode.py --gw [GW] --enable
- Connect the gateway to your laptop via USB connection:
- Run the following: wlt-cert-brg --gw SIM --brg <XXXXXXXXXXXX> --port <COM_PORT>
- For other options of running, see the 'run example' section. 

#### Bridge Certificate Release Notes:
Release
- First release of Bridge Certificate – includes validation tests for bridge functionality.
- Additional details are available in the JSON files.

# The following capabilities are not tested in this version

## Power management
  - Functionality of energize and transmit in sleep mode
## Edge management
  - Timing of heartbeat and interface packets 
## Module Energy 2400
  - Functionality of energy pattern, output power and duty cycle
## Module Energy SUB1G
  - Functionality of energy pattern and duty cycle 
## Module Datapath 
  - RSSI edge cases: -127 and 0 
  - Functionality of transmission pattern, output power
  - Pacer interval with channel 10 and 500k modulation
  - Pacer interval using GEN3 Pixels 
  - Packet filter: the following configuration - DEBUG, TEMP & DEBUG, TEMPS & DEBUG & ADVANCE
  - Rx rate feature with extended advertising 
  - Functionality of adaptive pacer algorithm
  - Supported Pixels for extended advertising and GEN3
## Calibration 
  - Functionality of output power and interval calibration 
  - Functionality of calibration transmission patterns for the configuration STANDARD & EU & DISABLE


```
usage: wlt-cert-brg [-h] [--brg BRG] [--brg_cloud_connectivity BRG_CLOUD_CONNECTIVITY] [--brg1 BRG1] --gw GW [--data {tags,sim}] [--port PORT] [--clean] [--tl TL] [--run RUN]
                              [--drun DRUN] [--exit_on_test_failure] [--exit_on_param_failure] [--analyze_interference]

# Bridge Certificate CLI

options:
  -h, --help            show this help message and exit
  --brg, -b BRG         Bridge id to run on the tests
  --brg_cloud_connectivity, -bcc BRG_CLOUD_CONNECTIVITY
                        Bridge with cloud connectivity id to run on the tests
  --brg1, -b1 BRG1      Second bridge id to run on tests two bridges needed
  --gw, -g GW           GW id to run on the test, SIM prefix is used for Gateway simulation
  --data, -d {tags,sim}
                        Choose if data generated from real tags or by simulation
  --port, -p PORT       Enable UT using UART connection for Gateway Simulation or Data Simulation
  --clean               Clean all logs
  --tl TL               Test list file to use
  --run RUN             String to filter tests to run
  --drun DRUN           String to filter tests not to run
  --exit_on_test_failure
                        Stop running the tests if a test failed
  --exit_on_param_failure
                        Sets exit_on_param_failure mode to true in order to prevent tests from continuing iteration over all possibilities in case of failure
  --analyze_interference, -ai
                        Analyze interference before tests start (relevant only for Gateway Simulator)

run examples:
  Run command example with COM PORT connection:
  wlt-cert-brg --gw SIM --brg <XXXXXXXXXXXX> --port <COM_PORT>
  Run command example with remote GW connection:
  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg <XXXXXXXXXXXX>
  Run command example for running datapath module tests only:
  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg <XXXXXXXXXXXX> --run datapath
  Run command example with sanity test list:
  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg <XXXXXXXXXXXX> --tl certificate_sanity_test_list.txt
  Run command example with COM PORT connection for bridge with cloud connectivity:
  wlt-cert-brg --gw SIM --brg_cloud_connectivity <XXXXXXXXXXXX> --tl certificate_bcc_test_list.txt --port <COM_PORT>
  Run command example with remote GW connection for bridge with cloud connectivity:
  wlt-cert-brg --gw <YYYYYYYYYYYY> --brg_cloud_connectivity <XXXXXXXXXXXX> --tl certificate_bcc_test_list.txt
  ```
