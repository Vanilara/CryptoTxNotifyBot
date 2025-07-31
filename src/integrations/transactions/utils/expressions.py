from pydantic import BaseModel
from core.networks import Network
from utils.hasher.common import Hasher
import logging

import json

JS_TEMPLATE = """
function main(payload) {{
  const TARGET_ADDRESSES = {addresses};
  if (!Array.isArray(payload.data)) return null;
  const matchedLogs = [];
  for (const logGroup of payload.data) {{
    for (const log of logGroup) {{
      if (log.length == 0) continue;
      for (const l of log) {{
        if (
          log[0].topics[0] === "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" &&
          (
            TARGET_ADDRESSES.includes(log[0].topics[1].toLowerCase()) ||
            TARGET_ADDRESSES.includes(log[0].topics[2].toLowerCase())
          )
        ) {{
          matchedLogs.push(log[0]);
        }}
      }}
    }}
  }}
  return matchedLogs.length > 0 ? matchedLogs : null;
}}
"""
class Expression(BaseModel):
    hashed: str
    readable: str

class ExpressionMaker:
    transfer_event = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

    @classmethod
    def make_expression(
        cls, network: Network, addresses: list
    ) -> Expression:
        converted_addresses =[
            network.addresses_converter.convert_to_evm(address) for address in addresses
        ]
        if len(converted_addresses) == 1:
            converted_addresses = [converted_addresses[0]]
        expression = JS_TEMPLATE.format(addresses=json.dumps(converted_addresses, ensure_ascii=False)).strip()
        clear_expression = " ".join(expression.split())
        hashed_expression = Hasher.hash_to_base_64(clear_expression)
        return Expression(
            hashed = hashed_expression,
            readable = clear_expression
        )