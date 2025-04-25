# Importations des modules

import json
import os
import base64
import ctypes
from ctypes import POINTER, Structure, c_void_p, c_char, c_char_p, c_int, c_uint, c_ubyte, c_ushort, c_ulong, byref, c_bool
from datetime import datetime
import uuid
from PIL import Image
from pathlib import Path

# Définitions des fonctions
    
def enregistrerEmpreinteDigitale(filename, imageData, width, height):

    # Docstring de la fonction

    """

        --  Cette fonction permet d'enregistrer l'image d'une empreinte digitale.

        --  Arguments :

            *   filename : Représente le nom et l'extension du fichier image
            *   imageData : Représente l'image de l'empreinte digitale en Byte
            *   width : Représente la largeur de l'image de l'empreinte digitale
            *   height : Représente la hauteur de l'image de l'empreinte digitale
    
    """

    # Convertir le buffer ctypes en bytes Python

    imageBytes = bytes(imageData)

    # Créer une image Pillow à partir des données en niveaux de gris

    image = Image.frombytes('L', (width, height), imageBytes)

    # Dossier de sauvegarde (Par défaut)

    dossierSortie = "images_empreintes_digitales"

    os.makedirs(dossierSortie, exist_ok = True)

    # Construire le chemin absolu complet

    cheminAbsolu = os.path.abspath(os.path.join(dossierSortie, filename))

    # Sauvegarde de l’image

    image.save(cheminAbsolu)

    # Retourne le path au format POSIX pour JSON propre
    
    return Path(cheminAbsolu).as_posix()

def viderCache():

    # Docstring de la fonction

    """
    
        --  Cette fonction permet de supprimer le cache de Secugen.

        --  Fichier à supprimer :

            *  .sgfplib_config.ini 
        
    """

    # Suppression du fichier de configuration Secugen

    if os.path.exists(".sgfplib_config.ini"):

        os.remove(".sgfplib_config.ini")

