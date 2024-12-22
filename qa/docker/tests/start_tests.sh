#!/usr/bin/env bash
set -ex

poetry run pytest --alluredir allure-results tests
