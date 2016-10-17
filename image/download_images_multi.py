"""
Download images into directories separated by categories

python -m image.download_images_multi image_category data/images 8
"""
import pandas as pd
import urllib
import os
import sys
import Queue
import threading
import simplejson as json
import logging
from utils.logger import logger


def download_image(url, product_id, save_path):
    """

    Downloads image from url and saves to save path, naming the image product ID

    :param url:
    :param product_id:
    :param save_path:
    :return:
    """
    try:
        urllib.urlretrieve(url, '{}/{}.jpg'.format(save_path, product_id))
        return True

    except IOError as io:
        logger.error('Download error: {} | Reason: {}'.format(url, io))
        return False


def download_image_worker(url_q, log_q):
    """

    Gets url, product ID, and save path from the queue, downloads images
    For each image url, adds log dictionary to queue indicated product ID, url, and download status for tracking

    :param url_q: Queue of urls, product IDs and save path
    :return:
    """
    queue_full = True
    while queue_full:
        try:
            url, product_id, save_path = url_q.get(block=True)

            log_dict = {'product_id': product_id, 'url': url}

            if download_image(url, product_id, save_path):
                log_dict['downloaded'] = 'success'
            else:
                log_dict['downloaded'] = 'fail'

            log_q.put(log_dict)

            url_q.task_done()

        except Queue.Empty:
            logger.info('Queue Empty')
            queue_full = False


def image_log_worker(image_log_file, log_q, count, max_log_size=10000):
    """

    Writes image download status to image log file based on log queue

    :param image_log_file:
    :param log_q:
    :param count:
    :param max_log_size:
    :return:
    """
    file_number = count / max_log_size

    while True:

        with open(image_log_file + str(file_number) + '.json', 'a') as img_file:

            for i in range(max_log_size):

                result_dict = log_q.get(block=True)
                result_dict_str = json.dumps(result_dict)

                count += 1

                img_file.write(result_dict_str)
                img_file.write('\n')

                log_q.task_done()

                if count % 100 == 0:
                    img_file.flush()

                if count % 1000 == 0:
                    logger.info('Images downloaded: {}'.format(count))

            file_number += 1


def download_images_from_df(df, output_dir, nthreads):
    """
    (DataFrame) -> Images separated by categories into directories

    Downloads images from imUrl provided and saves them into directories
    based on the product category.

    >>> download_images_from_df(df, output_dir):
    Start downloading 20 images
    No. of images downloaded: 15
    ...
    ...
    ...
    Image downloads complete!

    :param df: Dataframe containing product ID (asin), image url (imUrl),
    and category (category_path)
    :param output_dir: Directory path to where to store images (../data/images)
    :param nthreads: No. of threads to download images with
    """
    logger.info('Start downloading {} images'.format(df.shape[0]))

    url_q = Queue.Queue()
    log_q = Queue.Queue()

    # Load previous log files and loads list of successfully downloaded images
    log_dir = os.path.join(data_dir, 'image_download_logs')
    log_file_name = os.path.join(data_dir, 'image_download_logs', 'image_log')
    completed = set()

    if os.path.exists(log_dir):
        for log_file in os.listdir(log_dir):
            log_file = os.path.join(log_dir, log_file)

            if log_file.endswith('.json'):
                logger.info('loading image download logs from: {}'.format(log_file))

                with open(log_file) as json_log:
                    i = 0
                    for line in json_log:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get('downloaded', '') == 'success':
                                completed.add(entry['product_id'])
                        except ValueError as e:
                            logger.error('Json error in {} on line {}: {} '.format(log_file, i, e))
                        i += 1

        logger.info('No. of images downloaded: {}'.format(len(completed)))

    else:  # If log dir does not exist
        os.makedirs(log_dir)

    # Start download threads
    for i in xrange(nthreads):
        t = threading.Thread(target=download_image_worker, args=(url_q, log_q))
        t.daemon = True
        t.start()

    # Start writer thread
    writer_thread = threading.Thread(target=image_log_worker, args=(log_file_name, log_q, len(completed)))
    writer_thread.daemon = True
    writer_thread.start()

    # Add urls into the queue
    for i, row in df.iterrows():
        product_id = row['asin']

        if product_id not in completed:

            url = row['imUrl']
            category_path = row['category_path']
            # logger.info('Category: {}, URL: {}'.format(category_path, url))

            # Create save path
            save_path = '{}/{}'.format(output_dir, category_path)

            # Create directory if it does not exist
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            url_q.put((url, product_id, save_path))

    # Block until all tasks are done
    url_q.join()
    log_q.join()

    logger.info('Image downloads complete!')


if __name__ == '__main__':

    data_dir = 'data'
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    nthreads = int(sys.argv[3])

    log_file = os.path.join(data_dir, 'image_download_log.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')

    # Create file handler that logs debug messages
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    # Read input file
    input_file_path = os.path.join(data_dir, input_file + '.csv')
    df = pd.read_csv(input_file_path)

    # Download images
    download_images_from_df(df, output_dir, nthreads)
