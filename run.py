
from app.crew.groq_compat import apply_groq_compatibility

apply_groq_compatibility()

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
