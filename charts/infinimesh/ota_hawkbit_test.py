#!/usr/bin/env python3
"""Render the chart and check the hawkBit addon Deployment."""

import subprocess
import sys

CHART = "charts/infinimesh"
ON = [
    "--set", "addons.otaHawkbit.enabled=true",
    "--set", "addons.otaHawkbit.image.tag=local",
    "--set", "addons.otaHawkbit.otaNamespace=plant",
    "--set", "addons.otaHawkbit.hawkbitURL=https://hawkbit.example",
    "--set", "addons.otaHawkbit.existingSecret=ota-hawkbit",
]


def render(extra):
    return subprocess.check_output(
        ["helm", "template", "infinimesh", CHART, *extra], text=True
    )


def docs(text):
    return [d for d in text.split("---\n") if d.strip()]


def fail(msg):
    sys.exit(msg)


def deployment(text):
    found = []
    for doc in docs(text):
        if "kind: Deployment" in doc and "name: infinimesh-ota-hawkbit" in doc:
            found.append(doc)
    return found


off = render([])
if deployment(off):
    fail("disabled chart rendered infinimesh-ota-hawkbit")

on = render(ON)
got = deployment(on)
if len(got) != 1:
    fail(f"enabled chart rendered {len(got)} ota-hawkbit Deployments")

body = got[0]
for key in ("OTA_ADDON_TOKEN", "HAWKBIT_USER", "HAWKBIT_PASSWORD"):
    if f"key: {key}" not in body or "secretKeyRef:" not in body:
        fail(f"{key} is not read from a secret")
if "name: ota-hawkbit" not in body:
    fail("existingSecret name was not rendered")
for bad in ("CHANGEME", "admin", "seeeecreet"):
    if bad in body:
        fail(f"deployment contains {bad}")

for doc in docs(on):
    if "kind: Secret" in doc and "OTA_ADDON_TOKEN" in doc:
        fail("chart wrote OTA_ADDON_TOKEN into a Secret")

both = subprocess.run(
    ["helm", "template", "infinimesh", CHART, *ON, "--set", "addons.otaHawkbit.otaNamespaces=other"],
    text=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
if both.returncode == 0:
    fail("both namespace settings were accepted")
