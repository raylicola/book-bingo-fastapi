# 読書推進BINGO
マスが数字の代わりに本になっているビンゴ.

## 目的
普段読まない本に興味を持ってもらう.

## 使い方
1. ユーザー登録
    * ユーザー登録ページを開き,ユーザー名を登録してください.

<img width="500" alt="スクリーンショット 2022-05-04 17 15 29" src="https://user-images.githubusercontent.com/76393580/166646637-190d5f8b-1fdd-45a6-adf5-f1e1c762a495.png">


2. ログイン
    * ログインページを開き, 先ほど登録したユーザー名でログインしてください.

<img width="500" alt="スクリーンショット 2022-05-04 17 15 53" src="https://user-images.githubusercontent.com/76393580/166646654-98326513-d945-4af3-9263-7620e28a9ed1.png">


3. ビンゴカードの作成
    * ビンゴページを開いてください.
    * サイドバーのセレクトボックスから好きなジャンルを選び, 'カードを作成'をクリックする.

<img width="123" alt="スクリーンショット 2022-05-04 17 16 13" src="https://user-images.githubusercontent.com/76393580/166647296-7300f940-3a5f-4778-b7ee-59d079239b87.png">　　<img width="150" alt="スクリーンショット 2022-05-04 17 34 35" src="https://user-images.githubusercontent.com/76393580/166647673-506ebd75-db03-4ddf-83e2-aed6a33bfb13.png">



4. 9つのマスに本が表示されるので,好きな本を読む.
5. 読み終わったら, マスのチェックボックスをクリックする.

<img width="500" alt="スクリーンショット 2022-05-04 17 17 50" src="https://user-images.githubusercontent.com/76393580/166645770-952f320b-1bf0-440d-9e4e-076f917de6a5.png">

6. ビンゴになるとサイドハーにボタン('ビンゴです')が表示されるので,クリックするとそのカードをビンゴ済にできる.
    * ビンゴできた枚数が記録されます.
    * ビンゴになる前にカードを削除して新しく作り直すこともできます. 'カードを削除'のボタンをクリックしてください.


<img width="500" alt="スクリーンショット 2022-05-04 17 42 40" src="https://user-images.githubusercontent.com/76393580/166648822-fe62db86-2392-4396-8619-b7fb61cd2638.png">

### ヘルプ
カード作成, 削除後は自動でリロードが行われません. 一度他のカードのページを選択するなどしてください.

## 使用技術
* Docker
* FastAPI
* [Streamlit](https://streamlit.io/)
* [楽天ブックス書籍検索API](https://webservice.rakuten.co.jp/documentation/books-book-search)
