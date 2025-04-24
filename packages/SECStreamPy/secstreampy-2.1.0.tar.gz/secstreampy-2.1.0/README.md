# SECStreamPy Library  

---

![Python Versions](https://img.shields.io/badge/python-3.12|3.13-blue) 
![Latest Release](https://img.shields.io/badge/Release-v2.0.5-blue.svg)


## Introduction

`SECStreamPy` is a powerful and user-friendly Python package designed to enhance data analysis. 
It simplifies the extraction and presentation of information for various forms from the SEC website, 
offering enriched data display for SEC form types, filing details, and financial statements, 
making it an essential tool for professionals working with regulatory filings.


## Features

- 📁 **Access any SEC filing**: You can access any filings on SEC forms of Form 8-K and Form 10-K etc.
- 📅 **List filings for any date range**: List filings by date e.g. or date range `2024-02-29:2024-03-15`
- 🌟 **User Friendly library**: Uses **[rich](https://rich.readthedocs.io/en/stable/introduction.html) & [tabulate](https://github.com/astanin/python-tabulate)** library to display SEC Edgar data in a beautiful way.
- 🏗️ **Filter filings data**: Build data filtering by cik, accession number, form type, filing date
- 🔍 **Preview the text data for a filing**: You can preview the filing (sections) in the terminal or a notebook.
- 📊 **Parse to Dataframe**: You can parse filings to a dataframe.
- 📈 **Financial Statement**: Get financial statements of Form 8-K and Form 10-K of various companies.


## Get Started on Windows/MacOS/Linux Terminal

-------

You can use `Poetry` or any dependency manager or use the general `pip install` command to install `SECStreamPy`.
Before you install `SECStreamPy`,it is best to set your environment variable `SEC_IDENTITY` in a .`env` file.

## Set up `SEC_IDENTITY` environment variable in a `.env` file in your project.

   ```dotenv
   SEC_IDENTITY=<your sec identity here>
   ```

----------------------


You can install the latest `SECStreamPy` version or any version. 
Below is how to use the latest version of `SECStreamPy` or any version in your terminal.

   ```commandline
   pip install --upgrade SECStreamPy
   ```

or

   ```commandline
   pip install SECStreamPy==<latest version number here>   
   ```

----------


### Using pip command to install `SECStreamPy`

```commandline
pip install SECStreamPy
```

### Using Poetry to install `SECStreamPy`


1. Open your terminal and install poetry _[if you do not have poetry]_ using `pip`.
    
    ```commandline
   pip install poetry
   ```
   or Install poetry using `pipx`.
    
    ```commandline 
   pipx install poetry
    ```
   or Install using `curl`

   ```commandline
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Create a project using poetry command. This will create a `pyproject.TOML` in your project.
Follow the instructions to finish creating your project

    ```commandline
    poetry new project_name
    ```

3. Change directory to your project

   ```commandline
   cd project_name
   ```

4. Run the poetry command to add `SECStreamPy`: 

    ```commandline
   poetry add SECStreamPy
   ```


## Use SECStreamPy with Jupyter

----------

1. Open notebook in your project and install `SECStreamPy` using `pip` command.
    
    ```bash
   pip install SECStreamPy
   ```

----------------------------------


## Do you have any issue or want to contribute to `SECStreamPy` library?

If you have any issue or contribution, please write an issue with this link: https://github.com/DataDock-AI/SECStreamPy/issues
