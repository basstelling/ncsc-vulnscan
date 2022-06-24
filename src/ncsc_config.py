import configparser


config_file = configparser.ConfigParser()

def set_config():
    # TLS versies
    config_file.add_section('TLS')
    config_file.set("TLS", "Goed", "TLSv1.3")
    config_file.set("TLS", "Voldoende", "TLSv1.2")
    config_file.set("TLS", "Uit te faseren", "TLSv1.1")
    config_file.set("TLS", "Onvoldoende", 
    "SSL3.0\n"
    "SSL2.0\n"
    "SSL1.0\n")
    # Cipher Suites
    config_file.add_section("Cipher Suites")
    config_file.set("Cipher Suites", "goed",
    "TLS_AES_256_GCM_SHA384\n"
    "TLS_CHACHA20_POLY1305_SHA256\n"
    "TLS_AES_128_GCM_SHA256")
    config_file.set("Cipher Suites", "voldoende",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\n"
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\n"
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\n"
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\n"
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\n"
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\n"
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384\n"
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA\n"
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256\n"
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA\n"
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384\n"
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\n"
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256\n"
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\n"
    "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384\n"
    "TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256\n"
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256\n"
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256\n"
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA\n"
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256\n"
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA")
    config_file.set("Cipher Suites", "Uit te faseren",
    "TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA\n"
    "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA\n"
    "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA\n"
    "TLS_RSA_WITH_AES_256_GCM_SHA384\n"
    "TLS_RSA_WITH_AES_128_GCM_SHA256\n"
    "TLS_RSA_WITH_AES_256_CBC_SHA256\n"
    "TLS_RSA_WITH_AES_256_CBC_SHA\n"
    "TLS_RSA_WITH_AES_128_CBC_SHA256\n"
    "TLS_RSA_WITH_AES_128_CBC_SHA\n"
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA")

    # Te scannen websites -- momenteel niet in gebruik
    config_file.add_section("Te scannen websites")
    config_file.set("Te scannen websites", "websites", "https://www.nu.nl")

    # moet altijd '1', 'yes', 'true', of 'on' zijn om data op te slaan!
    config_file.add_section("Export data")
    config_file.set("Export data", "boolean", "True")

    # config file aanmaken en webschrijven naar bestand
    with open(r"ncsc_configs.ini", "w") as configFileObj:
        config_file.write(configFileObj)
        configFileObj.flush()

# functie om data op te halen uit de config
def read_config(section, key):
    config_file.read(r'ncsc_configs.ini')
    section = config_file.get(section, key)
    return section

# aparte functie om booleans op te halen zodat het degelijk als boolean gereturned wordt ipv string
def get_boolean(section):
    config_file.read(r'ncsc_configs.ini')
    boolean = config_file.getboolean(section, option='boolean')
    return boolean

# set_config()
# print(read_config("Export data", "boolean"))