import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.timezone import make_aware
from django_cron import CronJobBase, Schedule
from .models import Changelog
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Map Spanish month names to their English counterparts
month_translation = {
    'enero': 'January',
    'febrero': 'February',
    'marzo': 'March',
    'abril': 'April',
    'mayo': 'May',
    'junio': 'June',
    'julio': 'July',
    'agosto': 'August',
    'septiembre': 'September',
    'octubre': 'October',
    'noviembre': 'November',
    'diciembre': 'December'
}

TEAMS_WEBHOOK_URL = 'YOUR_TEAMS_WEBHOOK_URL'  # Replace with your Teams webhook URL

def send_teams_notification(site, title, date):
    message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": f"Nuevo changelog en {site}",
        "sections": [{
            "activityTitle": f"Nuevo changelog en {site}",
            "facts": [
                {"name": "Título", "value": title},
                {"name": "Fecha", "value": date.strftime('%Y-%m-%d')},
            ],
            "markdown": True
        }]
    }
    response = requests.post(TEAMS_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        logger.error(f"Error sending notification to Teams: {response.status_code}, {response.text}")

class FetchMercadoPagoChangelog(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'changelog.fetch_mercado_pago_changelog'  # a unique code

    def do(self):
        url = 'https://www.mercadopago.com.ar/developers/es/changelog'
        logger.info(f"Fetching data from {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            logger.info("Successfully fetched the changelog page.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching the changelog page: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first date header and its associated entry
        date_header = soup.find('h3', class_='dev-news-changelog-container__log-title')
        if not date_header:
            logger.error("No date header found.")
            return

        date_str = date_header.text.strip()
        logger.debug(f"Found date string: {date_str}")

        for spanish_month, english_month in month_translation.items():
            date_str = date_str.replace(spanish_month, english_month)

        try:
            date = datetime.strptime(date_str, '%B de %Y')
            date = make_aware(datetime.combine(date, datetime.min.time()))
        except ValueError:
            logger.error(f"Error parsing date: {date_str}")
            return

        entry = date_header.find_next('div', class_='dev-news-secondary-list__card')
        if not entry:
            logger.error("No entry found.")
            return

        try:
            title = entry.find('h4').text.strip()
            content = entry.find('p').text.strip()
        except AttributeError:
            logger.error("Error parsing entry content.")
            return

        # Log the entry details
        logger.info(f"Processing entry: {date}, {title}")

        # Check if an entry with the same title already exists
        if Changelog.objects.filter(title=title).exists():
            logger.info("An entry with the same title already exists. Skipping creation.")
            return

        # Create the entry in the database
        try:
            Changelog.objects.create(
                site="Mercado Pago",
                date=date,
                title=title,
                content=content
            )
            logger.info("Successfully created changelog entry in the database.")
            send_teams_notification("Mercado Pago", title, date)
        except Exception as e:
            logger.error(f"Error creating changelog entry in the database: {e}")

class FetchVTEXChangelog(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'changelog.fetch_vtex_changelog'  # a unique code

    def do(self):
        url = 'https://developers.vtex.com/updates/release-notes'
        logger.info(f"Fetching data from {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            logger.info("Successfully fetched the changelog page.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching the changelog page: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all release note containers
        releases = soup.find_all('div', class_='css-1m1wppb')
        if not releases:
            logger.error("No release notes found.")
            return

        for release in releases:
            try:
                # Extract title, date, and content
                title = release.find('div', class_='css-1pdb3hq').text.strip()
                date_str = release.find('div', class_='css-emnilb').text.strip()
                content = release.find('div', class_='css-1on1hp9').text.strip()

                # Convert date string to datetime
                date = datetime.strptime(date_str, '%B, %d')
                date = make_aware(datetime.combine(date, datetime.min.time()))

                # Log the entry details
                logger.info(f"Processing entry: {date}, {title}")

                # Check if an entry with the same title already exists
                if Changelog.objects.filter(title=title).exists():
                    logger.info("An entry with the same title already exists. Skipping creation.")
                    continue

                # Create the entry in the database
                try:
                    Changelog.objects.create(
                        site="VTEX",
                        date=date,
                        title=title,
                        content=content
                    )
                    logger.info("Successfully created changelog entry in the database.")
                    send_teams_notification("VTEX", title, date)
                except Exception as e:
                    logger.error(f"Error creating changelog entry in the database: {e}")
            except (AttributeError, ValueError) as e:
                logger.error(f"Error parsing release note data: {e}")
                continue
