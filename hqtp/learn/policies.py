
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List
from ..logic.parser import Clause, Literal
from .features import extract_clause_features, extract_literal_features

class ClausePolicy(nn.Module):
    """Neural network policy for clause selection"""
    
    def __init__(self, feature_dim: int = 8, hidden_dim: int = 64):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.feature_dim = feature_dim
    
    def score_clause(self, clause: Clause) -> float:
        """Score a clause for selection"""
        features = extract_clause_features(clause)
        
        # Pad or truncate features to expected dimension
        if len(features) < self.feature_dim:
            features = np.pad(features, (0, self.feature_dim - len(features)))
        else:
            features = features[:self.feature_dim]
        
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            score = self.network(features_tensor).item()
        
        return score
    
    def update(self, clause: Clause, reward: float):
        """Update policy based on reward"""
        features = extract_clause_features(clause)
        
        if len(features) < self.feature_dim:
            features = np.pad(features, (0, self.feature_dim - len(features)))
        else:
            features = features[:self.feature_dim]
        
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        score = self.network(features_tensor)
        
        # Simple policy gradient update
        loss = -reward * torch.log(score + 1e-8)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

class LiteralPolicy(nn.Module):
    """Neural network policy for literal selection"""
    
    def __init__(self, feature_dim: int = 6, hidden_dim: int = 32):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.feature_dim = feature_dim
    
    def score_literal(self, literal: Literal, clause: Clause) -> float:
        """Score a literal for selection"""
        features = extract_literal_features(literal, clause)
        
        if len(features) < self.feature_dim:
            features = np.pad(features, (0, self.feature_dim - len(features)))
        else:
            features = features[:self.feature_dim]
        
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            score = self.network(features_tensor).item()
        
        return score
    
    def update(self, literal: Literal, clause: Clause, reward: float):
        """Update policy based on reward"""
        features = extract_literal_features(literal, clause)
        
        if len(features) < self.feature_dim:
            features = np.pad(features, (0, self.feature_dim - len(features)))
        else:
            features = features[:self.feature_dim]
        
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        score = self.network(features_tensor)
        
        loss = -reward * torch.log(score + 1e-8)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
