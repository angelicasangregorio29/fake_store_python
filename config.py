"""Configurazione globale dell'applicazione"""
import logging

BASE_URL: str = "https://api.escuelajs.co/api/v1/products"

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
