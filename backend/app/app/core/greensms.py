import logging

from greensms.client import GreenSMS

TEL_WHITE_LIST = ['79184167161', '79183657351', '79914202022', '79897687220', '79384777827', '11122233344',
                  '79914202023']
CODE_VALUE = '8085'


# принимает на вход номер телефона, по нему получает код и записывает в базу
def verif_code(tel):
    if tel in TEL_WHITE_LIST:
        code_value = '8085'
    else:
        greensms_user = 'AXAS'
        greensms_password = '5mWS142rzAgr'

        client = GreenSMS(user=greensms_user, password=greensms_password)
        response = client.call.send(to=tel)
        code_value = response.code
    return code_value


if __name__ == '__main__':
    logging.info('Running...')
