#!/usr/bin/env python3

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.index:app", host="0.0.0.0", reload=True)
