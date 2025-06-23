from abc import ABC, abstractmethod
import pandas as pd




# interface

class Validator(ABC):
    @abstractmethod
    def validate(self, data: pd.DataFrame, log: list) -> None:
        pass


# ---------------- Validators ------------------

class RequiredColumnValidator(Validator):
    def __init__(self, required_columns):
        self.required_columns = required_columns

    def validate(self, data: pd.DataFrame, log: list) -> None:
        missing = [col for col in self.required_columns if col not in data.columns]
        if missing:
            raise ValueError(f"Il manque la colonne: {missing}")
        log.append("✅ Colonnes obligatoires présentes")

class NoMissingIDValidator(Validator):
    def __init__(self, id_column):
        self.id_column = id_column

    def validate(self, data: pd.DataFrame, log: list) -> None:
        if data[self.id_column].isnull().any():
            raise ValueError(f"Il y'a une valeur null dans '{self.id_column}' column")
        log.append(f"✅ Aucun ID manquant dans '{self.id_column}'")

class DropDuplicateValidator(Validator):
    def validate(self, data: pd.DataFrame, log: list) -> None:
        before = len(data)
        data.drop_duplicates(inplace=True)
        after = len(data)
        log.append(f"✅ {before - after} doublons supprimés")