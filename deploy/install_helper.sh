if [[ $# -ne 2 ]]; then
    echo "must provide either terraform or packer as the first argument and the download link as the second argument"
    exit 1
fi

software=$1
dllink=$2

mkdir ~/$software/
curl "$dllink" > ~/$software/$software.zip
cd ~/$software
unzip $software
cat <<EOI >> ~/.bashrc
export PATH=\$PATH:~/$software
EOI
