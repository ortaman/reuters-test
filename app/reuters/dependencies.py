
from pathlib import Path


class DMSApi:

    def get_content_file(self, date):
        """ 
        Simulate the request to DSM API
        Return the url where the file was downloaded

        """
    
        path = Path.cwd() / "tests/dms-responses/" / f"{date}.jsonl"
        return path
