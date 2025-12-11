"""Modulo API per le operazioni di comunicazione con il server"""
from requests import get, exceptions
from config import logger


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
