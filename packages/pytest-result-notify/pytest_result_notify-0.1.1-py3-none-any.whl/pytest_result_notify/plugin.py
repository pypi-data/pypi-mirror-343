import logging
from datetime import datetime
from time import sleep, time
from typing import Dict, Literal

import pytest
import requests

from .components.utils import format_time

data = {"passed": 0, "failed": 0}


def pytest_addoption(parser: pytest.Parser):
    parser.addini(
        "send_when",
        help="When do you like to send your content?\n every or on_fail.",
    )
    parser.addini(
        "send_api",
        help="Where will you send your content?\n Please input your link.",
    )
    parser.addoption("--delay", action="store", default=0, help="Delay in seconds between test cases")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    delay = float(item.config.getoption("--delay"))
    logging.info(f"Run test start: {item.nodeid}")

    yield
    logging.info(f"Run test end: {item.nodeid}")
    result = nextitem
    logging.info(f"Next test case: {result}")

    if delay > 0:
        if nextitem is not None:
            sleep(delay)


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含了全部用例
    data["total"] = len(session.items)
    print("==================:", data["total"])


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


# 到这里，配置已经加载完成，包括pytest.ini
def pytest_configure(config: pytest.Config):
    """
    配置加载完毕之后
    测试用例执行之前
    """
    data["start_time"] = datetime.now()
    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """统计测试结果"""
    case_dict = {}
    logging.info(f"terminalreporter.stats: {terminalreporter.stats}")
    # case_dict["TOTAL"] = terminalreporter._numcollected # 既包含 selected，也包含 deselected
    case_dict["PASSED"] = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    error = len(terminalreporter.stats.get("error", []))
    case_dict["FAILED"] = failed + error
    case_dict["SKIP"] = len(terminalreporter.stats.get("skipped", []))
    case_dict["XFAIL"] = len(terminalreporter.stats.get("xfailed", []))
    case_dict["XPASS"] = len(terminalreporter.stats.get("xpassed", []))
    case_dict["RERUN"] = len(terminalreporter.stats.get("rerun", []))
    # case_dict["RUN_TIME_S"] = round(time() - terminalreporter._sessionstarttime, 2)
    RUN_TIME_S = round(time() - terminalreporter._sessionstarttime, 2)
    case_dict["RUN_TIME"] = format_time(RUN_TIME_S)
    logging.info(case_dict)

    send_result(case_dict, "slack")


def send_result(case_dict: Dict, to: Literal["slack", "wechat"]):
    if not data["send_when"]:
        return
    if data["send_when"] == "on_fail" and data["failed"] == 0:
        return
    if not data["send_api"]:
        return

    if to == "slack":
        send_slack(case_dict)


def send_slack(case_dict):
    from .components.slack_client import SlackClient

    test_summary = SlackClient.markdown_dict_to_code_block(case_dict)
    channel = "zbs-auto-test"
    msg_payload = SlackClient.assemble_slack_msg(test_summary, channel=channel, slack_user=None)

    slack = SlackClient()
    slack.send_slack_msg(msg_payload)

    data["send_done"] = 1  # 发送成功


# fake
def send_wechat():
    url = data["send_api"]
    content = f"""
        python自动化测试结果


        测试时间：{data['start_time']}
        用例数量：{data['total']}
        执行时长：{data['duration']}
        测试通过：<font color="green">{data['passed']}</font>
        测试失败：<font color="red">{data['failed']}</font>
        测试通过率：{data['passed_ratio']}


        测试报告地址: http://baidu.com
        """

    try:
        requests.post(
            url,
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": content,
                },
            },
        )
    except Exception:
        pass

    data["send_done"] = 1  # 发送成功
