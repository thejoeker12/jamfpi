"""Requests library to facilitate HTTP/S requests, JSON for json file parsing"""
# pylint: disable=line-too-long
import json
import requests
from ..config.defaultconfig import defaultconfig

def import_config(filepath) -> str:
    """imports config file and parses as json"""
    with open(filepath, "r", encoding="UTF-8") as file:
        json_file = json.load(file)

    return json_file


def get_bearer_token(basic_credentials, cloud_tenant_name):
    """Accepts basic credentials and jamf instance strings, returns barer token"""
    config = defaultconfig
    endpoint = config["urls"]["bearer_token"]
    token_url = config["urls"]["base"].format(tenant=cloud_tenant_name) + endpoint
    headers = {"Authorization": f"Basic {basic_credentials}"}
    token_request = requests.post(token_url, headers=headers, timeout=10)
    if token_request.ok:
        return token_request.json()

    raise requests.HTTPError(f"Bad response: {token_request.status_code}\n{token_request.text}")


def generate_client_token(cloud_tenant_name, client_id, client_secret):
    """Generated client token with secret and client id"""
    url = f"https://{cloud_tenant_name}.jamfcloud.com/api/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "grant_type": "client_credentials",
        "client_secret": client_secret
    }
    call = requests.post(url=url, headers=headers, data=data, timeout=10)
    if call.ok:
        return call.json()

    raise requests.HTTPError("Bad call", call, call.text)


def response_handler(response, raise_error=False):
    """
    Warns if unsuccessful status code detected
    Throws error on unsuccess detection if "raise_error" is True
    """
    if response.ok:
        return True

    response_str = f"{(response.request.method).upper()} Call to {response.url} failed with error {response.status_code}"
    print(response_str)
    if raise_error:
        error_str = f"Bad Response:\n{response.status_code}\nError Text:\n{response.text}"
        raise requests.HTTPError(error_str)
    return False


def fix_jamf_time_to_iso(time):
    time.replace("Z", "+00:00")
    if len(time) in [26, 27, 28]:
        time_split = time.split(".")
        date_time_no_seconds = time_split[0]

        seconds_and_tz = time_split[1]
        s_tz_split = seconds_and_tz.split("+")
        
        seconds = s_tz_split[0]
        while len(seconds) < 3:
            seconds += "0"

        time = f"{date_time_no_seconds}.{seconds}+{s_tz_split[1]}"

        return time
    else:
        return time
         

