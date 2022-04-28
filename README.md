# book-bingo-fastapi
マスが数字の代わりに本になっているビンゴ.

## 目的
読書をしない人が増えているので, ゲーム感覚で読書の習慣を身につけてもらう.

## 使い方
1. ビンゴカードを作成する. 本のジャンルなどを指定できる. カードは複数枚作成することができる.
2. 各マスに書かれた本のうち, 好きな本を読む.
3. 読み終わったら, マスをクリックして感想を書くと, 穴を開けることができる.
4. ビンゴになったカードを見ることができる.

## 使用技術
* FastAPI
* Docker
* [Streamlit](https://streamlit.io/)
* [楽天ブックス書籍検索API](https://webservice.rakuten.co.jp/documentation/books-book-search)
