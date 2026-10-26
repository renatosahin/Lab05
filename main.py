import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)

    txt_tipo = ft.TextField(label = "Tipo")
    txt_marca = ft.TextField(label = "Marca")
    txt_anno_acquisto = ft.TextField(label = "Anno acquisto")

    txt_valore = ft.TextField(value = "0",
                              disabled = True,
                              width = 120,
                              text_size = 16,
                              text_align = ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"


    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"


    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def handler_minus(e):
        valore = int(txt_valore.value)
        if valore > 0: # gestisco i valori negativi, non voglio un prezzo negativo
            txt_valore.value = str(valore - 1)
            page.update()

    def handler_plus(e):
        valore = int(txt_valore.value)
        txt_valore.value = str(valore + 1)
        page.update()

    def aggiungi_nuovo_strumento(e):
        # strip per restituire le stringhe pulite
        tipo = txt_tipo.value.strip()
        marca = txt_marca.value.strip()
        anno_acquisto_str = txt_anno_acquisto.value.strip()
        valore_str = txt_valore.value

        # Controllo la validità dei campi con valori numerici
        if anno_acquisto_str.isdigit() and valore_str.isdigit(): # controllo che siano numerici
            anno_acquisto = int(anno_acquisto_str)
            valore = float(valore_str)
            # Aggiungo lo strumento al deposito in questo caso
            deposito.aggiungi_strumento(tipo, marca, anno_acquisto, valore)

            # Svuoto i campi TextField e riporto il contatore del valore a 0
            txt_tipo.value = ""
            txt_marca.value = ""
            txt_anno_acquisto.value = ""
            txt_valore.value = "0"

            # Aggiorna la ListView e la pagina
            aggiorna_lista_strumenti()
        else:
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e posti.")



    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btnMinus = ft.IconButton(icon = ft.Icons.REMOVE,
                             icon_color = ft.Colors.RED,
                             icon_size = 20,
                             on_click=handler_minus)
    btnPlus = ft.IconButton(icon = ft.Icons.ADD,
                            icon_color = ft.Colors.GREEN,
                            icon_size = 20,
                            on_click=handler_plus)

    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click = aggiungi_nuovo_strumento) # pulsante aggiungi strumento


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(), # il divider posto alla fine della sezione 1 non è stato posto alla fine della sezione 2, devo aggiungerlo qui
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=20,   # un po meno spazio rispetto a prima altrimenti il counter non entra
               controls=[txt_tipo, txt_marca, txt_anno_acquisto, btnMinus, txt_valore, btnPlus], # tutti i controlli in ordine di comparsa nella schermata
               alignment=ft.MainAxisAlignment.CENTER),
               pulsante_aggiungi_strumento, # pulsante finale per aggiungere lo strumento


        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
