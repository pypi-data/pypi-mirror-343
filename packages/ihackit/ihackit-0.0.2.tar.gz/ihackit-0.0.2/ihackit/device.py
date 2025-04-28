import random
from .constant import (
    DEVICE,
    DEVICE_LIST,
    COUNTRY,
    COUNTRY_LIST
)

class Device:
    
    def __init__(self, device_brand: str = None, device_model: str = None, device_country: str = None, device_operator: str = None, **kwargs):
        self.device_brand = device_brand
        self.device_model = device_model
        self.device_country = device_country
        self.device_operator = device_operator
        self.kwargs = kwargs
        
    def device_dpi(self):
        return random.choice(['480dpi; 1080x2400','480dpi; 720x1600','480dpi; 720x1560','480dpi; 1080x2376','480dpi; 1080x2404','480dpi; 1080x2408','320dpi; 1080x2340','560dpi; 1440x3040','560dpi; 1440x3088','560dpi; 1080x2400','320dpi; 1600x2560','320dpi; 720x1568','560dpi; 1440x2560','480dpi; 1344x2772'])
    
    def device_build(self):
        return '{}.{}'.format(random.choice(['SP1A','QP1A','RP1A','TP1A','RKQ1','SKQ1']), str(random.randint(200999,220905)) + '.0{}'.format(random.choice(['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16'])))
    
    def device_armeabi(self):
        return random.choice(['arm64-v8a','armeabi-v8a:armeabi','armeabi-v7a:armeabi','x86_64:x86:x86_64','x86_64:arm64-v8a:x86_64'])
    
    def device_density(self):
        return random.choice(['{density=3.0,width=1080,height=2068}','{density=3.0,width=1080,height=1920}','{density=2.3,width=2149,height=1117}','{density=1.0,width=2060,height=1078}','{density=1.8,width=1582,height=558}','{density=3.0,width=1080,height=1920}','{density=2.0,width=720,height=1193}','{density=2.1,width=1814,height=1023}'])
    
    def info(self):
        if self.device_brand and self.device_brand.upper() in DEVICE_LIST:
            if self.device_model:
                device_data = next((d for d in DEVICE[self.device_brand.upper()] if d['device_model'] == self.device_model), None)
                if not device_data: device_data = random.choice(DEVICE[self.device_brand.upper()])
            else: device_data = random.choice(DEVICE[self.device_brand.upper()])
        else:
            self.device_brand = random.choice(DEVICE_LIST)
            device_data = random.choice(DEVICE[self.device_brand.upper()])
        if not self.device_country and self.device_country not in COUNTRY_LIST: self.device_country = random.choice(COUNTRY_LIST)
        country_data = COUNTRY[self.device_country.upper()]
        if not self.device_operator: self.device_operator = random.choice(COUNTRY[self.device_country]['operator'])
        return {
            'device_brand': self.device_brand.capitalize() if len(self.device_brand) > 3 else self.device_brand,
            'device_model': device_data['device_model'],
            'device_board': device_data['device_board'],
            'device_build': self.device_build(),
            'device_vendor': device_data['device_vendor'],
            'device_version': device_data['device_version'],
            'device_armeabi': self.device_armeabi(),
            'device_density': self.device_density(),
            'device_dpi': self.device_dpi(),
            'device_sdk': str(19 + int(device_data['device_version'])),
            'device_number': country_data['number'],
            'device_country': self.device_country,
            'device_language': country_data['language'],
            'device_operator': self.device_operator
        }