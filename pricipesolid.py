import os
import streamlit as st
import io
from loader import LoaderFactory
import validator
import transformer
from exporter import CSVExporter, ExcelExporter, JSONExporter
from processor import DataProcessor



# ---------------- Interface Streamlit ------------------#
def run_app():
    st.set_page_config(page_title="🧹 Nettoyeur de Données", layout="centered")
    st.title("🧼 Application de Nettoyage de Données")
    st.markdown("Téléversez un fichier CSV, JSON ou Excel et obtenez un fichier propre.")

    uploaded_file = st.file_uploader("Choisissez un fichier", type=["csv", "json", "xlsx"])
    export_format = st.selectbox("Choisissez le format d'export", ["csv", "xlsx", "json"])

    if uploaded_file:
        extension = os.path.splitext(uploaded_file.name)[1]
        try:
            loader = LoaderFactory.get_loader(extension)
            data = loader.load(uploaded_file)
            logs = []

            if export_format == "csv":
                exporter = CSVExporter()
                output_name = "nettoye.csv"
                mime = "text/csv"
                output_bytes = lambda df: df.to_csv(index=False).encode('utf-8')
            elif export_format == "xlsx":
                exporter = ExcelExporter()
                output_name = "nettoye.xlsx"
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                output_bytes = lambda df: io.BytesIO().write(df.to_excel(index=False))  # manually override below
            elif export_format == "json":
                exporter = JSONExporter()
                output_name = "nettoye.json"
                mime = "application/json"
                output_bytes = lambda df: df.to_json(orient='records', indent=2).encode('utf-8')
            else:
                st.error("Format d’exportation non reconnu.")
                return
            

            processor = DataProcessor(
                loader=loader,
                validators=[
                    validator.RequiredColumnValidator(["IDclient", "article"]),
                    validator.NoMissingIDValidator("IDclient"),
                    validator.DropDuplicateValidator()
                ],
                transformers=[
                    transformer.DropEmptyRowsTransformer(),
                    transformer.StandardizeDataTransformer(),
                    transformer.CleanStringFieldsTransformer(),
                    transformer.FormatDateColumnsTransformer(["date"]),
                    transformer.ImputerNaN()
                    
                ],
                exporter=exporter
            )

            if st.button("🚀 Nettoyer les données"):
                result = processor.process(uploaded_file, output_name, logs)
                st.success("✔ Fichier nettoyé avec succès !")
                st.subheader("🔍 Journal des traitements effectués")
                for entry in logs:
                    st.write(entry)
                st.dataframe(result.head())

                if export_format == "xlsx":
                    towrite = io.BytesIO()
                    result.to_excel(towrite, index=False, engine='openpyxl')
                    towrite.seek(0)
                    st.download_button("📥 Télécharger le fichier nettoyé", data=towrite, file_name=output_name, mime=mime)
                else:
                    st.download_button("📥 Télécharger le fichier nettoyé", data=output_bytes(result), file_name=output_name, mime=mime)

        except Exception as e:
            st.error(f"Erreur : {e}")

if __name__ == "__main__":
    run_app()
