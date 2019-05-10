from requests import get
from geolite2 import geolite2
import logging


#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)




def main():
    ip = get('https://api.ipify.org').text
    get_ip_info = geolite2.reader()
    ip_data = get_ip_info.get(ip)

    if ip_data is not None:
        print('My public IP address is: {}'.format(ip))
        print(ip_data['city']['names']['en'])
        print(ip_data['continent']['names']['en'])
        print(ip_data['country']['names']['en'])
        print(ip_data['registered_country']['names']['en'])
        print(ip_data['registered_country']['names']['en'])
        print(ip_data['subdivisions'][0]['names']['en'])
    else:
        logging.info('Could not get geoip info for {}'.format(ip))

if __name__ == '__main__':
    main()
