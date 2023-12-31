import os
from os.path import exists
import sys

import numpy as np
import torch
from tqdm.auto import trange

from . import load_data as ld
from . import convlstm as md
from . import convlstm_training as tr
from . import evaluation as ev

def download(s3):
    os.makedirs('ST-UQ/data', exist_ok=True)

    data_fn = [
        'beijing_aqi_stations.csv',
        'beijing_aqi_test_03.csv',    
        'beijing_aqi_train_17_18_01.csv',
        'beijing_aqi_val_02.csv', 
        'beijing_meo_test_03.csv',
        'beijing_meo_train_17_18_01.csv',
        'beijing_meo_val_02.csv'
    ]

    for fn in data_fn:
        if not exists(f'ST-UQ/data/{fn}'):
            s3.download(f'st-uq/{fn}', f'ST-UQ/data/{fn}')

def main():
    for k in range (1):
        # Random seed
        random_seed = k
        torch.manual_seed(random_seed)
        torch.cuda.manual_seed(random_seed)
        np.random.seed(random_seed)
        # Create directory
        directory = 'seed'+str(random_seed)
        path = os.path.join('ST-UQ/', directory)

        if not exists(path):
            os.mkdir(path)
        # Training data
        grid_seqs = ld.load_batch_seq_data()
        input_seqs, target_meo_seqs, _, _ = tr.seq_preprocessing(grid_seqs)
        # Dev data
        dev_grid_seqs = ld.load_batch_dev_seq_data()
        dev_input_seqs, dev_target_meo_seqs, _, _ = \
            tr.seq_preprocessing(dev_grid_seqs)
        # Test data
        test_grid_seqs = ld.load_batch_test_seq_data()
        test_input_seqs, test_target_meo_seqs, avg_grid, std_grid = \
            tr.seq_preprocessing(test_grid_seqs)

        model = md.ConvLSTMForecast2L((21, 31), 256, 3, 1).cuda() #256
        snapshots = []
        losses = []
        dev_losses = []
        test_losses = []

        for i in trange (10, file=sys.stdout): 
            model, loss, dev_loss = tr.train(
                model, input_seqs, target_meo_seqs, dev_input_seqs, dev_target_meo_seqs, 
                snapshots, iterations=1, lr=0.001)

            test_loss = ev.compute_dev_set_loss(
                model,
                test_input_seqs,
                test_target_meo_seqs)

            losses.append(loss)
            dev_losses.append(dev_loss)
            test_losses.append(test_loss)

            print('Epoch: {}, Train loss: {}, Dev loss: {}, Test loss: {}'.format(
                i, loss, dev_loss, test_loss))

if __name__ == "__main__":
    download()
    main()
