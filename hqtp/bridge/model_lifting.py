from typing import Dict, Any
from ..sat.extractor import GroundInstantiator

def lift_sat_model(model: Dict[int, bool],
                   instantiator: GroundInstantiator) -> Dict[str, Any]:
    """Lift propositional model to first-order logic model"""
    return instantiator.lift_model(model)