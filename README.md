# CSVCONV
Small python script used to convert a CSV file to various formats. Currently, it only supports HTML.

## Usage

### Configure environment
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

### First run
This tool expects the first column to be the data header.

It also allows you to merge columns by appending ">" to the column name. This works by merging the current column to the previous one if the previous ends with a ">" character.
Example:
```
col1;col2;col3>;col4
val1;val2;val3;val4
```
The following table will be created:
```
+------+------+-----------+
| col1 | col2 | col3:col4 |
+------+------+-----------+
| val1 | val2 | val3:val4 |
+------+------+-----------+
```

Sample run command:
```
$ python main.py sample.csv
```
