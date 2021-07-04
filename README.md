# AWS-SDK_Delete_CloudFormationStacks

- 指定した複数のCloudFormationのスタックを削除するスクリプト
- スタックの誤削除を防止するため、Dry-runと削除防止機能あり

## ファイル構成

|ファイル名|概要|
|---|---|
|deleteCFnStacks.py|スクリプト本体|
|deleteCfnStacks_BlockList.json|削除しないスタックの条件を設定|

## スクリプト実行方法

```
PS C:\Users\user01\test> python deleteCFnStacks.py -f {削除するスタックのName(前方一致)} -d False|True
```

|オプション|概要|
|---|---|
|`-f`|スタックの絞り込みオプション。削除するスタックのNameの値を指定(前方一致)|
|`-d`|`False`を指定するとDry-runが無効になりスタック削除処理が実行される。指定しない場合は、Dry-runが有効になる|

スクリプト実行例）Nameが `test` から始まるスタックを削除する

```
PS C:\Users\user01\test> python deleteCFnStacks.py -f test -d False
```

スクリプト実行例）Nameが `test` から始まるスタックを確認する（スタック削除しない）

```
PS C:\Users\user01\test> python deleteCFnStacks.py -f test
```

## ブロックリストの設定方法

- `deleteCfnStacks_BlockList.json`により、削除しないスタックを設定できる。
- `deleteCfnStacks_BlockList.json`は、`StackName`,`Date`の2通りの設定方法がある。
- `StackName`は、Nameタグの文字列で前方一致するスタックが削除不可の対象に含まれる。
- `Date`は、スタックの作成時刻が `Start`,`End`の間の期間にあるスタックが削除不可の対象に含まれる。
- `deleteCfnStacks_BlockList.json`の記載例

```
{
    "StackName" : 
        [
            "hoge",
            "fuga"
        ],
    "Date" : 
        [
            {"Start":"2021-07-05 09:35:00","End":"2021-07-05 09:35:59","note":"メモ１"},
            {"Start":"2020-07-04 00:00:00","End":"2020-08-04 23:59:59","note":"メモ２"}
        ]
}
```


## 実行時に表示されるメッセージ例

Name `test` で始まるスタック名を削除対象にした場合、ブロックリストに含まれるスタックは削除できない。

- 例１）
  - ブロックリスト(Date)により、`test001-subnet1`スタックが削除されず
  - ブロックリスト(StackName)により、`test001-vpc`スタックが削除されず
  - Dry-runが有効なため、`test001-sg`スタックは削除されず

```
PS C:\Users\user01\test> python deleteCFnStacks.py -f test
Python Version Check [OK] : sys.version_info(major=3, minor=9, micro=5, releaselevel='final', serial=0)
[BLOCK(Date)] test001-subnet1 は、ブロックリストによりブロックされました
[BLOCK(StackName)] test001-vpc は、ブロックリストによりブロックされました
[Dry-run:ON] スタック削除は実行しません
■-- 選定されたスタック --■
2021-07-04 09:36:27 test001-sg
■----------------------■
PS C:\Users\user01\test>
```

- 例２）
  - ブロックリスト(Date)により、`test001-subnet1`スタックが削除されず
  - ブロックリスト(StackName)により、`test001-vpc`スタックが削除されず
  - Dry-runが無効なため、`test001-sg`スタックを削除

```
PS C:\Users\user01\test> python deleteCFnStacks.py -f test -d False
Python Version Check [OK] : sys.version_info(major=3, minor=9, micro=5, releaselevel='final', serial=0)
[BLOCK(Date)] test001-subnet1 は、ブロックリストによりブロックされました
[BLOCK(StackName)] test001-vpc は、ブロックリストによりブロックされました
[Dry-run:OFF] スタック削除を実行します
2021-07-04 09:36:27 test001-sg
{'ResponseMetadata': {'RequestId': 'aaaaaaaa-7777-7777-7777-777777777777', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'aaaaaaaa-7777-7777-7777-777777777777', 'content-type': 'text/xml', 'content-length': '212', 'date': 'Sun, 04 Jul 2021 12:08:34 GMT'}, 'RetryAttempts': 0}}
[LOG] CFn Delete Stack [test001-sg] start.
[LOG] CFn Delete Stack [test001-sg] end.
PS C:\Users\user01\test>
```
