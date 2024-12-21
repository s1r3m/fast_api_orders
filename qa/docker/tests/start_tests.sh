#!/usr/bin/env bash
set -ex

poetry run pytest tests --alluredir allure-results --clean-alluredir
