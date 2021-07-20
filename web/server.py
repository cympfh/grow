from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(name="grow")


@app.get("/api/{slug}")
async def api(slug: str):
    """Returns HTML Fragment for the markdown"""
    return {"hoge": "fuga"}


class MountFiles(StaticFiles):
    """Flavoured StaticFiles"""

    async def get_response(self, path, scope):
        """Rewrite to / if 404"""
        response = await super().get_response(path, scope)
        if response.status_code != 404:
            return response
        return await super().get_response("", scope)


app.mount("/", MountFiles(directory="web/public", html=True), name="static")
