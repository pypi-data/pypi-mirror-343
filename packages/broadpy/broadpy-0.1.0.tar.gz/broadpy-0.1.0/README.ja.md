# BRoaDpy

BRoaD I/III のPython用APIクラス

* プログラム言語： Python 3.9+
* ライセンス: MIT License

他の言語で読む場合は: [English](README.md), [日本語](README.ja.md)

![BRoaDpy](src/broadpy/docs/images/broadpy.png)


## BRoaDとは

BRoaDはBee Beans Technologiesで開発された実験用のデジタル信号処理機器です。
BRoaDを使うと分配や同期信号ロジックを実験室で様々なデジタル信号ロジックを簡単に作成することができます。


BRoaDには、[BRoaD I](https://www.bbtech.co.jp/products/broad-1-new/) 、 [BRoaD III](https://www.bbtech.co.jp/products/broad-v3/)　という2つのタイプがあります。


## BRoaDpyとは

BRoaDは、GUIアプリケーション(BRoaD application)により、デジタル信号処理を定義することができます。
BRoaDpyはPythonのプログラミングインタフェースで、BRoaD Applicationで作成、BRoaD本体にダウンロードされたロジックを使って得られるカウンタ値の読み出しやユーザ制御信号を操作することができます。

## インストール

PyPIまたはGitHubからインストールできます。

```
pip install broadpy # from PyPI
pip install git+https://github.com/BeeBeansTechnologies/BRoaDpy.git # from GitHub
```

ローカルにコピーしたソースコードからもインストールできます。

```
git clone https://github.com/BeeBeansTechnologies/BRoaDpy.git
cd ./BRoaDpy
pip install .
```

##  使い方
BRoaD Iを対象とする場合は`BRoaD1`クラスを、BRoaD IIIを操作する場合は`BRoaD3`クラスを使用します。

```
from broadpy import BRoaD1

mybroad = BRoaD1('192.168.10.16', 24, 4660) # 使用する機器に合わせて、BRoaD1クラスまたはBRoaD3クラスを使用します。
mybroad.connect() # BRoaDとの接続を初期化します。
```

`disconnect`で、使用を終了します。


### Measure Counter
MeasureCounterの制御(Connect, Start, Stop, Disconnect)を、`broadpy`を通じて実行することができます。
`connect_measure_counter`でBRoaDとのTCP接続を確立し、データを受信すると`set_counter_function`、`set_raw_function`で指定した関数を実行します。
* `set_counter_function` : MeasureCounterの番号と測定値を引数にとります。
    * MeasureCounterのSRC設定がGate Time, True Timeの場合は、渡される測定値はnsecとなります。
    * MeasureCounterのSRC設定がそれ以外の場合は、渡される測定値はパルス数のカウントとなります。
* `set_raw_function` : 受信した生データ(8バイト)を引数にとります。

```
def sample_counter_function(id, count):
    """
    Callback function to receive decoded ID and counter value
    """
    print(f"counter {id}:{count}")

def sample_raw_function(counter_byte:bytes ):
    """
    Callback function to receive raw byte data
    """
    print(f"counter bytes : {counter_byte.hex()}")

mybroad.connect_measure_counter() # BRoaDとのTCP接続を確立
mybroad.set_counter_function(sample_counter_function) # TCPデータ受信時に実行する関数を指定
mybroad.set_raw_function(sample_raw_function) # TCPデータ受信時に実行する関数を指定(生データ)
```

MeasureCounterのGate設定がUser Controlになっているものに対しては、`start_read`、`stop_read`で測定の開始・終了を制御できます。
```
mybroad.start_read(0) # MeasureCounter:0の測定を開始します。
mybroad.stop_read(0) # MeasureCounter:0の測定を終了します。TCPデータがBRoaDから送信され、set_counter_function、set_raw_functionで指定した関数が実行されます。
```

`disconnect_measure_counter`で、TCP接続を終了します。

```
mybroad.disconnect_measure_counter()
```


### User Control
BRoaD IIIの機能である`User Control`について、`broadpy`を通じて指定した入力のON/OFFの読み書きを行うことができます。

```
from broadpy import BRoaD3

mybroad = BRoaD3('192.168.10.16', 24, 4660) # UserControl機能は、BRoaD IIIにのみ搭載されています。
mybroad3.connect()
mybroad3.user_control_value = mybroad3.read_user_control(0) # 現在のINPUT0のUser Control(ON:True, OFF:False)をBRoaDから読み出します
mybroad3.user_control(0, True) # INPUT0のUser Controlの値をON:True, OFF:False)に書き換えます

```

## バージョン履歴

0.1.0 - 初回リリース