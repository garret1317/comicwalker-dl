import argparse
import json
import logging
import os
import requests
import sys

from binascii import unhexlify

parser = argparse.ArgumentParser()
parser.add_argument('cid', help='content id, &cid={...}. see url when reading a chapter')
parser.add_argument('-v', '--verbose', help='no progressive download logs on terminal', action="store_true")
args = parser.parse_args()

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

def start(url, headers):
    meta = requests.get(url=url, headers=headers).json()
    img_url = f'{url}/frames?enable_webp=true'

    try:
        cid_info = {
            "TITLE": meta['data']['extra']['content']['title'],
            "CHAPTER": meta['data']['result']['title']
        }

    except KeyError:
        logging.error("Metadata malformed, check CID's validity")
        sys.exit()

    else:
        print('{} - {}'.format(cid_info['TITLE'], cid_info['CHAPTER']))

        undrm(img_url, headers, cid_info)

def undrm(url, headers, cid_info):
    meta = requests.get(url=url, headers=headers).json()

    print('Page count: {}\n'.format(len(meta['data']['result'])))

    save_path = os.path.join('downloaded_chapters/{}/{}'.format(cid_info['TITLE'], cid_info['CHAPTER']))

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print(f'Saving chapter to {save_path}\n')

    for num, page in enumerate(meta['data']['result']):

        if args.verbose:
            logging.info(f'Downloading page {num+1}')

        key = page['meta']['drm_hash']
        file = requests.get(page['meta']['source_url'], headers=headers).content
        pagination = str(num + 1) + '.webp'

        if key is not None:
            key = unhexlify(key[:16])
            file = xor(file, key)

        with open(f'{save_path}/{pagination}', 'wb') as f:
            f.write(file)

    logging.info('Done.')

def xor(bin, key):
    retval = []

    for idx, val in enumerate(bin):
        retval.append(val ^ key[idx % len(key)])

    return bytes(retval)

def main():

    headers = {
        'authority': 'comicwalker-api.nicomanga.jp',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://comic-walker.com',
        'pragma': 'no-cache',
        'referer': 'https://comic-walker.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-Blowfisht': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }

    content_url = f'https://comicwalker-api.nicomanga.jp/api/v1/comicwalker/episodes/{args.cid}'

    start(content_url, headers)

if __name__ == "__main__":
    main()
