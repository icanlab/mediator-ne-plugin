#!/bin/bash
function getdir()
{
    for element in `ls $1`
    do  
        dir_or_file=$1"/"$element
        if [ -d $dir_or_file ]
        then 
            getdir $dir_or_file $2
        else
            echo $dir_or_file
            cp -rf $dir_or_file $2
        fi  
    done
}

ANSIBLE_PATH="$ansible_path"
if [ -z "$ANSIBLE_PATH" ]; then
 echo "Error: ansible has not been installed."
   exit 1
fi
if [ `ansible --version | head -1 | cut -f2 -d' '|cut -c1-3` >= "2.9" ]; then
   echo "Error: The script only supports ansible 2.9."
   exit 1
fi

NCCLIENT_PATH="$ncclient_path"

if [ -z "$ANSIBLE_PATH" ] ; then
    echo "Error: Can not get Ansible location."
        if [ "which pip" ] ;then
			pip install ansible
		else
			echo "Please install pip"
		fi
    exit 1
else
    echo "Ansible path:$ANSIBLE_PATH"
fi

echo "ne modules path:$ANSIBLE_PATH/modules/network"
mkdir -p $ANSIBLE_PATH/module_utils/network/ne
mkdir -p $ANSIBLE_PATH/modules/network/ne
echo "Copying files ..."
if [ -d "./modules" ]
then
    cp -rf ./modules/network/ne/* $ANSIBLE_PATH/modules/network/ne
fi
if [ -d "./module_utils" ]; then
    cp -a ./module_utils/network/ne/* $ANSIBLE_PATH/module_utils/network/ne
fi
if [ -d "./plugins" ]; then
    cp -rf ./plugins/action/* $ANSIBLE_PATH/plugins/action
    cp -rf ./plugins/terminal/* $ANSIBLE_PATH/plugins/terminal
    cp -rf ./plugins/netconf/* $ANSIBLE_PATH/plugins/netconf
	cp -rf ./plugins/cliconf/* $ANSIBLE_PATH/plugins/cliconf
fi

if [ -d "$NCCLIENT_PATH" ]; then
    echo "$NCCLIENT_PATH"
	if [ ! -f "$NCCLIENT_PATH/devices/huaweiyang.py" ]; then
		if [ -d "./tools/ncclient" ]; then
			cp -rf ./tools/ncclient/rpc.py $NCCLIENT_PATH/operations/third_party/huawei/rpc.py
			cp -rf ./tools/ncclient/huaweiyang.py $NCCLIENT_PATH/devices/huaweiyang.py
			cp -rf ./tools/ncclient/operations/rpc.py $NCCLIENT_PATH/operations/rpc.py
			echo "Copy huaweiyang.py Success"
		fi
	else 
		echo "Ncclient already exit : $NCCLIENT_PATH/devices/huaweiyang.py"
	fi
	if [ -d "./tools/ncclient/operations" ]; then
		cp -rf ./tools/ncclient/operations/rpc.py $NCCLIENT_PATH/operations/rpc.py
		echo "Copy ncclient/operations/rpc.py Success"
	fi
else
	echo "Error: ncclient has not been installed."
		if [ "which pip" ]; then
			pip install ncclient
		else 
			echo "Please install pip"
		fi
   exit 1
fi



echo "Updateing base.yml"
ne_exist=`cat $ANSIBLE_PATH/config/base.yml | grep "NETWORK_GROUP_MODULES"| grep "ne"`
if [ -z "$ne_exist" ]; then
    name_exist=`grep -rnw ", ne" $ANSIBLE_PATH/config/base.yml  | cut -d ":" -f 1`
    if [ $name_exist ]; then
        echo "Update base.yml failed, ne has already in base.yml."
    else 
        replace_line=`grep -rn ", aireos," $ANSIBLE_PATH/config/base.yml  | cut -d ":" -f 1`
        if [ $replace_line ]; then
            sed -i "s/aireos/aireos, ne/g" $ANSIBLE_PATH/config/base.yml
        else
            echo "Update base.yml failed, NETWORK_GROUP_MODULES in base.yml should be manually updated."
        fi
    fi
fi

echo "Updateing plugin/conection/netconf.py"
huaweiyang_exist=`cat $ANSIBLE_PATH/plugins/connection/netconf.py | grep "NETWORK_OS_DEVICE_PARAM_MAP ="`
if [ "$huaweiyang_exist" ]; then
    ne_exist=`grep -rn '    "ne": "huaweiyang",' $ANSIBLE_PATH/plugins/connection/netconf.py  | cut -d ":" -f 1`
    if [ $ne_exist ]; then
        echo "plugin/conection/netconf.py failed, ne has already in NETWORK_OS_DEVICE_PARAM_MAP."
    else 
        sed -i '/^NETWORK_OS_DEVICE_PARAM_MAP =/a\    "ne": "huaweiyang",' $ANSIBLE_PATH/plugins/connection/netconf.py
                   echo "Update plugins/connetion/netconf.py Success."
    fi
fi

echo "Updateing plugin/action/net_base.py"
ne_platform_exist=`cat $ansible_path/plugins/action/net_base.py | grep "_NETCONF_SUPPORTED_PLATFORMS ="`
if [ "$ne_platform_exist" ]; then
    sed -i '/NETCONF_SUPPORTED_PLATFORMS =/d'  $ansible_path/plugins/action/net_base.py
    sed -i '/CLI_ONLY_MODULES =/a\_NETCONF_SUPPORTED_PLATFORMS = frozenset(["junos", "iosxr", "ne"])'  $ansible_path/plugins/action/net_base.py
fi

echo "ne Ansible library installed."