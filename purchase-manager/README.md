## PurchaseManager ##
1. [What is it?](#what-is-it)<br/>
2. [How to use](#how-to-use)<br/>
3. [Installation](#installation)<br/>

### What is it? ###
PurchaseManager is purchase manager (isn't it obvious?).<br/>
It uses CSV file to store items.<br/>
### How to use ###
```bash
pmanager [-p PATH] -m MONEY [-a | --add-item [-n | --name] [-pr | --price] [-pri | --priority] [-am | --amount]] [-rm | --remove [-n | --name]]
```
<br/>
You can find example of CSV file in examples directory.<br/>
First column is a name of item.<br/>
Second column is a price of item.<br/>
Third column is a priority of item.<br/>
Fourth column is an amount of item.<br/><br/>

Example:<br/>
```
Test item,20,7.8,2
```
### Installation ###
Run setup.py:<br/>
```bash
python setup.py install
```
<br/>
Then run install.sh:<br/>
```bash
./install.sh
```
