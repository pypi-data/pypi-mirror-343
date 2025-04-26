'''**ETLX** is a modern and highly configurable ETL and reporting tool powered by DuckDB.  
This Python package provides a simple interface to run ETLX workflows directly from Python.'''
import os
import subprocess
from pathlib import Path
from datetime import date, datetime
from typing import Optional, Union, List

class ETLX:
    '''main class'''
    def __init__(
        self,
        bin: str = "etlx",
        config: str = "config.md",
        date_ref: Union[str, date, datetime] = None,
        only: Optional[Union[str, List[str]]] = None,
        skip: Optional[Union[str, List[str]]] = None,
        steps: Optional[str] = None,
        file: Optional[str] = None,
        clean: bool = False,
        drop: bool = False,
        rows: bool = False,
        cwd: Union[str, Path] = ".",
    ):
        self.bin = bin
        self.config = config
        self.date_ref = self._format_date(date_ref)
        self.only = only
        self.skip = skip
        self.steps = steps
        self.file = file
        self.clean = clean
        self.drop = drop
        self.rows = rows
        self.cwd = Path(cwd)

    def _format_date(self, dt):
        if dt is None:
            return datetime.now().strftime("%Y-%m-%d")
        if isinstance(dt, (datetime, date)):
            return dt.strftime("%Y-%m-%d")
        return str(dt)

    def _to_flag(self, key: str, value: Optional[Union[str, bool, List[str]]]) -> List[str]:
        if value is None or value is False:
            return []
        if isinstance(value, list):
            value = ",".join(value)
        if isinstance(value, bool):
            return [f"-{key}"]
        return [f"-{key}", str(value)]

    def execute(self) -> int:
        '''Execute ETLX'''
        args = [
            self.bin,
            *self._to_flag("config", self.config),
            *self._to_flag("date", self.date_ref),
            *self._to_flag("only", self.only),
            *self._to_flag("skip", self.skip),
            *self._to_flag("steps", self.steps),
            *self._to_flag("file", self.file),
            *self._to_flag("clean", self.clean),
            *self._to_flag("drop", self.drop),
            *self._to_flag("rows", self.rows),
        ]
        print(f"[ETLX] Executing: {' '.join(args)} in {self.cwd.resolve()}")
        result = subprocess.run(args, cwd = self.cwd, check = False) #, env=env)
        return result.returncode
