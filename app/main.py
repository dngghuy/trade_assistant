import uvicorn
import os


if __name__ == "__main__":
    uvicorn.run('app.app:app', host='0.0.0.0', port=os.getenv("PORT", default=7272), reload=True)
