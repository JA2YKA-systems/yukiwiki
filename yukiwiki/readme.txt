NAME
    YukiWiki - 自由にページを追加・削除・編集できるWebページ構築CGI

        Copyright (C) 2000,2001 by Hiroshi Yuki.
        結城浩 <hyuki@hyuki.com>
        http://www.hyuki.com/
        http://www.hyuki.com/yukiwiki/

SYNOPSIS
        http://www.hyuki.com/yukiwiki/yukiwiki.cgi

DESCRIPTION
    YukiWiki（結城ウィキィ）は参加者が自由にページを追加・削除・編集できる
    不思議なWebページ群を作るCGIです。
    Webで動作する掲示板とちょっと似ていますが、
    Web掲示板が単にメッセージを追加するだけなのに対して、
    YukiWikiは、Webページ全体を自由に変更することができます。

    YukiWikiは、Cunningham & CunninghamのWikiWikiWebの
    仕様を参考にして独自に作られました。

    YukiWikiはPerlで書かれたCGIスクリプトとして実現されていますので、
    Perlが動作するWebサーバならば比較的容易に設置できます。

    あとはdbmopenが使える環境ならば設置できます(Version
    1.5.0以降ならdbmopenが使えなくても設置できます)。

    YukiWikiはフリーソフトです。 ご自由にお使いください。

