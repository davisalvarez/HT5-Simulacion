import simpy
import random
RANDOM_SEED = 35

procesos = 200
intervalo = 5.0
tiempoProcesos=[]
def constructor(env,procesos,intervalo, cpu):
    for i in range(procesos):
        tiempoTotal=12.0
        t = random.expovariate(1.0 / intervalo)
        cantidadRam = random.randint(1,10)
        env.process(ram(env, 'proceso %d' % i, cpu, cantidadRam, tiempoTotal))
        yield env.timeout(t)
        
def ram(env,nombre,cpu,cantidadRam,tiempoTotal):
    tiempollegada= env.now
    print('%7.4f %s: llega' %(tiempollegada,nombre))
    with cpu.request() as req:
            yield req
    tiempoEsperado= env.now-tiempollegada
    print('%7.4f %s: ha esperado:%6.3f' %(env.now,nombre, tiempoEsperado))
    with cpu.request() as req:
        containerRam.get(cantidadRam)
        results = yield req 
        print('%7.4f %s: Esparado por: %6.3f' % (env.now,nombre, tiempoEsperado))
        tiempoEnCpu = random.expovariate(1.0/tiempoTotal)
        yield env.timeout(tiempoEnCpu)
        print('%7.4f %s:Saliendo: %6.3f' %(env.now,nombre, tiempoEsperado))       
        containerRam.put(cantidadRam)
    tiempoTotal +=(env.now+tiempoEnCpu)
    tiempoProcesos.append(tiempoTotal)        


random.seed(RANDOM_SEED)
env = simpy.Environment()
cpu= simpy.Resource(env,capacity=1)
containerRam = simpy.Container(env,init=200,capacity=200)

# correr la simulacion
env.process(constructor(env,procesos,intervalo,cpu))
env.run()

#Estadisticas:
resultadoPromedio = 0
for i in tiempoProcesos:
    resultadoPromedio=resultadoPromedio+i
promedio = (resultadoPromedio/procesos)
resultado = 0
for xinicial in tiempoProcesos:
    resultado+=(xinicial-promedio)**2
desv = (resultado/(procesos-1))**0.5
print('Desviacion estandar: %f' %(desv))
print('Tiempo promedio: %f' %(promedio))
