# RecipeFinder

RecipeFinder is a sms based recipe finder using Twilio and Spoonacular.

## Installation

The easiest way to run this project is to have the following installed:

```bash
pip install flask
pip install spoonacular
pip install twilio
```

As well as [ngrok](https://ngrok.com/).

## Usage
Run main.py and take note of where your server is running.

In a terminal window run:
```
 ./ngrok http 'your localhost port'
```

In Twilio's console, select the number you would like to use. Under 
**Messaging** / A Message Comes In:

Replace url with 
```
https://[your generated ID].ngrok.io/sms 
```


### API KEY
You will need to obtain an API key from [Spoonacular](https://spoonacular.com/)

## Examples
The following are possible texts you can send:
```
# Hello: Receive a welcome message
# Bye: Receive a goodbye message
# Help?: Receive a help message
# Random: Receive a random recipe
# Custom text: Receive a recipe(s) based on food items parsed from custom text

# texts are case sensitive except for the custom text. An example of custom
# text can be: "Find me a recipe for a cheeseburger."

```
