
from pathlib import Path


class DMSApi:

    def get_files_stored(self, date):
        """ Simulate the request to DSM API using the files saved"""

        path = Path.cwd() / "tests/dms-responses/" / f"{date}.jsonl"
        file = open(path, "r")

        return file.read()
