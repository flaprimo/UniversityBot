from datetime import datetime
from universitybot.calls.calls_manager import call


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
        url = PolimiAPI.base_url + 'elencoAule/{}'.format(sede)

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
        url = PolimiAPI.base_url + 'dettaglioAula/{}'.format(id_aula)

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
        url = PolimiAPI.base_url + 'contatti/{}'.format(id_persona)

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

        payload = 'soloAuleLibere={}&dalleAulaLibera={}&alleAulaLibera={}&dataAulaLibera={}' \
            .format('S', start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), date.strftime('%d/%m/%Y'))

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
        url = PolimiAPI.base_url + 'elencoServiziShell/{}'.format(matricola)

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
        url = PolimiAPI.base_url + 'docente/{}/foto/'.format(id_persona)

        return call(url)
