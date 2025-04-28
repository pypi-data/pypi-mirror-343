from minio import Minio
import os
from cloudteam_logger import cloudteam_logger


class blobber:
    def __init__(self, MinIODomain, MinIOAccessKey, MinIOSecretKey, LoggerObj, Secured=True):
        self.client = Minio(MinIODomain, MinIOAccessKey,
                            MinIOSecretKey, secure=Secured)
        self.log = LoggerObj

    def Get_Blob(self, bucket, filename, PathToDownload):
        try:
            self.client.fget_object(bucket, filename, PathToDownload)
        except Exception as error:
            self.log.error(f'Unable to download file: {error}')
            return error
        self.log.info(f'{filename} downloaded successfuly')

    def Delete_Blob(self, bucket, filename):
        try:
            self.client.remove_object(bucket, filename)
        except Exception as error:
            self.log.error(f'Unable to delete file: {error}')
            return error
        self.log.info(f'{filename} deleted successfuly')

    def Put_Blob(self, bucket, file):
        file_name = os.path.basename(file)
        try:
            self.client.fput_object(
                bucket,
                file_name,
                file
            )
        except Exception as error:
            self.log.error(f'Unable to PUT file: {error}')
            return
        self.log.info(f'Uploaded file: {file} successfuly')

    def List_Blob(self, bucket=''):
        objects = []
        if (not bucket):
            try:
                buckets = self.client.list_buckets()
            except Exception as error:
                self.log.error("Unable to list buckets: %s", error)
                return error
        else:
            buckets = [bucket]
        allBLOBs = {}
        for buck in buckets:
            try:
                try:
                    bucket = buck.name
                except Exception:
                    bucket = buck
                objects = self.client.list_objects(bucket)
            except Exception as error:
                self.log.error(f'Unable to list objects of in bucket: {error}')
                return error
            blobsNames = []
            try:
                for obj in objects:
                    blobsNames.append(obj.object_name)
                allBLOBs[bucket] = blobsNames
            except Exception:
                self.log.error(
                    "Unable to unable to connect to bucket or there is no buckets")
                return error
        return allBLOBs

    def List_Blobs(self, bucket='', recursive=True, prefix=''):
        objects = []
        if (not bucket):
            try:
                buckets = self.client.list_buckets()
            except Exception as error:
                self.log.error("Unable to list buckets: %s", error)
                raise
        else:
            buckets = [bucket]
        allBLOBs = {}
        for buck in buckets:
            try:
                try:
                    bucket = buck.name
                except Exception:
                    bucket = buck
                objects = self.client.list_objects(
                    bucket, recursive=recursive, prefix=prefix if prefix else None)
            except Exception as error:
                self.log.error(f'Unable to list objects of in bucket: {error}')
                raise
            blobsNames = []
            try:
                for obj in objects:
                    blobsNames.append(obj)
                allBLOBs[bucket] = blobsNames
            except Exception as error:
                self.log.error(
                    "Unable to unable to connect to bucket or there is no buckets: %s", error)
                raise
        return allBLOBs

    def List_Buckets(self):
        try:
            buckets = self.client.list_buckets()
        except Exception as error:
            self.log.error("Unable to list buckets: %s", error)
            return error
        bucket_list = []
        for bucket in buckets:
            bucket_list.append(bucket.name)
        return bucket_list

    def Blob_Metadata(self, bucket, blob):
        try:
            metadata = self.client.stat_object(bucket, blob)
        except Exception as error:
            self.log.error("Unable to return blob metadata: %s", error)
            return error
        return metadata
