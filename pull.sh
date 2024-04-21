
current_user=$(whoami)
start_dir="/home/${current_user}"
dir_name="80211bd-heterogeneousPlatooning-EDCA-ReliabilityStudy"

# Find the ns-3.36.1 directory
ns3_dir=$(find $start_dir -type d -name "ns-3.36.1" -print -quit)

if [[ -z "$ns3_dir" ]]; then
    echo "ns-3.36.1 directory not found."
    exit 1
else
    echo "ns-3.36.1 directory found at: $ns3_dir"
fi

user_source_path="${ns3_dir}/scratch/${dir_name}"
user_destination_path="${ns3_dir}"
source_dir="include"
destination_dir="build/include/ns3"

echo -e "\n\nExecuting git pull"
git pull

echo -e "\n\nobtaining new files that were pulled."
files=()
for file in "${source_dir}/"*.h; do
    file_name=$(basename "${file}")
    files+=("$file_name")
    echo $file_name
done

echo -e "\n\nRemoving old symlink files"
for file in "${files[@]}"; do
echo "Removing ${destination_dir}/${file}"
rm -rf "${user_destination_path}/${destination_dir}/${file}"
done

echo -e "\n\nCreating new Symlinks"
for file in "${files[@]}"; do
    echo "Added ${source_dir}/${file} ${destination_dir}/${file}"
    ln -s "${user_source_path}/${source_dir}/${file}" "${user_destination_path}/${destination_dir}/${file}"
done

