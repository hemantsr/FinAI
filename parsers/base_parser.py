from abc import ABC, abstractmethod
import pandas as pd

class BrokerParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> pd.DataFrame:
        """
        Must return DataFrame with columns:
        stock_name, isin, quantity, closing_value
        """
        pass
