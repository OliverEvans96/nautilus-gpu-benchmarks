import os

from s3fs.core import S3FileSystem

import deep_stpp.main
import glow.main
import st_uq.main
import tf_net.main

def main():
    if 'DATA_DIR' in os.environ:
        data_dir = os.environ['DATA_DIR']
        print("Using data dir: {}".format(data_dir))
        # Create the directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        # Switch to that directory
        os.chdir(data_dir)

    s3 = S3FileSystem(
        key='jMc2Bgylpg3eyeAHV5Cu',
        secret='V3qP2YcCkpK6SJp7LOZlxdBTaQ2tR5i74xNEjDij',
        client_kwargs={
            'endpoint_url': 'https://rosedata.ucsd.edu',
            'region_name': 'US'
        }
    )

    deep_stpp.main.download(s3)
    glow.main.download(s3)
    st_uq.main.download(s3)
    tf_net.main.download(s3)

if __name__ == '__main__':
    main()
