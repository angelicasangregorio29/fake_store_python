"""Modulo per le operazioni sui prodotti (business logic)"""
from api import get_data
from config import logger, BASE_URL
from models import product_model


def get_all_products() -> list[dict[str, any]]:
    """Recupera la lista completa dei prodotti dall'API"""
    try:
        logger.info("Recupero della lista completa dei prodotti")
        products = get_data(BASE_URL)
        
        if not isinstance(products, list):
            raise ValueError("Risposta API non è una lista")
        
        if not products:
            raise ValueError("Nessun prodotto disponibile")
        
        logger.info(f"Recuperati {len(products)} prodotti")
        return products
    
    except ValueError as e:
        if "prodotto" in str(e).lower():
            raise
        error_msg = f"Errore nel recupero della lista: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e


def get_product_by_id(product_id: str) -> dict[str, any]:
    """Recupera un singolo prodotto per ID"""
    try:
        if not product_id.isdigit():
            raise ValueError("L'ID deve essere un numero intero")
        
        logger.info(f"Richiesta per il prodotto ID: {product_id}")
        
        raw_product = get_data(f"{BASE_URL}/{product_id}")
        product = product_model(raw_product)
        
        logger.info(f"Prodotto {product_id} recuperato con successo")
        return product
    
    except ValueError as e:
        logger.warning(f"Errore nel recupero del prodotto {product_id}: {e}")
        raise
