# Pdf To Unicode
Convert Pdf Files containing Krutidev and/or latin to unicode while preserving font information

## Dependencies
* Python version 2.7
* pdfminer `pip install pdfminer`

```bash
$ python2 pdf2unicode.py -i input.pdf -o output.txt
```

Pdfs containg kurtidev along with latin characters are supported given that font information is encoded with every character. See sample Directory for reference.
Converts those pdfs successfully keeping intact the different font information to unicode

View Sample Conversions in the sample Directory
