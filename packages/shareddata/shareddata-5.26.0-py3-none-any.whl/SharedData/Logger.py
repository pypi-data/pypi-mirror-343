import os
import sys
import logging
import boto3
from pathlib import Path
from datetime import datetime, timedelta, timezone
import glob
import pandas as pd
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

        except Exception:
            self.handleError(record)
        
        finally:            
            self.release()
