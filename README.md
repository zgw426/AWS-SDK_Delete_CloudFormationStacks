# AWS-SDK_Delete_CloudFormationStacks

- 指定した複数のCloudFormationのスタックを削除するスクリプト
- スタックの誤削除を防止するため、Dry-runと削除防止機能あり

## ファイル構成




## 実行時に表示されるメッセージ例

Name `test` で始まるスタック名を削除対象にした場合、ブロックリストに含まれるスタックは削除できない。

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

```
PS C:\Users\user01\test> python deleteCFnStacks.py -f test
Python Version Check [OK] : sys.version_info(major=3, minor=9, micro=5, releaselevel='final', serial=0)
[BLOCK(Date)] test001-subnet1 は、ブロックリストによりブロックされました
[BLOCK(StackName)] test001-vpc は、ブロックリストによりブロックされました
[Dry-run:OFF] スタック削除を実行します
2021-07-04 09:36:27 test001-sg
{'ResponseMetadata': {'RequestId': 'aaaaaaaa-7777-7777-7777-777777777777', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '77777777-7777-7777-7777-777777777777', 'content-type': 'text/xml', 'content-length': '212', 'date': 'Sun, 04 Jul 2021 12:08:34 GMT'}, 'RetryAttempts': 0}}
[LOG] CFn Delete Stack [test001-sg] start.
[LOG] CFn Delete Stack [test001-sg] end.
PS C:\Users\user01\test>
```
