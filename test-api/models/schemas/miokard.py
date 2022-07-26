# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:00:49 2022

@author: Rusin
"""

from pydantic import BaseModel, conlist
from typing import List, Any


class Miokard(BaseModel):
    data: List[conlist(float, min_items=107, max_items=108)]


class MiokardPredictionResponse(BaseModel):
    prediction: List[int]
    probability: List[Any]
    log_probability: List[Any]