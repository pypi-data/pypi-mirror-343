# src/incept/dl_video.py
import subprocess
import click
import browser_cookie3
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def launch_chrome(debug_port: int = 9222):
    """
    Launch (or re-launch) Chrome in remote-debugging mode.
    """
    cmd = [
        "open", "-a", "Google Chrome", "--args",
        f"--remote-debugging-port={debug_port}"
    ]
    subprocess.Popen(cmd)
    click.echo(f"\n🚀 Launched Chrome on port {debug_port}.")
    click.prompt("🔑  Log in, then hit ENTER here to continue", default="", show_default=False)


def make_chrome_driver(debug_port: int = 9222, headless: bool = True):
    """
    Attach Selenium to the already-running Chrome debug port.
    """
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")  # or just "--headless"
    opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
    svc = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=svc, options=opts)


def make_download_session(
    retries: int = 5,
    backoff_factor: float = 1,
    status_forcelist=(429, 500, 502, 503, 504)
):
    """
    Build a requests.Session that:
      - Reuses your browser cookies for auth
      - Retries on HTTP 5xx/429/timeouts
    """
    cj = browser_cookie3.chrome()
    sess = requests.Session()
    sess.cookies.update(cj)

    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    sess.mount("https://", adapter)
    sess.mount("http://", adapter)
    return sess


def download_stream(
    session: requests.Session,
    url: str,
    dest_path: str,
    timeout_connect: int = 10,
    timeout_read: int = 300
):
    """
    Stream a large file down to disk in 1MiB chunks.
    """
    with session.get(url, stream=True, timeout=(timeout_connect, timeout_read)) as r:
        r.raise_for_status()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(1024*1024):
                if chunk:
                    f.write(chunk)
