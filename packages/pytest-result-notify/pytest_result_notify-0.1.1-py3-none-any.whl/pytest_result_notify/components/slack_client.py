import json
import logging
from typing import Dict

import requests


class SlackClient:
    def __init__(
        self,
        url="https://smartx1.slack.com/api/chat.postMessage",
        token="xoxb-4376593009-7495604502759-uLSsp7F3oTopRlclH2VEcx5V",
    ):
        self.url = url
        self.token = token
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}

    @staticmethod
    def markdown_dict_to_code_block(dict_data: Dict) -> Dict:
        format_dict = "```\n"
        for key, value in dict_data.items():
            format_dict += f"{key}: {value}\n"
        format_dict += "```"
        return format_dict

    @staticmethod
    def assemble_slack_msg(test_summary: str, test_report: str = None, channel=None, slack_user=None) -> Dict:
        msg = ""
        if test_report is None:
            if slack_user and slack_user.lower() != "none":
                msg = f"""
                    *Test Report*: \tNone @{slack_user}\n*Test Summary*: {test_summary}
                """
            else:
                msg = f"""
                    *Test Report*: \tNone\n*Test Summary*: {test_summary}
                """
        else:
            if slack_user and slack_user.lower() != "none":
                msg = f"""
                    *Test Report*: \t{test_report} @{slack_user}\n*Test Summary*: {test_summary}
                """
            else:
                msg = f"""
                    *Test Report*: \t{test_report}\n*Test Summary*: {test_summary}
                """
        msg_payload = {"text": msg, "mrkdwn": True, "link_names": 1}

        if channel and channel.lower() != "none":
            msg_payload["channel"] = channel

        return msg_payload

    def send_slack_msg(self, msg_payload: Dict):
        response = requests.post(self.url, headers=self.headers, data=json.dumps(msg_payload))

        if response.status_code == 200:
            logging.info("Send message success!")
        else:
            logging.error(f"Send message failed, status_code: {response.status_code}, response_text: {response.text}")
