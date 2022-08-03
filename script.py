from dotenv import load_dotenv
import requests
import os
import sys
import csv
import json

load_dotenv()
subdomain = os.environ["SUBDOMAIN"]
app_id = int(os.environ["APP_ID"])
email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]


def main():
    settings = {"models": ""}

    with open(os.path.join(sys.path[0], "models.csv"), "r", encoding="utf-8") as models:
        r = csv.DictReader(models)
        for row in r:
            if settings["models"]:
                settings["models"] += ";"
            settings["models"] += row["Model"]

    session = requests.Session()
    session.headers["Content-Type"] = "application/json"
    session.auth = (email, password)

    updateAppSettings(session, "Sell", settings)
    updateAppSettings(session, "Support", settings)
    input("Press ENTER to exit")
    return


def getInstallationId(session, product):
    if product == "Sell":
        url = f"https://{subdomain}.zendesk.com/api/sell/apps/installations.json"
    elif product == "Support":
        url = f"https://{subdomain}.zendesk.com/api/v2/apps/installations.json"
    else:
        print(f"{product} is not a supported product")
        return None

    res = session.get(url)
    resJSON = res.json()
    if res.status_code == 200 and resJSON:
        for installation in resJSON["installations"]:
            if installation["app_id"] == app_id:
                return installation["id"]
    else:
        print(f"Unable to get app installations: {res.status_code} - {resJSON.text}")
        return None


def updateAppSettings(session, product, settings):
    installationId = getInstallationId(session, product)
    if installationId:
        print(f"{product} app ID {app_id} found with installation ID {installationId}")
    else:
        print(f"{product} app ID {app_id} not found")
        return False

    if product == "Sell":
        url = f"https://{subdomain}.zendesk.com/api/sell/apps/installations/{installationId}.json"
    elif product == "Support":
        url = f"https://{subdomain}.zendesk.com/api/v2/apps/installations/{installationId}.json"
    else:
        print(f"{product} is not a supported product")
        return False

    data = json.dumps({"settings": settings})
    res = session.put(url=url, data=data)
    resJSON = res.json()
    if res.status_code == 200 and resJSON:
        print(f"Sucessfully updated {product} app settings")
        return True
    else:
        print(
            f"Error updating {product} app settings: {res.status_code} - {resJSON.text}"
        )
        return False


if __name__ == "__main__":
    main()
