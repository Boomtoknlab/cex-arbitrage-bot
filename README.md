# Arbitrage Opportunity Analyzer

The Arbitrage Opportunity Analyzer is a Python script that identifies potential arbitrage opportunities among different cryptocurrency exchanges. It uses the order book data from various exchanges, calculates the maximum buy quantities and sell amounts, and analyzes the differences to find the most profitable opportunities.

## Getting Started

### Prerequisites

This script requires Python 3.6+ and the following packages:

- `requests`
- `aiohttp`
- `asyncio`

Install the required packages using `pip`:

```bash
pip install requests aiohttp
```


### Usage

1. Import the `ArbitrageAnalyzer` class and the `Books` class from their respective files:

```python
from arbitrage_analyzer import ArbitrageAnalyzer
from orderbook import Books
```

2. Instantiate the ArbitrageAnalyzer class with the token symbol (e.g., 'BTC'):

```python
analyzer = ArbitrageAnalyzer('BTC')
```

3. Run the analyzer to find arbitrage opportunities:

```python
analyzer.run()
```

# Code Structure
`orderbook.py`: Contains the Books class, which fetches order book data from various exchanges and processes it.
`arbitrage_analyzer.py`: Contains the ArbitrageAnalyzer class, which analyzes the order book data to find arbitrage opportunities.
`functions.py`: Contains helper functions for data processing.
`project_exceptions.py`: Contains custom exceptions for the project.
# Contributing
To contribute to this project, please submit a pull request with your proposed changes.


# License
This project is licensed under the MIT License. See the LICENSE file for details.

```c#
Create a new file named `README.md` in your project directory and paste the content above into the file. This will serve as the main documentation for your project.
```