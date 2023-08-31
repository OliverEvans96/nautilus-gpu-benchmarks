import os

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

    deep_stpp.main.download()
    glow.main.download()
    st_uq.main.download()
    tf_net.main.download()

if __name__ == '__main__':
    main()
