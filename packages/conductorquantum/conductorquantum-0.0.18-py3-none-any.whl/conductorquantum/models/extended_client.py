from __future__ import annotations

import os
import tempfile
import typing
from json.decoder import JSONDecodeError
from typing import Union, Any

import numpy as np

from ..core.api_error import ApiError
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..core import File
from ..errors.not_found_error import NotFoundError
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from .client import ModelsClient, AsyncModelsClient
from ..types.http_validation_error import HttpValidationError
from ..types.model_result_public import ModelResultPublic

OMIT = typing.cast(Any, ...)

class ExtendedModelsClient(ModelsClient):
    """Extended models client that adds support for numpy arrays."""

    def _convert_to_file(self, data: Union[File, np.ndarray]) -> File:
        """
        Convert input data to a File object if necessary.
        
        Parameters
        ----------
        data : Union[File, np.ndarray,]
            The input data to convert
            
        Returns
        -------
        File
            A file object containing the data
        """
        if isinstance(data, np.ndarray):
            
            # Create a temporary file and save the numpy array
            temp_file = tempfile.NamedTemporaryFile(suffix='.npy', delete=False)
            file_handle = None
            try:
                np.save(temp_file, data)
                temp_file.close()
                # Open in binary read mode for upload
                file_handle = open(temp_file.name, 'rb')
                return file_handle
            finally:
                # Schedule file for deletion after it's closed
                os.unlink(temp_file.name)
                if file_handle and file_handle.closed:
                    file_handle.close()
        return data

    def execute(
        self,
        *,
        model: str,
        data: typing.Union[File, np.ndarray],
        plot: typing.Optional[bool] = OMIT,
        dark_mode: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ModelResultPublic:
        """Execute a model with the provided data."""
        file_obj = self._convert_to_file(data)
        _response = self._raw_client._client_wrapper.httpx_client.request( # pylint: disable=protected-access
            "models",
            method="POST",
            data={
                "model": model,
                "plot": plot,
                "dark_mode": dark_mode,
            },
            files={
                "data": file_obj,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ModelResultPublic,
                    parse_obj_as(
                        type_=ModelResultPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError as err:
            raise ApiError(status_code=_response.status_code, body=_response.text) from err
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncExtendedModelsClient(AsyncModelsClient):
    """Async version of ExtendedModelsClient with support for numpy arrays."""

    def _convert_to_file(self, data: Union[File, np.ndarray]) -> File:
        """
        Convert input data to a File object if necessary.
        
        Parameters
        ----------
        data : Union[File, np.ndarray]
            The input data to convert
            
        Returns
        -------
        File
            A file object containing the data
        """
        if isinstance(data, np.ndarray):
  
            # Create a temporary file and save the numpy array
            temp_file = tempfile.NamedTemporaryFile(suffix='.npy', delete=False)
            file_handle = None
            try:
                np.save(temp_file, data)
                temp_file.close()
                # Open in binary read mode for upload
                file_handle = open(temp_file.name, 'rb')
                return file_handle
            finally:
                # Schedule file for deletion after it's closed
                os.unlink(temp_file.name)
                if file_handle and file_handle.closed:
                    file_handle.close()
        return data

    async def execute(
        self, *, model: str, data: typing.Union[File, np.ndarray], request_options: typing.Optional[RequestOptions] = None
    ) -> ModelResultPublic:
        """
        Executes a model with the provided data.

        Parameters
        ----------
        model : str
            The model to run.

        data : Union[File, np.ndarray]
            The input data. Can be:
            - File: A file object (used as-is)
            - np.ndarray: A numpy array (automatically converted to .npy file)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ModelResultPublic
            Successful Response

        Raises
        ------
        NotFoundError
            If the model is not found.
        UnprocessableEntityError
            If the request is invalid.
        ApiError
            If there is an error processing the request.
      Examples
        --------
        Testing...

        """
        file_obj = self._convert_to_file(data)
        _response = await self._raw_client._client_wrapper.httpx_client.request( # pylint: disable=protected-access
            "models",
            method="POST",
            data={
                "model": model,
            },
            files={
                "data": file_obj,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ModelResultPublic,
                    parse_obj_as(
                        type_=ModelResultPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError as err:
            raise ApiError(status_code=_response.status_code, body=_response.text) from err
        raise ApiError(status_code=_response.status_code, body=_response_json) 
