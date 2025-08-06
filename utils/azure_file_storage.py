import json
import os
import logging
import re
from datetime import datetime, timedelta, timezone
from azure.storage.file import FileService

def safe_json_loads(json_str):
    """
    Safely loads JSON string, handling potential errors.
    """
    if not json_str:
        return {}
    try:
        if isinstance(json_str, (dict, list)):
            return json_str
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {json_str}"}

class AzureFileStorageManager:
    def __init__(self):
        storage_connection = os.environ.get('AzureWebJobsStorage', '')
        if not storage_connection:
            raise ValueError("AzureWebJobsStorage connection string is required")
        
        connection_parts = dict(part.split('=', 1) for part in storage_connection.split(';'))
        
        self.account_name = connection_parts.get('AccountName')
        self.account_key = connection_parts.get('AccountKey')
        self.share_name = os.environ.get('AZURE_FILES_SHARE_NAME', 'azfbusinessbot3c92ab')
        self.shared_memory_path = "shared_memories"  # Default shared memories path
        self.default_file_name = 'memory.json'
        self.current_guid = None
        self.current_memory_path = self.shared_memory_path  # Initialize to shared memory path
        
        if not all([self.account_name, self.account_key]):
            raise ValueError("Invalid storage connection string")
        
        self.file_service = FileService(
            account_name=self.account_name,
            account_key=self.account_key
        )
        self._ensure_share_exists()

    def _ensure_share_exists(self):
        try:
            self.file_service.create_share(self.share_name, fail_on_exist=False)
            
            # Only ensure shared memories directory and file exist
            self.ensure_directory_exists(self.shared_memory_path)
            try:
                self.file_service.get_file_properties(
                    self.share_name,
                    self.shared_memory_path,
                    self.default_file_name
                )
            except Exception:
                self.file_service.create_file_from_text(
                    self.share_name,
                    self.shared_memory_path,
                    self.default_file_name,
                    '{}'  # Empty JSON object
                )
                logging.info(f"Created new {self.default_file_name} in shared memories directory")
        except Exception as e:
            logging.error(f"Error ensuring share exists: {str(e)}")
            raise

    def set_memory_context(self, guid=None):
        """Set the memory context - only create new directories if valid GUID is provided"""
        if not guid:
            self.current_guid = None
            self.current_memory_path = self.shared_memory_path
            return True
        
        # Validate GUID format
        guid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
        if not guid_pattern.match(guid):
            logging.warning(f"Invalid GUID format: {guid}. Using shared memory.")
            self.current_guid = None
            self.current_memory_path = self.shared_memory_path
            return False
        
        try:
            # Only proceed with GUID-specific setup if GUID is valid
            guid_dir = f"memory/{guid}"
            guid_file = "user_memory.json"
            
            # Check if GUID directory already exists before creating
            try:
                self.file_service.get_file_properties(
                    self.share_name,
                    guid_dir,
                    guid_file
                )
                # If we get here, the file exists
                self.current_guid = guid
                self.current_memory_path = guid_dir
                return True
            except Exception:
                # Create new GUID directory and file
                self.ensure_directory_exists(guid_dir)
                self.file_service.create_file_from_text(
                    self.share_name,
                    guid_dir,
                    guid_file,
                    '{}'  # Empty JSON object
                )
                logging.info(f"Created new memory file for GUID: {guid}")
                self.current_guid = guid
                self.current_memory_path = guid_dir
                return True
            
        except Exception as e:
            logging.error(f"Error setting memory context for GUID {guid}: {str(e)}")
            self.current_guid = None
            self.current_memory_path = self.shared_memory_path
            return False

    def read_json(self):
        """Read from either GUID-specific memory or shared memories"""
        if self.current_guid and self.current_memory_path != self.shared_memory_path:
            try:
                return self._read_guid_memory()
            except Exception:
                # Fall back to shared memory on any error
                self.current_guid = None
                self.current_memory_path = self.shared_memory_path
                return self._read_shared_memory()
        else:
            return self._read_shared_memory()

    def _read_shared_memory(self):
        try:
            file_content = self.file_service.get_file_to_text(
                self.share_name,
                self.shared_memory_path,
                self.default_file_name
            )
            return safe_json_loads(file_content.content)
        except Exception as e:
            logging.error(f"Error reading from shared memory: {str(e)}")
            if "ResourceNotFound" in str(e):
                self._ensure_share_exists()
            return {}

    def _read_guid_memory(self):
        try:
            file_content = self.file_service.get_file_to_text(
                self.share_name,
                self.current_memory_path,
                "user_memory.json"
            )
            return safe_json_loads(file_content.content)
        except Exception as e:
            logging.error(f"Error reading from GUID memory: {str(e)}")
            raise  # Let read_json handle the fallback

    def write_json(self, data):
        """Write to either GUID-specific memory or shared memories"""
        if self.current_guid and self.current_memory_path != self.shared_memory_path:
            try:
                self._write_guid_memory(data)
            except Exception:
                # Fall back to shared memory on any error
                self.current_guid = None
                self.current_memory_path = self.shared_memory_path
                self._write_shared_memory(data)
        else:
            self._write_shared_memory(data)

    def _write_shared_memory(self, data):
        try:
            json_content = json.dumps(data, indent=4)
            self.file_service.create_file_from_text(
                self.share_name,
                self.shared_memory_path,
                self.default_file_name,
                json_content
            )
        except Exception as e:
            logging.error(f"Error writing to shared memory: {str(e)}")
            if "ResourceNotFound" in str(e):
                self._ensure_share_exists()
                self._write_shared_memory(data)

    def _write_guid_memory(self, data):
        try:
            json_content = json.dumps(data, indent=4)
            self.file_service.create_file_from_text(
                self.share_name,
                self.current_memory_path,
                "user_memory.json",
                json_content
            )
        except Exception as e:
            logging.error(f"Error writing to GUID memory: {str(e)}")
            raise  # Let write_json handle the fallback

    def ensure_directory_exists(self, directory_name):
        """Only creates directories that are explicitly needed"""
        try:
            if not directory_name:
                return False
                
            self.file_service.create_share(self.share_name, fail_on_exist=False)
            
            # Handle nested directories
            parts = directory_name.split('/')
            current_path = ""
            
            for part in parts:
                if part:
                    if current_path:
                        current_path = f"{current_path}/{part}"
                    else:
                        current_path = part
                        
                    self.file_service.create_directory(
                        self.share_name,
                        current_path,
                        fail_on_exist=False
                    )
            return True
        except Exception as e:
            logging.error(f"Error ensuring directory exists: {str(e)}")
            return False

    def write_file(self, directory_name, file_name, content):
        """
        Writes a file to Azure File Storage, properly handling binary data.
        
        Args:
            directory_name (str): The directory to write to
            file_name (str): The name of the file
            content: The content to write (can be str, bytes, or BytesIO)
            
        Returns:
            bool: Success or failure
        """
        try:
            self.ensure_directory_exists(directory_name)
            
            # Check if content is binary or string
            if isinstance(content, (bytes, bytearray)):
                # It's already binary data - use create_file_from_bytes
                self.file_service.create_file_from_bytes(
                    self.share_name,
                    directory_name,
                    file_name,
                    content
                )
            elif hasattr(content, 'read') and callable(content.read):
                # It's a file-like object (like BytesIO), read it as binary
                content.seek(0)
                binary_content = content.read()
                if isinstance(binary_content, (bytes, bytearray)):
                    self.file_service.create_file_from_bytes(
                        self.share_name,
                        directory_name,
                        file_name,
                        binary_content
                    )
                else:
                    # Not binary data, encode and use as text
                    self.file_service.create_file_from_text(
                        self.share_name,
                        directory_name,
                        file_name,
                        str(binary_content)
                    )
            else:
                # It's probably a string, use create_file_from_text
                self.file_service.create_file_from_text(
                    self.share_name,
                    directory_name,
                    file_name,
                    str(content)
                )
            
            return True
        except Exception as e:
            logging.error(f"Error writing file: {str(e)}")
            return False

    def read_file(self, directory_name, file_name):
        """
        Reads a file from Azure File Storage.
        
        For text files, returns the content as a string.
        For binary files, consider using read_file_binary instead.
        
        Args:
            directory_name (str): The directory to read from
            file_name (str): The name of the file
            
        Returns:
            str or None: The file content or None if an error occurs
        """
        try:
            # For known binary file types, use get_file_to_bytes
            if file_name.lower().endswith(('.pptx', '.docx', '.xlsx', '.pdf', '.zip', '.jpg', '.png', '.gif')):
                return self.read_file_binary(directory_name, file_name)
            
            # Otherwise try to get as text
            try:
                file_content = self.file_service.get_file_to_text(
                    self.share_name,
                    directory_name,
                    file_name
                )
                return file_content.content
            except Exception as text_error:
                # If getting as text fails, try as binary
                logging.warning(f"Failed to read as text, trying binary: {str(text_error)}")
                return self.read_file_binary(directory_name, file_name)
                
        except Exception as e:
            logging.error(f"Error reading file: {str(e)}")
            return None
            
    def read_file_binary(self, directory_name, file_name):
        """
        Reads a file from Azure File Storage as binary data.
        
        Args:
            directory_name (str): The directory to read from
            file_name (str): The name of the file
            
        Returns:
            bytes or None: The binary file content or None if an error occurs
        """
        try:
            binary_stream = self.file_service.get_file_to_bytes(
                self.share_name,
                directory_name,
                file_name
            )
            
            return binary_stream.content
        except Exception as e:
            logging.error(f"Error reading binary file: {str(e)}")
            return None

    def list_files(self, directory_name):
        try:
            return self.file_service.list_directories_and_files(
                self.share_name,
                directory_name
            )
        except Exception as e:
            logging.error(f"Error listing files: {str(e)}")
            return []
            
    def generate_download_url(self, directory, filename, expiry_time):
        """
        Generates a temporary download URL with SAS token for a file in Azure File Storage.
        
        Args:
            directory (str): The directory containing the file
            filename (str): The filename to download
            expiry_time (datetime): When the URL should expire
            
        Returns:
            str: The download URL or None if failed
        """
        try:
            # Get the full file path
            if directory.endswith('/'):
                file_path = f"{directory}{filename}"
            else:
                file_path = f"{directory}/{filename}"
            
            # Get directory and file path for the API
            directory_path = '/'.join(file_path.split('/')[:-1])
            file_name = file_path.split('/')[-1]
            
            # Use current time as start time to ensure proper ordering
            start_time = datetime.utcnow()
            
            # Set expiry time to a safe value (30 minutes from now)
            expiry_time = start_time + timedelta(minutes=30)
            
            # Generate SAS token with minimal parameters
            sas_token = self.file_service.generate_file_shared_access_signature(
                share_name=self.share_name,
                directory_name=directory_path,
                file_name=file_name,
                permission='r',  # Read permission only
                expiry=expiry_time
            )
            
            # Create the full URL with SAS token
            file_url = f"https://{self.account_name}.file.core.windows.net/{self.share_name}/{file_path}"
            download_url = f"{file_url}?{sas_token}"
            
            return download_url
            
        except Exception as e:
            logging.error(f"Error generating download URL: {str(e)}")
            logging.error(f"Directory: {directory}, Filename: {filename}")
            return None