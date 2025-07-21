
import zipfile

zip_pfad = r"C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Ati_java_lib\commons-math4-4.0-beta1-bin.zip"

with zipfile.ZipFile(zip_pfad, 'r') as zip_ref:
    for dateiname in zip_ref.namelist():
        print(dateiname)
