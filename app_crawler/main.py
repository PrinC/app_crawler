from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
import json

parser = argparse.ArgumentParser(description='App Crawler')
parser.add_argument('-n', '--name', type=str,  help='the name of crawler you want to run', default="myapp")
parser.add_argument('-i', '--item_count', type=int, help='the count of item you want to collect', default=0)
parser.add_argument('-d', '--data_dest', type=str, help='the destination directory where stores the apk files', default="default/data")
parser.add_argument('-r', '--run_dir', type=str, help='the directory save persistent states of crawl', default="default/run")
parser.add_argument('-l', '--log_file', type=str, help='the directory save crawler log', default="default/default.log")
parser.add_argument('-c', '--config_file', type=str, help='config file of app_crawler')

args = parser.parse_args()
settings = get_project_settings()
config_file = args.config_file
# TODO check config schema
if config_file:
    with open(config_file) as f:
        config = json.load(f)
    item_count = config["item_count"]
    data_dest = config["data_dest"]
    log_file = config["log_file"]
    run_dir = config["run_dir"]
    name = config["name"]
else:
    name = args.name
    item_count = args.item_count
    data_dest = args.data_dest
    log_file = args.log_file
    run_dir = args.run_dir

settings.set('CLOSESPIDER_ITEMCOUNT', item_count)
settings.set('FILES_STORE', data_dest)
settings.set('LOG_FILE', log_file)
settings.set('JOBDIR', run_dir)
process = CrawlerProcess(settings)


process.crawl(name, mongo_uri=settings['MONGO_URI'], mongo_db=settings['MONGO_DATABASE'], mongo_collection=name + '_meta')
process.start()
