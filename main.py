"""Modulo principale - punto di ingresso dell'applicazione"""
from config import logger
from ui import menu_principale, print_lista_prodotti, print_prodotto
from products import get_all_products, get_product_by_id


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
                    try:
                        product = get_product_by_id(product_id)
                        print()
                        print_prodotto(product)
                        logger.info("Prodotto visualizzato con successo")
                    except ValueError as e:
                        print(f"❌ Errore: {e}")
            
            elif choice == "2":
                # Cerca un prodotto per ID
                logger.info("Utente ha scelto: cerca per ID")
                user_input = input("Inserisci l'id del prodotto da visualizzare: ").strip()
                
                # Validazione input
                if not user_input:
                    raise ValueError("ID non può essere vuoto")
                
                try:
                    product = get_product_by_id(user_input)
                    print()
                    print_prodotto(product)
                    logger.info("Prodotto visualizzato con successo")
                except ValueError as e:
                    print(f"❌ Errore di validazione: {e}")
            
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
