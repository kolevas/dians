import schedule
import time
import logging
from scrapy.crawler import CrawlerProcess
from mse_scraper.spiders.today_spider import TodaySpider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def run_today_spider():
    """
    Function to run the TodaySpider using Scrapy's CrawlerProcess.
    Logs before and after the spider runs.
    """
    try:
        logger.info("Starting TodaySpider...")
        process = CrawlerProcess()
        process.crawl(TodaySpider)
        process.start()
        logger.info("TodaySpider finished successfully.")
    except Exception as e:
        logger.error(f"Error running TodaySpider: {e}", exc_info=True)

# Schedule tasks
schedule.every().day.at("08:00").do(run_today_spider)
schedule.every().day.at("12:00").do(run_today_spider)
schedule.every().day.at("16:00").do(run_today_spider)

def main():
    logger.info("Jobs scheduled:")
    for job in schedule.jobs:
        logger.info(job)

    # Main loop to run scheduled tasks
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error in scheduler: {e}", exc_info=True)


# Entry point for the script
if __name__ == "__main__":
    main()