import abc


class IClient(abc.ABC):
    @abc.abstractmethod
    def sign_in(self) -> bool:
        pass
    
    @abc.abstractmethod
    def sign_out(self):
        pass
