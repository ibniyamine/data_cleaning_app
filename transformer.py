from abc import ABC, abstractmethod
import pandas as pd

# Interface
class Transformer(ABC):
    @abstractmethod
    def transform(self, data: pd.DataFrame, log: list) -> pd.DataFrame:
        pass



# ---------------- Transformers ------------------

class DropEmptyRowsTransformer(Transformer):
    def transform(self, data: pd.DataFrame, log: list) -> pd.DataFrame:
        before = len(data)
        data = data.dropna(how="all")
        after = len(data)
        log.append(f"✅ {before - after} lignes entièrement vides supprimées")
        return data

class StandardizeDataTransformer(Transformer):
    def transform(self, data: pd.DataFrame, log: list) -> pd.DataFrame:
        data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]
        log.append("✅ Noms des colonnes standardisés")
        return data

class CleanStringFieldsTransformer(Transformer):
    def transform(self, data: pd.DataFrame, log: list) -> pd.DataFrame:
        for col in data.select_dtypes(include="object").columns:
            data[col] = data[col].astype(str).str.strip().str.lower()
        log.append("✅ Champs texte nettoyés (espaces & majuscules)")
        return data
    
class ImputerNaN(Transformer):
    def transform(self, data: pd.DataFrame, log: list) -> pd.DataFrame:
        for col in data.select_dtypes(include="number").columns:
            if -0.5 <= data[col].skew() <= 0.5:
                data[col].fillna(data[col].mean(), inplace=True)
            else:
                data[col].fillna(data[col].median(), inplace=True)
        for col in data.select_dtypes("object").columns:
            data[col].fillna(data[col].mode()[0], inplace=True)
        for col in data.select_dtypes("datetime").columns:
            data[col].bfill(inplace=True)
            data[col].ffill(inplace=True)
        log.append("✅ Valuer NaN remplacé (Number et chaine et date)")
        return data

class FormatDateColumnsTransformer(Transformer):
    def __init__(self, date_columns):
        self.date_columns = date_columns

    def transform(self, data: pd.DataFrame, log: list) -> pd.DataFrame:
        for col in self.date_columns:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], errors="coerce")
        log.append("✅ Colonnes de date formatées")
        return data
