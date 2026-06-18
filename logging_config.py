import logging

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s" , filename="logs/app.log" , level=logging.INFO)

logger = logging.getLogger(__name__)