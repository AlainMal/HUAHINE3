from Package.CAN_dll import CanMsg

# ======================================================================================================================
# Cette classe sert uniquement à traiter les résultats en temps réel.
# Ces méthodes sont synchrones, car on ne peut pas extraire tous en mode asynchrone
# ======================================================================================================================
class TempsReel:
    def __init__(self):
        pass

    # Méthode du temps réel sur bus CAN. --------------------------------------------------------------------------------
    @staticmethod
    def TempsReel(msg:CanMsg, file_path, coche_file, coche_buffer,coche_nmea, main_window):
        # Initialise datas comme un str vide.
        # datas = ""
        # On a défini les huit octets dans "datas".
        # for i in range(msg.len):
            # On commence par un espace, car ça fini par le dernier octet.
        #    datas += " " + format(msg.data[i], "02X")

        if msg:
            # On met le résultat dans un fichier si la case à cocher est validée.
            if coche_file:
                with open(file_path, "a") as file:
                    # Formatage des données en hexadécimal, max 8 octets
                    datas = ' '.join([f"{byte:02X}" for byte in msg.data[:8]])  # Sécurité : max 8 octets
                    # Écriture : timestamp, ID sur 8 caractères hex, longueur sur 2 caractères hex, données
                    file.write(f"{msg.TimeStamp} {msg.ID:08X} {msg.len:01X} {datas}\n")

            # On met le résultat dans la table si la case à cocher est validée
            # Cette opération n'est pas utile, À SUPPRIMER.
            if coche_buffer:
                # Préparation d'un tuple pour la table
                tuple_modifie = (
                    format(msg.ID,'08X'),  # Identifiant CAN sur huit caractères en hexadécimale.
                    str(msg.len),  # Longueur des données sur un caractère.
                    ' '.join(f"{byte:02X}" for byte in msg.data)  # Données formatées (hexadécimal)
                )
                # On met le tuple modifié dans la table en buffer tournant.
                main_window.add_to_buffer(tuple_modifie)

            # *************** EMPLACEMENT PRÉVU POUR METTRE LE TEMPS REEL *********************
            #                             NMEA 2000
            #                       Affichage des jauges
            #                       Affichage des MMSI
            #                       Affichage des positions sur la carte
            #                       Affichage des instruments sur NMEA 2000
            # *********************************************************************************

            # On appelle la routine "octets" si la case à cocher est activée pour NMEA 2000 en temps réel.
            if coche_nmea:
                # Récupère le pgn.
                pgn =  main_window.nmea_2000.pgn( msg.ID)
                # Récupère la source.
                source = main_window.nmea_2000.source(msg.ID)
                # Appelle la fonction "octets" dans "NMEA_2000.py"
                main_window.nmea_2000.octets(pgn, source, msg.data) # Ce qui est fait dans "octets".
            # =================================================================================
