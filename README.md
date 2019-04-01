# CertificateMakerSender
This tool will generate a training certificate in PDF format and send it to the recipient.

## GetttingStarted
These instructions will help you get a copy of this tool and how to make it work on your device.

### Installing

#### Download a copy:
```
git clone https://github.com/RonBulaon/CertificateMakerSender.git
```

#### To install requirements :
Ensure that you have edited the samples/namelist.csv to your actual data. Make a certificate template in PNG format.
```
cd CertificateMakerSender
```

```
pip install -r requirements.txt
```

#### Run:
Execute the tool by running below command (or make an executable file). Once the GUI has started supply the needed information from samples folder.
```
python app.py
```
#### Samples:
* output/namelist.csv - sample input file
* output/cert.png - sample certificate template
* samples/output/<files>.pdf - sample output files

#### Convert to an executable file:
Run command below and execute the file at dict/app.exe folder.
```
pyinstaller -wF app.py
```

### Acknowledgements
I have used the following modules. Thank you!
* fpdf - http://www.fpdf.org/
* PySimpleGUI - https://pypi.org/project/PySimpleGUI/
* PyInstaller - https://www.pyinstaller.org/
* HTML2PDF - https://pypi.org/project/html2pdf/
