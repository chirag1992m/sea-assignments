#!/usr/bin/env python3
import pickle, os

print("Creating inverted indexes...")
os.system("python -m assignment3.coordinator --mapper_path=assignment4/mr_apps/invindex_mapper.py --reducer_path=assignment4/mr_apps/invindex_reducer.py --job_path=assignment4/invindex_jobs --num_reducers=3 --timeout=120")
print("Created inverted indexes!")

print("Creating document stores...")
os.system("python -m assignment3.coordinator --mapper_path=assignment4/mr_apps/docs_mapper.py --reducer_path=assignment4/mr_apps/docs_reducer.py --job_path=assignment4/docs_jobs --num_reducers=3 --timeout=120")
print("Created document stores!")

print("Creating IDF...")
os.system("python -m assignment3.coordinator --mapper_path=assignment4/mr_apps/idf_mapper.py --reducer_path=assignment4/mr_apps/idf_reducer.py --job_path=assignment4/idf_jobs --num_reducers=1 --timeout=120")
print("Created IDF!")

def move_files(src_path, dst_path, dst_ext):
	for fn in os.listdir(src_path):
		if fn.endswith(".out"):
			root, ext = os.path.splitext(fn)
			if os.path.exists(dst_path + root + dst_ext):
				os.remove(dst_path + root + dst_ext)
			os.rename(src_path + fn, dst_path + root + dst_ext)

print("Now moving indexes...")
move_files("assignment4/docs_jobs/", "assignment2/document_posting_", ".index")
move_files("assignment4/invindex_jobs/", "assignment2/index_posting_", ".index")
move_files("assignment4/idf_jobs/", "assignment2/idf_posting_", ".index")

print("Indexes created!")

'''
This is a glue code
for assignment4 to run with assignment2

In assignment-2, we directly created the TF-IDF from 
the documents. But in assignment-4, we store the IDF 
multiplier in a different file and thus needs to be 
merged with the inverted indexes for this to run.
'''
def run():
	IDFs = []
	for fn in os.listdir("assignment2/"):
		if fn.startswith("idf_posting"):
			fn = os.path.join("assignment2/", fn)
			IDFs.append(pickle.load(open(fn, "rb")))
			os.remove(fn)

	if len(IDFs) == 0:
		return #In the case of assignment-2

	print("Running the glue between assignment-2 and assignment-4...")
	TFs = []
	for fn in os.listdir("assignment2/"):
		if fn.startswith("index_posting"):
			fn = os.path.join("assignment2/", fn)
			TFs.append((fn, pickle.load(open(fn, "rb"))))

	for idx_tf in range(len(TFs)):
		for word in TFs[idx_tf][1].keys():
			idf = 1
			for idx_idf in range(len(IDFs)):
				if word in IDFs[idx_idf]:
					idf = IDFs[idx_idf][word]
			for doc in TFs[idx_tf][1][word].keys():
				TFs[idx_tf][1][word][doc] *= idf

	for idx_tf in range(len(TFs)):
		pickle.dump(TFs[idx_idf][1], open(TFs[idx_idf][0], "wb"))

run()
