from itertools import groupby
from universitybot.providers.polimi_api import PolimiAPI


class FreeClassroomsProvider:
    """
    Search for free classrooms at Politecnico di Milano
    """
    @staticmethod
    def get_freeclassrooms(location, date, start_time, end_time):
        try:
            freeclassrooms_json = PolimiAPI.get_elenco_aule_libere(location, date, start_time, end_time)

            classroom_type_filter = ['DEPARTMENTAL CLASSROOM', 'CONFERENCE ROOM', 'AUDITORIUM', 'MASTER CLASSROOM']

            # get tuple list of classrooms
            classroom_list = []
            for classroom in freeclassrooms_json:
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

            return FreeClassroomsProvider._to_string(classrooms)

        except:
            raise ConnectionError('Politecnico di Milano server seems not responding')

    @staticmethod
    def _to_string(freeclassrooms_list):
        freeclassrooms_string = ''

        for address in freeclassrooms_list:
            freeclassrooms_string += "*{}*\n".format(address[0])
            for classroom in address[1]:
                freeclassrooms_string += "   {}\n".format(classroom)
            freeclassrooms_string += "\n"

        return freeclassrooms_string
