import base64
import json
import logging
import os.path
from pathlib import Path
from typing import Union

from srunbit.model import Account

home = Path.home()
name = ".bitsrun"
path = os.path.join(str(home), name)


def read_account() -> Union[Account, None]:
    try:
        with open(path, "rb") as f:
            ss = f.read()
            s = base64.b64decode(ss)
            return Account.from_dict(json.loads(s))
    except Exception as e:
        logging.debug(f"failed to read account: {e}")
        return None


def write_account(account: Account):
    with open(path, "wb") as f:
        s = json.dumps(account.to_dict())
        ss = base64.b64encode(bytes(s, encoding="utf-8"))
        f.write(ss)
