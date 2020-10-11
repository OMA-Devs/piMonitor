# piMonitor
Controlador de temperatura diseñado para RPI. Funciona con cualquier versión.
El propósito de este controlador es añadir una función PWM a ventiladores que no la poseen, como los ventiladores de 35-40mm 5v que incluyen muchas carcasas comerciales de RPI4.

El hardware consiste en un circuito básico con un transistor 2n2222, una resistencia de 1kohm y un diodo de protección 1n4001 en configuración flyback para evitar que posibles corrientes inversas dañen el transistor. El script es utilizable con cualquier otro hardware que acepte señal PWM 3.3v.

## A tener en cuenta
La frecuencia del pwm puede ser modificada directamente en el archivo SpeedController al inicializar el controlador de velocidad. Los ventiladores para los que está diseñado este script son poco versátiles y una alta frecuencia de switching puede generar ruido audible y llegar a ser más molesta que el ventilador constantemente al 100%. Se ha determinado una frecuencia baja para evitar ese sonido, pero puede ser modificada a conveniencia y necesidad del hardware.

## Pin de control
El pin de control está hardcodeado en el numero 12. Puede ser cambiado en el código fuente del archivo PiMonitor.py durante la inicialización del controlador de velocidad.

## Logs
El programa utiliza el modulo logging para almacenar los datos y la información. Por defecto, el nivel de log es "WARNING", pero puede ser cambiado a "INFO" tanto para los avisos de GUI en PiMonitor.py como para los avisos específicos del controlador de velocidad en SpeedController.py.

Utilizar y limpiar con prudencia. Si se establece el nivel de log como "INFO", se va a guardar mucha información.
