#-------------------------------------------------------
# Proxy

class ResourceHeavyObject:

    def __init__(self):
        self.running = True

    def start_computation(self, job):
        self.running = True
        self.compute = job
        print("Pouzivam casovo narocne spracovanie vsetkych prostriedkov")

    def stop_computation(self):
        self.running = False
        print("Skoncil som casovo narocny vypcet ulohy")

    @property
    def state(self):
        return self.running


class Computation:
    pass

class Proxy:

    def __init__(self) -> None:
        self.heavy_object = ResourceHeavyObject()

    def execute_job(self, job):
        if not self.heavy_object.state:
            self.heavy_object.start_computation(job)
        else:
            print("Nedostatok volnych prostriedkov na vypocet")

heavy = ResourceHeavyObject()
job = Computation

proxy = Proxy()
proxy.execute_job(job)

proxy.heavy_object.stop_computation()

proxy.execute_job(job)



#-------------------------------------------------------
# Template

from abc import ABC, abstractclassmethod

class AbstractProcessing(ABC):

    @abstractclassmethod
    def dataload(self):
        pass

    @abstractclassmethod
    def datatransformation(self):
        pass

    @abstractclassmethod
    def modeling(self):
        pass

    @abstractclassmethod
    def modelevaluation(self):
        pass

    @abstractclassmethod
    def modelsaving(self):
        pass

    def run(self):
        self.dataload()
        self.datatransformation()
        self.modeling()
        self.modelevaluation()
        self.modelsaving()


class Modeling_Data1(AbstractProcessing):

    def dataload(self):
        print('Nacitanie dat 1')

    def datatransformation(self):
        print('Merge data 1')

    def modeling(self):
        print('Modeling data 1')

    def modelevaluation(self):
        print('Hodnotenie modelu 1')

    def modelsaving(self):
        print('ulozenie modelu 1')

class Modeling_Data2(AbstractProcessing):

    def dataload(self):
        print('Nacitanie dat 2')

    def datatransformation(self):
        print('Merge data 2')

    def modeling(self):
        print('Modeling data 2')

    def modelevaluation(self):
        print('Hodnotenie modelu 2')

    def modelsaving(self):
        print('ulozenie modelu 2')

processing1 = Modeling_Data1()
processing1.run()

processing2 = Modeling_Data2()
processing2.run()




#-------------------------------------------------------
# Command
import pandas as pd

class DataStructure:
    def __init__(self, data=pd.DataFrame):
        self.data = data
        self.selection = pd.DataFrame()
    
    @property
    def columns(self):
        return self.data.columns

    def select_columns(self, columns):
        self.selection = self.data[columns]

    def save_selection(self):
        self.selection.to_csv('_'.join(self.selection.columns.to_list())+'.csv', sep=',')

    def return_selection(self):
        return self.selection

from abc import ABC, abstractmethod

class Command:
    def __init__(self, datastructure):
        self.datastructure = datastructure

    @abstractmethod
    def execute():
        pass

class SelectAndShow(Command):
    def __init__(self, datastructure, columns):
        super().__init__(datastructure)
        self.columns = columns

    def execute(self):
        self.datastructure.select_columns(self.columns)
        print(self.datastructure.return_selection())

class SelectAndSave(Command):
    def __init__(self, datastructure, columns):
        super().__init__(datastructure)
        self.columns = columns

    def execute(self):
        self.datastructure.select_columns(self.columns)
        self.datastructure.save_selection()

df = pd.read_csv('patterns.csv')
ds = DataStructure(df)

ds.columns
sashow = SelectAndShow(ds, ['email'])
sashow.execute()

sasave = SelectAndSave(ds, ['id', 'name'])
sasave.execute()



#-------------------------------------------------------
# Observer

class DataSource:
    def __init__(self) -> None:
        self.__observers = []
        self.__temperature = None
    
    def register(self, observer):
        if not observer in self.__observers:
            self.__observers.append(observer)

    def unregister(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notifyObservers(self, temperature):
        for observer in self.__observers:
            observer.update(temperature)


from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def update(self, temperature):
        pass

class DBObserver:

    def __init__(self, source) -> None:
        self.source = source
        self.source.register(self)

    def update(self, temperature):
        self.temperature = temperature
        print("Teplota ", self.temperature, " ulozena v db")

class AlertObserver:

    def __init__(self, source) -> None:
        self.source = source
        self.source.register(self)

    def update(self, temperature):
        self.temperature = temperature
        if self.temperature > 20:
            print("Pozor teplota ", self.temperature, " > 20")

class DisplayObserver:

    def __init__(self, source) -> None:
        self.source = source
        self.source.register(self)

    def update(self, temperature):
        self.temperature = temperature
        print("Aktualna teplota ", self.temperature)

ds = DataSource()
for Observer in [DBObserver, AlertObserver, DisplayObserver]:
     Observer(ds)

ds.notifyObservers(18)
ds.notifyObservers(25)




#-------------------------------------------------------
#Factory method

import pandas as pd
import json
import sqlite3

class JSONConnector:
    def __init__(self, file):
        self.dataframe = pd.read_json(file)

    def get_dataframe(self):
        return self.dataframe

class Sqlite3Connector:
    def __init__(self, database, query):
        con = sqlite3.connect(database)
        self.dataframe = pd.read_sql(sql=query, con=con)

    def get_dataframe(self):
        return self.dataframe

def connection_factory(data_file, *args):
    if data_file.endswith('json'):
        connector = JSONConnector
        return connector(data_file)

    elif data_file.endswith('db'):
        connector = Sqlite3Connector
        return connector(data_file, args[0])

cf = connection_factory('patterns.db', 'select * from users')
cf.get_dataframe()



#-------------------------------------------------------
# Borg

class Borg():
    __shared_state = {}
    def __init__(self, name=None):
        self.__dict__ = self.__shared_state
        if name is not None:
            self.name = name

    def __str__(self):
        return f"Name: {self.name}"

b1 = Borg("Misko")
print(b1)
b2 = Borg("Jarko")
print(b2)



#-------------------------------------------------------
# Singleton

class Single():
    _single = None
    def __new__(cls):
        if not cls._single:
            cls._single = super(Single, cls).__new__(cls)
        return cls._single

    def __str__(self) -> str:
        print(self)

s1 = Single()
s2 = Single() 

s1 == s2