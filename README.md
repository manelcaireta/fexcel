# Fexcel

A simple mock excel generator. `fexcel` reads a `JSON` file declaring the excel schema to use and creates a new excel file with said configuration.

## Installation

Install fexcel with `pip`

```sh
pip install fexcel
```

check the installation was successful

```sh
fexcel --help
```

## Usage

Before using fexcel, a JSON file containing the schema to be used for the fake resulting excel should be created. For example, to create a fake excel with a name and an address you would use

```json
[
  {
    "name": "Employee",
    "type": "name"
  },
  {
    "name": "Address",
    "type": "address"
  }
]
```

Then, you would use `fexcel` to create the resulting excel.

### CLI

You can use the command line to create a fake excel based on an existing schema declaration

```sh
fexcel /path/to/input/schema.json /path/to/output/file.xlsx --num-fakes 100
```

### API

You can leverage `fexcel`'s main interface `Fexcel` to parse a schema and write the resulting excel in a file as such

```python
from fexcel import Fexcel

fexcel = Fexcel.from_file("schema.json")
fexcel.write_to_file("output.xlsx")
```

## Plugins

`fexcel` relies on [`faker`](https://pypi.org/project/Faker/) to generate quality mock data and [`pyexcel`](https://docs.pyexcel.org/en/latest/) for excel file handling.

As `pyexcel` has a plugin structure, `fexcel` has a plugin structure too, and to work with each different kind of file a dedicated `pyexcel` plugin should be installed.

As a commodity, several extras can be installed alongside `fexcel` to work with the most usual file type (based on [`pyexcel`](https://docs.pyexcel.org/en/latest/#id3) own plugin table). The following table lists them:

| extra | file types                          |
| ----- | ----------------------------------- |
| csv   | `.csv`, `.tsv`, `.csvz` and `.tsvz` |
| xls   | `.xls`                              |
| xlsx  | `.xlsx`                             |
| ods   | `.ods`                              |
| all   | All of the above                    |

Therefore, to handle `.xlsx` files you would install `fexcel` as

```
pip install 'fexcel[xlsx]'
```

## Schema

Fexcel expects to have its schema defined in a JSON file with the following structure

```json
[
  {
    "name": "FIRST_FIELD_NAME",
    "type": "FIRST_FIELD_TYPE",
    "constraints": {
      "constraint1": "CONSTRAINT_VALUE",
      "constraint2": "CONSTRAINT_VALUE"
    }
  },
  {
    "name": "SECOND_FIELD_NAME",
    "type": "SECOND_FIELD_TYPE",
    "constraints": {
      "constraint1": "CONSTRAINT_VALUE"
    }
  }
]
```

- The `name` attribute defines how the final excel field will be named.
- The `type` attribute specifies the data type of the field.
- The `constraints` attribute specifies a set of key-value pairs to customize how the data will be generated.

The `name` and `type` attributes are required and the `constraints` attribute is always optional and has a default implementation.

The possible `constraints` for each `type` are listed below.

### Text Fields

The supported text fields are

| type     | description                           |
| :------- | :------------------------------------ |
| Name     | An ordinary randomly generated name   |
| Email    | A randomly generated e-mail           |
| Phone    | A phone address                       |
| Address  | An address of a person or institution |
| UUID     | A Universally Unique Identifier       |
| Location | A locale string (e.g. `en_EN`)        |

Currently this fields admit no constraints

### Numeric Fields

The supported numeric fields are

| type          | description                                        |
| :------------ | :------------------------------------------------- |
| float         | A random decimal value following some distribution |
| int / integer | A random integer value following some distribution |

The possible constraints are

| constraint   | description                                                                             | values                                        |
| :----------- | :-------------------------------------------------------------------------------------- | --------------------------------------------- |
| distribution | Statistic distribution of the data                                                      | `uniform` (default), `normal`, or `lognormal` |
| min_value    | Lower bound for the field values, can only be specified with the `uniform` distribution | numeric value, defaults to `0`                |
| max_value    | Upper bound for the field values, can only be specified with the `uniform` distribution | numeric value, defaults to `100`              |
| mean         | Mean value for `normal` or `lognormal` distributions                                    | numeric value, defaults to `0`                |
| std          | Standard deviation for `normal` or `lognormal` distributions                            | numeric value, defaults to `1`                |

### Choice Fields

The supported choice fields are

| type   | description                                |
| :----- | :----------------------------------------- |
| choice | Choose between an array of possible values |

The possible constraints are

| constraint     | description                                                                                                                                                                                                                                                              | values                                                                                                                                       |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| allowed_values | Array of values to choose from when filling the data                                                                                                                                                                                                                     | Array of string values, defaults to `["NULL"]`                                                                                               |
| probabilities  | Array of float values defining the probability of each allowed value. Each probability corresponds to the probability of the value in that position, if there are values left unspecified the remaining probability will be equidistributed amongst the remaining values | Array of floating values between 0 and 1. Must sum up to 1 (or less if some probabilities are left unspecified). Defaults to an empty array. |

### Temporal fields

The supported temporal fields are

| type     | description                                                                       |
| :------- | :-------------------------------------------------------------------------------- |
| date     | A day of the year in the Gregorian Calendar, without time part                    |
| time     | A time part of a date consisting only on hours, minutes, seconds and microseconds |
| datetime | A date with time part of the Gregorian Calendar                                   |

The possible constraints are

| constraint    | description                                              | values                                                                                                                     |
| :------------ | :------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| format_string | The format string to which the values will be displayed  | A valid datetime format string, defaults to `"%Y-%m-%d %H-%M-%S"` for `datetime` fields and `"%Y-%m-%d"` for `date` fields |
| start_date    | A date to which all values of the field will precede     | A date represented in the `format_string` representation or in ISO 8601, defaults to `1970-01-01 00:00:00`                 |
| end_date      | A date to which all values of the field will be prior to | A date represented in the `format_string` representation or in ISO 8601, defaults to the current execution time            |

### Boolean fields

The supported boolean fields are

| type           | description                       |
| :------------- | :-------------------------------- |
| bool / boolean | A boolean `True` or `False` value |

The possible constraints are

| constraint  | description                                | values                                          |
| :---------- | :----------------------------------------- | ----------------------------------------------- |
| probability | The probability for the field to be `True` | A number between `0` and `1`, defaults to `0.5` |

### Network fields

The supported network fields are

| type | description                                        |
| :--- | :------------------------------------------------- |
| url  | HTTP and HTTPS random valid URLs                   |
| IPv4 | A random IPv4 address or network with a valid CIDR |
| IPv6 | A random IPv6 address or network with a valid CIDR |
