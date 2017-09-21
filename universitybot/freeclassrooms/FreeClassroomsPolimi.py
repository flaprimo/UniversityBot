import requests
from lxml import html
from itertools import groupby
from universitybot.freeclassrooms.FreeClassrooms import FreeClassrooms


class FreeClassroomsPolimi(FreeClassrooms):
    """
    Search for free classrooms at Politecnico di Milano
    """

    @staticmethod
    def get_free_classrooms(date, start_time, end_time):
        # get list of free classrooms from polimi website as html page
        url = 'https://www7.ceda.polimi.it/spazi/spazi/controller/RicercaAuleLibere.do?jaf_currentWFID=main'

        payload = {'spazi___model___formbean___RicercaAvanzataAuleLibereVO___postBack': 'true',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___formMode': 'FILTER',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___categoriaScelta': 'D',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___tipologiaScelta': 'tutte',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___sede': 'MIA',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___iddipScelto': 'tutti',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___sigla': '',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___giorno_day': date.day,
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___giorno_month': date.month,
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___giorno_year': date.year,
                   'jaf_spazi___model___formbean___RicercaAvanzataAuleLibereVO___giorno_date_format': 'dd/MM/yyyy',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___orario_dal': start_time.strftime('%H:%M'),
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___orario_al': end_time.strftime('%H:%M'),
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___soloPreseElettriche_default': 'N',
                   'spazi___model___formbean___RicercaAvanzataAuleLibereVO___soloPreseDiRete_default': 'N',
                   'evn_ricerca_avanzata': 'Ricerca aule libere'}

        response = requests.get(url=url, params=payload)

        #print(response.url)

        if response.ok:
            # parse free classrooms for html page
            root = html.fromstring(response.content)
            classrooms_table = root.xpath('//tbody[@class="TableDati-tbody"]/tr')

            names = classrooms_table[0].xpath('//tr/td[@class="TestoSX Dati1"][2]/b/text()')
            addresses = list(map(lambda address: address.strip(), classrooms_table[0]
                                 .xpath('//tr/td[@class="TestoSX Dati1"][1]/text()[2]')))

            # group classrooms by address
            classrooms = []
            for address, classroom_names in groupby(zip(addresses, names), lambda x: x[0]):
                names_list = []
                for classroom_name in classroom_names:
                    names_list.append(classroom_name[1])
                classrooms.append((address, names_list))

            return FreeClassroomsPolimi._to_string(classrooms)
        else:
            response.raise_for_status()

    @staticmethod
    def _to_string(freeclassrooms_list):
        freeclassrooms_string = ""

        for address in freeclassrooms_list:
            freeclassrooms_string += "*" + address[0] + "*\n"
            for classroom in address[1]:
                freeclassrooms_string += "   " + classroom + "\n"
            freeclassrooms_string += "\n"

        return freeclassrooms_string