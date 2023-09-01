import os

import deep_stpp.main
import glow.main
import st_uq.main
import tf_net.main

def main():
    print("Running benchmarks")

    if 'DATA_DIR' in os.environ:
        data_dir = os.environ['DATA_DIR']
        print("Using data dir: {}".format(data_dir))
        # Create the directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        # Switch to that directory
        os.chdir(data_dir)

    print("deep_stpp")
    deep_stpp.main.main()

    print("glow")
    glow_args = glow.main.create_arg_parser().parse_args()
    glow.main.main(glow_args)

    print("st_uq")
    st_uq.main.main()

    print("tf_net")
    tf_net.main.main()

    print("Done")

if __name__ == '__main__':
    main()
