import os
from subprocess import run
from uuid import uuid4

import boto3
from localstack_client import session
from pytest import fixture

from src.index import handler


def get_output(name: str) -> str:
    stdout = run(
        f"cd localstack_tests && terraform output {name}",
        shell=True,
        check=True,
        capture_output=True,
    ).stdout.decode()
    return stdout.strip("\n").strip('"')


@fixture(autouse=True, scope="session")
def integration():
    if os.getenv("ENVIRONMENT") != "local":
        run("cd localstack_tests && terraform init", shell=True, check=True)
        run(
            "cd localstack_tests && terraform destroy -auto-approve",
            shell=True,
            check=True,
        )
        run(
            "cd localstack_tests && terraform apply -auto-approve",
            shell=True,
            check=True,
        )
    os.environ["DYNAMO_TABLE_NAME"] = get_output("dynamo_table_name")
    yield {}
    if os.getenv("ENVIRONMENT") != "local":
        run(
            "cd localstack_tests && terraform destroy -auto-approve",
            shell=True,
            check=True,
        )


@fixture(autouse=True)
def boto3_localstack_patch(monkeypatch):
    session_ls = session.Session()
    monkeypatch.setattr(boto3, "client", session_ls.client)
    monkeypatch.setattr(boto3, "resource", session_ls.resource)


@fixture()
def event():
    return {
        "detail": {
            "PostId": str(uuid4()),
            "Author": "Josh Armitage",
            "Title": "Don't Mock Me",
        },
        "detail-type": "v1",
        "source": "contino.BlogPublished",
    }


@fixture()
def table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ["DYNAMO_TABLE_NAME"])


def clear_item(key, table) -> None:
    if "Item" in table.get_item(Key=key):
        table.delete_item(Key=key)


def test_handler_does_not_throw_exception(event):
    handler(event, {})


def test_handler_writes_event_to_dynamo(event, table):
    key = {"PKEY": f"BLOGPOST#{event['detail']['PostId']}"}
    clear_item(key, table)

    handler(event, {})

    assert "Item" in table.get_item(Key=key)


def test_handler_writes_author_to_dynamo(event, table):
    key = {"PKEY": f"BLOGPOST#{event['detail']['PostId']}"}
    clear_item(key, table)

    handler(event, {})

    item = table.get_item(Key=key)["Item"]
    assert item["Author"] == event["detail"]["Author"]


def test_handler_writes_title_to_dynamo(event, table):
    key = {"PKEY": f"BLOGPOST#{event['detail']['PostId']}"}
    clear_item(key, table)

    handler(event, {})

    item = table.get_item(Key=key)["Item"]
    assert item["Title"] == event["detail"]["Title"]
