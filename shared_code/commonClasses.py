def extract_config_value(config_file, key):
    if key in config_file:
        return config_file[key]
    else:
        return ""

class Configuration:

    def __init__ (self, config_file):
        self.application_version        =           extract_config_value(config_file, "application_version")
        self.n_images                   =           extract_config_value(config_file, "n_images")
        self.n_titles                   =           extract_config_value(config_file, "n_titles")
        self.outbrain                   =           extract_config_value(config_file, "outbrain")
        self.taboola                    =           extract_config_value(config_file, "taboola")
        self.sql                        =           extract_config_value(config_file, "sql")
        self.shutterstock               =           extract_config_value(config_file, "shutterstock")
        self.pexels                     =           extract_config_value(config_file, "pexels")
        self.pixabay                    =           extract_config_value(config_file, "pixabay")
        self.google_lense               =           extract_config_value(config_file, "google_lense")
        self.openai                     =           extract_config_value(config_file, "openai")
        self.statistics                 =           extract_config_value(config_file, "statistics")

class Image:
    def __init__ (self, stock, url, stock_id):
        self.stock = stock
        self.url = url
        self.stock_id = stock_id

class Title:
    def __init__(self, description):
        self.description = description