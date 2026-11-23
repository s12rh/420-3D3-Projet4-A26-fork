import os
import sqlite3

class Config:
    """Configuration de l'application TransFormateur."""

    CONVERSIONS_DISPONIBLES = [
        ("csv", "json"),
        ("json", "csv"),
        ("csv", "xml"),
        ("xml", "csv"),
        ("json", "xml"),
        ("xml", "json"),
        ("md", "html"),
    ]
    
    FORMATS_SUPPORTES = ["csv", "json", "xml", "md"]


    def __init__(self):
        self.dossier_upload = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(self.dossier_upload, exist_ok=True)
        self.connexion = sqlite3.connect("stats.db", check_same_thread=False)
        self._initialiser_tables()
        self._charger_config()

    def _initialiser_tables(self):
        self.connexion.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                cle TEXT PRIMARY KEY,
                valeur INTEGER DEFAULT 0
            )
        """)
        self.connexion.execute("""
            INSERT OR IGNORE INTO stats (cle, valeur) VALUES ('nb_conversions', 0)
        """)
        self.connexion.execute("""
            CREATE TABLE IF NOT EXISTS config (
                cle TEXT PRIMARY KEY,
                valeur TEXT
            )
        """)
        self.connexion.execute("""
            INSERT OR IGNORE INTO config (cle, valeur) VALUES ('taille_max_octets', '2097152')
        """)
        self.connexion.execute("""
            INSERT OR IGNORE INTO config (cle, valeur) VALUES ('formats_supportes', 'csv,json,xml,md')
        """)
        self.connexion.commit()

    def _charger_config(self):
        """Lit les valeurs depuis la BD et les met dans des attributs d'instance."""
        curseur = self.connexion.execute("SELECT cle, valeur FROM config")
        valeurs = dict(curseur.fetchall())
        self.taille_max_octets = int(valeurs.get("taille_max_octets", 2 * 1024 * 1024))
        self.formats_supportes = valeurs.get("formats_supportes", "csv,json,xml,md").split(",")

    def recharger(self):
        """Relit la configuration depuis la BD."""
        self._charger_config()

    def mettre_a_jour(self, valeurs: dict) -> None:
        """Met à jour des valeurs dans la BD et recharge."""
        for cle, valeur in valeurs.items():
            if cle == "formats_supportes" and isinstance(valeur, list):
                valeur = ",".join(valeur)
            self.connexion.execute(
                "UPDATE config SET valeur = ? WHERE cle = ?",
                (str(valeur), cle)
            )
        self.connexion.commit()
        self._charger_config()

    def incrementer_conversions(self):
        self.connexion.execute(
            "UPDATE stats SET valeur = valeur + 1 WHERE cle = 'nb_conversions'"
        )
        self.connexion.commit()

    def nb_conversions(self) -> int:
        curseur = self.connexion.execute(
            "SELECT valeur FROM stats WHERE cle = 'nb_conversions'"
        )
        return curseur.fetchone()[0]