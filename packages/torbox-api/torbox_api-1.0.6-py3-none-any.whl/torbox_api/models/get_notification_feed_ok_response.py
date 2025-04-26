from typing import List
from typing import Union
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({"id_": "id"})
class GetNotificationFeedOkResponseData(BaseModel):
    """GetNotificationFeedOkResponseData

    :param auth_id: auth_id, defaults to None
    :type auth_id: str, optional
    :param created_at: created_at, defaults to None
    :type created_at: str, optional
    :param id_: id_, defaults to None
    :type id_: float, optional
    :param message: message, defaults to None
    :type message: str, optional
    :param title: title, defaults to None
    :type title: str, optional
    """

    def __init__(
        self,
        auth_id: str = SENTINEL,
        created_at: str = SENTINEL,
        id_: float = SENTINEL,
        message: str = SENTINEL,
        title: str = SENTINEL,
        **kwargs
    ):
        """GetNotificationFeedOkResponseData

        :param auth_id: auth_id, defaults to None
        :type auth_id: str, optional
        :param created_at: created_at, defaults to None
        :type created_at: str, optional
        :param id_: id_, defaults to None
        :type id_: float, optional
        :param message: message, defaults to None
        :type message: str, optional
        :param title: title, defaults to None
        :type title: str, optional
        """
        if auth_id is not SENTINEL:
            self.auth_id = auth_id
        if created_at is not SENTINEL:
            self.created_at = created_at
        if id_ is not SENTINEL:
            self.id_ = id_
        if message is not SENTINEL:
            self.message = message
        if title is not SENTINEL:
            self.title = title
        self._kwargs = kwargs


@JsonMap({})
class GetNotificationFeedOkResponse(BaseModel):
    """GetNotificationFeedOkResponse

    :param data: data, defaults to None
    :type data: List[GetNotificationFeedOkResponseData], optional
    :param detail: detail, defaults to None
    :type detail: str, optional
    :param error: error, defaults to None
    :type error: any, optional
    :param success: success, defaults to None
    :type success: bool, optional
    """

    def __init__(
        self,
        data: List[GetNotificationFeedOkResponseData] = SENTINEL,
        detail: str = SENTINEL,
        error: Union[any, None] = SENTINEL,
        success: bool = SENTINEL,
        **kwargs
    ):
        """GetNotificationFeedOkResponse

        :param data: data, defaults to None
        :type data: List[GetNotificationFeedOkResponseData], optional
        :param detail: detail, defaults to None
        :type detail: str, optional
        :param error: error, defaults to None
        :type error: any, optional
        :param success: success, defaults to None
        :type success: bool, optional
        """
        if data is not SENTINEL:
            self.data = self._define_list(data, GetNotificationFeedOkResponseData)
        if detail is not SENTINEL:
            self.detail = detail
        if error is not SENTINEL:
            self.error = error
        if success is not SENTINEL:
            self.success = success
        self._kwargs = kwargs
