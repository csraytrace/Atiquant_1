import inspect
import ast  # Sichere Konvertierung von Strings zu Listen/Zahlen

def call_function_with_config(funktion, einstellung):#Konfig:[a=x,b=y]
    """
    Bereitet die Argumente aus der Konfiguration vor und ruft die Funktion auf.
    """
    # Konfiguration in ein Dictionary umwandeln
    einstellung_dict = dict(item.split("=") for item in einstellung[0].split(","))

    # Dynamische Typkonvertierung basierend auf den Standardwerten
    signature = inspect.signature(funktion)
    updated_values = {}

    for key, value in einstellung_dict.items():
        # Prüfe, ob das Argument in der Signatur von `funktion` existiert
        if key in signature.parameters:
            param = signature.parameters[key]
            # Konvertiere den Wert in den Typ des Standardwertes der Funktion
            if param.default is not inspect.Parameter.empty:  # Nur wenn Standardwert existiert
                target_type = type(param.default)  # Typ des Standardwerts (z. B. float, str)

                try:
                    updated_values[key] = target_type(value)
                except ValueError:
                    updated_values[key] = value  # Fallback: Originalwert
            else:
                updated_values[key] = value  # Fallback: Originalwert
        else:
            raise ValueError(f"Ungültiges Argument: {key}")

    # Standardwerte abrufen und überschreiben
    defaults = {k: v.default for k, v in signature.parameters.items()}
    #print(defaults)
    updated_values = {**defaults, **updated_values}

    # Funktion mit den kombinierten Werten aufrufen
    return funktion(**updated_values)


def call_class_with_config_0(cls, einstellung):
    """
    Bereitet die Argumente aus der Konfiguration vor und ruft die Klasse auf.
    """
    # Konfiguration in ein Dictionary umwandeln
    einstellung_dict = dict(item.split("=") for item in einstellung[0].split(","))

    # Bereinige Schlüssel und Werte, konvertiere Typen, falls möglich
    for key, value in list(einstellung_dict.items()):
        clean_key = key.strip()  # Schlüssel bereinigen
        clean_value = value.strip()  # Wert bereinigen

        try:
            einstellung_dict[clean_key] = eval(clean_value)  # Konvertiere zu int, float, etc., wenn möglich
        except:
            einstellung_dict[clean_key] = clean_value  # Behalte String, falls Konvertierung fehlschlägt

        # Entferne den alten Schlüssel, falls er durch Leerzeichen verändert wurde
        if clean_key != key:
            del einstellung_dict[key]

    # Signatur der Klasse abrufen
    signature = inspect.signature(cls.__init__)

    # Standardwerte der Klasse extrahieren
    defaults = {k: v.default for k, v in signature.parameters.items() if k != "self"}

    # Konfigurationswerte mit Standardwerten kombinieren
    updated_values = {**defaults, **einstellung_dict}
    print(updated_values)

    # Instanziiere die Klasse mit den kombinierten Werten
    return cls(**updated_values)


def call_class_with_config(cls, einstellung):
    """
    Bereitet die Argumente aus der Konfiguration vor und ruft die Klasse auf.
    """
    # Erkennen, ob `einstellung` eine Liste ist oder direkt eine Zeichenkette
    if isinstance(einstellung, list):
        einstellung = einstellung[0]  # Hole die Zeichenkette aus der Liste

    # Konfiguration in ein Dictionary umwandeln
    einstellung_dict = {}
    for item in einstellung.split(","):
        item = item.strip()  # Entferne Leerzeichen
        if "=" in item:  # Nur valide Key-Value-Paare verarbeiten
            key, value = item.split("=", 1)  # Split einmal durchführen
            einstellung_dict[key.strip()] = value.strip()  # Bereinigte Schlüssel und Werte speichern
        else:
            raise ValueError(f"Ungültiges Argument: '{item}' in Einstellung")

    # Konvertiere Werte, falls möglich
    for key, value in einstellung_dict.items():
        try:
            einstellung_dict[key] = eval(value)  # Konvertiert zu int, float, etc., wenn möglich
        except:
            einstellung_dict[key] = value  # Behalte String, falls Konvertierung fehlschlägt

    # Standardwerte der Klasse abrufen
    signature = inspect.signature(cls.__init__)
    defaults = {k: v.default for k, v in signature.parameters.items() if k != "self"}


    # Konfigurationswerte mit Standardwerten kombinieren
    updated_values = {**defaults, **einstellung_dict}
    #updated_values.update(einstellung_dict)
    #print(updated_values)

    # Instanziiere die Klasse mit den kombinierten Werten
    return cls(**updated_values)



def call_class_with_config_2(cls, einstellung):
    """
    Bereitet die Argumente aus der Konfiguration vor und ruft die Klasse auf.
    Unterstützt Zahlen, Strings und Listen in der Konfiguration.
    """
    # Falls `einstellung` eine Liste ist, nehme das erste Element
    if isinstance(einstellung, list):
        einstellung = einstellung[0]  # Zeichenkette extrahieren

    # Falls `einstellung` als Zeichenkette übergeben wurde, versuchen wir, sie in ein Dictionary umzuwandeln
    if isinstance(einstellung, str):
        try:
            einstellung_dict = ast.literal_eval(einstellung)  # Direkt in ein dict umwandeln
        except (SyntaxError, ValueError):
            raise ValueError(f"Fehlerhafte Eingabe für `einstellung`: {einstellung}")
    elif isinstance(einstellung, dict):
        einstellung_dict = einstellung  # Falls es bereits ein Dictionary ist, benutze es direkt
    else:
        raise TypeError("`einstellung` muss eine Zeichenkette oder ein Dictionary sein.")

    # Standardwerte der Klasse abrufen
    signature = inspect.signature(cls.__init__)
    defaults = {k: v.default for k, v in signature.parameters.items() if k != "self"}

    # Konfigurationswerte mit Standardwerten kombinieren
    updated_values = {**defaults, **einstellung_dict}
    print(updated_values)  # Debug-Ausgabe

    # Instanziiere die Klasse mit den kombinierten Werten
    return cls(**updated_values)

