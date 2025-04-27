from ..services.storage.connection_storage import ConnectionStorage
from ..services.key_storage_helper import KeyStorageHelper
import logging
logger = logging.getLogger(__name__)

class ConnectionStorageHelper:
    _instance = None  
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionStorageHelper, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, 'initialized'):  
            self.connectionStorage = ConnectionStorage() 
            self.key_storage_helper = KeyStorageHelper()

            self.initialized = True
    def store_connection(self, application_id, connection_data):
        existing_connection = self.retrieve_connection(application_id)
        if existing_connection:
            logger.info("Connection already exists")
            return existing_connection

        connection_data['stored_key_count'] = 0
        connection_data['application_id'] = application_id
        return self.connectionStorage.create(application_id, connection_data)
    def update_connnection(self, application_id, key, value):
        existing_connection = self.connectionStorage.read(application_id)
        if existing_connection:
            existing_connection[key] = value
            self.connectionStorage.store_connection(application_id, existing_connection)
            logger.info(f"Connection {application_id} updated successfully")
            return existing_connection
        logger.info(f"No connection found for ID {application_id}")
        return None
    
    def retrieve_connection(self, application_id):
        connection_response =  self.connectionStorage.read(application_id)
        if connection_response:
            connection_response['stored_key_count'] = self.key_storage_helper.storage_key_count(application_id)
            return connection_response
        return None


    def delete_connection(self, application_id):
         self.connectionStorage.delete(application_id)
         self.key_storage_helper.delete_key_in_storage(application_id=application_id)

    def get_active_connections(self):
        connection_list = self.connectionStorage.read()
        active_connections = []
        for connection in connection_list:
            if connection['stored_key_count'] < connection['max_keys_count']:
                active_connections.append(connection)
        return active_connections        


