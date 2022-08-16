import hashlib
import logging
import os
import re
import subprocess
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(name="grow")
grow_root = Path(os.environ.get("GROW_ROOT", "."))
root = Path(os.environ.get("ROOT", "."))
logger = logging.getLogger("uvicorn")


def compile(path_mkd: Path, path_cache: Path):
    """Compile markdown -> HTML"""
    logger.info("compile %s => %s", path_mkd, path_cache)
    mdc = (grow_root / "bin/grow-compile").as_posix()
    with open(path_mkd, "rt") as input:
        with open(path_cache.as_posix(), "wb") as output:
            subprocess.run(["bash", mdc], stdin=input, stdout=output)


@app.get("/api/list")
async def list(tag: str = ""):
    """File list"""

    _ = tag

    def without_ext(path):
        return re.sub(r".md$", "", str(path))

    return sorted(
        [without_ext(path.relative_to(root)) for path in root.glob("**/*.md")]
    )


@app.get("/api/content")
async def content(slug: str):
    """Returns HTML Fragment for the markdown"""
    path = root / (slug + ".md")
    try:
        with open(path, "rb") as f:
            content = f.read()
            hashcode = hashlib.md5(content).hexdigest()
            cache = Path.home() / ".cache" / "grow.md" / hashcode
            if not cache.exists():
                compile(path, cache)
            with open(cache, "rt") as f:
                content = f.read()
                return {"ok": True, "slug": slug, "html": content}
    except Exception as err:
        logging.exception(err)
        return {"ok": False, "slug": slug, "error": str(err)}


class MountFiles(StaticFiles):
    """Flavoured StaticFiles"""

    async def get_response(self, path, scope):
        """Rewrite to / if 404"""
        response = await super().get_response(path, scope)
        if response.status_code != 404:
            return response
        return await super().get_response("", scope)


app.mount("/", MountFiles(directory=grow_root / "web/public", html=True), name="static")
