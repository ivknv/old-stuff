#!/usr/bin/env bash
if [ -z $1 ]; then
	script_name="pro"
else
	script_name=$1
fi

if [ -z $2 ]; then
	installation_path=/usr/local/bin
else
	if [ -d $2 ]; then
		installation_path=$2
	fi
fi
name="pro"
packages="pro"
files="__init__.py config.py"
script="__init__.py"
echo -n "Are you sure you want to install $name to $installation_path? (y/n) "
read yn
case $yn in
y|Y|yes|YES|Yes|yep|yap) echo "Installation started";;
*) echo "Installation aborted"
exit 0;;
esac
echo "installation path: $installation_path"
for package in $packages; do
echo "going to $package"
cd $package
for file in $files; do
if [ $file == $script ]; then
	echo "installing $file as $installation_path/$script_name"
	cp $file $installation_path/$script_name
	if [ -f "$installation_path/$script_name" ]; then
		echo "installed $file as $installation_path/$script_name"
	else
		echo "failed to install $file as $installation_path/$script_name"
	fi
elif [ -d $file ]; then
	echo "installing $file as $installation_path/$file"
	cp -r $file $installation_path/$file
	if [ -d "$installation_path/$file" ]; then
		echo "installed $file as $installation_path/$file"
	else
		echo "failed to install $file as $installation_path/$file"
	fi
else
	echo "installing $file as $installation_path/$file"
	cp $file $installation_path/$file
	if [ -f "$installation_path/$file" ]; then
		echo "installed $file as $installation_path/$file"
	else
		echo "failed to install $file as $installation_path/$file"
	fi
fi
if [ -f $file ]; then
	if [ $file == $script ]; then
		echo "chmod 755 $installation_path/$script_name"
		chmod 755 $installation_path/$script_name
	else
		echo "chmod 755 $installation_path/$file"
		chmod 755 $installation_path/$file
	fi
else
	echo "chmod -R 755 $installation_path/$file"
	chmod -R 755 $installation_path/$file
fi
done
echo "going back"
cd -
done
