# src/incept/dl_rebelway.py
import os
import html
import pandas as pd
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import click

from .dl_video import (
    launch_chrome,
    make_chrome_driver,
    make_download_session,
    download_stream,
)
from selenium.common.exceptions import InvalidSessionIdException


def find_source_url(html_text: str) -> str | None:
    soup = BeautifulSoup(html_text, "html.parser")
    sel  = soup.select_one("select.video-download-selector")
    if not sel:
        return None
    for opt in sel.find_all("option"):
        if "source" in opt.get_text(strip=True).lower():
            return html.unescape(opt["value"])
    return None


@click.command("dl-rebelway")
@click.option("--excel",  "excel_path",  required=True, type=click.Path(exists=True))
@click.option("--output", "out_dir",     required=True, type=click.Path())
@click.option("--skip-first", default=0,  help="Number of rows to skip (zero-based).", type=int)
@click.option("--chrome-port", default=9222, help="Chrome remote port.", type=int)
def cli_download_rebelway(excel_path, out_dir, skip_first, chrome_port):
    """
    Download SOURCE-quality MP4s from Rebelway for every lesson in the given Excel.
    """
    # 1) Launch & wait for login.
    launch_chrome(debug_port=chrome_port)

    # 2) Read the sheet.
    df = pd.read_excel(excel_path, sheet_name="lessons", engine="openpyxl")
    if not {"chapter_index","name","link"}.issubset(df.columns):
        raise click.ClickException("Excel must have columns: chapter_index, name, link")

    # 3) Bootstrap drivers & sessions.
    driver = make_chrome_driver(debug_port=chrome_port)
    sess   = make_download_session()

    os.makedirs(out_dir, exist_ok=True)

    # 4) Episode counters per chapter
    ep = {}
    for row in df.iloc[:skip_first].itertuples():
        c = int(row.chapter_index)
        ep[c] = ep.get(c, 0) + 1

    # 5) Iterate & download
    for idx, row in df.iterrows():
        if idx < skip_first:
            continue

        chap, name, lesson = int(row.chapter_index), row.name, row.link
        ep.setdefault(chap, 0)
        ep[chap] += 1

        season, episode = chap, ep[chap]
        slug = name.lower()
        slug = "".join(ch for ch in slug if ch.isalnum() or ch.isspace()).strip().replace(" ", "_")

        click.echo(f"\n[{idx+1}] {lesson} → s{season:02d}e{episode:02d}_{slug}.mp4")

        # load page (restart on session death)
        try:
            driver.get(lesson)
        except InvalidSessionIdException:
            driver.quit()
            driver = make_chrome_driver(debug_port=chrome_port)
            driver.get(lesson)

        driver.implicitly_wait(3)
        html_body = driver.page_source
        src_url   = find_source_url(html_body)
        if not src_url:
            click.echo("No SOURCE option found.")
            continue

        ext    = os.path.splitext(urlsplit(src_url).path)[1] or ".mp4"
        fname  = f"s{season:02d}e{episode:02d}_{slug}{ext}"
        dest   = os.path.join(out_dir, fname)

        if os.path.exists(dest):
            click.echo(f"⏭ Already have {fname}")
            continue

        sess.headers["Referer"] = lesson
        click.echo(f"↓ Downloading: {fname}")
        try:
            download_stream(sess, src_url, dest)
            click.echo(f"Saved → {dest}")
        except Exception as e:
            click.echo(f"Failed: {e}")

    driver.quit()
    click.echo("\nAll done.")
