import uvicorn


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, reload=False, access_log=True)