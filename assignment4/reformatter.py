import argparse
import xml.etree.ElementTree as et 
import os, pickle

parser = argparse.ArgumentParser(prog="Wiki-Data Reformatter")

parser.add_argument("data_file", help="Path where the wiki-data file resides", type=str, default="assignment2/data/info_ret.xml")
parser.add_argument("--job_path", help="Path where re-formatted files will be saved", type=str, default="assignment4/idf_jobs/")
parser.add_argument("--num_partitions", help="Number of partition of file", type=int, default=1)

def partition_file(opt):
	root = et.parse(opt.data_file).getroot()
	pages = [child for child in root if child.tag.endswith('page')]
	
	files = []
	for i in range(opt.num_partitions):
		files.append(open(os.path.join(opt.job_path, str(i) + ".in"), "wb"))

	for idx, page in enumerate(pages):
		pickle.dump(page, files[idx%opt.num_partitions])

if __name__ == "__main__":
	options = parser.parse_args()
	partition_file(options)