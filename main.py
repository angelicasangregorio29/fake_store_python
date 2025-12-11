from requests import get, exceptions
import logging

BASE_URL: str = "https://api.escuelajs.co/api/v1/products"

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_data(URL: str) -> dict[str, any] | list[dict[str, any]]:
    """Recupera i dati dall'API"""
    if not URL:
        error_msg = "L'URL non può essere vuoto!"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        response = get(URL, timeout=5)
        response.raise_for_status()
        return response.json()

    except exceptions.Timeout:
        error_msg = f"Timeout: La richiesta a {URL} ha impiegato troppo tempo"
        logger.error(error_msg)
        raise
    
    except exceptions.ConnectionError:
        error_msg = f"Errore di connessione: Impossibile raggiungere {URL}"
        logger.error(error_msg)
        raise
    
    except exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 404:
            error_msg = "Prodotto non trovato (404): ID inesistente"
        elif status_code == 400:
            error_msg = "Richiesta non valida (400): Parametri errati"
        elif status_code >= 500:
            error_msg = f"Errore del server ({status_code}): Riprovare più tardi"
        else:
            error_msg = f"Errore HTTP ({status_code}): {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
    
    except ValueError:
        error_msg = "Errore nel parsing della risposta JSON"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    except Exception as e:
        error_msg = f"Errore imprevisto: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        raise


def print_prodotto(product: dict[str, any]) -> None:
    """Stampa i dettagli del prodotto"""
    try:
        print("*" * 30)
        print("PRODOTTO")
        print("*" * 30)
        print(f"ID: {product['id']}")
        print(f"Titolo: {product['title']}")
        print(f"Category: {product['category']}")
        print(f"PRICE: {product['price']}")
        print(f"DESCRIPTION: {product['description']}")
    except KeyError as e:
        error_msg = f"Errore: Campo mancante nel prodotto - {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
    except Exception as e:
        error_msg = f"Errore nella stampa del prodotto: {e}"
        logger.error(error_msg)
        raise


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
    

def main() -> None:
    """Funzione principale con gestione errori robusta"""
    try: 
        user_input = input("Inserisci l'id del prodotto da visualizzare: ").strip()
        
        # Validazione input
        if not user_input:
            raise ValueError("ID non può essere vuoto")
        
        if not user_input.isdigit():
            raise ValueError("L'ID deve essere un numero intero")
        
        logger.info(f"Richiesta per il prodotto ID: {user_input}")
        
        product = product_model(get_data(f"{BASE_URL}/{user_input}"))
        print_prodotto(product)
        logger.info("Prodotto visualizzato con successo")
    
    except ValueError as e:
        print(f"❌ Errore di validazione: {e}")
        logger.warning(f"Errore di validazione: {e}")
    
    except KeyError as e:
        print(f"❌ Errore nei dati: Campo {e} non trovato")
        logger.error(f"Campo mancante: {e}")
    
    except (ConnectionError, TimeoutError):
        print("❌ Errore di connessione: Controllare la connessione internet")
        logger.error("Errore di connessione all'API")
    
    except Exception as e:
        print(f"❌ Errore inaspettato: {type(e).__name__} - {e}")
        logger.critical(f"Errore inaspettato: {type(e).__name__} - {e}")

    

if __name__ == "__main__":
    main()