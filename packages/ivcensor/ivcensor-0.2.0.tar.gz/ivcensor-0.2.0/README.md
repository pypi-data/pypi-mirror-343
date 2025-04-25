# Genius Censor

[![PyPI version](https://img.shields.io/pypi/v/genius-censor)](https://pypi.org/project/genius-censor)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Overview

Genius Censor is a Python package for bias-adjusted estimation in censored data settings, leveraging neural networks and ensemble models. It implements functions for data generation, nuisance function estimation, and the generalized estimating equation for the parameter of interest.

## Features

- Generate synthetic data with controlled censoring.
- Estimate nuisance functions via neural networks, random forests, XGBoost, or linear regression.
- Compute point estimates, standard errors, and test statistics using empirical likelihood, exponential tilt, or CUE.