def capturerEmpreinteDigitale():
    
    # Docstring de la fonction

    """
    
        --  Cette fonction permet de capturer une empreinte digitale avec un lecteur USB Secugen.

        --  SDK pris en charge :

            *   FDx SDK Pro for Windows v4.3.1

        --  Architecture prise en charge :

            *   x64

        --  Fichiers .dll nécessaires :

            *   sgbledev.dll
            *   sgfdusda.dll
            *   sgfdusdax64.dll
            *   sgfpamx.dll
            *   sgfplib.dll
            *   sgwsqlib.dll

    """

    # Gestion des exceptions

    try:

        # Charger le fichier .dll de Secugen

        pathFichierDll = os.path.abspath("sgfplib.dll")

        sgfplib = ctypes.WinDLL(pathFichierDll)

        # Définition des constantes Secugen

        SGFDX_ERROR_NONE = 0
        SG_DEV_AUTO = 0xFF
        USB_AUTO_DETECT = 0x3BC+1
        SG_IMPTYPE_LP = 0x00
        SG_FINGPOS_UK = 0x00

        # Définition des structures de données

        class SGDeviceInfoParam(Structure):

            _fields_ = [
                ("DeviceID", c_ulong),
                ("DeviceSN", c_char * 16),
                ("ComPort", c_ulong), 
                ("ComSpeed", c_ulong), 
                ("ImageWidth", c_ulong),
                ("ImageHeight", c_ulong),
                ("Contrast", c_ulong),
                ("Brightness", c_ulong),
                ("Gain", c_ulong),    
                ("ImageDPI", c_ulong),
                ("FWVersion", c_ulong)
            ]

        class SGFingerInfo(Structure):

            _fields_ = [
                ("FingerNumber", c_int),
                ("ImageQuality", c_int),
                ("ImpressionType", c_int),
                ("ViewNumber", c_int),
                ("Reserved", c_ubyte * 64)
            ]

        # Type personnalisé pour handle

        HSGFPM = c_void_p

        # Création d’un objet périphérique

        fpm = HSGFPM()
        res = sgfplib.SGFPM_Create(byref(fpm))

        if res != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_Create (Secugen)"}, ensure_ascii = False)

        # Initialisation

        res = sgfplib.SGFPM_Init(fpm, SG_DEV_AUTO)

        if res != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_Init (Secugen)"}, ensure_ascii = False)

        # Ouverture automatique du périphérique

        res = sgfplib.SGFPM_OpenDevice(fpm, USB_AUTO_DETECT)

        if res != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_OpenDevice (Secugen)"}, ensure_ascii = False)

        # Récupération des infos du lecteur

        device_info = SGDeviceInfoParam()

        res = sgfplib.SGFPM_GetDeviceInfo(fpm, byref(device_info))

        # Allocation mémoire pour l’image

        image_size = device_info.ImageWidth * device_info.ImageHeight
        image_buffer = (c_ubyte * image_size)()

        # Capture de l’image

        res = sgfplib.SGFPM_GetImage(fpm, image_buffer)

        if res == SGFDX_ERROR_NONE:
            
            cheminAbsoluImageEmpreinteDigitale = enregistrerEmpreinteDigitale(f"empreinte_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.png", image_buffer, device_info.ImageWidth, device_info.ImageHeight)
            
            # Récupération de la qualité

            quality = c_ulong(0)

            res = sgfplib.SGFPM_GetImageQuality(fpm, device_info.ImageWidth, device_info.ImageHeight, image_buffer, byref(quality))

        else:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_GetImage (Secugen)"}, ensure_ascii = False)

        # Luminosité

        niveauLuminosite = 70

        res = sgfplib.SGFPM_SetBrightness(fpm, niveauLuminosite)

        if res != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_SetBrightness (Secugen)"}, ensure_ascii = False)

        # Taille max du template

        taille_max_template = c_ulong()

        res = sgfplib.SGFPM_GetMaxTemplateSize(fpm, byref(taille_max_template))

        if res != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_GetMaxTemplateSize (Secugen)"}, ensure_ascii = False)

        # Extraction du template

        buffer_template = (c_ubyte * taille_max_template.value)()

        finger_info = SGFingerInfo(FingerNumber = SG_FINGPOS_UK, ImageQuality = quality.value, ImpressionType = SG_IMPTYPE_LP, ViewNumber = 0, Reserved = (c_ubyte * 64)())

        res = sgfplib.SGFPM_CreateTemplate(fpm, byref(finger_info), image_buffer, buffer_template)

        if res != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_CreateTemplate (Secugen)"}, ensure_ascii = False)

        # Encodage base64 du template
        
        template_bytes = bytes(buffer_template[:taille_max_template.value])

        template_base64 = base64.b64encode(template_bytes).decode('utf-8')

        # Libération des ressources

        sgfplib.SGFPM_CloseDevice(fpm)

        sgfplib.SGFPM_Terminate(fpm)

        viderCache()

        # Retourne les informations

        informationsEmpreinteDigitale = {
            "Identifiant_du_peripherique": device_info.DeviceID,
            "Numero_de_serie": device_info.DeviceSN.decode('utf-8'),
            "Lecteurs_USB_Port": device_info.ComPort,
            "Largeur_image": device_info.ImageWidth,
            "Hauteur_image": device_info.ImageHeight,
            "Contraste": device_info.Contrast,
            "Luminosite_parametre": device_info.Brightness,
            "Niveau_Luminosite_mesure": niveauLuminosite,
            "Gain": device_info.Gain,
            "Resolution_image_DPI": device_info.ImageDPI,
            "Version_firmware": device_info.FWVersion,
            "Qualite_image": quality.value,
            "Taille_modele": taille_max_template.value,
            "Modele_empreinte_base64": template_base64,
            "chemin_absolu_image_empreinte_digitale": cheminAbsoluImageEmpreinteDigitale,
        }

        return json.dumps(informationsEmpreinteDigitale, ensure_ascii = False)

    except Exception as exception:

        # Vider le cache

        viderCache()

        # Retourne l'exception en JSON

        return json.dumps({"erreur": str(exception)}, ensure_ascii = False)

