from decimal import Decimal
import os
from typing import Dict

import boto3


def handler(event: Dict, _: Dict) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.getenv("DYNAMO_TABLE_NAME"))
    table.put_item(
        Item={
            "PKEY": f"BLOGPOST#{event['detail']['PostId']}",
            "Author": event["detail"]["Author"],
            "Title": event["detail"]["Title"],
        }
    )
