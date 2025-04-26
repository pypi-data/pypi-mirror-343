# coding: utf-8
import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import StrictStr
from typing import Optional
from securden_sdk.models.get_password_200_response import GetPassword200Response

from securden_sdk.api_client import ApiClient, RequestSerialized
from securden_sdk.api_response import ApiResponse
from securden_sdk.rest import RESTResponseType


class DefaultApi:
    def __init__(self, api_client):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def get_password(
        self,
        account_id: Optional[int] = None,
        account_name: Optional[StrictStr] = None,
        account_title: Optional[StrictStr] = None,
        account_type: Optional[StrictStr] = None,
        account_category: Optional[int] = None,
        ticket_id: Optional[StrictStr] = None,
        reason: Optional[StrictStr] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> GetPassword200Response:
        """Retrieves password information


        :param account_id:
        :type account_id: int
        :param account_name:
        :type account_name: str
        :param account_title:
        :type account_title: str
        :param account_type:
        :type account_type: str
        :param account_category:
        :type account_category: int
        :param ticket_id:
        :type ticket_id: str
        :param reason:
        :type reason: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_password_get_serialize(
            account_id=account_id,
            account_name=account_name,
            account_title=account_title,
            account_type=account_type,
            account_category=account_category,
            ticket_id=ticket_id,
            reason=reason,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetPassword200Response",
            '400': None,
            '500': None,
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def get_password_with_additional_info(
        self,
        account_id: Optional[int] = None,
        account_name: Optional[StrictStr] = None,
        account_title: Optional[StrictStr] = None,
        account_type: Optional[StrictStr] = None,
        account_category: Optional[int] = None,
        ticket_id: Optional[StrictStr] = None,
        reason: Optional[StrictStr] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[GetPassword200Response]:
        """Retrieves password information


        :param account_id:
        :type account_id: str
        :param account_name:
        :type account_name: str
        :param account_title:
        :type account_title: str
        :param account_type:
        :type account_type: str
        :param account_category:
        :type account_category: int
        :param ticket_id:
        :type ticket_id: str
        :param reason:
        :type reason: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_password_get_serialize(
            account_id=account_id,
            account_name=account_name,
            account_title=account_title,
            account_type=account_type,
            account_category=account_category,
            ticket_id=ticket_id,
            reason=reason,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetPassword200Response",
            '400': None,
            '500': None,
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def get_password_without_preload_content(
        self,
        account_id: Optional[int] = None,
        account_name: Optional[StrictStr] = None,
        account_title: Optional[StrictStr] = None,
        account_type: Optional[StrictStr] = None,
        account_category: Optional[int] = None,
        ticket_id: Optional[StrictStr] = None,
        reason: Optional[StrictStr] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Retrieves password information


        :param account_id:
        :type account_id: str
        :param account_name:
        :type account_name: str
        :param account_title:
        :type account_title: str
        :param account_type:
        :type account_type: str
        :param account_category:
        :type account_category: int
        :param ticket_id:
        :type ticket_id: str
        :param reason:
        :type reason: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_password_get_serialize(
            account_id=account_id,
            account_name=account_name,
            account_title=account_title,
            account_type=account_type,
            account_category=account_category,
            ticket_id=ticket_id,
            reason=reason,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "GetPassword200Response",
            '400': None,
            '500': None,
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_password_get_serialize(
        self,
        account_id,
        account_name,
        account_title,
        account_type,
        account_category,
        ticket_id,
        reason,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if account_id is not None:
            
            _query_params.append(('account_id', account_id))
            
        if account_name is not None:
            
            _query_params.append(('account_name', account_name))
            
        if account_title is not None:
            
            _query_params.append(('account_title', account_title))
            
        if account_type is not None:
            
            _query_params.append(('account_type', account_type))
            
        if account_category is not None:
            
            _query_params.append(('account_category', account_category))
            
        if ticket_id is not None:
            
            _query_params.append(('ticket_id', ticket_id))
            
        if reason is not None:
            
            _query_params.append(('reason', reason))
            
        # process the header parameters
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/secretsmanagement/get_password_via_tools',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