def comparaisonEmpreintesDigitales(premierEmpreinteDigitaleBase64, deuxiemeEmpreinteDigitaleBase64, niveauDeSecurite = "NORMAL"):

    # Docstring de la fonction

    """

        --  Cette fonction permet de comparer deux empreintes digitales à travers les données en base64.

        --  SDK pris en charge :

            *   FDx SDK Pro for Windows v4.3.1

        --  Architecture prise en charge :

            *   x64

        --  Fichiers .dll nécessaires :

            *   sgbledev.dll
            *   sgfdusda.dll
            *   sgfdusdax64.dll
            *   sgfpamx.dll
            *   sgfplib.dll
            *   sgwsqlib.dll

    """

    niveauxDeSecurite = {
        "NONE": 0,
        "LOWEST": 1,
        "LOWER": 2,
        "LOW": 3,
        "BELOW_NORMAL": 4,
        "NORMAL": 5,
        "ABOVE_NORMAL": 6,
        "HIGH": 7,
        "HIGHER": 8,
        "HIGHEST": 9
    }

    # Vérification des modèles d'empreintes digitales

    if not premierEmpreinteDigitaleBase64 or not deuxiemeEmpreinteDigitaleBase64:

        # Retourne une reponse en JSON

        return json.dumps({"message": "Une ou les deux empreintes sont vides ou nulles"}, ensure_ascii = False)

    # Vérification du niveau de sécurité

    niveauDeSecurite = niveauDeSecurite.strip().upper()

    if not niveauDeSecurite in niveauxDeSecurite:

        # Retourne une reponse en JSON

        return json.dumps({"message": "Le niveau de sécurité est invalide."}, ensure_ascii = False)

    # Gestion des exceptions

    try:

        # Charger le fichier .dll de Secugen

        pathFichierDll = os.path.abspath("sgfplib.dll")

        sgfplib = ctypes.WinDLL(pathFichierDll)

        # Définition des constantes Secugen

        SGFDX_ERROR_NONE = 0
        SG_DEV_AUTO = 0xFF
        LEVEL = niveauxDeSecurite[niveauDeSecurite]

        # Handle du lecteur

        HSGFPM = c_void_p

        fpm = HSGFPM()

        # Initialisation

        if sgfplib.SGFPM_Create(byref(fpm)) != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_Create (Secugen)"}, ensure_ascii = False)

        if sgfplib.SGFPM_Init(fpm, SG_DEV_AUTO) != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_Init (Secugen)"}, ensure_ascii = False)

        # Décodage des modèles base64 vers buffer ctypes

        premierEmpreinteDigitaleByte = base64.b64decode(premierEmpreinteDigitaleBase64)
        deuxiemeEmpreinteDigitaleByte = base64.b64decode(deuxiemeEmpreinteDigitaleBase64)

        premierEmpreinteDigitaleBuffer = (c_ubyte * len(premierEmpreinteDigitaleByte))(*premierEmpreinteDigitaleByte)
        deuxiemeEmpreinteDigitaleBuffer = (c_ubyte * len(deuxiemeEmpreinteDigitaleByte))(*deuxiemeEmpreinteDigitaleByte)

        # Préparation des résultats

        matched = c_bool(False)
        score = c_ulong(0)

        # Comparaison des empreintes

        if sgfplib.SGFPM_MatchTemplate(fpm, premierEmpreinteDigitaleBuffer, deuxiemeEmpreinteDigitaleBuffer, LEVEL, byref(matched))  != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_MatchTemplate (Secugen)"}, ensure_ascii = False)

        if sgfplib.SGFPM_GetMatchingScore(fpm, premierEmpreinteDigitaleBuffer, deuxiemeEmpreinteDigitaleBuffer, byref(score))  != SGFDX_ERROR_NONE:

            # Vider le cache

            viderCache()

            # Retourne une reponse en JSON

            return json.dumps({"message": "Erreur SGFPM_GetMatchingScore (Secugen)"}, ensure_ascii = False)

        # Libération des ressources

        sgfplib.SGFPM_Terminate(fpm)

        viderCache()

        # Retourne les informations de comparaison

        informationsDeComparaison = {
            "NiveauSecurite": LEVEL,
            "Score": score.value,
            "ValidationEmpreintesIdentiques": matched.value
        }

        return json.dumps(informationsDeComparaison, ensure_ascii = False)
    
    except Exception as exception:

        # Vider le cache

        viderCache()

        # Retourne l'exception en JSON

        return json.dumps({"erreur": str(exception)}, ensure_ascii = False)
    