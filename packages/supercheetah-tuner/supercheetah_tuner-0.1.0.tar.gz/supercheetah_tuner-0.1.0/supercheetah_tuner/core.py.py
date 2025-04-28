#!/usr/bin/env python
# coding: utf-8

# In[1]:


# supercheetah_tuner.py
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.base import clone

class SuperCheetahTuner:
    def __init__(self, model_class, param_bounds, X, y, mode='classification', 
                 n_agents=20, max_iter=30, patience=5, cv=3, random_state=42):
        """
        Nature-inspired hyperparameter optimization.
        
        model_class: sklearn-like estimator class (not instance!)
        param_bounds: dict of param: (min, max)
        X: features
        y: target
        mode: 'classification' or 'regression'
        n_agents: number of candidate solutions
        max_iter: max number of iterations
        patience: early stopping patience
        cv: cross-validation folds
        random_state: random seed
           
        Example:
        >>> tuner = SuperCheetahTuner(RandomForestClassifier, 
        ...                     {'n_estimators': (10,100)},
        ...                     X_train, y_train)
        >>> best_params = tuner.optimize()
        """
        self.model_class = model_class
        self.param_bounds = param_bounds
        self.X = X
        self.y = y
        self.mode = mode
        self.n_agents = n_agents
        self.max_iter = max_iter
        self.patience = patience
        self.cv = cv
        self.random_state = random_state

        self.best_score = np.inf
        self.best_params = None

    def _objective(self, params):
        # Clone the model fresh each time
        model = self.model_class(**params)
        
        # For classification, maximize accuracy
        if self.mode == 'classification':
            score = cross_val_score(model, self.X, self.y, cv=self.cv).mean()
            return 1 - score  # minimize 1 - accuracy
        # For regression, minimize RMSE
        else:
            scores = cross_val_score(model, self.X, self.y, cv=self.cv, scoring='neg_root_mean_squared_error')
            return -scores.mean()

    def _random_solution(self):
        solution = {}
        for key, (low, high) in self.param_bounds.items():
            solution[key] = np.random.uniform(low, high)
        return solution

    def _clip_params(self, params):
        clipped = {}
        for key, (low, high) in self.param_bounds.items():
            value = params[key]
            value = max(min(value, high), low)
            if isinstance(low, int) and isinstance(high, int):
                value = int(round(value))
            clipped[key] = value
        return clipped

    def optimize(self):
        np.random.seed(self.random_state)
        
        pop = [self._random_solution() for _ in range(self.n_agents)]
        no_improvement_counter = 0
        
        for iteration in range(self.max_iter):
            scores = [self._objective(self._clip_params(p)) for p in pop]
            best_idx = np.argmin(scores)
            best_candidate = pop[best_idx]

            if scores[best_idx] < self.best_score:
                self.best_score = scores[best_idx]
                self.best_params = self._clip_params(best_candidate)
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1

            # Update population towards best
            new_pop = []
            for p in pop:
                new_p = {}
                for key in p:
                    r = np.random.rand()
                    new_p[key] = p[key] + r * (self.best_params[key] - p[key])
                new_pop.append(self._clip_params(new_p))
            pop = new_pop

            if no_improvement_counter >= self.patience:
                print(f"Early stopping at iteration {iteration+1}")
                break

        print(f"Best parameters found: {self.best_params} with score: {1 - self.best_score if self.mode=='classification' else self.best_score}")
        return self.best_params

    def get_best_model(self):
        return self.model_class(**self.best_params)



# In[ ]:




