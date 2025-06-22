import pandas as pd
from abc import ABC, abstractmethod



# Interface
class Exporter(ABC):
    @abstractmethod
    def export(self, data: pd.DataFrame, output_path: str) -> None:
        pass


# ---------------- Exporters ------------------

class CSVExporter(Exporter):
    def export(self, data: pd.DataFrame, output_path: str) -> None:
        data.to_csv(output_path, index=False)
        print(f"✅ Data exported to {output_path}")

class ExcelExporter(Exporter):
    def export(self, data: pd.DataFrame, output_path: str) -> None:
        data.to_excel(output_path, index=False)
        print(f"✅ Data exported to {output_path}")

class JSONExporter(Exporter):
    def export(self, data: pd.DataFrame, output_path: str) -> None:
        data.to_json(output_path, orient='records', indent=2)
        print(f"✅ Data exported to {output_path}")