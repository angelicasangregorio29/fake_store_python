"""Modulo per la trasformazione e validazione dei dati dei prodotti"""
from config import logger


def product_model(product: dict[str, any]) -> dict[str, any]:
    """Trasforma il prodotto API nel modello interno"""
    required_fields = ["id", "title", "price", "category", "description"]
    
    try:
        # Validazione campi obbligatori
        for field in required_fields:
            if field not in product:
                raise KeyError(f"Campo obbligatorio mancante: {field}")
        
        # Validazione struttura category
        if not isinstance(product["category"], dict) or "name" not in product["category"]:
            raise ValueError("Struttura category non valida")
        
        return {
            "id": product["id"], 
            "title": product["title"], 
            "price": product["price"], 
            "category": product["category"]["name"],
            "description": product["description"]
        }
    
    except KeyError as e:
        error_msg = f"Errore nei dati del prodotto: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
    
    except (ValueError, TypeError) as e:
        error_msg = f"Errore nella validazione del prodotto: {e}"
        logger.error(error_msg)
        raise
