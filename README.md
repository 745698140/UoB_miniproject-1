# mini-project
HSBC mini project for UoB Data Science MSc

## Discussion Board

- The difference between mid-price and micro-price

    For liquid stocks, the difference is trivial. For illiquid stocks, the difference is non-trivial.

    Models and features are differentiated for these two types.So, we need to calcualte the liquidity of each stock firstly.

- data normalisation
   remove outliners, eg transaction recorded outside official training time or other s

- Can we skip to sample examples without considering time series?
    we can do it if the previous time series don't affect the price movements. Or we can sample the previous k steps with the examples.

- What is our input, LOB or transaction events?

- Don't foreget to normalise features
