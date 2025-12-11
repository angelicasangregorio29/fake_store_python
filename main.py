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
    """Stampa i dettagli del prodotto in formato professionale"""
    try:
        print("\n" + "=" * 80)
        print(f"{'DETTAGLI PRODOTTO':^80}")
        print("=" * 80)
        
        print(f"\n🆔  ID: {product['id']}")
        print("\n📦 TITOLO:")
        print(f"   {product['title']}")
        
        print(f"\n🏷️  CATEGORIA: {product['category']}")
        
        print(f"\n💰 PREZZO: €{product['price']:.2f}")
        
        print("\n📝 DESCRIZIONE:")
        # Stampa la descrizione con word wrap
        description = product['description']
        max_width = 76
        words = description.split()
        current_line = "   "
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += word + " "
            else:
                print(current_line)
                current_line = "   " + word + " "
        
        if current_line.strip() != "":
            print(current_line)
        
        print("\n" + "=" * 80 + "\n")
        
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


def print_lista_prodotti(products: list[dict[str, any]]) -> None:
    """Stampa la lista dei prodotti mostrando solo ID e titolo"""
    try:
        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'TITOLO':<75}")
        print("=" * 80)
        
        for idx, product in enumerate(products, 1):
            try:
                product_data = product_model(product)
                title = product_data["title"]
                if len(title) > 75:
                    title = title[:72] + "..."
                print(f"{product_data['id']:<5} {title:<75}")
            except ValueError:
                logger.warning(f"Prodotto non valido, saltato: ID {product.get('id', 'N/A')}")
                continue
        
        print("=" * 80)
        print(f"Totale prodotti: {len(products)}\n")
    
    except Exception as e:
        error_msg = f"Errore nella stampa della lista: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e


def menu_principale() -> str:
    """Mostra il menu principale e restituisce la scelta dell'utente"""
    print("\n" + "=" * 40)
    print("🛍️  FAKE STORE - MENU PRINCIPALE")
    print("=" * 40)
    print("1. Visualizza lista completa prodotti")
    print("2. Cerca un prodotto per ID")
    print("3. Esci")
    print("=" * 40)
    
    choice = input("Seleziona un'opzione (1-3): ").strip()
    return choice


def main() -> None:
    """Funzione principale con gestione errori robusta"""
    while True:
        try:
            choice = menu_principale()
            
            if choice == "1":
                # Visualizza lista completa
                logger.info("Utente ha scelto: visualizza lista completa")
                products = get_all_products()
                print_lista_prodotti(products)
                
                # Chiedi di visualizzare i dettagli di un prodotto
                product_id = input("Inserisci l'ID di un prodotto per visualizzare i dettagli (o premi Invio per tornare al menu): ").strip()
                
                if product_id:
                    if not product_id.isdigit():
                        print("❌ L'ID deve essere un numero intero")
                        logger.warning(f"ID non valido: {product_id}")
                    else:
                        logger.info(f"Richiesta dettagli prodotto ID: {product_id}")
                        product = product_model(get_data(f"{BASE_URL}/{product_id}"))
                        print()
                        print_prodotto(product)
                        logger.info("Prodotto visualizzato con successo")
            
            elif choice == "2":
                # Cerca un prodotto per ID
                logger.info("Utente ha scelto: cerca per ID")
                user_input = input("Inserisci l'id del prodotto da visualizzare: ").strip()
                
                # Validazione input
                if not user_input:
                    raise ValueError("ID non può essere vuoto")
                
                if not user_input.isdigit():
                    raise ValueError("L'ID deve essere un numero intero")
                
                logger.info(f"Richiesta per il prodotto ID: {user_input}")
                
                product = product_model(get_data(f"{BASE_URL}/{user_input}"))
                print()
                print_prodotto(product)
                logger.info("Prodotto visualizzato con successo")
            
            elif choice == "3":
                print("\n👋 Arrivederci!\n")
                logger.info("Utente ha chiuso l'applicazione")
                break
            
            else:
                print("❌ Opzione non valida. Seleziona 1, 2 o 3.\n")
                logger.warning(f"Opzione non valida selezionata: {choice}")
        
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