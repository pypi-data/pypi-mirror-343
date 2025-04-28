import os
import sys
import logging
import boto3
from pathlib import Path
from datetime import datetime, timedelta, timezone
import glob
import pandas as pd
import numpy as np
from io import StringIO

from pythonjsonlogger.jsonlogger import JsonFormatter
import boto3
import json
import requests
import lz4

from SharedData.IO.AWSKinesis import KinesisLogHandler

class Logger:

    log = None
    user = 'guest'
    source = 'unknown'
    last_day_read = False
    dflogs = pd.DataFrame(
        [],
        columns=['shardid', 'sequence_number', 'user_name', 'asctime', 'logger_name', 'level', 'message']
    )
    logfilepath = Path('')
    logfileposition=0

    @staticmethod
    def connect(source, user=None):
        if Logger.log is None:
            if 'SOURCE_FOLDER' in os.environ:
                try:
                    commompath = os.path.commonpath(
                        [source, os.environ['SOURCE_FOLDER']])
                    source = source.replace(commompath, '')
                except:
                    pass
            elif 'USERPROFILE' in os.environ:
                try:
                    commompath = os.path.commonpath(
                        [source, os.environ['USERPROFILE']])
                    source = source.replace(commompath, '')
                except:
                    pass

            finds = 'site-packages'
            if finds in source:
                cutid = source.find(finds) + len(finds) + 1
                source = source[cutid:]                        
            source = source.replace('\\','/')
            source = source.lstrip('/')
            source = source.replace('.py', '')
            Logger.source = source

            if not user is None:
                Logger.user = user
            
            loglevel = logging.INFO
            if 'LOG_LEVEL' in os.environ:
                if os.environ['LOG_LEVEL'] == 'DEBUG':
                    loglevel = logging.DEBUG                
                
            # Create Logger
            Logger.log = logging.getLogger(source)
            Logger.log.setLevel(logging.DEBUG)
            # formatter = logging.Formatter(os.environ['USER_COMPUTER'] +
            #                               ';%(asctime)s;%(name)s;%(levelname)s;%(message)s',
            #                               datefmt='%Y-%m-%dT%H:%M:%S%z')
            formatter = logging.Formatter(os.environ['USER_COMPUTER'] +
                                          ';%(asctime)s;%(levelname)s;%(message)s',
                                          datefmt='%H:%M:%S')
            # log screen
            handler = logging.StreamHandler()
            handler.setLevel(loglevel)
            handler.setFormatter(formatter)
            Logger.log.addHandler(handler)

            # log to API
            if str(os.environ['LOG_API']).upper()=='TRUE':
                apihandler = APILogHandler()
                apihandler.setLevel(logging.DEBUG)
                jsonformatter = JsonFormatter(os.environ['USER_COMPUTER']+
                                            ';%(asctime)s;%(name)s;%(levelname)s;%(message)s',
                                            datefmt='%Y-%m-%dT%H:%M:%S%z')
                apihandler.setFormatter(jsonformatter)
                Logger.log.addHandler(apihandler)

            # log to file
            if str(os.environ['LOG_FILE']).upper()=='TRUE':
                path = Path(os.environ['DATABASE_FOLDER'])
                path = path / 'Logs'
                path = path / datetime.now().strftime('%Y%m%d')
                path = path / (os.environ['USERNAME'] +
                            '@'+os.environ['COMPUTERNAME'])
                path = path / (source+'.log')
                path.mkdir(parents=True, exist_ok=True)
                fhandler = logging.FileHandler(str(path), mode='a')
                fhandler.setLevel(loglevel)
                fhandler.setFormatter(formatter)
                Logger.log.addHandler(fhandler)
            
            # log to aws kinesis
            if str(os.environ['LOG_KINESIS']).upper()=='TRUE':
                kinesishandler = KinesisLogHandler(user=Logger.user)
                kinesishandler.setLevel(logging.DEBUG)
                jsonformatter = JsonFormatter(os.environ['USER_COMPUTER']+
                                            ';%(asctime)s;%(name)s;%(levelname)s;%(message)s',
                                            datefmt='%Y-%m-%dT%H:%M:%S%z')
                kinesishandler.setFormatter(jsonformatter)
                Logger.log.addHandler(kinesishandler)

    @staticmethod
    def read_last_day_logs():
        Logger.last_day_read = True
        lastlogfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        lastlogfilepath = lastlogfilepath / \
            ((pd.Timestamp.utcnow() + timedelta(days=-1)).strftime('%Y%m%d')+'.log')        
        if lastlogfilepath.is_file():
            try:
                _dflogs = pd.read_csv(lastlogfilepath, header=None, sep=';',
                                      engine='python', on_bad_lines='skip')
                _dflogs.columns = ['shardid', 'sequence_number',
                                   'user_name', 'asctime', 'logger_name', 'level', 'message']
                Logger.dflogs = pd.concat([_dflogs, Logger.dflogs], axis=0)
            except Exception as e:
                print(f'Error reading last day logs: {e}')

    @staticmethod
    def readLogs():
        if not Logger.last_day_read:
            Logger.read_last_day_logs()

        _logfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        _logfilepath = _logfilepath / \
            (pd.Timestamp.utcnow().strftime('%Y%m%d')+'.log')
        if Logger.logfilepath != _logfilepath:
            Logger.logfileposition = 0
            Logger.logfilepath = _logfilepath

        if Logger.logfilepath.is_file():
            try:
                with open(Logger.logfilepath, 'r') as file:
                    file.seek(Logger.logfileposition)
                    newlines = '\n'.join(file.readlines())
                    dfnewlines = pd.read_csv(StringIO(newlines), header=None, sep=';',
                                             engine='python', on_bad_lines='skip')
                    dfnewlines.columns = [
                        'shardid', 'sequence_number', 'user_name', 'asctime', 'logger_name', 'level', 'message']
                    Logger.dflogs = pd.concat([Logger.dflogs, dfnewlines])
                    Logger.logfileposition = file.tell()
            except:
                pass

        return Logger.dflogs

    @staticmethod
    def getLogs():
        df = Logger.readLogs()
        if not df.empty:
            idxhb = np.array(['#heartbeat#' in s for s in df['message'].astype(str)])
            idshb = np.where(idxhb)[0]
            if len(idshb > 100):
                idshb = idshb[-100:]
            ids = np.where(~idxhb)[0]
            ids = np.sort([*ids, *idshb])
            df = df.iloc[ids, :]
        return df

        
class APILogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        if not 'SHAREDDATA_ENDPOINT' in os.environ:
            raise Exception('SHAREDDATA_ENDPOINT not in environment variables')
        self.endpoint = os.environ['SHAREDDATA_ENDPOINT']+'/api/logs'

        if not 'SHAREDDATA_TOKEN' in os.environ:
            raise Exception('SHAREDDATA_TOKEN not in environment variables')
        self.token = os.environ['SHAREDDATA_TOKEN']        

    def emit(self, record):
        try:
            self.acquire()
            user = os.environ['USER_COMPUTER']    
            dt = datetime.fromtimestamp(record.created, timezone.utc)
            asctime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
            msg = {
                'user_name': user,
                'asctime': asctime,
                'logger_name': record.name,
                'level': record.levelname,
                'message': str(record.msg).replace('\'', '\"'),
            }                                    
            body = json.dumps(msg)
            compressed = lz4.frame.compress(body.encode('utf-8'))
            headers = {
                'Content-Type': 'application/json',
                'Content-Encoding': 'lz4',
                'X-Custom-Authorization': self.token,
            }
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=compressed,
                timeout=15
            )
            response.raise_for_status()

        except Exception as e:
            # self.handleError(record)
            print(f"Could not send log to server:{record}\n {e}")
        finally:            
            self.release()
