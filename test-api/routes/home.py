# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:23:17 2022

@author: Rusin
"""

from fastapi import APIRouter
app_home = APIRouter()


@app_home.get('/', tags=["Intro"])
async def hello():
    return {"message": "Hello!"}


@app_home.get('/bye', tags=["Intro"])
async def bye():
    return {"message": "Bye!"}