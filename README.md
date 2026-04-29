# raspi-controller
Raspberry Piに接続したゲームコントローラーからESP32とシリアル通信してロボットを動かしたい  

# 構成
```text
raspi-controller/
├─ src/
│  ├─ config/                   # 設定ファイル
│  │  ├─ DualShock4.json        # PS4コントローラー用
│  │  ├─ ElecomPad.json         # なんかあったエレコムのコントローラー用
│  │  ├─ ESP32.json             # ESP32との通信用(未使用)
│  │  └─ laptop.json            # 画面描画用
│  ├─ requirements.txt          # ライブラリ一覧
│  ├─ main.py                   # メインプログラム(未完成)
│  ├─ test_checkcontroller.py   # コントローラーのボタン割り当て確認用テストコード
│  ├─ GamepadInput.py           # コントローラーの入力受付用
│  ├─ GraphicalInterface.py     # コントローラー入力確認用の画面描画用
│  └─ SerialCommunication.py    # マイコンとの通信用(未完成)
├─ LICENSE                      # これでいいのかわかってない
└─ README.md                    # 説明用の文書
```
 今のところコントローラー入力の取得、画面の描画、シリアル通信をそれぞれGamepadInput.py,GraphicInterface.py,SerialCommunication.pyで行い、main.pyでそれを統合する予定。  
 各プログラムにはその機能を担うクラスと、単体テストを行うためのmain関数がある。main.pyは3つのクラスを継承したControllerクラスを作ってmainメソッドを呼べば動くようにする予定。test_checkcontroller.pyではこのうちシリアル通信機能を省いたものを結合テストその1として作成した(PCにて動作確認済み)。  
 configフォルダ内のjsonファイルはコントローラーのボタン割り当てや画面の構成、通信関連の設定とかを保存しておいて、読み込むファイルを変えることで実行環境への依存度が減ったらいいな...ってやつ。  
 まだラズパイ上では実行してない。  