from urllib3.exceptions import InsecureRequestWarning
import warnings
from daspython.services.alcs.aclservice import AclService, ChangeOwnershipRequest
from daspython.common.api import Token
from daspython.auth.authenticate import DasAuth
from dotenv import load_dotenv
import os
import unittest
import sys
sys.path.insert(0, "C:\Workspace\das-python\daspython")

load_dotenv(dotenv_path='./.env')
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


class TestAclService(unittest.TestCase):

    def _get_token(self) -> Token:
        load_dotenv()
        auth = DasAuth(os.getenv("DAS_URL"), os.getenv(
            "DAS_USERNAME"), os.getenv("DAS_PASSWORD"))
        auth.authenticate(os.getenv("CHECK_HTTPS").lower() == 'true')
        return auth

    def test_change_owner(self):

        acl_service = AclService(self._get_token())

        payload = ChangeOwnershipRequest()
        payload.attributeId = 55
        payload.entryId = 'f3cfd83d-b95d-4876-9217-312eec681e37'
        payload.newOwnerId = 57

        response = acl_service.change_owner(payload)

        self.assertEqual(response, True)


if __name__ == '__main__':
    unittest.main()
