import os
import tabulate
import subprocess
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Local imports
import brg_certificate.cert_utils as cert_utils
import brg_certificate.cert_prints as cert_prints
from brg_certificate.wlt_types import *
from brg_certificate.cert_defines import *


##################################
# GENERIC
##################################
# Defines
WLT_CERT_HEADLINE =                "Wiliot Certificate Results"
WLT_CERT_PASS_HEADLINE =           "Wiliot Certificate Passed!"
WLT_CERT_FAIL_HEADLINE =           "Wiliot Certificate Failed!"
WLT_CERT_ERROR_HEADLINE =          "Wiliot Certificate Error!"
SUMMARY_HEADLINE =                 "Summary"
RUN_INFO =                         "Run Information"
RUN_DATETIME =                     "Run Time & Date"
RUN_DUR =                          "Run Duration"
CERT_VER =                         "Certificate Version"
TESTING_DEVICE_INFO =              "Testing Device Information"
TESTED_DEVICE_INFO =               "Tested Device Information"
SIM =                              "Simulator"
BRG =                              "Bridge"
BLE_MAC_ADDRESS =                  "BLE MAC Address"
BOARD_TYPE =                       "Board Type"
BLE_VER =                          "BLE Version"
SUP_API_VER =                      "Supported API Version"

result_map = {TEST_FAILED: cert_prints.color("RED", "FAIL"), TEST_SKIPPED: cert_prints.color("WARNING", "SKIPPED"),
              TEST_PASSED: cert_prints.color("GREEN", "PASS"), TEST_INIT: cert_prints.color("CYAN", "INIT")}
pass_or_fail = lambda obj : result_map[obj.rc]
param_name_to_title = lambda s : ' '.join(word.lower().capitalize() for word in s.split('_')).replace('2 4', '2.4') if '_' in s else s

class TestResult:
    def __init__(self, name="", devices_to_print="", test_table=None, result=None, duration=0, purpose="", kb_link="", compliance="", test_skipped=False):
        self.name = name
        self.devices = devices_to_print
        self.result = result
        self.test_table = test_table
        self.duration = duration
        self.purpose = purpose
        self.kb_link = kb_link
        self.compliance = compliance
        self.test_skipped = test_skipped
    
    def __repr__(self):
        return self.name

def generate_tests_table(tests=[], html=False):
    headers = ["Module", "Test Name", "Device", "Result Breakdown", "Result", "Run Time"]
    inner_format = "unsafehtml" if html else "simple"
    _pass_or_fail = pass_or_fail_html if html else pass_or_fail
    tests_results = []
    for test in tests:
        brgs_to_print = (test.gw if not test.brg0 or test.gw_only else
                         (f"{test.brg0.id_str}\n{test.brg1.id_str}" if test.brg1 and test.multi_brg else test.brg0.id_str))
        inner_table = [[phase.name, _pass_or_fail(phase), phase.reason] for phase in test.phases]
        result_breakdown_table = tabulate.tabulate(inner_table, headers=["Phase", "Result", "Notes"], tablefmt=inner_format)
        tests_results.append([cert_utils.module2name(test.test_module),
                              test.module_name if (not test.internal_brg or "gw" in test.module_name) else f"{test.module_name} (internal brg)",
                              brgs_to_print,
                              result_breakdown_table,
                              _pass_or_fail(test),
                              test.duration])
    return tabulate.tabulate(tests_results, headers=headers, tablefmt="unsafehtml" if html else "fancy_grid")

def get_update_status_from_log_file(log_file="update_log.txt"):
    update_status = "No version update logs were found"
    if os.path.isfile("update_log.txt"):
        with open(os.path.join(BASE_DIR, log_file), "r") as update_log:
            for l in update_log.readlines():
                if "ERROR: Didn't get response from BRG" in l:
                    update_status = "Didn't get response from BRG in order to start the update!"
                    break
                elif "ERROR: Didn't get response from" in l:
                    update_status = "Didn't get response from GW in order to start the update!"
                    break
                elif "version_update_test failed!" in l:
                    update_status = "GW version update failed!"
                    break
                elif "ota_test failed!" in l:
                    update_status = "BRG OTA failed!"
                    break
                elif "PASSED!" in l:
                    update_status = "GW and BRG versions were updated to latest successfully!"
                    break
                elif "SKIPPED!" in l:
                    update_status = "GW and BRG versions update skipped!"
                    break
    return update_status

