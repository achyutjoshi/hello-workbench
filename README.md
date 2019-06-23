
# FIPS module documentation

## Motivation
In many cases journalists encounter dirty locational data where the state and county names are not uniform. [FIPS](https://en.wikipedia.org/wiki/FIPS_county_code) is a code which uniquely identified counties and county equivalents in the United States. This module uses fuzzy matching to clean the state and county names in the raw input data.

## How does fuzzy matching works?
The module uses a python module called [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy). It uses [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to calculate the differences between sequences. The 'Fuzzy Match Percentage' value in the module refers to how much two strings are similar (derived from the Levenshtein distance). Value of 100 means a perfect match while a value of 70 means a 70% match.

## Using the module
There are four input values -
1. State column
2. County column
3. Fuzzy Match Percentage
4. Add FIPS  - a boolean which when true also adds the FIPS numeric code

There are two use cases that can be tackled using this -
1. Data has only state values - When your raw data has only state values, you have to keep the county column empty and the module will just fuzzy match with the state FIPS values.
2. Data has both state and county values - When your data has both state and county values, you select both the column. The module first normalises the state column and uses the normalised state values as context to clean the county values. This was implemented because several states have same county names (eg : Colorado and Florida both have a county named Jackson).

### Understanding the Fuzzy Match Percentage
The main input value that you have to decide is the Fuzzy Match Percentage. It is important to understand that this is a statistical score and might introduce some errors in matching. The following examples will help you understand what score to use -

Correct word - 'California'
Options and their Fuzzy Match Percentages -
1. 'CALIFORNIA' - 100
2. 'CA' - 90
3. 'Cali' - 90
4. 'FL' - 45
5. 'Alaska' - 38

In future releases we will expose more scorer options that is provided in fuzzywuzzy (https://github.com/seatgeek/fuzzywuzzy/blob/master/fuzzywuzzy/fuzz.py). By default we are using the WRatio right now.

Note - There is a bug which occurs when the 'Fuzzy Match Percentage > 80'. We are working to solve that. 


# hello-workbench

Example Workbench module for new developers.

# Getting Started

* Set up a
  [Workbench development environment](https://github.com/CJWorkbench/cjworkbench/wiki/Setting-up-a-development-environment)
* Clone this repository into a _sibling_ directory. For example, if Workbench
  is in `~/src/cjworkbench/cjworkbench`, clone this repository into
  `~/src/cjworkbench/hello-workbench`
* Start Workbench in the Workbench directory: `bin/dev start`
* Watch this module from the Workbench directory:
  `bin/dev develop-module hello-workbench`. Every time files change, this will
  re-import your module.
* Browse to your local Workbench at
  [http://localhost:8000](http://localhost:8000) to try out your module.
* Edit this module. Refresh in Workbench to see your edits.

# Developing

1. Add tests to ``test_module.py``
2. Run ``python3 test_module.py`` to find errors
3. Edit code in ``module.py``
4. Push to GitHub

For lots more information, see the
[module development documentation](https://github.com/CJWorkbench/cjworkbench/wiki/Creating-A-Module).
