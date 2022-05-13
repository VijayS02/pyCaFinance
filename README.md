
_Note: This application is currently under development and features are being added_
# pyCaFinance
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

 A simple finance calculator written in python to help organize finances for a simple personal use case. Please note that this program is not sufficient for enterprise or business applications and was only intended to be used for personal banking.

## Functionality
 - Import *multiple* CSV files from various banks into a list of objects(`Transaction`) in python
 - Extendable classes that allow addition of new banks(`Bank`) and parsing of unique csv(`Parser`) file formats
 - Extendable model class that can group and categorize transactions into groupings
 - Plotting and summarize capability from a list of transactions



## Entities
The program operates with a few core entities (implemented as abstract classes in python) that can be extended or replicated for personalized usage
#### `Bank`
The bank entity simply stores a name and a parser so that the program knows how to parse the bank's CSV files into a list of transactions.
#### `Parser`
A parser entity is a class only used to parse `.csv` files containing transaction history from banks. 
#### `Account`
An account entity stores information on the account i.e. if it is a chequing/savings/credit card account.
#### `Transaction`
A transaction entity stores information about one particular transaction including but not limited to:
 - Date
 - Value
 - Account
 - Description
#### `Model`
The model entity is used to model transacations and categorize them as required by an individual, current functions of a model include:
 - Mapping a description of a transaction to a category (i.e. `"Point of Sale - Interac RETAIL PURCHASE ***** A&W #****"` gets categorized as food)
 - Determining if a certain category of transaction is one to include in calculations for balances. (Certain transactions may want to be ignored for calculation sake)
 - Saving a model onto local storage
## Usage
