SELinux Type Enforcement Lookup (Ver 0.1.1)
===

SELinux Type Enforcement上で、プロセスがパーミッションを持つファイルを、本ツールは探し当てます。

このツールがない時は、対象のプロセスがアクセスできるファイルを探す出すのに苦労しました。

しかし現在では、簡単に、速く、取得できるのです！

# Description
SELinuxを設定する際、あなたはどうやってシステムの状態を調査しますか？
もしプロセスがアクセスできるファイルを知りたい場合、
あなたはsesearchやseinfo、semanageといったツールを組み合わせて用い、
以下の手順を踏むことになるでしょう。
1) プロセスのドメインをソースとして持つルールはどれか？
1) ルールのターゲットドメインをもつファイルコンテキストはどれか？
1) ファイルコンテキストのパターンにマッチするファイルはどれか？

加えて、以下も考慮せねばなりません。
1) ドメインはアトリビュート、タイプのどちらに属するか？
1) アトリビュートの場合、そのアトリビュートに含まれるタイプはなにか？
1) タイプの場合、そのタイプが属するアトリビュートはあるか？
1) アトリビュートとタイプがSEPolicyルールとファイルコンテキストにどのように関わっているか？

本ツールはこの煩雑さからあなたを解放します。

あなたは対象プロセスのドメインといくつかのオプションを渡すだけです。
あとは以下のように探索してくれます。
1) 指定したドメインをソースドメインとするポリシールールを探索
1) ルールのターゲットタイプをラベルに持つファイルコンテキストを探索
1) ファイルコンテキストのパターンに一致するファイルを探索

もちろんアトリビュートも考慮されます。

このように、SELinux Type Enforcement下でプロセスがパーミッションをもつファイルを探し出すことができるのです。

# DEMO
'httpd_t'ドメインのプロセスが読み書きできるファイルの一覧を取得してみましょう。
```
$ sudo python selinux-te-lookup.py httpd_t --perm read write --stdout
File-Context-Pattern,File-Context-Target-Type,File-Context-Label,Matched-File-Path,File-Type,File-Label,SAME-SELinux-Type
/dev/shm,directory,system_u:object_r:tmpfs_t:s0,/dev/shm,d,system_u:object_r:tmpfs_t:s0,OK
/dev/tty,character device,system_u:object_r:devtty_t:s0,/dev/tty,c,system_u:object_r:devtty_t:s0,OK
/dev/full,character device,system_u:object_r:null_device_t:s0,/dev/full,c,system_u:object_r:null_device_t:s0,OK
/dev/zero,character device,system_u:object_r:zero_device_t:s0,/dev/zero,c,system_u:object_r:zero_device_t:s0,OK
--omit--
```

# OUTPUT
##FILE 
--stdoutオプションがない場合、結果は”result.csv"ファイルに出力します。

## CSV COLUMNS
１レコードはファイルコンテキストとそれにマッチしたファイルを記録しています。

- File-Context-Pattern
   - ファイルパスにマッチしたファイルコンテキストの正規表現パターン

- File-Context-Target-Type
  - ファイルタイプに一致したファイルコンテキストのターゲットタイプ

- File-Context-Label
  - ファイルコンテキストのラベル

- Matched-File-Path
  - ファイルコンテキストのパターンにマッチしたファイルのパス

- File-Type
  - ファイルタイプ: ファイル(f), ディレクトリ(d), シンボリックリンク(l) など

- File-Label
  - ファイルのSELinuxセキュリティコンテキストラベル

- SAME-SELinux-Type
  - ファイルコンテキストとファイルのタイプが同じかどうか

# Requirements
- policycoreutils-python
- setroubleshoot-server
- setools-console
- python2


# INSTALL
 圧縮ファイルをダウンロードし、任意のフォルダに展開してください。
 

# Usage
- 'httpd_t' ドメインのプロセスがパーミッションをもつファイルを取得
```
sudo python selinux-te-lookup.py 'httpd_t'
```

- 'httpd_t' ドメインのプロセスが読み書きできるファイルを取得
```
sudo python selinux-te-lookup.py 'httpd_t' --perm write read
``` 

- 'httpd_t' ドメインのプロセスがパーミッションをもつ/usr以下のファイルを取得
```
sudo python selinux-te-lookup.py 'httpd_t' --root /usr
```

- /procディレクトリを検索から除外
```
sudo python selinux-te-lookup.py 'httpd_t' --prune /proc
```

- 'httpd_t' ドメインのプロセスがパーミッションをもつ’tmp_t'ドメインのファイルを取得
```
sudo python selinux-te-lookup.py 'httpd_t' --target 'tmp_t'
```

- 'httpd_t' ドメインのプロセスがパーミッションをもつディレクトリを取得
  - --class
    - file: file
    - dir: directory
    - lnk_file: synbolic link
    - sock_file: socket
```
sudo python selinux-te-lookup.py 'httpd_t' --class 'dir'
```

 
- 'httpd_t' ドメインのプロセスがパーミッションをもつファイルのうち、ファイルコンテキストとファイルのタイプが一致した物のみ取得
```
sudo python selinux-te-lookup.py 'httpd_t' --only-ok
```

- ファイルのタイプがファイルコンテキストのものから変更されており、'httpd_t'ドメインがアクセスできなくなっている物のみ取得
```
sudo python selinux-te-lookup.py 'httpd_t' --only-ng
```

- 標準出力に結果を表示
```
sudo python selinux-te-lookup.py 'httpd_t' --stdout
```

## INI FILE
config.iniには上記オプションを記載できます。例えば、常に/procディレクトリを除外したければ、次のように記載します。
```
[settings]
prune = /proc
```

config.iniとコマンドライン引数が重複して設定されている場合は、コマンドライン引数が優先されます。

# Contribution
TODO


# License
Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.

Licensed under the MIT License.
You may obtain a copy of the License at

* https://opensource.org/licenses/MIT

This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OF ANY KIND.
