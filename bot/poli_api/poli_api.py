import logging
import time

import requests
import requests_cache

logger = logging.getLogger(__name__)
requests_cache.install_cache(cache_name='cache/cache', backend='sqlite', expire_after=2.628e+6)


class PolimiAPI:
    """
    Provides Politecnico di Milano APIs

    API summary (of working apis):
    * get_elenco_aule(sede)
      Returns a list of the classrooms from a location (sede) in Politecnico di Milano.
      returns: [{"id_aula": int, "sigla": str, "categoria": str, "dove": str, "aula_studio": char}, [...]]

    * get_ricerca_rubrica()
      Returns a list of the staff of Politecnico di Milano.
      returns: [{"id_persona": int, "n_persona": str},[...]]

    * get_dettaglio_aula(id_aula)
      Returns the details of a classrooms in Politecnico di Milano.
      returns: [{"id_aula": int, "sigla": str, "categoria": str, "dove": str}]

    * get_contatti(id_persona)
      Returns the details of a person staff in Politecnico di Milano.
      returns: [{"id_persona": int, "n_persona": str, "mail": str, "lista_telefono_ufficio": [str]}]

    * get_elenco_sedi()
      Returns a list of the locations (sede) in Politecnico di Milano.
      returns: [{"cod_sede": str, "desc_sede": str, "nome": str, "csis": str, "lat": str, "lng": str}, [...]]

    * get_elenco_aule_libere(sede, date, start_time, end_time)
      Returns a list of the free classrooms in Politecnico di Milano given constraints.
      return: [{"id_aula": int, "sigla": str, "categoria": str, "dove": str, "aula_studio": char}, [...]]

    """

    base_url = 'https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/'

    @staticmethod
    def get_elenco_aule(sede):
        """
        Returns a list of the classrooms from a location (sede) in Politecnico di Milano.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/elencoAule/{sede}

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
        url = PolimiAPI.base_url + 'elencoAule/%s' % sede

        return call(url)

    @staticmethod
    def get_ricerca_rubrica():
        """
        Returns a list of the staff of Politecnico di Milano.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/ricerca_rubrica/

        Returns
        -------
        dict
            staff of Politecnico di Milano

        Examples
        --------
        Excerpt of a returned JSON:
        [
            {
                "id_persona": 252772,
                "n_persona": "Abate Stefano Cesare Cornelio"
            },
            {
                "id_persona": 252797,
                "n_persona": "Abba' Antonella"
            },
            [...]
        ]

        """
        url = PolimiAPI.base_url + 'ricerca_rubrica/'

        return call(url)

    @staticmethod
    def get_dettaglio_aula(id_aula):
        """
        Returns the details of a classrooms in Politecnico di Milano.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/dettaglioAula/{id_aula}

        Parameters
        ----------
        id_aula : str
            classroom id of Politecnico di Milano.
            accepted strings can be taken from get_elenco_aule(sede)

        Returns
        -------
        dict
            details about a classroom in Politecnico di Milano

        Examples
        --------
        Excerpt of a returned JSON:
        [
            {
              "id_aula": 1,
              "sigla": "A.1.1",
              "categoria": "TEACHING ROOM",
              "dove": "Milano Citt\u00e0 Studi"
            }
        ]

        """
        url = PolimiAPI.base_url + 'dettaglioAula/%s' % id_aula

        return call(url)

    @staticmethod
    def get_contatti(id_persona):
        """
        Returns the details of a person staff in Politecnico di Milano.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/contatti/{id_persona}

        Parameters
        ----------
        id_persona : str
            person staff id of Politecnico di Milano.
            accepted strings can be taken from get_ricerca_rubrica()

        Returns
        -------
        dict
            details about a person staff in Politecnico di Milano

        Examples
        --------
        Excerpt of a returned JSON:
        [
          {
            "id_persona": 2612,
            "n_persona": "Tiano Katia",
            "mail": "katia.tiano@polimi.it",
            "lista_telefono_ufficio": [
              "6094"
            ]
          }
        ]

        """
        url = PolimiAPI.base_url + 'contatti/%s' % id_persona

        return call(url)

    @staticmethod
    def get_elenco_sedi():
        """
        Returns a list of the locations (sede) in Politecnico di Milano.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/elencoSedi/

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

        return call(url)

    @staticmethod
    def get_elenco_aule_libere(sede, date, start_time, end_time):
        """
        Returns a list of the free classrooms in Politecnico di Milano given constraints.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/elencoAule/{sede}?
            soloAuleLibere=S&dalleAulaLibera={hh:mm}&alleAulaLibera={hh:mm}&dataAulaLibera={dd/mm/yyyy}

        Parameters
        ----------
        sede : str
            location (sede) of Politecnico di Milano.
            accepted strings are: 'All', 'COE' Como, 'CRG' Cremona, 'LCF' Lecco, 'MNI' Mantova, 'MIB' Milano Bovisa,
            'MIA' Milano Leonardo, 'PCL' Piacenza
        date : # TODO add type
            the day to search for free classrooms
        start_time : # TODO add type
            the start time to search for free classrooms
        end_time : # TODO add type
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
        url = PolimiAPI.base_url + 'elencoAule/%s' % sede

        payload = {'soloAuleLibere': 'S',
                   'dalleAulaLibera': start_time.isoformat(timespec='minutes'),
                   'alleAulaLibera': end_time.isoformat(timespec='minutes'),
                   'dataAulaLibera': time.strftime('%d/%m/%Y', date.timetuple())}

        return call(url, payload)

    @staticmethod
    def get_elenco_servizi_shell(matricola):
        """
        Not working.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/elencoServiziShell/{matricola}

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
        url = PolimiAPI.base_url + 'elencoServiziShell/%s' % matricola

        return call(url)

    @staticmethod
    def get_docente(id_persona):
        """
        Not working. Returns the photo of a person staff in Politecnico di Milano.
        GET: https://m.servizionline.polimi.it/info-didattica/rest/polimimobile/docente/{id_persona}/foto/

        Parameters
        ----------
        id_persona : str
            person staff id of Politecnico di Milano.
            accepted strings can be taken from get_ricerca_rubrica()

        Returns
        -------
        dict
            unknown

        """
        url = PolimiAPI.base_url + 'docente/%s/foto/' % id_persona

        return call(url)

    @staticmethod
    def get_photo(name, url):
        """
        Downloads a photo from the given url, despite not beign an official polimi api it's used to download polimi
        photo

        :param name: str
            name of the file
        :param url: str
            url pointing to the photo
        :return:
        """
        local_filename = 'cache/' + str(name) + '.png'
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return local_filename


def call(url, payload=None):
    logger.debug('Handle API call for: %s' % url)
    logger.debug('Payload: %s' % payload)

    r = requests.get(url, params=payload)

    logger.debug('From cache: %s' % r.from_cache)
    logger.debug('Response code: %s' % r.status_code)

    return r.json()
