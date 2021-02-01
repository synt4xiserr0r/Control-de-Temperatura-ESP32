"""
///////////////////////////////////////////////////////////////////////////////
//Nombre del programa: Control temperatura                                   //
//Resumen del programa:                                                      //
//Este programa funciona como un control de temperatura con un termistor PTC //
//Y un led RGB que nos dira si la temperatura es alta, baja o "ambiente"     //    
//Tabla de pines                                                             //
//Red = caliente    Pin(18)                                                  //
//Blue = frio   Pin(14)                                                      //
//Green = ambiente  Pin(33)                                                  //
//adc = valor del PTC Pin(32)                                                //
///////////////////////////////////////////////////////////////////////////////
"""
# Librerias
import machine as ma
import time
from math import log

# Declaracion de variables

Pins = [18, 14, 33]       # Pines que seran utilizados
leds = []                 # Array donde se guardara los pines inicialzados 
Vcc = 3.3                 # Voltaje de referencia (Vref)
Error = 0                 # Error agregado por el ADC en el esp32 no hay error
Rserie = 10000            # Valor de la resintecia en serie con el termistor
frio = 15                 # Valor de referencia para frio
caliente = 27             # Valor de referencia para caliente

# Inicializacion de Pines  
for i in Pins:
  leds.append(ma.Pin(i, ma.Pin.OUT)) # Inicializamos los pines de la matriz Pins como salida
  
adc = ma.ADC(ma.Pin(32)) # Pin del ADC
adc.atten(ma.ADC.ATTN_11DB)   # amplifica el rango de voltaje de 0 a 3.6


# Definicion de funciones
def apagar_todo():
  leds[0].off()
  leds[1].off()
  leds[2].off()
  
def error():
  leds[0].on()
  leds[1].on()
  leds[2].on()
  print("ADC = 0, revise las conexiones")
  time.sleep(3)

def obtener_temperatura():

  adc_value = adc.read()
  while adc_value !=0:
    V = 1/(4095/(Vcc*adc_value))-Error  # Obtencion del voltaje medido por el adc, este voltaje es el del termistor
    Vr = Vcc - V # Voltaje de la resistencia
    R = ((Rserie*Vcc)/Vr)-Rserie # Obtenemos la resistencia del termistor en base a un divisor de voltaje
    logR = log(R)			# logaritmo de R
    R_th = 1 / (0.0011407594231661565 + 0.00023881194449697142 * logR + 1.755718253617776e-8 * logR * logR * logR)
    # Obtencion de la temperatura en K
    celsius = R_th -273.15 # pasamos el voltaje a Celsius
    return celsius
    
  if adc_value == 0:
    error()
  
while True:
  t = obtener_temperatura()
  print(t)
  time.sleep_ms(500)
  
  if t >= caliente:
    apagar_todo()
    leds[0].on()
    print("La temperatura es caliente")
    time.sleep_ms(500)
    
  elif t <= frio:
    apagar_todo()
    leds[1].on()
    print("La temperatura es fria")
    time.sleep_ms(500)
    
  elif t <= caliente and t >= frio:
    apagar_todo()
    leds[2].on()
    print("La temperatura es ideal")
    time.sleep_ms(500)
    
  
  




