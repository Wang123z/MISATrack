import os
import sys
import time
import argparse
import functools
sys.path.append("./")

from pysot.core.config import cfg
from glob import glob
from tqdm import tqdm
from multiprocessing import Pool
from toolkit.datasets import UAV10Dataset,UAV20Dataset,DTBDataset,UAVDataset,UAVDTDataset,UAVTrack112Dataset
from toolkit.evaluation import OPEBenchmark
from toolkit.visualization import draw_success_precision

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser(description='Single Object Tracking Evaluation')
    parser.add_argument('--dataset_dir', default='',type=str, help='dataset root directory')
    parser.add_argument('--dataset', default='DTB70',type=str, help='dataset name')
    # baseline  baseline_ffe  bs_ffe_effi5  bs_ffe_effi345  sflanof  sflanos
    results_dir = 'sflanof'
    parser.add_argument('--tracker_path',default=f'../results/{results_dir}/130', type=str, help='tracker result root')
    parser.add_argument('--tracker_prefix',default='SiamFFLA', nargs='+')
    parser.add_argument('--vis', default='',dest='vis', action='store_true')
    parser.add_argument('--show_video_level', default='',dest='show_video_level', action='store_true')
    parser.add_argument('--cle', default='',dest='cle', action='store_true')
    parser.add_argument('--num', default=1, type=int, help='number of processes to eval')
    args = parser.parse_args()

    tracker_dir = os.path.join(args.tracker_path, args.dataset)
    trackers = glob(os.path.join(args.tracker_path,
                                  args.dataset,
                                  args.tracker_prefix+'*'))
    trackers = [x.split('/')[-1] for x in trackers]


    root = os.path.realpath(os.path.join(os.path.dirname(__file__),
                             '../../../../raid/datasets'))
    root = os.path.join(root, args.dataset)

    trackers=args.tracker_prefix

  
    assert len(trackers) > 0
    args.num = min(args.num, len(trackers))
    # 评估会有问题，注意修改benchmark.eval_success，benchmark.eval_precision
    if 'UAV123@10fps' in args.dataset:
        dataset = UAV10Dataset(args.dataset, root)
        dataset.set_tracker(tracker_dir, trackers)
        benchmark = OPEBenchmark(dataset)
        if args.cle:
            benchmark.draw_cle(args.dataset)
        else:
            success_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_success,
                    trackers), desc='eval success', total=len(trackers), ncols=18):
                    success_ret.update(ret)
            precision_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_precision,
                    trackers), desc='eval precision', total=len(trackers), ncols=18):
                    precision_ret.update(ret)
            benchmark.show_result(success_ret, precision_ret,
                    show_video_level=args.show_video_level)
        if args.vis:
            for attr, videos in dataset.attr.items():
                draw_success_precision(success_ret,
                            name=dataset.name,
                            videos=videos,
                            attr=attr,
                            precision_ret=precision_ret)
    elif 'UAV12320l' in args.dataset:
        dataset = UAV20Dataset(args.dataset, root)
        dataset.set_tracker(tracker_dir, trackers)
        benchmark = OPEBenchmark(dataset)
        success_ret = {}
        with Pool(processes=args.num) as pool:
            for ret in tqdm(pool.imap_unordered(benchmark.eval_success,
                trackers), desc='eval success', total=len(trackers), ncols=18):
                success_ret.update(ret)
        precision_ret = {}
        with Pool(processes=args.num) as pool:
            for ret in tqdm(pool.imap_unordered(benchmark.eval_precision,
                trackers), desc='eval precision', total=len(trackers), ncols=18):
                precision_ret.update(ret)
        benchmark.show_result(success_ret, precision_ret,
                show_video_level=args.show_video_level)
        if args.vis:
            for attr, videos in dataset.attr.items():
                draw_success_precision(success_ret,
                            name=dataset.name,
                            videos=videos,
                            attr=attr,
                            precision_ret=precision_ret)
    elif 'DTB70' in args.dataset:
        dataset = DTBDataset(args.dataset, root)
        dataset.set_tracker(tracker_dir, trackers)
        benchmark = OPEBenchmark(dataset)
        if args.cle:
            benchmark.draw_cle(args.dataset)
        else:
            success_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_success,
                    trackers), desc='eval success', total=len(trackers), ncols=18):
                    success_ret.update(ret)
            precision_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_precision,
                    trackers), desc='eval precision', total=len(trackers), ncols=18):
                    precision_ret.update(ret)
            benchmark.show_result(success_ret, precision_ret,
                    show_video_level=args.show_video_level)
        if args.vis:
            for attr, videos in dataset.attr.items():
                draw_success_precision(success_ret,
                            name=dataset.name,
                            videos=videos,
                            attr=attr,
                            precision_ret=precision_ret)
    elif 'UAV123' in args.dataset:
        dataset = UAVDataset(args.dataset, root)
        dataset.set_tracker(tracker_dir, trackers)
        benchmark = OPEBenchmark(dataset)
        if args.cle:
            benchmark.draw_cle(args.dataset)
        else:
            success_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_success,
                    trackers), desc='eval success', total=len(trackers), ncols=18):
                    success_ret.update(ret)
            precision_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_precision,
                    trackers), desc='eval precision', total=len(trackers), ncols=18):
                    precision_ret.update(ret)
            benchmark.show_result(success_ret, precision_ret,
                    show_video_level=args.show_video_level)
        if args.vis:
            for attr, videos in dataset.attr.items():
                draw_success_precision(success_ret,
                            name=dataset.name,
                            videos=videos,
                            attr=attr,
                            precision_ret=precision_ret)
    elif 'UAVDT' in args.dataset:
        dataset = UAVDTDataset(args.dataset, root)
        dataset.set_tracker(tracker_dir, trackers)
        benchmark = OPEBenchmark(dataset)
        if args.cle:
            benchmark.draw_cle(args.dataset)
        else:
            success_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_success,
                    trackers), desc='eval success', total=len(trackers), ncols=18):
                    success_ret.update(ret)
            precision_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_precision,
                    trackers), desc='eval precision', total=len(trackers), ncols=18):
                    precision_ret.update(ret)
            benchmark.show_result(success_ret, precision_ret,
                    show_video_level=args.show_video_level)
        if args.vis:
            for attr, videos in dataset.attr.items():
                draw_success_precision(success_ret,
                            name=dataset.name,
                            videos=videos,
                            attr=attr,
                            precision_ret=precision_ret)
    elif 'UAVTrack112' in args.dataset:
        dataset = UAVTrack112Dataset(args.dataset, root)
        dataset.set_tracker(tracker_dir, trackers)
        benchmark = OPEBenchmark(dataset)
        if args.cle:
            benchmark.draw_cle(args.dataset)
        else:
            success_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_success,
                    trackers), desc='eval success', total=len(trackers), ncols=18):
                    success_ret.update(ret)
            precision_ret = {}
            with Pool(processes=args.num) as pool:
                for ret in tqdm(pool.imap_unordered(benchmark.eval_precision,
                    trackers), desc='eval precision', total=len(trackers), ncols=18):
                    precision_ret.update(ret)
            benchmark.show_result(success_ret, precision_ret,
                    show_video_level=args.show_video_level)
        if args.vis:
            for attr, videos in dataset.attr.items():
                draw_success_precision(success_ret,
                            name=dataset.name,
                            videos=videos,
                            attr=attr,
                            precision_ret=precision_ret)
    else:
        print('dataset error')


    



 