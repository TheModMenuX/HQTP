import numpy as np
from typing import List
import torch
import torch.nn as nn
from .features import extract_clause_features, extract_literal_features

class SimpleNN(nn.Module):
    """Simple neural network for scoring clauses/literals"""
    
    def __init__(self, input_size: int, hidden_size: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.net(x)

class ClausePolicy:
    """Policy for selecting clauses"""
    
    def __init__(self):
        self.model = SimpleNN(input_size=3)  # Adjust based on features
        self.optimizer = torch.optim.Adam(self.model.parameters())
        
    def score_clause(self, clause) -> float:
        features = extract_clause_features(clause)
        with torch.no_grad():
            return float(self.model(torch.FloatTensor(features)))
            
    def update(self, clause, reward: float):
        """Update policy based on reward"""
        features = extract_clause_features(clause)
        self.optimizer.zero_grad()
        score = self.model(torch.FloatTensor(features))
        loss = nn.MSELoss()(score, torch.FloatTensor([reward]))
        loss.backward()
        self.optimizer.step()

class LiteralPolicy:
    """Policy for selecting literals"""
    
    def __init__(self):
        self.model = SimpleNN(input_size=2)  # Adjust based on features
        self.optimizer = torch.optim.Adam(self.model.parameters())
        
    def score_literal(self, literal, clause) -> float:
        features = extract_literal_features(literal, clause)
        with torch.no_grad():
            return float(self.model(torch.FloatTensor(features)))
            
    def update(self, literal, clause, reward: float):
        features = extract_literal_features(literal, clause)
        self.optimizer.zero_grad()
        score = self.model(torch.FloatTensor(features))
        loss = nn.MSELoss()(score, torch.FloatTensor([reward]))
        loss.backward()
        self.optimizer.step()