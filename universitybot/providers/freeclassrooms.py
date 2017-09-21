import requests
import json
from itertools import groupby


class FreeClassroomsProvider:
    """
    Search for free classrooms at Politecnico di Milano
    """
    @staticmethod
    def get_free_classrooms(location, date, start_time, end_time):
        url = 'https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/elencoAule/{}'.format(location)

        payload = 'soloAuleLibere={}&dalleAulaLibera={}&alleAulaLibera={}&dataAulaLibera={}'\
            .format('S', start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), date.strftime('%d/%m/%Y'))

        response = requests.get(url=url, params=payload)

        # print(response.url)

        if response.ok:
            classrooms_json = json.loads(response.text)

            classrooms = FreeClassroomsProvider._parse_response(classrooms_json)

            return FreeClassroomsProvider._to_string(classrooms)
        else:
            response.raise_for_status()

    @staticmethod
    def _parse_response(classrooms_json):
        classroom_type_filter = ['DEPARTMENTAL CLASSROOM', 'CONFERENCE ROOM', 'AUDITORIUM', 'MASTER CLASSROOM']

        # get tuple list of classrooms
        classroom_list = []
        for classroom in classrooms_json:
            if classroom['categoria'] not in classroom_type_filter:
                (location, address) = classroom['dove'].split(', ')
                classroom_list.append((address, classroom['sigla']))

        # group classrooms by address
        classrooms = []
        for address, classroom_names in groupby(classroom_list, lambda x: x[0]):
            names_list = []
            for classroom_name in classroom_names:
                names_list.append(classroom_name[1])
            classrooms.append((address, names_list))

        return classrooms

    @staticmethod
    def _to_string(freeclassrooms_list):
        freeclassrooms_string = ''

        for address in freeclassrooms_list:
            freeclassrooms_string += "*{}*\n".format(address[0])
            for classroom in address[1]:
                freeclassrooms_string += "   {}\n".format(classroom)
            freeclassrooms_string += "\n"

        return freeclassrooms_string
