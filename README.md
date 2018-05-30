# auditor v2.0.0
Makes sure your CSV's remain compliant

There are times that CSV files need either cleaning, or replacement of certain items, or filtering 
of specific values or sorting etc. 

Enter Auditor. This software is meant to scan through and clean your csv in various ways and make sure that
everything is ready to go before your application needs to do the rest of the data processing.

## Configs

Auditor no longer uses configs as of version `2.0.0`. Please consult the examples to figure out how to
migrate to the new system.

## Usage

Auditor defines a Domain Specific Language (D.S.L) which is yet to be named. It allows one to write an
auditor program that operates on a csv on a row by row basis to do things like rename columns, apply
data transforms, remove whitespace, compare one value in a row to another, whitelist and blacklist items,
and do lookups.

`$ auditor <path_to_my_program>`

## Development

Adding further features to auditor falls into two categories: new column transforms and other things.
If all you need is to add a transform to the `col` block to implement something, for example fixed length
fields, follow the following steps:

  * fork this repo
  * clone this repository
  * install the dev-requirements with `pip3 install -r dev-requirements.txt`
  * 'cd <repo-clone-directory>/auditor/transforms'
  * run `python3 ../dev_scripts/make_new_col_transform.py <transforms-you-need>...`
  * edit the code till it works. Testing against a program and data file in the examples directory
  * submit a pull request

## Examples

Look in the examples folder for a sample program of all features that are currently implemented.

## Language specification

There are two parts to the auditor D.S.L. The preamble, which describes the two csv files, their paths,
how they are structured and whether to remove bad data, and the `col` blocks which describe how to transform
a given row column pair in a csv.

In the D.S.L. you can specify a string with spaces by surrounding it with `"` characters.

### Preamble

| keyword           | meaning / function                                             |      # args | arg types                                       |
|-------------------|----------------------------------------------------------------|-------------|-------------------------------------------------|
| `read`            | specifies the input file                                       |           1 | relative file path from where the script is run |
| `write`           | specifies the output file                                      |           1 | relative file path from where the script is run |
| `separator`       | the character that separates columns in the input file         |           1 | single unescaped character                      |
| `quotechar`       | the character that quotes a cell in the input file             |           1 | single unescaped character                      |
| `encoding`        | the encoding of the input file                                 |           1 | an encoding string python3 understands          |
| `column_add`      | adds any columns to the output                                 | more than 0 | space separated list of column names to add     |
| `column_order`    | the output order of the columns                                | num of cols | space separated list of column names in order   |
| `column_rename`   | rename column from first arg to second                         |           2 | space separated list of old column name and new |
| `remove_bad_data` | flag to remove rows from the output with a `<BAD_DATA>` string |           0 | this arg is a flag and takes no args            |

Note that columns not listed in the column order will not be put into the output file.

Additionally you can have as many column rename instructions as you want. If you want to rename 5 columns, you should have 5 instructions.

### col blocks

These describe the sequence of transforms to take place in a run of auditor. Each block should have:
  * A newline before and after
  * A start line of `col <column_name> <optional_priority>`
  * An ending line of `| done`
  
The column name in the first line should be the name after renaming. The priority denotes which blocks get executed first.
Since a column has access to the rest of the row, there are times you want to do something before something else.
Higher priority col blocks get executed first. If two col blocks have the same priority, there is no defined behavior for
which goes first.
