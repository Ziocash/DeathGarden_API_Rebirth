"""

"""
import logging

# ------------------------------------------------------- #
# imports
# ------------------------------------------------------- #
from flask import Flask, send_from_directory, request, jsonify, render_template, make_response
from threading import Thread
import os
import yaml
import graypy
import requests


# ------------------------------------------------------- #
# functions
# ------------------------------------------------------- #
def load_config():
    with open('config//api_config.yaml', 'r') as f:
        config_file = yaml.safe_load(f)
    return config_file


def setup_graylog():
    if use_graylog:
        global my_logger
        my_logger = logging.getLogger('deathgarden_api')
        my_logger.setLevel(logging.DEBUG)
        handler = graypy.GELFUDPHandler(graylog_server, 12201)
        my_logger.addHandler(handler)
        my_logger.debug('Started Death Garden API')
    else:
        print("Graylog disabled. Not sending any Logs.")


def graylog_logger(message, level):
    if use_graylog:
        if level == "debug":
            my_logger.debug(message)
        if level == "warning":
            my_logger.warning(message)
        if level == "error":
            my_logger.error(message)
        if level == "info":
            my_logger.info(message)
    else:
        print("Graylog disabled. Not sending any Logs.")


def get_remote_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_addr = request.environ['REMOTE_ADDR']
    else:
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
    print("New Connection from: " + ip_addr)


app = Flask(__name__)


