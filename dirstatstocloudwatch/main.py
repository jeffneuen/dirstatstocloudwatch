import boto3
import logging
import yaml
import argparse
from util import get_folder_object_info


def read_config_file(config_file_path):
    with open(config_file_path, 'r') as file:
        cfg = yaml.safe_load(file)
    return cfg


def write_result_to_cloudwatch(metricname, dimensions, unit, value):
    client = boto3.client('cloudwatch')
    client.put_metric_data(
        Namespace='Dir Stats to CloudWatch',
        MetricData=[
            {
                'MetricName': metricname,
                'Dimensions': dimensions,
                'Value': value,
                'Unit': unit
            },
        ]
    )
    logging.debug(f'Fake write {metricname}, {value}')


def get_data_and_publish(cfg):
    for dir in cfg['directories']:
        result = get_folder_object_info(dir['location'], get_object_count=dir['objects'], get_total_bytes=dir['bytes'])
        if 'total_bytes' in result.keys():
            write_result_to_cloudwatch(metricname='total_bytes',
                                       dimensions=
                                       [
                                           {
                                               'Name': 'folder',
                                               'Value': dir['location']
                                           }
                                       ]
                                       ,
                                       unit='Count',
                                       value=result['total_bytes']
                                       )

        if 'object_count' in result.keys():
            write_result_to_cloudwatch(metricname='total_objects',
                                       dimensions=
                                       [
                                           {
                                               'Name': 'folder',
                                               'Value': dir['location']
                                           }
                                       ]
                                       ,
                                       unit='Count',
                                       value=result['object_count']
                                       )


if __name__ == '__main__':
    if __name__ == '__main__':
        logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
        logging.getLogger('boto3').setLevel(logging.INFO)

        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--configfilepath', help='Full path to config file')
        args = parser.parse_args()
        config_filename = args.configfilepath
        logging.info(f'Using config file: {config_filename}')
        cfg = read_config_file(config_filename)
        get_data_and_publish(cfg)
