#import time
#import pyotp
from pyotp import TOTP

#print(pyotp.random_base32())
chave_mestre = "NFZ2MLGB2BASVIQQYGZJNCODOEP5Q4Q6"
gerar_codigo=TOTP(chave_mestre)
gerar_codigo.interval=120
#print(gerar_codigo.now())

#time.sleep(15)