@app.route("/")
def root():
    get_remote_ip()
    return jsonify({"status": "success"})
    # return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    get_remote_ip()
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/metrics/client/event", methods=["POST"])
def receive_event():
    get_remote_ip()
    try:
        print("Responded to Metrics api call POST")
        data = request.get_json()
        graylog_logger("Metric API: " + str(data), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/metrics/httplog/event", methods=["POST"])
def metrics_httplog_event():
    get_remote_ip()
    try:
        data = request.get_json()
        graylog_logger("Upload: " + str(data), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/healthcheck", methods=["GET"])
def healthcheck():
    get_remote_ip()
    try:
        return jsonify({"status": "success", "online": "true"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/services/tex")
def services_tex():
    get_remote_ip()
    try:
        print("Responded to tex api call GET")
        return {"status": "success"}
        # return jsonify({"status": "success", "online": "true", "Version": "te-18f25613-36778-ue4-374f864b",
        #                "ProjectID": "F72FA5E64FA43E878DC72896AD677FB5",
        #                "DefaultFactoryName": "HttpNetworkReplayStreaming", "ServeMatchDelayInMin": "30.0f"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/gameDataAnalytics", methods=["POST"])
def analytics_post():
    get_remote_ip()
    try:
        print("Responded to analytics api call POST")
        data = request.get_json()
        graylog_logger("DataAnalytics: " + str(data), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/gameDataAnalytics/batch", methods=["POST"])
def analytics_batch_post():
    get_remote_ip()
    try:
        print("Responded to analytics batch api call POST")
        data = request.get_json()
        graylog_logger("Batch upload: " + str(data), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/auth/provider/steam/login", methods=["POST"])
def steam_login():
    get_remote_ip()
    # Here the Client sends a signed session ticket as a hex string to the Server.
    # The Session Ticket allways starts with: 14000000
    try:
        steam_session_token = request.args.get('token')
        graylog_logger("Login by Session Ticket: " + steam_session_token, "info")
        headers = {
            'X-Kraken-Client-Platform': 'steam',
            'X-Kraken-Client-Provider': 'steam',
            'X-Kraken-Client-Resolution': '3440x1440',
            'X-Kraken-Client-Timezone-Offset': '-120',
            'X-Kraken-Client-Os': '10.0.22621.1.256.64bit',
            'X-Kraken-Client-Version': '3.6.1',
            'User-Agent': 'TheExit/++UE4+Release-4.21-CL-0 Windows/10.0.19045.1.256.64bit',
        }

        params = {
            'token': steam_session_token,
        }
        response = requests.get(
            'https://api.steampowered.com/ISteamUserAuth/AuthenticateUserTicket/v1/?key={}&ticket={}&appid=555440'.format(
                steam_api_key, steam_session_token), params=params,
            headers=headers)
        print("DEBUG: " + str(response.json()))
        steamid = response.json()["response"]["params"]["result"]["steamid"]
        owner_id = response.json()["response"]["params"]["result"]["ownersteamid"]  # This is providerId
        # Read: Doc -> AUTH
        # You can copy and paste the JSON from the Auth Doc here. If you don't have a steam api key.
        # The Client does not validate this and just uses it.
        # Game id = 555440
        return jsonify({"preferredLanguage": "en", "friendsFirstSync": {"steam": True},
                        "fixedMyFriendsUserPlatformId": {"steam": True}, "id": "xx000x00-x000-00x0-x0xx-x0000000000x",
                        "provider": {"providerId": {steamid}, "providerName": "steam",
                                     "userId": "xx000x00-x000-00x0-x0xx-x0000000000x"},
                        "providers": [{"providerName": "steam", "providerId": {steamid}}], "friends": [],
                        "triggerResults": {"success": [], "error": []},
                        "tokenId": "xx000x00-x000-00x0-x0xx-x0000000000x",
                        "generated": 1686004631, "expire": 1686091031, "userId": "xx000x00-x000-00x0-x0xx-x0000000000x",
                        "token": "0x0000x0-00x0-0xxx-00x0-x00x0x000x0x"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/utils/contentVersion/latest/2.11", methods=["GET"])
def content_version():
    get_remote_ip()
    try:
        print("Responded to content version api call GET")
        return jsonify({"latestSupportedVersion": "te-18f25613-36778-ue4-374f864b"})  # Don't know if this is correct. Just testing.
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/modifierCenter/modifiers/me", methods=["GET"])
def modifiers():
    get_remote_ip()
    try:
        print("Responded to modifiers api call GET")
        return jsonify({"status": "success", "modifiers": []}) # Don't know. Added as Placeholder.
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/api/v1/consent/eula2", methods=["GET"])
def consent_eula():
    get_remote_ip()
    try:
        print("Responded to consent eula api call GET")
        return jsonify({"status": "success", "consent": "true"}) # Don't know. Added as Placeholder.
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


# Logging
@app.route("/api/v1/extensions/quitters/getQuitterState", methods=["POST"])
def get_quitter_state():
    get_remote_ip()
    try:
        print("Responded to get quitter state api call POST")
        graylog_logger("Get quitter state: " + str(request.get_json()), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


# Logging
@app.route("/api/v1/extensions/progression/initOrGetGroups", methods=["POST"])
def extension_progression_init_or_get_groups():
    get_remote_ip()
    try:
        print("Responded to extension progression init or get groups api call POST")
        graylog_logger("Extension progression init or get groups: " + str(request.get_json()), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


# Logging
@app.route("/api/v1/me/richPresence", methods=["POST"])
def me_rich_presence():
    get_remote_ip()
    try:
        print("Responded to me rich presence api call POST")
        graylog_logger("Me_richPresence: " + str(request.get_json()), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


@app.route("/moderation/check/username", methods=["POST"])
def moderation_check_username():
    get_remote_ip()
    try:
        print("Responded to moderation check username api call POST")
        graylog_logger("Moderation check username: " + str(request.get_json()), "info")
        return jsonify({"status": "success",
                        "isAllowed": "true"})  # CLIENT: {"userId": "ID-ID-ID-ID-SEE-AUTH",	"username": "Name-Name-Name"}
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


# Logging for Server Events
@app.route("/metrics/server/event", methods=["POST"])
def metrics_server_event():
    get_remote_ip()
    try:
        print("Responded to metrics server event api call POST")
        graylog_logger("Metrics server event: " + str(request.get_json()), "info")
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


# [Backend]
@app.route("/tex", methods=["GET"])
def tex_get():
    get_remote_ip()
    try:
        return jsonify({"status": "success"})
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)

    t.start()


# ------------------------------------------------------- #
# global variables
# ------------------------------------------------------- #

config = load_config()
use_graylog = config['graylog']['use']
graylog_server = config['graylog']['host']
steam_api_key = config['steam']['api_key']

# ------------------------------------------------------- #
# main
# ------------------------------------------------------- #
setup_graylog()
keep_alive()
print("Exiting...")
exit(0)
