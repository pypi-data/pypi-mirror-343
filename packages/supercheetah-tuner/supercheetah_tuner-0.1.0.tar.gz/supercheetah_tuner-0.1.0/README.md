# SuperCheetahTuner - Nature-Inspired Hyperparameter Tuning with Cheetah Optimizer

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/cheetah-tuner)](https://pypi.org/project/cheetah-tuner/)
[![Downloads](https://img.shields.io/pypi/dm/cheetah-tuner)](https://pypistats.org/packages/cheetah-tuner)


## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)
- [Benchmarks](#benchmarks)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

## Features 

**Nature-inspired Algorithm**  
Emulates cheetah hunting strategies (search → chase → attack) for efficient optimization

**Universal Compatibility**  
Works with any scikit-learn compatible estimator and supports:
- Traditional ML (RandomForest, SVM, etc.)
- Neural Networks (via sklearn wrappers)
- Custom models

 **Multi-Problem Support**
```python
mode='classification'  # or 'regression'


## Smart Optimization
n_agents=20    # Number of candidate solutions
patience=5     # Early stopping rounds
cv=3           # Cross-validation folds

## Installation

# Stable version
pip install supercheetah-tuner

# Development version
pip install git+https://github.com/UjwalWtg/supercheetah-tuner.git

Requirements: Python 3.7+, numpy, scikit-learn

## Basic Example

from supercheetah_tuner import SuperCheetahTuner
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# 1. Load data
X, y = load_iris(return_X_y=True)

# 2. Define search space
param_bounds = {
    'n_estimators': (10, 200),      # Int values
    'max_depth': (2, 20),           # Int
    'max_features': (0.1, 1.0)      # Float
}

# 3. Initialize tuner
tuner = SuperCheetahTuner(
    model_class=RandomForestClassifier,
    param_bounds=param_bounds,
    X=X, y=y,
    mode='classification'
)

# 4. Run optimization
best_params = tuner.optimize()
print(f"Best parameters: {best_params}")

# 5. Get trained model
best_model = tuner.get_best_model()


# Expected Output

Iter 1/30 - Best Score: 0.8933
Iter 2/30 - Best Score: 0.9133
...
Early stopping at iteration 22
Best parameters: {
    'n_estimators': 137, 
    'max_depth': 12, 
    'max_features': 0.872
}


## API Reference
# SuperCheetahTuner Parameters

model_class =>	Class => sklearn estimator class (Required)
param_bounds =>	dict => {param: (min, max)} pairs (Required)
X, y	=> array => Training data (Required)
mode =>	str => 	'classification'/'regression' (default value 'classification')
n_agents => int => Population size (default value 20)
max_iter => int => Maximum generations (default value 30)
patience => int => Early stopping rounds (default value 5)
cv => int => Cross-validation folds (default value 3)
random_state => int => Random seed (default value None)
verbose	bool => int => progress	(default value True)

# Key Methods
.optimize() → dict: Returns best parameters

.get_best_model() → estimator: Returns fitted model

.get_best_score() → float: Returns best CV score


## How It Works 

# Search Phase (Exploration)

if np.random.rand() < 0.3:
    new_params = random_sample(bounds)

# Chase Phase (Exploitation)

else:
    new_params = best_params + noise * direction

# Attack Phase (Intensification)

if score < best_score:
    update_best()

## Citation
If you use SuperCheetahTuner in research:

bibtex
@software{SuperCheetahTuner,
  author = {Ujwal Watgule},
  title = {SuperCheetahTuner: Bio-Inspired Hyperparameter Tuning with Cheetah Optimizer},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/UjwalWtg/supercheetah-tuner}}
}

## License 
MIT License