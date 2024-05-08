<h1 align="center"> Mērījumu Sistēma </h1> <br>

## Saturs

- [Kas tas ir?](#kas-tas-ir)
- [Kāpēc risinājums ir nepieciešams?](#kāpēc-risinājums-ir-nepieciešams)
- [Aparatūra](#aparatūra)
- [Lietošanas instrukcija](#lietošanas-instrukcija)
- [Uzlabojumi](#uzlabojumi)
- [Alternatīvas](#alternatīvas)
- [Autori](#autori)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Kas tas ir?

Mērijumu Sistēma (MS) ir attālumu mērītājs, kas izmanto Time of Flight(ToF) komponentes, lai mērītu attālumu starp komponenti un objektu. Tof komponente sūta mērijuma datus uz mikrokontrolieri. Mikrokontrolieris saņem vai satur informāciju par citiem datiem - pīkstuļu slieksni un pīkstuļa skaļumu, slieksni vadāmu ar pogām, un skaļums vadāms ar potenciometru. Šī informācija tālāk tiek aizsūtīta uz Orgnaic Light-Emitting Diode (OLED) displeju un pīkstuli.

Šis risinājums ir noderīgs cilvēkiem ar vāju redzi vai neredzību, jo tas izmanto Time of Flight tehnoloģiju, lai precīzi mērītu attālumu starp komponenti un objektu. Šāda veida sistēma var būt noderīga cilvēkiem, kuriem ir grūtības novērtēt attālumu vai identificēt objektus apkārtējā vidē.

![image](https://github.com/SkylerAcer/Measurment-system-/assets/96178550/e88cd2ea-e769-4920-8dbe-cf7c679a871b)



## Kāpēc risinājums ir nepieciešams?

Latvijā ir ~140 tūkstošu cilvēku, kuriem ir kāda no invaliditātes pakāpēm, un 12+ tūkstošiem no tiem ir invaliditāte, kura satistīta ar redzes traucējumiem. (https://www.lnbiedriba.lv/lv/par-biedribu/statistika-un-petijumi/)



Neredzīgie var izmantot šo ierīci, lai noteiktu attālumu no dažādiem objektiem, kas uzlabotu viņu mobilitāti un neatkarību. Ar Infrasarkaniem stariem, MS palīdz identificēt šķēršļus un novērtēt attālumu no tiem, tādējādi veicinot drošu pārvietošanos.

## Aparatūra

### Detaļu saraksts:
- Mikrokontrolieris Raspberry Pi Pico W
- 2x ToF sensori
- Pīkstulis
- Potenciometrs
- 2x Pogas
- OLED displejs.

### Detaļu apraksts:
- Mikrokontrolieris Raspberry Pi Pico W - Atbild par datu ievākšanu un to apstrādāšanu.

- ToF sensori - Ar infrasarkano staru palīdzību iegūst datus par to cik tālu no tā atrodas kāds objekts. Tā maksimālais attāluma mērījums ir 8160mm, jeb 8m un 16cm.


## Lietošanas instrukcija
### Koda izmantošana
- Lejupielādē kodu.
- Savieno Raspberry Pi Pico W mikrokonrolieri ar datoru un augšupielādēt failus.
- Savienot kopā vajadzīgās komponentes.
- Palaist caur Thonny programmu.

### Komponentes lietošana

- Skaņas regulēšana - Potenciometru regulējot, maina brīdinājuma skaļumu sistēmai.

- Sliekšņa regulēšana - 2 pogas, kas regulē MS attāluma slieksni, viena mazina attāluma slieksni, otra palielina attāluma slieksni.


## Uzlabojumi
Drošāku 

Pievienot skaņu signālu dažādu komponentu izmantošanai.

Nodrošināt veidu kā piestiprināt sistēmu uz cilvēka.


## Alternatīvas
Alternatīvas šādam asistences risinājumam jau patāvkuri, kri satur ToF sensorus, piemēri, Smart Cane

## Autori
- Anrijs Dambis
- Vanesa Vidiņa

