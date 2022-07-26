# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:23:58 2022

@author: Rusin
"""

from fastapi import APIRouter
from models.schemas.miokard import Miokard, MiokardPredictionResponse
import models.ml.classifier as clf

app_miokard_predict_v1 = APIRouter()


@app_miokard_predict_v1.post('/miokard/predict',
                          tags=["Predictions"],
                          response_model=MiokardPredictionResponse,
                          description="Get a classification from Miokard")
async def get_prediction(miokard: Miokard):
    data = dict(miokard)['data']
    prediction = clf.model.predict(data).tolist()
    probability = clf.model.predict_proba(data).tolist()
    log_probability = clf.model.predict_log_proba(data).tolist()
    return {"prediction": prediction,
            "probability": probability,
            "log_probability": log_probability}