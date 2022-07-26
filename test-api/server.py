# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:17:52 2022

@author: Rusin
"""

import uvicorn

if __name__ == '__main__':
    uvicorn.run("app:app",
                host="127.0.0.1",
                port=8432,
                reload=True,
                )