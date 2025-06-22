import exporter, transformer, validator
from loader import Loader

# ---------------- Processor ------------------

class DataProcessor:
    def __init__(self, loader: Loader, validators: list[validator.Validator], transformers: list[transformer.Transformer], exporter: exporter.Exporter):
        self.loader = loader
        self.validators = validators
        self.transformers = transformers
        self.exporter = exporter

    def process(self, filepath: str, output_path: str, log: list):
        data = self.loader.load(filepath)
        for validator in self.validators:
            validator.validate(data, log)
        for transformer in self.transformers:
            data = transformer.transform(data, log)
        self.exporter.export(data, output_path)
        return data