def generate_results_files(html=True, pdf=True, failures=0, skipped=0, start_time=datetime.datetime.now(), duration=0, brg=None, internal_brg=None, tests=[], error=None, pipeline=False):
    # Generate HTML file
    if html:
        f = open(os.path.join(BASE_DIR, UT_RESULT_FILE_HTML), "w", encoding="utf-8")
        f.write(HTML_START)
        update_status = get_update_status_from_log_file()
        if pipeline:
            p = subprocess.Popen('git log --format=%B -n 1 {}'.format(os.environ['BITBUCKET_COMMIT']),
                                stdout=subprocess.PIPE, shell=True, cwd=os.environ['BITBUCKET_CLONE_DIR'])
            output, err = p.communicate()
        if error:
            f.write(f"<br><h1 style='color:#ab0000'>{WLT_CERT_ERROR_HEADLINE}</h1><br>")
            if pipeline:
                f.write("<hr>" + output.decode("utf-8") + "<br>")
                f.write("<p><a href='https://bitbucket.org/wiliot/wiliot-nordic-firmware/commits/{}'>Commit page on bitbucket</a><hr>".format(os.environ['BITBUCKET_COMMIT']))
            f.write(update_status + "<br><br>")
            f.write(error + "<br><br>")
            f.write(f"{RUN_DUR}: {str(duration).split(".")[0]} <br><br>")
            if brg:
                f.write(f"{BRG} {BLE_VER}: {brg.version} <br><br>")
        elif tests:
            if not failures and ("successfully!" in update_status or "skipped!" in update_status or not pipeline):
                f.write(f"<br><h1 style='color:#00AB83'>{WLT_CERT_PASS_HEADLINE}</h1>")
            else:
                f.write(f"<br><h1 style='color:#ab0000'>{WLT_CERT_FAIL_HEADLINE}</h1>")
            if pipeline:
                f.write("<hr>" + output.decode("utf-8") + "<br>")
                f.write("<p><a href='https://bitbucket.org/wiliot/wiliot-nordic-firmware/commits/{}'>Commit page on bitbucket</a><hr>".format(os.environ['BITBUCKET_COMMIT']))
                f.write(update_status + "<br><br>")
            f.write(f"{RUN_DATETIME}: {start_time.strftime('%d/%m/%Y, %H:%M:%S')} <br><br>")
            f.write(f"{RUN_DUR}: {str(duration).split(".")[0]} <br><br>")
            f.write(f"{CERT_VER}: {CERT_VERSION} <br><br>")
            if internal_brg:
                f.write(f"{SIM} {BLE_MAC_ADDRESS}: {internal_brg.id_str} <br><br>")
                f.write(f"{SIM} {BLE_VER}: {internal_brg.version} <br><br>")
            if brg:
                f.write(f"{BRG} {BLE_MAC_ADDRESS}: {brg.id_str} <br><br>")
                f.write(f"{BRG} {BLE_VER}: {brg.version} <br><br>")
            f.write(tabulate.tabulate([[len(tests)-(failures+skipped), skipped, failures, len(tests)]], headers=["PASSED", "SKIPPED", "FAILED", "TOTAL"], tablefmt="html"))
            f.write(generate_tests_table(tests, html=True))
            f.write("<br><br>")
        if pipeline:
            f.write(f"<p><a href='https://bitbucket.org/wiliot/wiliot-nordic-firmware/pipelines/results/{os.environ['BITBUCKET_BUILD_NUMBER']}'>Build's page and artifacts on bitbucket</a></p><br><br>")
        f.write("<img src='https://www.wiliot.com/src/img/svg/logo.svg' width='100' height='40' alt='Wiliot logo'>")
        f.write(HTML_END)
        f.close()
    
    # Generate PDF file
    if pdf:
        doc = SimpleDocTemplate(os.path.join(BASE_DIR, UT_RESULT_FILE_PDF), pagesize=letter)
        doc.title = "Wiliot Certificate Results"
        elements, hdr_page = [], []

        # Add Wiliot Logo
        img = Image(os.path.join(BASE_DIR, "../common", "wlt_logo.png"), width=100, height=40)  # Adjust size as needed
        hdr_page.append(img)
        hdr_page.append(Spacer(1, 20))

        # Title and Summary
        red_header = STYLES_PDF.get("RED_HEADER", ParagraphStyle("Default"))
        black_header = STYLES_PDF.get("BLACK_HEADER", ParagraphStyle("Default"))
        module_header = STYLES_PDF.get("MODULE_HEADER", ParagraphStyle("Default"))
        test_header = STYLES_PDF.get("TEST_LINK_HEADER", ParagraphStyle("Default"))
        test_purpose = STYLES_PDF.get("TEST_HEADER", ParagraphStyle("Default"))
        bold_text_style = STYLES_PDF.get("BLACK_BOLD", ParagraphStyle("Default"))
        bold_right_text_style = STYLES_PDF.get("BLUE_BOLD_RIGHT", ParagraphStyle("Default"))
        centered_text_style = STYLES_PDF.get("BLACK", ParagraphStyle("Default"))
        if error:
            title = Paragraph(f"<b>{WLT_CERT_ERROR_HEADLINE}</b>", red_header)
            hdr_page.append(title)
            hdr_page.append(Spacer(1, 20))
            hdr_page.append(Paragraph(f"{error}", bold_text_style))
        else:
            title = Paragraph(f"<b>{WLT_CERT_HEADLINE}</b>", black_header)
            hdr_page.append(title)
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"<a name='{SUMMARY_HEADLINE}'/><b>{SUMMARY_HEADLINE}</b>", module_header))
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"<u>{RUN_INFO}:</u>", bold_text_style))
        hdr_page.append(Paragraph(f"{RUN_DATETIME}: {start_time.strftime('%d/%m/%Y, %H:%M:%S')}", bold_text_style))
        hdr_page.append(Paragraph(f"{RUN_DUR}: {str(duration).split('.')[0]}", bold_text_style))
        hdr_page.append(Paragraph(f"{CERT_VER}: {CERT_VERSION}", bold_text_style))
        hdr_page.append(Spacer(1, 10))
        if brg:
            hdr_page.append(Paragraph(f"<u>{TESTED_DEVICE_INFO}:</u>", bold_text_style))
            hdr_page.append(Paragraph(f"{BRG} {BLE_MAC_ADDRESS}: {brg.id_str}", bold_text_style))
            hdr_page.append(Paragraph(f"{BRG} {BOARD_TYPE}: {ag.BOARD_TYPES_LIST[brg.board_type]}", bold_text_style))
            hdr_page.append(Paragraph(f"{BRG} {BLE_VER}: {brg.version}", bold_text_style))
            hdr_page.append(Paragraph(f"{BRG} {SUP_API_VER}: {brg.api_version}", bold_text_style))
            hdr_page.append(Spacer(1, 10))
        if internal_brg:
            hdr_page.append(Paragraph(f"<u>{TESTING_DEVICE_INFO}:</u>", bold_text_style))
            hdr_page.append(Paragraph(f"{SIM} {BLE_MAC_ADDRESS}: {internal_brg.id_str}", bold_text_style))
            hdr_page.append(Paragraph(f"{SIM} {BOARD_TYPE}: {ag.BOARD_TYPES_LIST[internal_brg.board_type]}", bold_text_style))
            hdr_page.append(Paragraph(f"{SIM} {BLE_VER}: {internal_brg.version}", bold_text_style))
            hdr_page.append(Paragraph(f"{SIM} {SUP_API_VER}: {internal_brg.api_version}", bold_text_style))
        hdr_page.append(Spacer(1, 20))

        # Count Table
        count_data = [
            ["PASSED", "SKIPPED", "FAILED", "TOTAL"],
            [len(tests)-(failures+skipped), skipped, failures, len(tests)]
        ]
        count_table = Table(count_data)
        count_table.setStyle(inner_table_style('CENTER'))
        hdr_page.append(count_table)
        hdr_page.append(Spacer(1, 20))

        # Test Results
        results_per_module = generate_results_per_module_for_pdf(tests=tests)
        summary_data = []
        for module, test_results in results_per_module.items():
            module_objects = []
            module_skipped = True # Remains True if all tests are skipped
            module_objects.append(Paragraph(f"<b>{module + ' Module' if not 'Edge' in module else module}</b>", module_header))
            module_objects.append(Spacer(1, 20))
            for test_result in test_results:
                test_objects = []
                name = Paragraph(f'<a href="#{module}_{test_result.name}">{test_result.name}</a>', centered_text_style) if not test_result.test_skipped else test_result.name
                summary_data += [[module, name, test_result.result, test_result.compliance]]
                test_objects.append(Paragraph(f'<a name="{module}_{test_result.name}"/><a href="{test_result.kb_link}">{test_result.name}</a>', test_header))
                test_objects.append(Spacer(1, 10))
                test_objects.append(test_result.result)
                test_objects.append(Spacer(1, 10))
                test_objects.append(Paragraph(test_result.purpose, test_purpose))
                test_objects.append(Spacer(1, 10))
                if not test_result.test_skipped:
                    module_skipped = False # Set to False if at least one test isn't skipped
                    test_objects.append(Paragraph(f"Tested devices: {test_result.devices}", bold_text_style))
                    test_objects.append(Paragraph(f"Test duration: {test_result.duration}", bold_text_style))
                    test_objects.append(Spacer(1, 10))
                    test_objects.append(test_result.test_table)
                    test_objects.append(Spacer(1, 10))
                    test_objects.append(Paragraph(f"<a href='#{SUMMARY_HEADLINE}'>Back to {SUMMARY_HEADLINE}</a>", bold_right_text_style))
                    test_objects.append(Spacer(1, 20))
                module_objects.append(KeepTogether(test_objects))
            if not module_skipped:
                elements += module_objects
                elements.append(PageBreak())
        summary_table = Table([["Module", "Name", "Result", "Compliance"]] + summary_data)
        summary_table.setStyle(inner_table_style('LEFT'))
        elements = hdr_page + [summary_table, PageBreak()] + elements

        doc.build(elements)


