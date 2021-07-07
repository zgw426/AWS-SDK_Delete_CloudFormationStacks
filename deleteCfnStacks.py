import boto3
import json
import argparse
import sys
from datetime import datetime as dt

# python バージョン確認
if sys.version_info >= (3,8):
    print('Python Version Check [OK] : {0}'.format(sys.version_info) )
else:
    print('Python Version Check [NG] : {0}'.format(sys.version_info) )
    exit()

# オプション
helpStr = ''
helpStr += '-fオプションでEC2のNameタグをフィルタ(前方一致)'
parser = argparse.ArgumentParser(description=helpStr)
parser.add_argument('-f', '--Filter', required=True)
parser.add_argument('-d', '--DryRun', default=True)

blockList = "deleteCfnStacks_BlockList.json"
json_open = open(blockList, 'r', encoding='utf-8')
blklist = json.load(json_open)

args = parser.parse_args()
filterVal = args.Filter
dryrunFlg = args.DryRun

client = boto3.client('cloudformation')
stacks = client.list_stacks( StackStatusFilter=['CREATE_COMPLETE'] )
tgtlist = []
for stack in stacks['StackSummaries']:
    addFlg = 0
    blkKeyFlg = 0
    blkDateFlg = 0
    #print(stack['StackName'])
    #print(stack['CreationTime'])
    #print(str(stack['CreationTime']).split('.')[0])
    datetime = dt.strptime(str(stack['CreationTime']).split('.')[0] , '%Y-%m-%d %H:%M:%S')

    # 削除対象のスタックのみリスト(tgtlist)に登録
    if stack['StackName'].startswith(filterVal) == True:
        addFlg = 1
    for keyVal in blklist['StackName']:
        if stack['StackName'].startswith(keyVal) == True:
            blkKeyFlg = 1
            #if addFlg == 1:
            #    print("[BLOCK(StackName)] {0} は、ブロックリストによりブロックされました".format(stack['StackName']) )
            #addFlg = 0
    for dateVal in blklist['Date']:
        DateStart = dt.strptime(str(dateVal["Start"]) , '%Y-%m-%d %H:%M:%S')
        DateEnd   = dt.strptime(str(dateVal["End"]) , '%Y-%m-%d %H:%M:%S')
        if DateStart <= datetime <= DateEnd:
            blkDateFlg = 1
            #if addFlg == 1:
            #    print("[BLOCK(Date)] {0} は、ブロックリストによりブロックされました".format(stack['StackName']) )
    if blkKeyFlg + blkDateFlg > 0:
        if addFlg == 1:
            addFlg = 0
            if blkKeyFlg == 1:
                print("[BLOCK(StackName)] {0} は、ブロックリストによりブロックされました".format(stack['StackName']) )
            if blkDateFlg == 1:
                print("[BLOCK(Date)] {0} は、ブロックリストによりブロックされました".format(stack['StackName']) )

    if addFlg == 1:
        tgtStr = [ datetime, stack['StackName'] ]
        tgtlist.append( tgtStr )



## (念のため)削除対象のスタックを作成日時で降順にソート
tgtlist = sorted(tgtlist, key=lambda s: s[0], reverse=True)

# Dry-Run
if dryrunFlg == True:
    if len(tgtlist) > 0:
        print("[Dry-run:ON] スタック削除は実行しません")
        print("■-- 選定されたスタック --■\n作成日時 | スタック名")
        for stack in tgtlist:
            print("{0} {1}".format(stack[0], stack[1]) )
    else:
        print("\tTarget Stack not Found")
    print("■------------------------■")
else:
    print("[Dry-run:OFF] スタック削除を実行します")
    for stack in tgtlist:
        print("{0} {1}".format(stack[0], stack[1]) )
        res = client.delete_stack( StackName=stack[1] )
        print(res)
        
        print("[LOG] CFn Delete Stack [{0}] start.".format(stack[1]) )
        waiter = client.get_waiter('stack_delete_complete')
        waiter.wait(StackName=stack[1]) # スタック削除完了まで待つ
        print("[LOG] CFn Delete Stack [{0}] end.".format(stack[1])) # スタック完了後に実行される処理

