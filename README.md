# 目的
リクナビダイレクト(https://rikunabi-direct.jp/)の掲載企業をスクレイピングしてDBに登録します。
# 動機
リクナビダイレクトは検索ができず非常に不便だったため、DBにまとめて検索可能にしようと考えた.
#### DB
id, name, url, position, description, is_casual
INT TEXT  TEXT  TEXT        TEXT       BOOLEAN  