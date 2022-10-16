import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', type=str, default='CoatingMod2D')
    parser.add_argument('--n_jobs', '-j', type=int, default=-1)
    parser.add_argument('--log', '-l', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    args = parser.parse_args()  
    return args
