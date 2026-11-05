#The interface is a contract that should be signable by any object that can-be-shipped.

from abc import ABC, abstractmethod

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return shipping cost. Every class that signs this contract must implement this method."""
        pass