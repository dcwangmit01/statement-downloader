# statment-downloader

## Summary

This `statement-downloader` tool may be used to download statements banks.


* Charlese Schwab: https://www.schwab.com
  * All Bank Statements
  * All Brokerage Statements

## How it works

* The cli program will start a Selenium web browser.
* It directs the web browser to an instution's web page.
* It prompts the user to login to the web page.
* After the user logs in, the user presses enter to continue
* The script takes over and downloads all items

## Instructions

```
# Install selenium on your OSX machine
brew install selenium-server-standalone
brew install chromedriver

# Setup a self-contained python3 virtual environment
make venv

# Activate the venv
source .venv/bin/activate

# Install the editable version of this amazon-browser-cli tool
make install

# Run the program
#   Follow the prompts to login, and press enter to continue
# statement-downloader schwab all <downloads_folder> <save_to_folder>
statement-downloader schwab all ~/Downloads ~/Downloads/tmp/
```
