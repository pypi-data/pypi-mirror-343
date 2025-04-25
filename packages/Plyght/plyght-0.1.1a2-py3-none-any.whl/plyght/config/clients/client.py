"""
Defines an abstract client class that provides a core interface for client wrappers.
Subclasses must implement the connection handling methods and reference an underlying
client object.
"""

from abc import ABC, abstractmethod


class Client(ABC):
    """
    Abstract client class for implementing wrappers around external services.
    Subclasses must define how to connect, disconnect, and expose connection
    properties. The _config attribute can be set externally or inherited from
    a configuration decorator.
    """

    def __init__(self, **kwargs):
        """
        Initialize the client with an optional config dictionary. Additional
        keyword arguments are stored in _config, allowing subclass flexibility.
        """
        self._config = (
            kwargs | self._config.dump() if hasattr(self, "_config") else kwargs
        )

    @property
    @abstractmethod
    def client(self):
        """
        Return the underlying client instance.
        Must be implemented by subclasses.
        """
        pass

    @property
    @abstractmethod
    def status(self):
        """
        Return the current connection status. Subclasses may override with
        more detailed information.
        """
        pass

    @property
    @abstractmethod
    def host(self):
        """
        Return the host address from the client configuration, if specified.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def connect(self):
        """
        Establish a connection to the underlying service.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Terminate the connection to the underlying service.
        Must be implemented by subclasses.
        """
        pass
