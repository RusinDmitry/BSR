# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:05:49 2022

@author: Rusin
"""

import models.ml.classifier as clf
from fastapi import FastAPI, Body
from joblib import load
from routes.v1.miokard_predict import app_miokard_predict_v1
from routes.home import app_home

app = FastAPI(title="Miokard ML API", description="API for miokard dataset ml model", version="1.0")


@app.on_event('startup')
async def load_model():
    clf.model = load('models/ml/miokard_dt_v1.joblib')


app.include_router(app_home)
app.include_router(app_miokard_predict_v1, prefix='/v1')