import configparser

config_file = configparser.ConfigParser()

def set_config():
    # TLS versies
    config_file.add_section('TLS')
    config_file.set("TLS", "versie", "TLSv1.0\n"
    "TLSv1.1\n"
    "TLSv1.2\n"
    "TLSv1.3\n")
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

    # Te scannen websites
    config_file.add_section("Websites")

    # moet altijd '1', 'yes', 'true', of 'on' zijn!
    config_file.add_section("Export data")
    config_file.set("Export data", "boolean", "True")

    with open(r"ncsc_configs.ini", "w") as configFileObj:
        config_file.write(configFileObj)
        configFileObj.flush()
        configFileObj.close()
        # print("Config file 'ncsc_configs' created")

# print(config_file.get('Cipher Suites', 'goed'))

def read_config(section, key):
    config_file.read(r'ncsc_configs.ini')
    section = config_file.get(section, key)
    return section


def get_boolean(section, key):
    config_file.read(r'ncsc_configs.ini')
    boolean = config_file.getboolean("Export data", option='boolean')
    return boolean


def readConfig(section, key):
    read_file = open(r"ncsc_configs.ini", "r")
    configs = read_file.read()
    return configs
