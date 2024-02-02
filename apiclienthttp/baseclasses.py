from abc import ABC, abstractmethod


class BaseResponse(ABC):

    @abstractmethod
    def json(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def text(self):
        raise NotImplementedError()
