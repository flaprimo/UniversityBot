from datetime import datetime
import requests
import json

'''
Polimi TODO APIs:

* https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/ricerca_rubrica/
* https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/dettaglioAula/{id_aula}
* https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/contatti/{id_persona}
* https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/docente/{id_persona}/foto/
'''


class PolimiAPI:
    """
    Provide Politecnico di Milano APIs
    """

    base_url = 'https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/'

    @staticmethod
    def _get_response(url, *payload):

        if len(payload) > 0:
            response = requests.get(url=url, params=payload[0])
        else:
            response = requests.get(url=url)

        if response.ok:
            return json.loads(response.text)
        else:
            response.raise_for_status()

    @staticmethod
    def get_elenco_servizi_shell(matricola):
        """
        Not working.

        Parameters
        ----------
        matricola : str
            matricola of a person.

        Returns
        -------
        dict
            unknown

        Examples
        --------
        Excerpt of a returned JSON:
        [
           {
              "id_servizio":1,
              "nome_servizio":"Contacts",
              "badge":0
           },
           {
              "id_servizio":2,
              "nome_servizio":"Search Rooms",
              "badge":0
           },
           {
              "id_servizio":5,
              "nome_servizio":"Registrar's Office Queue",
              "badge":0
           }
        ]

        """
        url = PolimiAPI.base_url + 'elencoServiziShell/{}'.format(matricola)

        return PolimiAPI._get_response(url)

    @staticmethod
    def get_elenco_aule(sede):
        """
        Returns a list of the classrooms from a location (sede) in Politecnico di Milano.

        Parameters
        ----------
        sede : str
            location (sede) of Politecnico di Milano.
            accepted strings are: 'All', 'COE' Como, 'CRG' Cremona, 'LCF' Lecco, 'MNI' Mantova, 'MIB' Milano Bovisa,
            'MIA' Milano Leonardo, 'PCL' Piacenza

        Returns
        -------
        dict
            classrooms from specified location (sede) of Politecnico di Milano

        Examples
        --------
        Excerpt of a returned JSON:
        [
           {
              "id_aula":2216,
              "sigla":"AULA DIPARTIMENTALE",
              "categoria":"DEPARTMENTAL CLASSROOM",
              "dove":"Milano Città Studi, Piazza Leonardo da Vinci 32",
              "aula_studio":"N"
           },
           {
              "id_aula":2230,
              "sigla":"AULA DIPARTIMENTALE NATTA",
              "categoria":"DEPARTMENTAL CLASSROOM",
              "dove":"Milano Città Studi, Piazza Leonardo da Vinci 32",
              "aula_studio":"N"
           },
           [...]
        ]

        """
        url = PolimiAPI.base_url + 'elencoAule/{}'.format(sede)

        return PolimiAPI._get_response(url)

    @staticmethod
    def get_elenco_sedi():
        """
        Returns a list of the locations (sede) in Politecnico di Milano.

        Returns
        -------
        dict
            All locations (sede) of Politecnico di Milano

        Examples
        --------
        Excerpt of a returned JSON:
        [
           {
              "cod_sede":"all",
              "desc_sede":"All",
              "nome":"All",
              "csis":"all"
           },
           {
              "cod_sede":"CO",
              "desc_sede":"COMO",
              "nome":"Como",
              "csis":"COE",
              "lat":45.8051101937,
              "lng":9.09208289835
           },
           [...]
        ]

        """
        url = PolimiAPI.base_url + 'elencoSedi/'

        return PolimiAPI._get_response(url)

    @staticmethod
    def get_elenco_aule_libere(sede, date, start_time, end_time):
        """
        Returns a list of the free classrooms in Politecnico di Milano given constraints.

        Parameters
        ----------
        sede : str
            location (sede) of Politecnico di Milano.
            accepted strings are: 'All', 'COE' Como, 'CRG' Cremona, 'LCF' Lecco, 'MNI' Mantova, 'MIB' Milano Bovisa,
            'MIA' Milano Leonardo, 'PCL' Piacenza
        date : datetime
            the day to search for free classrooms
        start_time : datetime
            the start time to search for free classrooms
        end_time : datetime
            the end time to search for free classrooms
        Returns
        -------
        dict
            Free classrooms of Politecnico di Milano

        Examples
        --------
        Excerpt of a returned JSON:
        [
           {
              "id_aula":2216,
              "sigla":"AULA DIPARTIMENTALE",
              "categoria":"DEPARTMENTAL CLASSROOM",
              "dove":"Milano Città Studi, Piazza Leonardo da Vinci 32",
              "aula_studio":"N"
           },
           {
              "id_aula":2230,
              "sigla":"AULA DIPARTIMENTALE NATTA",
              "categoria":"DEPARTMENTAL CLASSROOM",
              "dove":"Milano Città Studi, Piazza Leonardo da Vinci 32",
              "aula_studio":"N"
           },
           [...]
        ]
        """
        url = PolimiAPI.base_url + 'elencoAule/{}'.format(sede)

        payload = 'soloAuleLibere={}&dalleAulaLibera={}&alleAulaLibera={}&dataAulaLibera={}'\
            .format('S', start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), date.strftime('%d/%m/%Y'))

        return PolimiAPI._get_response(url, payload)