##################################
# HTML
##################################
COLORS_HTML = {
    "HEADER": "color: #ff00ff;",  # Purple
    "BLUE": "color: #0000ff;",   # Blue
    "CYAN": "color: #00ffff;",   # Cyan
    "GREEN": "color: #00ff00;",  # Green
    "WARNING": "color: #ffff00;",  # Yellow
    "RED": "color: #ff0000;",    # Red
    "BOLD": "font-weight: bold;",
    "UNDERLINE": "text-decoration: underline;",
}
color_html = lambda c, t: f'<span style="{COLORS_HTML.get(c, "")}{COLORS_HTML["BOLD"]}">{t}</span>'
html_result_map = {TEST_FAILED: color_html("RED", "FAIL"), TEST_SKIPPED: color_html("WARNING", "SKIPPED"),
                   TEST_PASSED: color_html("GREEN", "PASS"), TEST_INIT: color_html("CYAN", "INIT")}
pass_or_fail_html = lambda obj : html_result_map[obj.rc]

HTML_START = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <meta http-equiv='X-UA-Compatible' content='IE=edge'>
        <title>Wiliot Certificate Results</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>
        html, body {{
                height: 100%;
            }}

            html {{
                display: table;
                margin: auto;
            }}

            body {{
                display: table-cell;
                vertical-align: middle;
            }}
        table {{
            border-collapse: collapse;
            font-family: Tahoma, Geneva, sans-serif;
        }}
        table td {{
            padding: 15px;
        }}
        table thead td {{
            background-color: #54585d;
            color: #ffffff;
            font-weight: bold;
            font-size: 13px;
            border: 1px solid #54585d;
        }}
        table tbody td {{
            color: #636363;
            border: 1px solid #dddfe1;
        }}
        table tbody tr {{
            background-color: #f9fafb;
        }}
        table tbody tr:nth-child(odd) {{
            background-color: #ffffff;
        }}
        </style>
    </head>
    <body>
    """
HTML_END = """
    </body>
    </html>
    """

##################################
# PDF
##################################
STYLES_PDF = {
    "BLACK_HEADER": ParagraphStyle("Black Header", fontName="Helvetica-Bold", fontSize=20, textColor=colors.black, alignment=TA_CENTER),
    "RED_HEADER": ParagraphStyle("Red Header", fontName="Helvetica-Bold", fontSize=20, textColor=colors.red, alignment=TA_CENTER),
    "MODULE_HEADER": ParagraphStyle("Module Header", fontName="Helvetica-Bold", fontSize=16, textColor=colors.navy, alignment=TA_CENTER),
    "TEST_HEADER": ParagraphStyle("Test Header", fontName="Helvetica-Bold", fontSize=12, textColor=colors.black, alignment=TA_LEFT),
    "TEST_LINK_HEADER": ParagraphStyle('Test Link Header', fontName="Helvetica-Bold", fontSize=14, textColor=colors.blue, alignment=TA_LEFT),
    "BLACK": ParagraphStyle("Black", fontName="Helvetica", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_LEFT, wordWrap = 'CJK'),
    "BLACK_BOLD": ParagraphStyle("Black Bold", fontName="Helvetica-Bold", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_LEFT, wordWrap = 'CJK'),
    "BLUE_BOLD_RIGHT": ParagraphStyle("Black Bold", fontName="Helvetica-Bold", fontSize=9, textColor=colors.blue, splitLongWords=False, alignment=TA_RIGHT, wordWrap = 'CJK'),
    "BLUE": ParagraphStyle("Blue", fontName="Helvetica-Bold", fontSize=9, textColor=colors.navy, splitLongWords=False, alignment=TA_CENTER),
    "CYAN": ParagraphStyle("Cyan", fontName="Helvetica-Bold", fontSize=9, textColor=colors.cyan, splitLongWords=False, alignment=TA_LEFT),
    "GREEN": ParagraphStyle("Green", fontName="Helvetica-Bold", fontSize=9, textColor=colors.green, splitLongWords=False, alignment=TA_LEFT),
    "WARNING": ParagraphStyle("Warning", fontName="Helvetica-Bold", fontSize=9, textColor=colors.gold, splitLongWords=False, alignment=TA_LEFT),
    "RED": ParagraphStyle("Red", fontName="Helvetica-Bold", fontSize=9, textColor=colors.red, splitLongWords=False, alignment=TA_LEFT),
}
def color_pdf(c, t):
    style = STYLES_PDF.get(c, ParagraphStyle("Default"))
    return Paragraph(t, style)
pdf_result_map = {TEST_FAILED: color_pdf("RED", "FAILED"), TEST_SKIPPED: color_pdf("WARNING", "SKIPPED"), 
                  TEST_PASSED: color_pdf("GREEN", "PASSED"),  TEST_INIT: color_pdf("CYAN", "INIT")}
pass_or_fail_pdf = lambda obj : pdf_result_map[obj.rc]

inner_table_style = lambda align :  TableStyle([
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), f'{align}'),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                                    ('WORDWRAP', (0, 0), (-1, -1), False),
                                ])

def generate_results_per_module_for_pdf(tests=[]):
    text_style = STYLES_PDF.get("BLACK", ParagraphStyle("Default"))
    results_per_module = {}
    for test in tests:
        devices_to_print = (test.gw if not test.brg0 or test.gw_only else
                        (f"{test.brg0.id_str}\n{test.brg1.id_str}" if test.brg1 and test.multi_brg else test.brg0.id_str))
        inner_table = [[Paragraph(param_name_to_title(phase.name), text_style), pass_or_fail_pdf(phase), Paragraph(phase.reason, text_style)] for phase in test.phases]
        test_table = Table([["Phase", "Result", "Notes"]] + inner_table)
        test_table.setStyle(inner_table_style('LEFT'))
        compliance = "Mandatory" if test.test_json[MANDATORY] else "Optional"
        test_result = TestResult(name=test.test_json[NAME], devices_to_print=devices_to_print, test_table=test_table, result=pass_or_fail_pdf(test),
                                 duration=test.duration, purpose=str(test.test_json[PURPOSE]), compliance=compliance,
                                 kb_link=test.test_json[DOCUMENTATION], test_skipped=(test.rc == TEST_SKIPPED))
        module_name = test.test_json[MODULE]
        if module_name not in results_per_module:
                results_per_module[module_name] = [test_result]
        else:
            results_per_module[module_name] += [test_result]
    return results_per_module
