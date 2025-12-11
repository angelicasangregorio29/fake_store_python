"""Modulo per le operazioni di visualizzazione e interfaccia utente"""
from config import logger
from models import product_model


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
