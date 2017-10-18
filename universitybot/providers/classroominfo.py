from universitybot.providers.polimi_api import PolimiAPI

class ClassroomInfoProvider:
    """
    TODO
    """

    @staticmethod
    def get_campuses():

        campuses_filter = ['all']

        try:
            campuses_json = PolimiAPI.get_elenco_sedi()

            campuses_codes = {}
            for campus in campuses_json:
                if campus['csis'] not in campuses_filter:
                    campuses_codes[campus['csis']] = campus['desc_sede']

            return campuses_codes

        except:
            raise ConnectionError('Politecnico di Milano server seems not responding')


    @staticmethod
    def get_campus_classroom(campus):
        try:
            return PolimiAPI.get_elenco_aule(campus)
        except:
            raise ConnectionError('Politecnico di Milano server seems not responding')

    @staticmethod
    def get_classroom_details(class_id):
        try:
            return PolimiAPI.get_dettaglio_aula(class_id)
        except:
            raise ConnectionError('Politecnico di Milano server seems not responding')

