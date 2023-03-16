import uvicorn


if __name__ == '__main__':
    # Start server
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False, access_log=True)