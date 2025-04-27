import pickle as pkl
import zlib
import os
from threading import RLock
import warnings
from typing import Any
from copy import deepcopy
import tempfile
from concurrent.futures import ThreadPoolExecutor

class SDB:
    def __init__(self, name: str):
        """
        A simple database class that stores data in a dictionary.
        :param name: The name of the database.
        """

        self.__name = name
        self.__data = {}
        self.__exchange_data = {}
        self.__tables = set()
        self.__exchange_tables = set()
        self.__saved = False
        self.access_lock = RLock()
        self.__in_exchange = False
        self.__saver = ThreadPoolExecutor(max_workers=1)
        self.__bsaver = ThreadPoolExecutor(max_workers=1)
        self.closed = False

        try:
            with open(f"{self.name}.sdb", "rb") as f:
                self.__data = pkl.loads(zlib.decompress(f.read()))
                self.__tables = set(self.__data.keys())
        except FileNotFoundError:
            self.save()

    @property
    def name(self):
        return self.__name

    @property
    def data(self):
        with self.access_lock:
            return self.__exchange_data or self.__data

    @property
    def tables(self):
        with self.access_lock:
            return self.__exchange_tables or self.__tables

    @property
    def in_exchange(self):
        with self.access_lock:
            return self.__in_exchange

    def get_table(self, name: str) -> list:
        with self.access_lock:
            content = self.__data.get(name, {})
            if not content:
                raise ValueError(f"Table {name} not found.")
            return content['content']

    def add_table(self, name: str):
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                warnings.warn("Exchange wasn't started. Skipping exchanges may increase the risk of data corruption/loss.", RuntimeWarning)
                self.start_exchange()
            if name in self.__exchange_tables:
                raise ValueError(f"Table {name} already exists.")
            self.__exchange_data[name] = dict()
            self.__exchange_data[name]['content'] = []
            self.__exchange_data[name]['index'] = dict()
            self.__exchange_tables.add(name)
            self.__saved = False
            if auto_exchange:
                self.commit()

    def remove_table(self, name: str):
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                warnings.warn("Exchange wasn't started. Skipping exchanges may increase the risk of data corruption/loss.", RuntimeWarning)
                self.start_exchange()

            if name not in self.__exchange_tables:
                raise ValueError(f"Table {name} not found.")
            del self.__exchange_data[name]
            self.__exchange_tables.remove(name)
            self.__saved = False
            if auto_exchange:
                self.commit()

    def add_content(self, table: str, content: Any):
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                warnings.warn("Exchange wasn't started. Skipping exchanges may increase the risk of data corruption/loss.", RuntimeWarning)
                self.start_exchange()
        
            if table not in self.__exchange_tables:
                raise ValueError(f"Table {table} not found.")
            indexes = self.__exchange_data[table]['index']
            new_index = len(self.__exchange_data[table]['content'])
            self.__exchange_data[table]['content'].append(content)
            self.__saved = False
            for index, values in indexes.items():
                val = None
                try:
                    try:
                        val = getattr(content, index)
                    except AttributeError:
                        val = content[index]
                    self.__exchange_data[table]['index'][index][val] = new_index
                except (IndexError, KeyError):
                    pass
                
        if auto_exchange:
            self.commit()

    def remove_content(self, table: str, index: int):
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                warnings.warn("Exchange wasn't started. Skipping exchanges may increase the risk of data corruption/loss.", RuntimeWarning)
                self.start_exchange()
            if table not in self.__exchange_tables:
                raise ValueError(f"Table {table} not found.")
            if index >= len(self.__exchange_data[table]['content']):
                raise ValueError(f"Index {index} out of range.")

            content = self.__exchange_data[table]['content'].pop(index)

            for index, values in self.__exchange_data[table]['index'].items():
                try:
                    try:
                        val = getattr(content, index)
                    except AttributeError:
                        val = content[index]
                    self.__exchange_data[table]['index'][index][val] = None
                except (IndexError, KeyError):
                    pass
        
        if auto_exchange:
            self.commit()

    def get_index_from_index(self, table: str, index: str, value: Any) -> int | None:
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                self.start_exchange()
            if table not in self.__exchange_tables:
                raise ValueError(f"Table {table} not found.")
            if index not in set(self.__exchange_data[table]['index'].keys()):
                raise ValueError(f"Index {index} not found.")
            data = self.__exchange_data[table]['index'][index].get(value)
        if auto_exchange:
            self.commit()
        return data

    def get_data_from_index(self, table: str, index: int) -> Any:
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                self.start_exchange()
            if table not in self.__exchange_tables:
                raise ValueError(f"Table {table} not found.")
            if index >= len(self.__exchange_data[table]['content']):
                raise ValueError(f"Index {index} out of range.")
            data = self.__exchange_data[table]['content'][index]
            if auto_exchange:
                self.commit()
            return data

    def add_index(self, table: str, index: str):
        with self.access_lock:
            auto_exchange = False
            if not self.in_exchange:
                auto_exchange = True
                warnings.warn("Exchange wasn't started. Skipping exchanges may increase the risk of data corruption/loss.", RuntimeWarning)
                self.start_exchange()
            if table not in self.__exchange_tables:
                raise ValueError(f"Table {table} not found.")
            if index in set(self.__exchange_data[table]['index'].keys()):
                warnings.warn(f"Attempted to create already existing index {index} (SBD:{self.name}:{table})", RuntimeWarning)
            self.__exchange_data[table]['index'][index] = dict()
            self.__saved = False
            for i, content in enumerate(self.__exchange_data[table]['content']):
                try:
                    try:
                        val = getattr(content, index)
                    except AttributeError:
                        val = content[index]
                    self.__exchange_data[table]['index'][index][val] = i
                except (IndexError, KeyError):
                    pass
        
        if auto_exchange:
            self.commit()

    def start_exchange(self):
        if self.__in_exchange:
            return
        with self.access_lock:
            self.__exchange_data = deepcopy(self.__data)
            self.__exchange_tables = deepcopy(self.__tables)
            self.__saved = False
            self.__in_exchange = True

    def commit(self):
        if not self.__in_exchange:
            return
        with self.access_lock:
            self.__data = deepcopy(self.__exchange_data)
            self.__tables = deepcopy(self.__exchange_tables)
            self.__exchange_data = {}
            self.__exchange_tables = set()
            self.__saved = False
            self.__save(f"{self.name}_temp")
            self.__in_exchange = False

    def rollback(self):
        with self.access_lock:
            self.__exchange_data = deepcopy(self.__data)
            self.__exchange_tables = deepcopy(self.__tables)
            self.__saved = False
        self.commit()

    def save(self):
        self.__save(f"{self.name}_backup")
        with self.access_lock:
            snapshot = deepcopy(self.__data)
        
        if self.__saved:
            return

        def _write(snapshot):
            fd, tmp = tempfile.mkstemp(dir='.', suffix='.sdb.tmp')
            with os.fdopen(fd, "wb") as f:
                f.write(zlib.compress(pkl.dumps(snapshot, protocol=pkl.HIGHEST_PROTOCOL), level=zlib.Z_BEST_COMPRESSION))
            os.replace(tmp, f"{self.name}.sdb")
            self.__saved = True

        self.__saver.submit(_write, snapshot)

    def __save(self, name: str):
        snapshot = deepcopy(self.__data)
        
        def _write(snapshot):
            with open(f"{name}.sdb", "wb") as f:
                f.write(zlib.compress(pkl.dumps(snapshot, protocol=pkl.HIGHEST_PROTOCOL), level=zlib.Z_BEST_COMPRESSION))

        self.__bsaver.submit(_write, snapshot)

    def load(self):
        with self.access_lock:
            with open(f"{self.name}.sdb", "rb") as f:
                self.__data = pkl.loads(zlib.decompress(f.read()))
                self.__tables = set(self.__data.keys())
            self.__saved = True

    def __enter__(self):
        self.start_exchange()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            warnings.warn(f"Rolling back exchange due to exception: {exc_val}", RuntimeWarning)
            self.rollback()
        self.save()

    def close(self):
        self.access_lock.acquire()
        if not self.__saved:
            raise RuntimeWarning("Attempted to close database file without saving.")
        os.remove(f"{self.name}_temp.sdb")
        def closed_error(*args, **kwargs):
            raise RuntimeError("Database object was closed. Edits cannot be made.")

        self.__saver.shutdown(True)  # Wait for threads to finish
        self.__bsaver.shutdown(True) # Wait for threads to finish

        self.add_content = closed_error
        self.add_index = closed_error
        self.add_table = closed_error
        self.commit = closed_error
        self.data = property(closed_error)
        self.get_data_from_index = closed_error
        self.get_index_from_index = closed_error
        self.get_table = closed_error
        self.tables = property(closed_error)
        self.in_exchange = property(closed_error)
        self.remove_content = closed_error
        self.load = closed_error
        self.name = property(closed_error)
        self.remove_table = closed_error
        self.rollback = closed_error
        self.save = closed_error
        self.start_exchange = closed_error

        self.closed = True
        
        self.access_lock.release()

    def delete(self):
        self.access_lock.acquire()
        self.save()
        os.remove(f"{self.name}.sdb")
        os.remove(f"{self.name}_backup.sdb")
        self.close()
        self.access_lock.release()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name and self.data == other.data
