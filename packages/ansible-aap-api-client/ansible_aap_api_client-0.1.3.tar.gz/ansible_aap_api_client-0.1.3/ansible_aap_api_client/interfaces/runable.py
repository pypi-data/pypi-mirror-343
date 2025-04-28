"""
Runable interface
"""

from abc import ABC, abstractmethod


class Runable(ABC):  # pylint: disable=too-few-public-methods
    """Interface for a runable object"""

    @abstractmethod
    def run(self, *args, **kwargs) -> None:
        """Abstract method to run an object

        :param args: Arguments
        :type args: Tuple
        :param kwargs: Keyword arguments
        :type kwargs: Dict

        :rtype: None
        :returns: Nothing
        """
