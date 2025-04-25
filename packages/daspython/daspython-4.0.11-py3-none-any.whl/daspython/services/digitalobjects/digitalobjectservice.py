from datetime import datetime
import json
import uuid
import requests
import os
from os.path import exists
from daspython.common.api import ApiMethods, Token
from daspython.services.entries.entryservice import EntryService
from enum import Enum
import base64
from math import ceil

class FileUploadForm():
    description = None
    digitalObjectTypeId = None
    fileName = None
    fileSize = 0
    index = 0
    totalCount = 0
    id = None


class UploadDigitalObjectRequest():
    entryCode = ''
    filePath = ''
    description = ''
    digital_object_type = 'Data file'


class AttributeDigitalObjectInput():
    attributeId: int
    attributeValueId: str
    digitalObjectId: str
    isDeleted: bool


class LinkExistingDigitalObjectInput():
    attributeId: int
    attributeValueId: str
    digitalObjects: list[dict]


class DownloadRequestInput():

    def __init__(self, entry_code: str, digital_object_codes: list[str]) -> None:
        self.entry_code = entry_code
        self.digital_object_codes = digital_object_codes


CHUNK_SIZE = 1000000


class DownloadRequestItemStatus(Enum):
    Enqueued = 1
    ApprovalRequested = 2
    WaitingForApproval = 3
    Approved = 4
    Declined = 5
    DeclinedNotificationSent = 6
    WaitingToBeDownloaded = 7
    InProcess = 8
    AvailableToDownload = 9
    Error = 10
    


class DownloadRequestStatus(Enum):
    NONE = 0
    Enqueued = 1
    ApprovalRequested = 2
    WaitingForApproval = 3
    Approved = 4
    Declined = 5
    HandleFilesToBeDelivered = 6
    CompatctingBundle = 7
    Completed = 8
    Incomplete = 9
    Failed = 10


class DownloadRequestItem():
    id: str
    is_ready: bool
    requester: str
    createdOn: datetime
    comment: str
    request_status: DownloadRequestStatus
    files: list[FileUploadForm]


class DownloadRequestResponse():
    total_count: int
    items: list[DownloadRequestItem]


class DigitalObject():
    id: str
    code: str
    name: str
    needle: str
    instrument: str
    digital_object_type: str
    comment: str
    owner: str
    file_status: DownloadRequestItemStatus