設置方法
  入手

    YukiWikiの最新版は、 http://www.hyuki.com/yukiwiki/ から入手できます。

  ファイル一覧

        readme.txt      ドキュメント
        yukiwiki.cgi    YukiWiki本体
        yukiwiki.gif    ロゴ（カラー版）
        yukimono.gif    ロゴ（モノクロ版）
        jcode.pl        漢字コードライブラリ

  インストール

    1.  アーカイブを解きます。

    2.  yukiwiki.cgiのはじめの方にある設定を確認します。
        通常は何もしなくてよいですが、
        はじめは$touchfileを''にした方がよいでしょう。

    3.  yukiwiki.cgiとjcode.plを同じところに設置します。

    4.  Diff.pmの設置場所は、yukiwiki.cgiの始めのコメントを参照してください�
        B

    5.  サイズ0のyukiwiki.dbというファイルを設置します。
        （Perlシステムによってはyukiwiki.pag, yukiwiki.dir）

    6.  yukiwiki.cgiにブラウザからアクセスします。

  ファイル構成とパーミッション

            ファイル            パーミッション      転送モード
            +--- yukiwiki.cgi    755                ASCII
            +--- yukiwiki.gif    644                BINARY
            +--- yukimono.gif    644                BINARY
            +--- jcode.pl        644                ASCII
            +--- Algorithm/      755                (ディレクトリなので転送なし)
                 +--- Diff.pm    644                ASCII

        $dbmopen = 1; にした場合:
            +--- yukiwiki.db     666                BINARY
                (yukiwiki.pag, yukiwiki.dirの場合もあり）

        $dbmopen = 0; にした場合: (カレントディレクトリを777にしておく)
            +--- .               777                (ディレクトリなので転送なし)

データのバックアップ方法
    $dbmopen = 1;の場合は、 データはすべてyukiwiki.db(.dir, .pag)に入る。
    これをバックアップすればよい。

    $dbmopen = 0;の場合は、 yukiwikiというディレクトリができるので、
    これ以下をバックアップすればよい。

新しいページの作り方
    1.  まず、適当なページ（例えばFrontPage）を選び、
        ページの下にある「編集」リンクをたどります。

    2.  するとテキスト入力ができる状態になるので、 そこにNewPageのような単語
        （大文字小文字混在している英文字列） を書いて「保存」します。

    3.  保存すると、FrontPageのページが書き換わり、
        あなたが書いたNewPageという文字列の後ろに ?
        というリンクが表示されます。 この ?
        はそのページがまだ存在しないことを示す印です。

    4.  その ? をクリックすると新しいページNewPageができますので、
        あなたの好きな文章をその新しいページに書いて保存します。

    5.  NewPageページができるとFrontPageの ? は消えて、リンクとなります。

テキスト整形のルール
    *   連続した複数行はフィルされて表示されます。

    *   空行は段落`<p>'の区切りとなります。

    *   HTMLのタグは書けません。

    *   ''ボールド''のようにシングルクォート二つではさむと、
        ボールド`<b>'になります。

    *   '''イタリック'''のようにシングルクォート三つではさむと、
        イタリック`<i>'になります。

    *   ----のようにマイナス4つがあると、 水平線`<hr>'になります。

    *   行を*ではじめると、 大見出し`<h2>'になります。

    *   行を**ではじめると、 小見出し`<h3>'になります。

    *   行をマイナス-ではじめると、 箇条書き`<ul>'になります。
        マイナスの数が増えるとレベルが下がります（3レベルまで）

            -項目1
            --項目1-1
            --項目1-2
            -項目2
            -項目3
            --項目3-1
            ---項目3-1-1
            ---項目3-1-2
            --項目3-2

    *   コロンを使うと、 用語と解説文のリスト`<dl>'が書けます。

            :用語1:いろいろ書いた解説文1
            :用語2:いろいろ書いた解説文2
            :用語3:いろいろ書いた解説文3

    *   リンク

        *   LinkToSomePageやFrontPageのように、
            英単語の最初の一文字を大文字にしたものが
            二つ以上連続したものはYukiWikiのページ名となり、
            それが文章中に含まれるとリンクになります。

        *   http://www.hyuki.com/ のようなURLは自動的にリンクになります。

        *   二重の大かっこ[[ ]]でくくった文字列も、
            YukiWikiのページ名になります。
            大かっこの中にはスペースを含めてはいけません。
            日本語も使えます。

    *   行頭がスペースやタブで始まっていると、
        それは整形済みの段落`<pre>'として扱われます。
        プログラムの表示などに使うと便利です。

    *   行を > ではじめると、 引用文`<blockquote>'が書けます。
        >の数が多いとインデントが深くなります（3レベルまで）。

            >文章
            >文章
            >>さらなる引用
            >文章

更新履歴
    *   2002年3月1日、Version 1.6.7。

        パッケージにDiff.pmを同梱。

    *   2001年10月20日、Version 1.6.6。

        更新の衝突対策。 元ページの簡単なチェックサムを取っておき、
        更新前にチェックサムを比較する。
        修正個所はdigestという文字列を検索すれば分かる。
        本来はMD5などでちゃんとやった方がいいのだけれど。

        衝突時に表示されるメッセージなどは「極悪」さんのページを参考にした。

    *   2001年10月17日、Version 1.6.5。

        プレビュー画面で、更新ボタンを押したときに送信される
        メッセージの内容をinput要素のtype="hidden"を使って埋め込むのをやめる
        。 代わりに、textarea要素を使う。
        再プレビュー用にmyspecial_を導入。でもきれいな対策ではない。

    *   2001年8月30日、Version 1.6.4。

        URLでダイレクトにページ名を指定しても、
        $WikiNameと$BracketName以外のページを作れないようにした。
        (is_valid_nameとis_editable参照)。

    *   2001年8月30日、Version 1.6.3。

        RecentChangesを編集・再編集不可とした。
        編集不可ページは@uneditableにページ名を入れる。

    *   2001年2月25日、Version 1.6.1, 1.6.2。

        差分機能のバグ修正。 do_previewで'>'が扱えないバグを修正
        （ユーザからの指摘）。

    *   2001年2月22日、Version 1.6.0。 差分機能を実装した。

    *   2001年2月19日、Version 1.5.4。
        画像ファイルへのリンクは画像にしてみた。

    *   2001年2月19日、Version 1.5.3。
        RecentChangesの中に削除したページがあるのをやめた。 use
        strict;で引っかかる部分を少し整理(完全ではない)。

    *   2001年2月16日、Version 1.5.2。
        textareaに表示およびプレビューする前に < や > を &lt; や &gt;
        に変換した (do_preview, editpage, print_preview_buttons)。

    *   2000年12月27日、Version 1.5.1。 プレビュー画面を整理した。

    *   2000年12月22日、Version 1.5.0。 全体的にずいぶん書き直した。
        一覧を別途作成するようにした(do_list)。
        書き込む前に確認画面を出すようにした(do_preview)。
        テキストの書き方を編集画面に入れた(do_edit, do_reedit)。
        WhatsNew→RecentChanges、TopPage→FrontPageに変更した。

    *   2000年12月20日、Version 1.1.0。
        tieを利用して、dbmopenが使えない場合でも動作するように修正。
        利用者の1人である「極悪」さんから
        送っていただいたコードを元にしています。

    *   2000年9月5日、Version 1.0.2。 <body color=...> → <body bgcolor=...>
        利用者からの指摘による。感謝。

    *   2000年8月6日、Version 1.0.1を公開。 C
        MAGAZINE（ソフトバンクパブリッシング）
        2000年10月号連載記事向け公開版。 [[ ]]
        の最後が「望」のようにシフトJISで 0x5Dになる場合の回避を行なった。

    *   2000年8月5日、Version 1.0.0を公開。

    *   2000年7月23日、Version 0.82を公開。 編集時のリンクミス。
        <textarea>の属性変更。

    *   2000年7月22日、Version 0.81を公開。 ロゴを組み込む。

    *   2000年7月21日、Version 0.80を公開。 PODをCGI中に書き込む。

    *   2000年7月19日、Version 0.70を公開。
        '''イタリック'''や、--、---、>>、>>>などを実装。

    *   2000年7月18日、Version 0.60を公開。 *太字*を''太字''に変更

    *   2000年7月17日、Version 0.50を公開。

    *   2000年7月17日、さらにいろいろ追加する。

    *   2000年7月16日、いろいろ追加。

    *   2000年7月15日、公開。

TODO
        - テキスト表示モード
        - Charsetを明示。
        - textarea中の閉じタグ対応
        - メニューの英語表記付記
        - プレビューのボタンで、mymsgをinputのvalueに入れているが、改行をそのままvalueにいれてはいけないのではないか。
        - 「再編集」の機能はブラウザの back で充分ではないか。プレビューはもっとシンプルに。
        - ページタイトル（Wikiname）が検索にかかるようにする。
        - InterWiki風の機能「URLを隠しつつ、リンクを張る」

作者
        Copyright (C) 2000 by Hiroshi Yuki.
        結城浩 <hyuki@hyuki.com>
        http://www.hyuki.com/
        http://www.hyuki.com/yukiwiki/

    質問、意見、バグ報告は hyuki@hyuki.com にメールしてください。

配布条件
    YukiWikiは、 GNU General Public Licenseにて公開します。

    YukiWikiはフリーソフトです。 ご自由にお使いください。
    自分好みのYukiWikiが作れるようにシンプルにしてあります。

謝辞
    本家のWikiWikiを作ったCunningham & Cunningham, Inc.に 感謝します。

    YukiWikiを楽しんで使ってくださる ネット上の方々に感謝します。

    YukiWikiのロゴをデザインしてくださった橋本礼奈さん
    http://city.hokkai.or.jp/~reina/ に感謝します。

    tieを使った版の元になるコードを送ってくださった
    「極悪」さんに感謝します。

参照リンク
    *   YukiWikiホームページ http://www.hyuki.com/yukiwiki/

    *   本家のWikiWiki http://c2.com/cgi/wiki?WikiWikiWeb

    *   本家のWikiWikiの作者(Cunningham & Cunningham, Inc.) http://c2.com/

    *   YukiWikiのロゴデザインをしてくださった橋本礼奈さんのページ
        http://city.hokkai.or.jp/~reina/

