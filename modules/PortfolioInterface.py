import abc

class PortfolioInterface(metaclass=abc.ABCMeta): 
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_pdf') and
            callable(subclass.load_pdf) or
            NotImplementedError)

    @abc.abstractmethod
    def load_pdf(self, pdf_file):
        """ The child classes must implement this method """
        raise NotImplementedError
