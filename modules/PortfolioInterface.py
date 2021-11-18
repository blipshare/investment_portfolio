import abc

from os import path

import pyarrow as pa
import pyarrow.parquet as pq

class PortfolioInterface(metaclass=abc.ABCMeta): 
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_pdf') and
            callable(subclass.login) or
            callable(subclass.get_top_movers) or
            NotImplementedError)

    @abc.abstractmethod
    def login(self):
        """ The child classes must implement this method """
        raise NotImplementedError

    @abc.abstractmethod
    def get_top_movers(self, output_dir, sp500=False, direction=None):
        """ The child classes must implement this method """
        raise NotImplementedError

    def write_to_output_file(self, df, name, output_dir):
        output_file = path.join(output_dir, '%s.parquet' % name)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, output_file)

    def load_parquet_file(self, filename, columns=None):
        if columns:
            return pq.read_pandas(filename, columns=columns).to_pandas()
        else:
            return pq.read_pandas(filename).to_pandas()

