# XML2DCM-ECG

## Description

This repository contains a Python-based solution for converting ECG data from XML format to the DICOM (Digital Imaging
and Communications in Medicine) format. The goal of this project is to facilitate the process of transforming clinical
ECG data stored in XML files into a standardized, widely-used DICOM format, which is essential for healthcare systems,
medical imaging devices, and Electronic Health Record (EHR) systems.

The solution handles the extraction and conversion of ECG information, including patient details, acquisition context,
and waveform data, from XML files into the DICOM format. The project also integrates essential metadata such as the type
of ECG lead (e.g., Lead I, Lead II), device information (e.g., acquisition device, software versions), and patient
demographics.

## Installation
You can install XML2DCM-ECG directly from PyPI:
```bash
pip install XML2DCM-ECG
```

## Usage
After installation, you can run the ECG XML-to-DICOM converter directly using the command-line interface.
1. Set `--ecg_xml_path` to the directory containing the XML files to be converted.
2. Set `--output_dir` to the directory where you want the converted DICOM files to be saved. The default is `ecg_dicom`.
3. If you want to enable debug mode, set `--debug` to `True`. Only the first `--debug_n` files will be processed in this mode. 
The default value for `--debug` is `False`, and the default value for `--debug_n` is `5` when `--debug` is enabled.
4. Run the following command to convert the XML files to DICOM format:

   ```bash
   xml2dicom --ecg_xml_path /path/to/xml_files --output_dir /path/to/save_dicom --debug True --debug_n 5
   ```

## Example results

The following are examples of the ECG data converted from XML to DICOM format:
![ecg_dicom.png](https://raw.githubusercontent.com/MedxEng/XML2DCM-ECG/f9f461195a593d801b28f187a15c75244010c858/assets/ecg_dicom.png)
   

