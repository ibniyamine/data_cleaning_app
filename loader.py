from abc import ABC, abstractmethod
import pandas as pd
import json


# interface
class Loader(ABC):
    @abstractmethod
    def load(self, filepath: str) -> pd.DataFrame:
        pass


# ---------------- Loaders ------------------
# class
class CSVLoader(Loader):
    def load(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

class JSONLoader(Loader):
    def load(self, filepath: str) -> pd.DataFrame:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)

class ExcelLoader(Loader):
    def load(self, filepath: str) -> pd.DataFrame:
        return pd.read_excel(filepath)
    


# ---------------- Factory Pattern ------------------

class LoaderFactory:
    loaders = {
        ".csv": CSVLoader,
        ".json": JSONLoader,
        ".xlsx": ExcelLoader
    }

    @staticmethod
    def get_loader(extension: str) -> Loader:
        loader_class = LoaderFactory.loaders.get(extension.lower())
        if not loader_class:
            raise ValueError(f"No loader for extension {extension}")
        return loader_class()

