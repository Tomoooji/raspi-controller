# raspi-controller
Raspberry Piに接続したゲームコントローラーからESP32とシリアル通信してロボットを動かしたい  

# 構成
```text
raspi-controller/
├─ src/
│  ├─ config/                   # 設定ファイルフォルダ
│  │  ├─ DualShock4.json        # PS4コントローラー用
│  │  ├─ DualShock4_raspi.json  # PS4コントローラー用(ラズパイ版)
│  │  ├─ ElecomPad.json         # なんかあったエレコムのコントローラー用
│  │  ├─ ESP32.json             # ESP32との通信用(未使用)
│  │  └─ DS4window.json         # 画面描画用
│  ├─ ESP32_EchoTest/
│  │  └─ ESP32_EchoTest.ino     # シリアル通信のテストコード
│  ├─ requirements.txt          # ライブラリ一覧
│  ├─ main.py                   # メインプログラム(半完成)
│  ├─ test_checkcontroller.py   # コントローラー入力→画面描画のテストコード
│  ├─ checkButtons.py.          # コントローラーのボタン割り当てを確認するプログラム
│  ├─ GamepadInput.py           # コントローラーの入力受付用
│  ├─ checkButtons.py           # コントローラーのボタン割り当て確認用
│  ├─ GraphicalInterface.py     # コントローラー入力確認画面の描画用
│  └─ SerialCommunication.py    # マイコンとの通信用
├─ LICENSE                      # これでいいのかわかってない
└─ README.md                    # 説明用の文書
```
 今のところコントローラー入力の取得、画面の描画、シリアル通信をそれぞれGamepadInput.py,GraphicInterface.py,SerialCommunication.pyで行い、main.pyでそれを統合する予定。  
 各プログラムにはその機能を担うクラスと、単体テストを行うためのmain関数がある。main.pyは3つのクラスを継承したControllerクラスを作ってmainメソッドを呼べば動くようにする予定。test_checkcontroller.pyではこのうちシリアル通信機能を省いたものを結合テストその1として作成した(PCにて動作確認済み)。  
 configフォルダ内のjsonファイルはコントローラーのボタン割り当てや画面の構成、通信関連の設定とかを保存しておいて、読み込むファイルを変えることで実行環境への依存度が減ったらいいな...ってやつ。  
 ラズパイで動かしてみたところ、どうもコントローラーのボタンの割り当てとかがPCとやや異なるようで、別のjsonファイルを作って互換性をつけた。  
　通信も特に問題なかった(python,ESPともにループの中でポーリングするようにしてるが、実行速度差を考えると非同期処理を使った方が良さそう)

```mermaid
classDiagram
    Controller --|> Gamepad
    Controller --|> GraphicInterface
    Controller --|> SerialCommunicater
    Dualshock4_json --* Gamepad
    DS4window_json --* GraphicInterface
    ESP32_json --* SerialCommunicater
    class Gamepad{
        __init__()
        bool print_log
        Joystick gamepad
        dict gamepad_info
        bool is_connect
        connect()
        getInput()
        onButtonDown()
        onAxisMove()
        onHatTilt()
        convertHat()
    }
    class GraphicInterface{
        __init__()
        Surface screen
        dict window_info
        begin()
        draw()
    }
    class SerialCommunicater{
        bool print_log
        Serial serial
        dict serial_dict
        str send_message
        begin()
        receive()
        send()
    }
```
```mermaid
graph TD
    subgraph Files [設定ファイル]
        JA[(JSON A)]
        JB[(JSON B)]
        JC[(JSON C)]
    end

    subgraph Classes [クラス構成]
        A[Class A]
        B[Class B]
        C[Class C]
        D{Class D}
    end

    JA --> A
    JB --> B
    JC --> C

    A --- D
    B --- D
    C --- D

    note right of D: 3つを継承して<br/>ロジックを統合
```
graph TB
    %% 外部データ層
    subgraph DataLayer [Data Source]
        direction LR
        JSON_A[(config_a.json)]
        JSON_B[(config_b.json)]
        JSON_C[(config_c.json)]
    end

    %% クラス定義層
    subgraph LogicLayer [Base Classes]
        direction LR
        A[Class A<br/>'ConfigA Holder']
        B[Class B<br/>'ConfigB Holder']
        C[Class C<br/>'ConfigC Holder']
    end

    %% 統合・継承層
    subgraph IntegrationLayer [Main Logic]
        D{{Class D<br/>'The Orchestrator'}}
    end

    %% リレーション
    JSON_A -- "load as dict" --> A
    JSON_B -- "load as dict" --> B
    JSON_C -- "load as dict" --> C

    A -.->|Inheritance| D
    B -.->|Inheritance| D
    C -.->|Inheritance| D

    %% 注釈
    note_d[D handles unified logic using A, B, and C dicts]
    D --- note_d

    %% スタイル設定
    style D fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style DataLayer fill:#fff3e0,stroke:#ef6c00,stroke-dasharray: 5 5

 ---
 最終更新:2026-05-08