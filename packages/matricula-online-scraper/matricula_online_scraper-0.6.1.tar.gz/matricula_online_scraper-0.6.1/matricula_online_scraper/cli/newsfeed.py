"""`newsfeed` command group for interacting with Matricula Online's newsfeed at https://data.matricula-online.eu/en/nachrichten/."""

from pathlib import Path
from typing import Annotated, Optional

import scrapy.signals
import typer
from rich.console import Console
from rich.progress import (
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TransferSpeedColumn,
)
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from matricula_online_scraper.logging_config import get_logger
from matricula_online_scraper.spiders.newsfeed_spider import NewsfeedSpider

from ..utils.file_format import FileFormat

logger = get_logger(__name__)

app = typer.Typer()


@app.command()
def fetch(
    outfile: Annotated[
        Path,
        typer.Argument(
            help=f"File to which the data is written (formats: {', '.join(FileFormat)})"
        ),
    ] = Path("matricula_news.jsonl"),
    # options
    last_n_days: Annotated[
        Optional[int],
        typer.Option(
            "--days",
            help="Scrape news from the last n days (including today).",
        ),
    ] = None,
    limit: Annotated[
        Optional[int],
        typer.Option(
            help=(
                "Limit the number of max news articles to scrape"
                "(note that this is a upper bound, it might be less depending on other parameters)."
            )
        ),
    ] = 100,
):
    """Download Matricula Online's newsfeed.

    Matricula has a minimal newsfeed where they announce new parishes, new registers, and\
 other changes: https://data.matricula-online.eu/en/nachrichten/.\
 This command will download the entire newsfeed or a limited number of news articles.
    """
    cmd_logger = logger.getChild(fetch.__name__)
    cmd_logger.debug("Start fetching Matricula Online's newsfeed.")

    try:
        format = FileFormat(outfile.suffix[1:])
    except Exception as e:
        reason = f"Invalid file format: '{outfile.suffix[1:]}'. Allowed file formats are: {', '.join(FileFormat)}"
        cmd_logger.error(reason)
        raise typer.BadParameter(reason, param_hint="outfile")

    if outfile.exists():
        reason = (
            f"A file with the same path as the outfile already exists: {outfile.resolve()}."
            " Will not overwrite it. Delete the file or choose a different path. Aborting."
        )
        cmd_logger.error(reason)
        raise typer.BadParameter(reason, param_hint="outfile")

    if limit and limit <= 0:
        reason = f"Parameter '--limit' must be greater than 0, but received: {limit}"
        cmd_logger.error(reason)
        raise typer.BadParameter(reason, param_hint="--limit")

    if last_n_days and last_n_days <= 0:
        reason = (
            f"Parameter '--days' must be greater than 0, but received: {last_n_days}"
        )
        cmd_logger.error(reason)
        raise typer.BadParameter(reason, param_hint="--days")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
        console=Console(stderr=True),
    ) as progress:
        item_task = progress.add_task(
            "Scraping...",
            total=limit,  # use limit as a rough estimate
        )

        try:
            runner = CrawlerRunner(
                settings={"FEEDS": {str(outfile): {"format": format.to_scrapy()}}}
            )

            crawler = runner.create_crawler(NewsfeedSpider)
            # crawler.signals.connect(
            #     lambda: progress.update(item_task, completed=True),
            #     signal=scrapy.signals.item_scraped,
            # )

            deferred = runner.crawl(crawler, limit=limit, last_n_days=last_n_days)
            deferred.addBoth(lambda _: reactor.stop())  # type: ignore
            reactor.run()  # type: ignore  # blocks until the crawling is finished

            # if crawler.stats:
            #     typer.echo(crawler.stats.get_stats(NewsfeedSpider()))

        except Exception as exception:
            cmd_logger.exception(
                "An error occurred while scraping Matricula Online's newsfeed."
            )
            raise typer.Exit(code=1) from exception

    cmd_logger.info(
        f"Done! Successfully scraped the newsfeed. The output was saved to: {outfile.resolve()}"
    )
