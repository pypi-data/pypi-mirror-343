from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def area(self):
        """Calculate the area of the shape"""
        pass

    @abstractmethod
    def _validate(self):
        """Input validation"""
        pass
