# tests/test_convertisseurs.py
import json
import pytest
from convertisseurs import CsvVersJson, JsonVersCsv, XmlVersCsv


class TestCsvVersJson:
    def test_convertit_ligne_simple(self):
        conv = CsvVersJson()
        entree = "nom,prix\nFleuve Noir,24.99"
        sortie = json.loads(conv.convertir(entree))
        assert sortie[0]["nom"] == "Fleuve Noir"
        assert sortie[0]["prix"] == "24.99"

    def test_csv_vide_retourne_liste_vide(self):
        conv = CsvVersJson()
        sortie = json.loads(conv.convertir("nom,prix\n"))
        assert sortie == []

    def test_plusieurs_lignes(self):
        conv = CsvVersJson()
        entree = "nom,prix\nA,1.00\nB,2.00\nC,3.00"
        sortie = json.loads(conv.convertir(entree))
        assert len(sortie) == 3


class TestAllerRetour:
    def test_csv_json_csv(self):
        """CSV → JSON → CSV doit redonner le CSV d'origine."""
        csv_original = "nom,prix\nFleuve Noir,24.99\n"
        intermediaire = CsvVersJson().convertir(csv_original)
        resultat = JsonVersCsv().convertir(intermediaire)
        assert resultat == csv_original

    @pytest.mark.parametrize("conv_aller,conv_retour,donnees", [
        (CsvVersJson(), JsonVersCsv(), "nom,prix\nA,1.00\n"),
        # Ajoutez d'autres paires ici
    ])
    def test_aller_retour_parametrise(self, conv_aller, conv_retour, donnees):
        intermediaire = conv_aller.convertir(donnees)
        resultat = conv_retour.convertir(intermediaire)
        assert resultat == donnees


class TestConfig:
    def test_incrementer_conversions(self):
        config = Config()
        config.incrementer_conversions()
        config.incrementer_conversions()
        assert config.nb_conversions() == 2

    def test_nb_conversions_demarre_a_zero(self):
        config = Config()
        assert config.nb_conversions() == 0  # ÉCHOUE — le compteur est déjà à 2