class DigitalObjectService(ApiMethods):
    def __init__(self, auth: Token):
        super().__init__(auth)

    # This is our chunk reader. This is what gets the next chunk of data ready to send.
    def __read_in_chunks(self, file_object, CHUNK_SIZE):
        while True:
            data = file_object.read(CHUNK_SIZE)
            if not data:
                break
            yield data

    def upload_to_entry(self, entry_code, file_path, description):
        request = UploadDigitalObjectRequest()
        request.entryCode = entry_code
        request.filePath = file_path
        request.description = description
        self.upload(request)

    def upload(self, request: UploadDigitalObjectRequest):

        if (not request or request.entryCode is None or request.filePath is None):
            raise Exception(
                'Invalid request. Entry Code and file path are required.')

        if not exists(request.filePath):
            raise FileNotFoundError(f'File not found at: {request.filePath}')

        file_metadata = FileUploadForm()

        head, tail = os.path.split(request.filePath)

        file_metadata.fileName = tail
        file_metadata.fileSize = os.path.getsize(request.filePath)
        file_metadata.description = request.description
        file_metadata.digitalObjectTypeId = self.__get_digital_object_type_id(request.digital_object_type)
        file_metadata.id = str(uuid.uuid4())
        file_metadata.description = request.description
        file_metadata.totalCount = ceil(file_metadata.fileSize / CHUNK_SIZE)
        file_metadata.index = 0

        binary_file = open(request.filePath, "rb")

        index = 0
        offset = 0
        headers = {}

        digital_object_id = None

        for chunk in self.__read_in_chunks(binary_file, CHUNK_SIZE):

            offset = index + len(chunk)
            headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset - 1, file_metadata.fileSize)
            headers['Authorization'] = f'bearer {self.token.api_token}'
            index = offset            
            json_string = json.dumps(file_metadata.__dict__)
            base64_bytes = base64.b64encode(json_string.encode('utf-8'))
            headers['metadata'] = base64_bytes.decode('utf-8') 
            
            try:

                file = {"file": chunk}
                r = requests.post(self.token.api_url_base + "/File/UploadDigitalObject",
                                  files=file, headers=headers, verify=self.token.check_https)
                if r.status_code != 200:
                    raise Exception(
                        f'Error uploading file. Status code: {r.status_code}')
                
                response = json.loads(r.content.decode('utf-8'))
                
                file_metadata.index += 1

                if response.get('result') is None:
                    continue

                digital_object_id = response.get('result')['id']

            except Exception as e:
                raise Exception(
                    f'Error uploading file: {e}')

        binary_file.close()

        self.__set_digital_object_relation(
            request.entryCode, digital_object_id)

    def __set_digital_object_relation(self, entry_code: str, digital_obj_id: str) -> None:

        entry_service = EntryService(self.token)

        response = entry_service.get_entry_by_code(code=entry_code)

        if response is None or response.entry is None:
            raise Exception(f'Entry not found with the code: {entry_code}')

        input = LinkExistingDigitalObjectInput()

        input.attributeId = response.attributeId
        input.attributeValueId = response.entry['id']
        attribute_value_digital_object = {
            'attributeId': response.attributeId,
            'attributeValueId': response.entry['id'],
            'digitalObjectId': digital_obj_id,
            'isDeleted': False
        }
        input.digitalObjects = []
        input.digitalObjects.append(attribute_value_digital_object)

        api_url = '/api/services/app/DigitalObject/LinkExistingDigitalObject'
        self.post_data(api_url, input)

    def __get_digital_object_type_id(self, digital_object_type: str) -> str:

        entry_service = EntryService(self.token)
        response = entry_service.get_entry_by_name(
            name=digital_object_type, attribute_name='Digital Object Type')

        if response is None:
            raise Exception(
                'Invalid Digital Object Type {digital_object_type}')

        return response['id']

    def link_existing(self, entry_code, digital_object_code):

        entry_service = EntryService(self.token)

        response_digital_object = entry_service.get_entry_by_code(
            code=digital_object_code)

        if response_digital_object is None or response_digital_object.entry is None:
            raise Exception(
                f'Digital Object not found with the code: {digital_object_code}')

        self.__set_digital_object_relation(
            entry_code=entry_code, digital_obj_id=response_digital_object.entry['id'])

    def create_download_request(self, download_request_input: list[DownloadRequestInput]):
        """
        Creates a download request based on the provided input.

        This method takes a list of DownloadRequestInput objects and generates a download request.

        Args:
            download_request_input (list[DownloadRequestInput]): A list of DownloadRequestInput
                objects that contain the necessary information for creating the download request.
                Defaults to an empty list.

        Returns:
            any | None: Returns the generated download request if successful, or None if there was an error.

        Example:

            download_inputs = [
                DownloadRequestInput(entry_code='a.b.c', digital_object_codes=['x.0y.z', 'x.3y.w']),
                DownloadRequestInput(entry_code='d.e.f', digital_object_codes=['x.1y.z', 'x.2y.w'])
            ]

            service = DigitalObjectService(get_token())
            request = service.create_download_request(download_inputs)
            if request:
                # Process the download request
            else:
                # Handle the error

        Note:
            - The `DownloadRequestInput` class should be properly defined with required attributes.
            - The returned value can be of any relevant type that represents the download request.
            - If an error occurs during download request creation, the method returns None.
        """

        request_body = {
            'items': []
        }

        if (download_request_input is None):
            raise Exception('Invalid input. Input is required.')

        if (len(download_request_input) == 0):
            raise Exception('Invalid input. Input is empty.')

        for request_input in download_request_input:

            response = self.__get_entry(request_input)

            entry_digital_object_list = json.loads(response.entry.get('6'))

            # If no digital object codes are provided, then all digital objects will be included in the request
            if (request_input.digital_object_codes is None or len(request_input.digital_object_codes) == 0):
                entry_do_code_list = [digital_object.get('code')
                                      for digital_object in entry_digital_object_list]
            else:
                # checks if the digital object code is in the entry digital object list
                entry_do_code_list = [digital_object.get('code') for
                                      digital_object in entry_digital_object_list if digital_object.get('code') in request_input.digital_object_codes]

            for digital_object_code in entry_do_code_list:
                item = self.__get_digital_object_id_name(
                    digital_object_code, entry_digital_object_list)
                item['sourceId'] = response.entry.get('id')
                item['sourceAttributeId'] = response.attributeId
                request_body['items'].append(item)

        api_url = '/api/services/app/DownloadRequest/Create'
        response = self.post_json_data(
            url=api_url, json_data=json.dumps(request_body))

        return response

    def __get_entry(self, request_input):

        entry_service = EntryService(self.token)

        if (request_input.entry_code is None):
            raise Exception('Invalid input. Entry code is required.')
        if (request_input.digital_object_codes is None):
            raise Exception(
                f'Invalid input. Digital object codes are required for {request_input.entry_code}.')

        response = entry_service.get_entry_by_code(
            code=request_input.entry_code)

        if response is None or response.entry is None:
            raise Exception(
                f'Entry not found with the code: {request_input.entry_code}')

        if response.entry.get('6') is None:
            raise Exception(
                f'No digital objects where found for an entry the following code: {request_input.entry_code}')

        return response

    def create_digital_object_download_request(self, digital_object_codes: list[str]):
        pass

    # def create_download_request(self, entry_code: str, digital_object_code_list: list[str] = []):

    #     entry_service = EntryService(self.token)

    #     response = entry_service.get_entry_by_code(entry_code)
    #     entry = response.entry

    #     if (entry is None):
    #         raise Exception(
    #             f'No entry found with the following code: {entry_code}')

    #     if (entry.get('6') is None):
    #         raise Exception(
    #             f'No digital objects where found for an entry the following code: {entry_code}')

    #     json_do_list = json.loads(entry.get('6'))

    #     entry_dos = [digital_object.get('code')
    #                  for digital_object in json_do_list]

    #     dos_set = set(entry_dos)

    #     intersection = [] if digital_object_code_list is None else list(
    #         dos_set.intersection(digital_object_code_list))

    #     input = {
    #         'items': []
    #     }

    #     if intersection:
    #         for digital_object_code in intersection:
    #             item = self.__get_request_items(
    #                 digital_object_code, json_do_list)
    #             item['sourceId'] = response.entry.get('id')
    #             item['sourceAttributeId'] = response.attributeId
    #             input['items'].append(item)
    #     else:
    #         for digital_object_code in entry_dos:
    #             item = self.__get_request_items(
    #                 digital_object_code, json_do_list)
    #             item['sourceId'] = response.entry.get('id')
    #             item['sourceAttributeId'] = response.attributeId
    #             input['items'].append(item)

    #     api_url = '/api/services/app/DownloadRequest/Create'
    #     response = self.post_json_data(
    #         url=api_url, json_data=json.dumps(input))
    #     return response

    def __get_digital_object_id_name(self, digital_object_code: str, entry_digital_object_list: any) -> any:
        digital_object = next(x for x in entry_digital_object_list if x.get(
            'code') == digital_object_code)
        result = {
            'name': digital_object.get('name'),
            'id': digital_object.get('id')
        }
        return result

    def get_my_requests(self) -> DownloadRequestResponse:

        api_url = '/api/services/app/DownloadRequest/GetMyRequests'
        response = self.get_data(url=api_url, request=None)

        result = DownloadRequestResponse()
        result.total_count = response.get('result').get('totalCount')
        result.items = self.__get_download_request_items(
            response.get('result').get('items'))
        return result

    def __get_download_request_items(self, items: any) -> list[DownloadRequestItem]:

        result = []

        for item in items:
            request_item = DownloadRequestItem()
            request_item.requester = item.get('requester')
            request_item.comment = item.get('comment')
            request_item.createdOn = None if item.get('createdOn') is None else datetime.strptime(
                item.get('createdOn')[:19], '%Y-%m-%dT%H:%M:%S')
            request_item.request_status = None if item.get(
                'status') is None else DownloadRequestStatus(item.get('status'))
            request_item.id = item.get('id')
            request_item.is_ready = item.get('isRead')
            request_item.files = self.__get_download_request_files(
                item.get('files'))
            result.append(request_item)

        return result

    def __get_download_request_files(self, items: any) -> list[DigitalObject]:

        result = []

        for item in items:
            digital_object = DigitalObject()
            digital_object.code = item.get('code')
            digital_object.comment = item.get('comment')
            digital_object.name = item.get('fileName')
            digital_object.needle = item.get('neddle')
            digital_object.instrument = item.get('instrument')
            digital_object.digital_object_type = item.get('digitalObjectType')
            digital_object.file_status = None if item.get(
                'status') is None else DownloadRequestItemStatus(item.get('status'))
            result.append(digital_object)

        return result

    def get_files_from_download_request(self) -> bool:
        """Download files from pending download requests."""

        results = []

        completed_download_requests = self.get_completed_download_requests()

        for request in completed_download_requests:
            request_url = f'/File/DownloadRequestSet?requestId={request.id}'
            result = self.download_file(url=request_url)
            results.append(result)

        # Return True if all requests were successful
        return all(results)

    def get_completed_download_requests(self):
        """Retrieve pending download requests."""

        response = self.get_my_requests()
        pending_requests = [
            request for request in response.items if not request.is_ready]

        return pending_requests
