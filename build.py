import glob
import os
import zipfile

src_dir_name = 'spectres-addon'
init_file_path = os.path.join(src_dir_name, '__init__.py')
init_file = open(init_file_path)

dist_archive_name = "Spectres"+".zip"
dist_dir_name = "dist"

if not os.path.exists(dist_dir_name):
    os.makedirs(dist_dir_name)

zipf = zipfile.ZipFile(
    os.path.join(dist_dir_name, dist_archive_name),
    'w',
    zipfile.ZIP_DEFLATED
)

for py_file in glob.glob(os.path.join(src_dir_name, '*.py')):
    zipf.write(py_file)

for json_file in glob.glob(os.path.join(src_dir_name, '*.json')):
    zipf.write(json_file)

for json_file in glob.glob(os.path.join(src_dir_name, '*.blend')):
    zipf.write(json_file)

zipf.close()





# todo
# version_parts = []
# for line in init_file.readlines():
#     if '"version":' in line:
#         version_string = line.split("(")[1]
#         version_string = version_string.split(")")[0]
#         version_parts = version_string.split(",")
#         version_parts = map(str.strip, version_parts)
#         break
# init_file.close()

# if len(version_parts) == 0:
#     raise "Could not extract version number from " + init_file_path
# dist_archive_name = "blenderStudies-" + ".".join(version_parts) + ".zip"
