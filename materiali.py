"""Genera la scheda materiali: materiali.xlsx (da scaricare) e materiali.js (letto da materiali.html).

Per aggiornare prezzi o prodotti si cambiano le liste qui sotto e si rilancia:
    python3 materiali.py
Serve openpyxl (pip install openpyxl).
"""
import json
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

AGGIORNATO = '3 novembre 2026'

# Superfici interne dalle scansioni, balconi e veranda esclusi.
STANZE = [
    ('Camera di Christian e Gabriele', 18.2),
    ('Camera di Alessia', 12.3),
    ('Camera da letto', 19.9),
    ('Salotto', 19.5),
    ('Cucina', 10.8),
    ('Bagno', 5.0),
    ('Corridoio', 6.8),
    ('Ingresso', 6.6),
    ('Sotto i muri demoliti', 0.7),
]
BATTISCOPA_M = 95  # perimetro senza bagno, tolte le porte, con il 10% in più

LM = 'https://www.leroymerlin.it/prodotti/'
IK = 'https://www.ikea.com/it/it/search/?q='
TM = 'https://www.tecnomat.it/it/'

# negozio, nome, tipo, spessore totale/legno, €/mq, mq per confezione, prezzo confezione, sconto alla cassa, scarto, link, note
PAVIMENTI = [
    ('Leroy Merlin', 'Parquet multistrato 4S ARTENS rovere naturale spazzolato e verniciato', 'Parquet multistrato', '10 / 2,5 mm', 27.99, 2.03, 56.82, 0, 0.08, LM + 'parquet-multistrato-4s-artens-in-rovere-naturale-spazzolato-e-verniciato-natura-sp-10-2-5-mm-2-03-m2-90544729.html', 'Il più economico in legno vero; sottile, adatto sopra il pavimento esistente'),
    ('Leroy Merlin', 'Parquet multistrato 4S ARTENS rovere sbiancato', 'Parquet multistrato', '10 / 2,5 mm', 33.99, 2.03, 69.00, 0, 0.08, LM + 'parquet-multistrato-4s-artens-in-rovere-sbiancato-sbiancato-natura-sp-10-2-5-mm-2-03-m2-90544731.html', ''),
    ('Leroy Merlin', 'Parquet multistrato 4S ARTENS rovere dorato levigato', 'Parquet multistrato', '10 / 2,5 mm', 33.99, 2.03, 69.00, 0, 0.08, LM + 'parquet-multistrato-4s-artens-in-rovere-dorato-levigato-natura-sp-10-2-5-mm-2-03-m2-90544730.html', ''),
    ('Leroy Merlin', 'Parquet multistrato Scala M rovere naturale spazzolato rustico', 'Parquet multistrato', '14 / 3 mm', 39.90, 1.44, 57.45, 0, 0.08, LM + 'parquet-multistrato-scala-m-in-rovere-naturale-spazzolato-rustico-sp-14-3-mm-1-44-m2-95888566.html', '3 mm di legno, il rustico nasconde i graffi'),
    ('Leroy Merlin', 'Parquet multistrato M ARTENS rovere naturale spazzolato e verniciato', 'Parquet multistrato', '14 / 2,5 mm', 45.99, 0.99, 45.53, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-rovere-naturale-spazzolato-e-verniciato-natura-sp-14-2-5-mm-0-99-m2-90544725.html', ''),
    ('Leroy Merlin', 'Parquet multistrato M ARTENS rovere spazzolato e verniciato', 'Parquet multistrato', '14 / 2,5 mm', 45.99, 0.99, 45.53, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-rovere-spazzolato-e-verniciato-natura-sp-14-2-5-mm-0-99-m2-90544735.html', ''),
    ('Leroy Merlin', 'Parquet multistrato L ARTENS rovere spazzolato e verniciato', 'Parquet multistrato', '14 / 2,5 mm', 46.99, 1.37, 64.38, 0, 0.08, LM + 'parquet-multistrato-l-artens-in-rovere-spazzolato-e-verniciato-natura-sp-14-2-5-mm-1-37-m2-90544736.html', ''),
    ('Leroy Merlin', 'Parquet multistrato M ARTENS bianco verniciato', 'Parquet multistrato', '14 / 2,5 mm', 48.99, 0.99, 48.50, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-bianco-verniciato-natura-sp-14-2-5-mm-0-99-m2-92302653.html', ''),
    ('Leroy Merlin', 'Parquet multistrato XL vetrificato', 'Parquet multistrato', '14 / 2,5 mm', 48.90, 1.37, 66.99, 0, 0.08, LM + 'parquet-multistrato-xl-vetrificato-natura-sp-14-2-5-mm-1-37-m2-72452296.html', '99 recensioni'),
    ('Leroy Merlin', 'Parquet multistrato M vetrificato', 'Parquet multistrato', '14 / 2,5 mm', 49.99, 0.99, 49.49, 0, 0.08, LM + 'parquet-multistrato-m-vetrificato-natura-sp-14-2-5-mm-0-99-m2-80179119.html', ''),
    ('Leroy Merlin', 'Parquet multistrato XL ARTENS marrone spazzolato', 'Parquet multistrato', 'non indicato', 49.99, 2.26, 112.98, 0, 0.08, LM + 'parquet-multistrato-xl-artens-in-marrone-spazzolato-natura-2-26-m2-92303382.html', 'Spessore da controllare sulla scheda'),
    ('Leroy Merlin', 'Parquet multistrato intenso M rovere irlandese vetrificato', 'Parquet multistrato', '14 / 3,3 mm', 51.21, 1.227, 62.84, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-rovere-naturale-vetrificato-natura-sp-14-3-3-mm-1-227-m2-80179067.html', 'In offerta al -10% (prima 56,90 €/mq)'),
    ('Leroy Merlin', 'Parquet multistrato XL BARLINEK spazzolato', 'Parquet multistrato', '14 / 2,5 mm', 51.90, 1.37, 71.10, 0.15, 0.08, LM + 'parquet-multistrato-xl-barlinek-spazzolato-natura-sp-14-2-5-mm-1-37-m2-82703044.html', 'Marca nota; -15% alla cassa'),
    ('Leroy Merlin', 'Parquet multistrato M ARTENS rovere naturale verniciato', 'Parquet multistrato', '14 / 2,5 mm', 52.99, 0.99, 52.46, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-rovere-naturale-verniciato-natura-sp-14-2-5-mm-0-99-m2-90544727.html', ''),
    ('Leroy Merlin', 'Parquet multistrato M ARTENS rovere chiaro spazzolato e verniciato', 'Parquet multistrato', '14 / 2,5 mm', 52.99, 0.99, 52.46, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-rovere-chiaro-spazzolato-e-verniciato-natura-sp-14-2-5-mm-0-99-m2-90544740.html', ''),
    ('Leroy Merlin', 'Parquet multistrato XL ARTENS rovere chiaro spazzolato e verniciato', 'Parquet multistrato', '14 / 2,5 mm', 54.99, 1.37, 75.34, 0, 0.08, LM + 'parquet-multistrato-xl-artens-in-rovere-chiaro-spazzolato-e-verniciato-natura-sp-14-2-5-mm-1-37-m2-90544741.html', ''),
    ('Leroy Merlin', 'PQT Delux S Natural 14 × 150 × 1200 mm', 'Parquet multistrato', '14 mm / non indicato', 54.99, 1.44, 79.19, 0, 0.08, LM + 'pqt-delux-s-natural-14-x-150-x-1200-mm-1-44-m2-77809687.html', 'Strato di legno da controllare'),
    ('Leroy Merlin', 'Parquet multistrato XXL ARTENS spazzolato', 'Parquet multistrato', 'non indicato', 58.99, 1.58, 93.20, 0, 0.08, LM + 'parquet-multistrato-xxl-artens-spazzolato-natura-1-58-m2-92303339.html', 'Spessore da controllare sulla scheda'),
    ('Leroy Merlin', 'Parquet Spina italiana M ARTENS rovere spazzolato e verniciato', 'Parquet a spina', '14 / 2,5 mm', 62.98, 0.65, 40.94, 0.15, 0.15, LM + 'parquet-multistrato-spina-italiana-m-artens-in-rovere-spazzolato-e-verniciato-natura-sp-14-2-5-mm-0-65-m2-90544737.html', '-15% alla cassa; posa a spina, più scarto'),
    ('Leroy Merlin', 'Parquet Spina italiana M ARTENS rovere naturale spazzolato e verniciato', 'Parquet a spina', '14 / 2,5 mm', 63.98, 0.65, 41.59, 0, 0.15, LM + 'parquet-multistrato-spina-italiana-m-artens-in-rovere-naturale-spazzolato-e-verniciato-natura-sp-14-2-5-mm-0-65-m2-90544742.html', 'Posa a spina, più scarto'),
    ('Leroy Merlin', 'Parquet striscia M rovere naturale spazzolato', 'Parquet', '10 / 2,5 mm', 64.90, 3.0, 194.70, 0, 0.08, LM + 'parquet-massello-striscia-di-parquet-m-in-rovere-naturale-spazzolato-natura-sp-10-2-5-mm-3-m2-90794723.html', ''),
    ('Leroy Merlin', 'Parquet multistrato M ARTENS rovere astrale vetrificato select', 'Parquet multistrato', '14 / 3,3 mm', 64.90, 1.227, 79.83, 0, 0.08, LM + 'parquet-multistrato-m-artens-in-rovere-astrale-vetrificato-select-sp-14-3-3-mm-1-227-m2-82762494.html', ''),
    ('Leroy Merlin', 'Parquet Spina italiana S rovere naturale verniciato select', 'Parquet a spina', '3 mm di legno', 73.89, 0.583, 43.08, 0, 0.15, LM + 'parquet-multistrato-spina-italiana-s-in-rovere-naturale-verniciato-select-3-mm-0-583-m2-93794488.html', 'Posa a spina, più scarto'),
    ('Leroy Merlin', 'Parquet multistrato L rovere naturale oliato', 'Parquet multistrato', '12 / 3 mm', 79.90, 1.542, 123.05, 0, 0.08, LM + 'parquet-multistrato-l-in-rovere-naturale-oliato-natura-sp-12-3-mm-1-542-m2-82679977.html', 'Oliato: da curare, sconsigliato in cucina'),
    ('Leroy Merlin', 'Parquet multistrato striscia L rovere naturale oliato', 'Parquet multistrato', '14 / 3 mm', 85.06, 2.086, 177.44, 0, 0.08, LM + 'parquet-multistrato-striscia-di-parquet-l-in-rovere-naturale-oliato-natura-sp-14-3-mm-2-086-m2-82128170.html', 'Oliato: da curare, sconsigliato in cucina'),
    ('Leroy Merlin', 'Pavimento bambù M ARTENS marrone nero vetrificato', 'Bambù', '14 / 14 mm', 42.90, 1.09, 46.76, 0, 0.08, LM + 'pavimento-bambu-m-artens-in-marrone-nero-vetrificato-select-sp-14-14-mm-1-09-m2-91758064.html', ''),
    ('Leroy Merlin', 'Pavimento bambù M ARTENS miele laccato', 'Bambù', '14 / 14 mm', 42.99, 1.37, 58.90, 0, 0.08, LM + 'pavimento-bambu-m-artens-in-miele-laccato-natura-sp-14-14-mm-1-37-m2-82664650.html', ''),
    ('Leroy Merlin', 'Pavimento bambù M ARTENS laccato boho', 'Bambù', '15 / 15 mm', 47.99, 1.09, 52.31, 0, 0.08, LM + 'pavimento-bambu-m-artens-in-rovere-naturale-laccato-boho-sp-15-15-mm-1-09-m2-82664649.html', ''),
    ('Leroy Merlin', 'Vinilico a incastro HEECK EICHE effetto rovere medio', 'Vinilico', 'non indicato', 25.53, 2.782, 70.98, 0, 0.08, LM + '2-782m2-pavimento-vinilico-a-incastro-effetto-legno-rovere-medio-con-isolamento-acustico-uso-intensivo-ambienti-umidi-2451-heeck-eiche-95562816.html', 'Venduto da un altro negozio sul sito; va bene anche in bagno'),
    ('Tecnomat', 'Parquet stratificato rovere sbiancato 3 strips, 1092 × 207 mm', 'Parquet multistrato', '10 / 2,5 mm', 25.9, 2.03, 52.58, 0, 0.08, TM + 'parquet-strat-rov-sb-3-strips-nat-10mm-10039308/', 'A click, flottante'),
    ('Tecnomat', 'Parquet stratificato rovere naturale Molti, 1092 × 207 mm', 'Parquet multistrato', '10 mm / non indicato', 27.9, 2.03, 56.64, 0, 0.08, TM + 'parquet-strat-rov-naturale-sp-10mm-25076377/', 'Strato di legno da controllare'),
    ('Tecnomat', 'Parquet stratificato rovere golden, 1092 × 130 mm', 'Parquet multistrato', '14 / 2,5 mm', 34.9, 0.99, 34.55, 0, 0.08, TM + 'parquet-strat-rov-golden-sp-14mm-25120259/', 'Flottante, laccato opaco'),
    ('Tecnomat', 'Parquet stratificato rovere naturale 3 strips, 1092 × 207 mm', 'Parquet multistrato', '14 / 3,2 mm', 34.9, 1.58, 55.14, 0, 0.08, TM + 'parquet-strat-rovere-3-strips-nat-14mm-10039310/', 'Consigliato: 3,2 mm di legno al prezzo più basso, a click'),
    ('Tecnomat', 'Parquet stratificato rovere cognac, 1092 × 130 mm', 'Parquet multistrato', '14 mm / non indicato', 37.9, 0.99, 37.52, 0, 0.08, TM + 'parquet-strat-rov-cognac-sp-14mm-25112344/', 'Strato di legno da controllare'),
    ('Tecnomat', 'Parquet stratificato rovere bianco, 725 × 180 mm', 'Parquet multistrato', '14 / 2,5 mm', 39.9, 0.91, 36.31, 0, 0.08, TM + 'parquet-strat-rov-bianco-sp-14mm-25076378/', ''),
    ('Tecnomat', 'Parquet stratificato rovere spazzolato 1 strip, 1092 × 130 mm', 'Parquet multistrato', '14 / 2,5 mm', 44.51, 0.99, 44.06, 0, 0.08, TM + 'parquet-strat-rovere-1-strip-spazz-14mm-10039315/', 'A click, flottante'),
    ('Tecnomat', 'Parquet stratificato rovere rustico 1 strip, 2200 × 180 mm', 'Parquet multistrato', '14 / 2,5 mm', 44.9, 2.77, 124.37, 0, 0.08, TM + 'parquet-strat-rov-rustico-1-strip-14mm-10052510/', 'Doghe lunghe 2,2 m; flottante o incollato'),
    ('Tecnomat', 'Parquet stratificato rovere a spina di pesce, 725 × 130 mm', 'Parquet a spina', '14 / 2,5 mm', 44.91, 0.65, 29.19, 0, 0.15, TM + 'parquet-strat-rov-sdp-1-strip-14-mm-25011686/', 'Posa a spina, più scarto'),
    ('Tecnomat', 'Parquet prefinito iroko massello, 450 × 70 mm', 'Parquet massello', '10 mm, tutto legno', 69.9, 1.89, 132.11, 0, 0.08, TM + 'parquet-massello-iroko-sp-10mm-25099970/', 'Massello, solo posa incollata'),
    ('IKEA', 'SLÄTTEN laminato effetto pino grigio perla', 'Laminato', '6 mm', 5.50, 3.0, 16.50, 0, 0.08, IK + '40424771', 'Prezzo di luglio 2022; solo camere, non per salotto e cucina'),
    ('IKEA', 'TUNDRA laminato effetto rovere', 'Laminato', '7 mm', 9.00, 2.25, 20.25, 0, 0.08, IK + '20424772', 'Prezzo di luglio 2022; AC3, garanzia 10 anni'),
    ('IKEA', 'PRÄRIE laminato effetto rovere', 'Laminato', '7 mm', 10.00, 2.25, 22.50, 0, 0.08, IK + '80487460', 'Prezzo di luglio 2022; AC3, garanzia 10 anni'),
    ('IKEA', 'GOLV laminato effetto rovere chiaro', 'Laminato', '8 mm', 15.00, 2.0, 30.00, 0, 0.08, IK + '30417568', 'Prezzo di luglio 2022; AC4, garanzia 15 anni'),
    ('IKEA', 'BETESMARK laminato rovere naturale', 'Laminato', '8 mm', 15.00, 2.2, 33.00, 0, 0.08, IK + '60488615', 'Prezzo di luglio 2022; AC5, 25 anni, resiste all\'acqua 24 h'),
    ('IKEA', 'TORRÄNG composito effetto legno', 'Composito', '4 mm', 31.50, 2.35, 74.02, 0, 0.08, IK + '30488612', 'Prezzo di luglio 2022; va bene anche in bagno'),
]

# materiale, quantità, unità, prezzo minimo e massimo in totale, quando serve
ALTRI = [
    ('Battiscopa', BATTISCOPA_M, 'm', 240, 950, 'Sempre; tutta la casa tranne il bagno'),
    ('Materassino sotto il pavimento flottante', 107, 'mq', 160, 380, 'Con laminato o parquet flottante'),
    ('Lamina contro l\'umidità', 107, 'mq', 100, 150, 'Con pavimento flottante su massetto o cemento'),
    ('Soglie e profili di passaggio', 9, 'pz', 135, 300, 'Sotto le porte e tra pavimenti diversi'),
    ('Prese, interruttori e placche', 50, 'punti', 400, 1000, 'Sempre'),
    ('Lampade e faretti', 12, 'punti luce', 300, 1000, 'Sempre'),
    ('Pavimento del bagno', 6, 'mq', 90, 240, 'Se si rifà il bagno'),
    ('Rivestimento del bagno', 22, 'mq', 330, 770, 'Se si rifà il bagno'),
    ('Piatto doccia 174 × 80 cm', 1, 'pz', 150, 400, 'Se si rifà il bagno'),
    ('Parete o box doccia', 1, 'pz', 250, 700, 'Se si rifà il bagno'),
    ('WC e bidet', 2, 'pz', 300, 700, 'Se si rifà il bagno'),
    ('Cassetta di scarico da incasso', 1, 'pz', 150, 250, 'Se il WC è sospeso'),
    ('Mobile da 120 cm con lavabo', 1, 'pz', 400, 1000, 'Se si rifà il bagno'),
    ('Rubinetti di lavabo, bidet e colonna doccia', 3, 'pz', 250, 800, 'Se si rifà il bagno'),
    ('Rubinetto della lavatrice', 1, 'pz', 15, 30, 'Se si rifà il bagno'),
    ('Specchio e accessori del bagno', 1, 'set', 100, 250, 'Se si rifà il bagno'),
    ('Climatizzatori', 4, 'split', 2000, 4000, 'Installazione del frigorista a parte'),
]

superficie = round(sum(m for _, m in STANZE), 1)
bagno = dict(STANZE)['Bagno']

# --- Excel ---
wb = Workbook()
VERDE, CHIARO, GRIGIO = '2F6F66', 'E2EFEC', 'F5F3EE'
titolo = Font(name='Calibri', size=16, bold=True, color=VERDE)
testa = Font(bold=True, color='FFFFFF')
fill_testa = PatternFill('solid', fgColor=VERDE)
fill_input = PatternFill('solid', fgColor='FFF4D6')
fill_tot = PatternFill('solid', fgColor=CHIARO)
linea = Border(bottom=Side(style='thin', color='DDD7CB'))
EURO = '#,##0.00 €;-#,##0.00 €'
EURO0 = '#,##0 €'

def intestazione(ws, riga, nomi, larghezze):
    for c, (n, w) in enumerate(zip(nomi, larghezze), 1):
        cell = ws.cell(riga, c, n)
        cell.font, cell.fill = testa, fill_testa
        cell.alignment = Alignment(vertical='center', wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[riga].height = 32

# Foglio 1: superfici
ws = wb.active
ws.title = 'Superfici'
ws['A1'] = 'Superfici della casa'; ws['A1'].font = titolo
ws['A2'] = f'Dalle scansioni 3D, balconi e veranda esclusi. Misure da ricontrollare col metro. Aggiornato al {AGGIORNATO}.'
intestazione(ws, 4, ['Stanza', 'Superficie (mq)'], [36, 16])
r = 5
for nome, mq in STANZE:
    ws.cell(r, 1, nome).border = linea
    c = ws.cell(r, 2, mq); c.number_format = '0.0'; c.border = linea
    r += 1
ultima = r - 1
ws.cell(r, 1, 'Tutta la casa').font = Font(bold=True)
c = ws.cell(r, 2, f'=SUM(B5:B{ultima})'); c.number_format = '0.0'; c.font = Font(bold=True)
for col in (1, 2): ws.cell(r, col).fill = fill_tot
RIGA_TOT = r
r += 2
ws.cell(r, 1, 'Bagno incluso? (SI / NO)').font = Font(bold=True)
c = ws.cell(r, 2, 'SI'); c.fill = fill_input; c.alignment = Alignment(horizontal='center')
RIGA_BAGNO = r
r += 1
ws.cell(r, 1, 'Superficie da coprire (mq)').font = Font(bold=True)
riga_bagno_stanza = 5 + [n for n, _ in STANZE].index('Bagno')
c = ws.cell(r, 2, f'=IF(UPPER(B{RIGA_BAGNO})="NO",B{RIGA_TOT}-B{riga_bagno_stanza},B{RIGA_TOT})'); c.number_format = '0.0'; c.font = Font(bold=True, size=13, color=VERDE)
RIGA_COPRIRE = r
r += 1
ws.cell(r, 1, 'Battiscopa (m), con il 10% in più')
ws.cell(r, 2, BATTISCOPA_M)
r += 2
ws.cell(r, 1, 'Cambia la cella gialla per togliere il bagno: il foglio Pavimenti si ricalcola.').font = Font(italic=True, color='6C675D')
COPRIRE = f"Superfici!$B${RIGA_COPRIRE}"

# Foglio 2: pavimenti
ws2 = wb.create_sheet('Pavimenti')
ws2['A1'] = 'Pavimenti per tutta la casa'; ws2['A1'].font = titolo
ws2['A2'] = f'Quantità calcolate sulla superficie del foglio Superfici, più lo scarto di posa. Prezzi letti il {AGGIORNATO}; quelli IKEA sono della lista di luglio 2022. Da verificare prima di comprare.'
nomi = ['Negozio', 'Prodotto', 'Tipo', 'Spessore totale / legno', '€ al mq', 'mq per confezione', 'Prezzo confezione', 'Scarto di posa', 'mq da comprare', 'Confezioni', 'mq comprati', 'Totale', 'Sconto alla cassa', 'Totale con sconto', 'Link', 'Note']
intestazione(ws2, 4, nomi, [13, 52, 18, 18, 10, 11, 11, 9, 11, 11, 11, 12, 10, 13, 12, 44])
ordinati = sorted(PAVIMENTI, key=lambda p: -(-superficie * (1 + p[8]) // p[5]) * p[6] * (1 - p[7]))
for i, (neg, nome, tipo, sp, eur, mqc, conf, sconto, scarto, link, note) in enumerate(ordinati):
    r = 5 + i
    vals = [neg, nome, tipo, sp, eur, mqc, conf, scarto,
            f'={COPRIRE}*(1+H{r})', f'=ROUNDUP(I{r}/F{r},0)', f'=J{r}*F{r}', f'=J{r}*G{r}', sconto, f'=L{r}*(1-M{r})', 'Apri', note]
    for c, v in enumerate(vals, 1):
        cell = ws2.cell(r, c, v); cell.border = linea
        cell.alignment = Alignment(vertical='top', wrap_text=c in (2, 16))
    ws2.cell(r, 5).number_format = EURO
    ws2.cell(r, 6).number_format = '0.000'
    ws2.cell(r, 7).number_format = EURO
    ws2.cell(r, 8).number_format = '0%'
    ws2.cell(r, 9).number_format = '0.0'
    ws2.cell(r, 11).number_format = '0.0'
    ws2.cell(r, 12).number_format = EURO0
    ws2.cell(r, 13).number_format = '0%'
    c = ws2.cell(r, 14); c.number_format = EURO0; c.font = Font(bold=True); c.fill = fill_tot
    c = ws2.cell(r, 15); c.hyperlink = link; c.font = Font(color='0563C1', underline='single')
ws2.freeze_panes = 'C5'
ws2.auto_filter.ref = f'A4:P{4 + len(PAVIMENTI)}'

# Foglio 0: lista acquisti completa, pavimento compreso
from openpyxl.worksheet.datavalidation import DataValidation
SCELTO = 'Parquet stratificato rovere naturale 3 strips, 1092 × 207 mm'
NO_DI_PARTENZA = {"Lamina contro l'umidità"}
ultima_pav = 4 + len(PAVIMENTI)
ws0 = wb.create_sheet('Lista acquisti', 0)
wb.active = 0
ws0['A1'] = 'Lista acquisti: tutti i materiali da comprare'; ws0['A1'].font = titolo
ws0['A2'] = 'Quelli che non sono nei preventivi di manodopera. Scegli il pavimento nella cella gialla e scrivi NO sui lavori che non fate: i totali si aggiornano.'
ws0['A4'] = 'Pavimento scelto'; ws0['A4'].font = Font(bold=True)
ws0.merge_cells('B4:E4')
c = ws0['B4']; c.value = SCELTO; c.fill = fill_input
dv_pav = DataValidation(type='list', formula1=f"=Pavimenti!$B$5:$B${ultima_pav}", allow_blank=False)
ws0.add_data_validation(dv_pav); dv_pav.add('B4')
intestazione(ws0, 6, ['Materiale', 'Quantità', 'Unità', 'Da (€)', 'A (€)', 'Lo facciamo?', 'Pagato (€)', 'Comprato?', 'Quando serve'], [42, 10, 11, 11, 11, 12, 12, 11, 44])
dv_si = DataValidation(type='list', formula1='"SI,NO"', allow_blank=False)
ws0.add_data_validation(dv_si)
trova = lambda col: f'INDEX(Pavimenti!${col}$5:${col}${ultima_pav},MATCH($B$4,Pavimenti!$B$5:$B${ultima_pav},0))'
righe = [('Pavimento scelto, tutta la casa', '=' + trova('K'), 'mq', '=' + trova('N'), '=' + trova('N'), 'SI', 'Sempre: il prodotto è quello della cella gialla')]
righe += [(n, q, u, a, b, 'NO' if n in NO_DI_PARTENZA else 'SI', quando) for n, q, u, a, b, quando in ALTRI]
for i, (nome, q, u, a, b, si, quando) in enumerate(righe):
    r = 7 + i
    for col, v in enumerate([nome, q, u, a, b, si, None, None, quando], 1):
        ws0.cell(r, col, v).border = linea
    ws0.cell(r, 2).number_format = '0.0' if i == 0 else '0'
    for col in (4, 5, 7): ws0.cell(r, col).number_format = EURO0
    for col in (6, 7, 8): ws0.cell(r, col).fill = fill_input
    ws0.cell(r, 6).alignment = Alignment(horizontal='center')
    dv_si.add(f'F{r}')
r = 7 + len(righe)
ws0.cell(r, 1, 'Totale dei lavori che fate').font = Font(bold=True)
for col, L in ((4, 'D'), (5, 'E'), (7, 'G')):
    f = f'=SUM({L}7:{L}{r - 1})' if L == 'G' else f'=SUMIF($F$7:$F${r - 1},"SI",{L}7:{L}{r - 1})'
    c = ws0.cell(r, col, f); c.number_format = EURO0; c.font = Font(bold=True); c.fill = fill_tot
ws0.freeze_panes = 'B7'

for w in wb.worksheets:
    w.sheet_view.showGridLines = False
wb.save('materiali.xlsx')

# --- dati per la pagina ---
dati = {
    'aggiornato': AGGIORNATO,
    'stanze': STANZE,
    'battiscopa': BATTISCOPA_M,
    'pavimenti': [dict(zip(['negozio', 'nome', 'tipo', 'spessore', 'eurMq', 'mqConf', 'prezzoConf', 'sconto', 'scarto', 'link', 'note'], p)) for p in PAVIMENTI],
    'altri': [dict(zip(['nome', 'q', 'u', 'min', 'max', 'quando'], a)) for a in ALTRI],
}
with open('materiali.js', 'w') as f:
    f.write('/* Generato da materiali.py: non modificare a mano. */\nconst MATERIALI = ' + json.dumps(dati, ensure_ascii=False, indent=1) + ';\n')
print('Superficie', superficie, 'mq; pavimenti', len(PAVIMENTI))
