if [ -z $1 ]; then
	script_name=tpler
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

echo "installation path: $installation_path"
cp tpler/__init__.py $installation_path/$script_name
echo "tpler/__init__.py installed as $installation_path/$script_name"
cp tpler/add_template.py $installation_path/addtemplate
echo "tpler/add_template.py installed as $installation_path/addtemplate"
cp tpler/rm_template.py $installation_path/rmtemplate
echo "tpler/rm_template.py installed as $installation_path/rmtemplate"
cp -r tpler/templates $installation_path/templates
echo "tpler/templates installed as $installation_path/templates"
chmod 755 $installation_path/$script_name
chmod 755 $installation_path/addtemplate
chmod 755 $installation_path/rmtemplate
chmod -R 755 $installation_path/templates
