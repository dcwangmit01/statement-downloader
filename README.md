# amazon-browser-cli

## Summary

This Amazon-Browser-CLI tool may be used to clear all Video History from an
Amazon Account.  It may be used to effectively reset viewing preferences and
suggestions for an AWS account.  It is needed, because Amazon does not provide
a way to to reset Video History without individually clicking on every single
watched video.


## How it works

The cli program will use Selenium to drive a web browser to simulate a user
which first logs into Amazon, then moves to the Video History page, and then
clicks on each movie one at a time.  A web browser will open during the
execution of the program.


## Instructions

```
# Install selenium on your OSX machine
brew install selenium-server-standalone
brew install chromedriver

# Setup a self-contained python3 virtual environment
make venv

# Activate the venv
source .venv/bin/activate

# Set your AWS login credentials into the environment
export AMAZON_USER='you@domain.com'
export AMAZON_PASSWORD='your-amazon-password'

# Install the editable version of this amazon-browser-cli tool
make install

# Run the program
amazon-browser-cli video clear_history

```
