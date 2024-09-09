#!/usr/pkg/bin/perl
use CGI::Carp 'fatalsToBrowser';
# use strict;
#
# yukiwiki.cgi - Yet another WikiWikiWeb clone.
#
# Copyright (C) 2000,2001 by Hiroshi Yuki.
# <hyuki@hyuki.com>
# http://www.hyuki.com/yukiwiki/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# $Id: yukiwiki.cgi 1.55 2001/12/27 17:09:40 yuki Exp yuki $
##############################
# 差分機能のためにAlgorithm::Diffというモジュールを使っています。
# ファイル名はDiff.pmです。
# 以下の2行は、yukiwiki.cgiがあるディレクトリ(.)の下に
# Algorithmというディレクトリがあり、
# その中にDiff.pmというファイルがあることを前提としています。
# YukiWikiを設置するサーバにすでに
# Algorithm::Diffがインストールされている場合には、
# 以下の2行をコメントアウトします。
use lib ".";
use Algorithm::Diff qw(traverse_sequences);
##############################
my $version = "1.6.7";
##############################
# 単独テストのときには 1 にする。
my $testing = 0;
##############################
# 漢字ライブラリ
my $jcodelib = 'jcode.pl';
##############################
# 保存・表示の漢字コード
my $kanjicode = 'sjis';     # 'sjis' 'euc'
my $charset = 'Shift_JIS';  # 'Shift_JIS' 'EUC-JP'
##############################
# dbmopenが使えるなら1、使えないなら0
my $dbmopen = 0;
##############################
# データベース名（.pag, .dir, .dbなどは不要）
# $dbmopen = 1のときはデータベース名、
# $dbmopen = 0のときはディレクトリ名になる。
my $dbname = './yukiwiki';
my $diffdbname = './yukidiff';
##############################
# 修正者の氏名（自由に変更してください）
my $modifier = 'Hiroshi Yuki';
##############################
# 修正者のWebページ（自由に変更してください）
my $modifierlink = 'http://www.hyuki.com/';
##############################
# このページのURL
my $thisurl = 'yukiwiki.cgi';
##############################
# 開始ページ名
my $toppage = 'FrontPage';
##############################
# 最終更新ページ名
my $whatsnew = 'RecentChanges';
##############################
# 最終更新に掲載するページ数
my $maxnew = 50;
##############################
# アイコンファイル名（カラー版）
my $iconfile = 'yukiwiki.gif';
##############################
# アイコンファイル名（モノクロ版）
# my $iconfile = 'yukimono.gif';
##############################
# ページを変更したときにtouchするファイル（''なら何もしない）
my $touchfile = 'touch.txt';
##############################
# プレビュー用の背景色
my $preview_color = '#FFCCCC';
##############################
# 全ページのスタイル
my $style = <<'EOD';
pre, dl, ul, ol, p, blockquote { line-height:120%; }
a { text-decoration: none; }
a:link { color: #0000FF; background-color: #FFFFFF; }
a:visited { color: #9900CC; background-color: #FFFFFF; }
a:hover { text-decoration: underline; }
EOD
##############################
# テキスト入力部分の大きさ
my $cols = 80;
my $rows = 20;
##############################
my %form = ();
my %database = ();
my %diffbase = ();
my $diff_text = '';
my @diff_added = ();
my @diff_deleted = ();
my $msgrefA;
my $msgrefB;
##############################
# 編集不可ページ名一覧
my @uneditable = ( $whatsnew );
##############################
# リンク用の正規表現
# YukiWikiのリンクは2種類ある。
# 
# (1) WikiName (RecentChangesとかFrontPageのようなもの)
# (2) BracketName ([[結城浩]]とか[[トラブルシュート]]のようなもの)
#
# ※シフトJISの2バイト目には ']' が来うるので、
# 文字']'を1つ多くとるようにしている。
#
my $WikiName = '([A-Z][a-z]+([A-Z][a-z]+)+)';
my $BracketName = '\[\[([^>\s]+?\]?)\]\]';

# アイコン部分のタグ
my $IconTag = <<"EOD";
<a href="http://www.hyuki.com/yukiwiki/"><img src="$iconfile"
 border="0" width="80" height="80" alt="[YukiWiki]" /></a>
EOD

require "$jcodelib";

&init_form($kanjicode);

# 動作テスト用
if ($testing) {
    %form = (
        # 'mycmd' => 'write',
        'mycmd' => 'read',
        #'mycmd' => 'search',
        #'mycmd' => 'edit',
        'mymsg' => <<"EOD",
はじめまして。
これからいろいろ書き込みますね。
LinkPageも見てください。
TestPageはどうでしょうか。
どうぞよろしく。
http://www.hyuki.com/
[[結城浩]]
EOD
        'mypage' => '<結城浩>',
        'myword' => '結',
        # '3C8C8B8FE98D5F3E' => '',
        # 'TestPage' => '',
    );
}
&main;
exit(0);

# メイン
sub main {
    &normalize_form;
    if ($dbmopen) {
        if (!dbmopen(%database, $dbname, 0666)) {
            &print_error("(dbmopen) $dbname が作れません。");
        }
    } else {
        if (!tie(%database, "YukiWikiDB", $dbname)) {
            &print_error("(tie error)");
        }
    }

    # myspecial対応
    foreach (keys %form) {
        if (/^myspecial_(.*)/) {
            $form{mycmd} = $1;
            last;
        }
    }

    if ($form{mycmd} eq 'read') {
        &do_read;
    } elsif ($form{mycmd} eq 'preview') {
        &do_preview;
    } elsif ($form{mycmd} eq 'write') {
        &do_write;
    } elsif ($form{mycmd} eq 'edit') {
        &do_edit;
    } elsif ($form{mycmd} eq 'reedit') {
        &do_reedit;
    } elsif ($form{mycmd} eq 'search') {
        &do_search;
    } elsif ($form{mycmd} eq 'list') {
        &do_list;
    } elsif ($form{mycmd} eq 'diff') {
        &do_diff;
    } else {
        $form{mypage} = $toppage;
        &do_read;
    }
    if ($dbmopen) {
        dbmclose(%database);
    } else {
        untie(%database);
    }
}

# ページの表示
sub do_read {
    my $page_name = $form{mypage};
    my $percent_name = &encode_percent($page_name);
    &print_header($page_name);
    print qq|<h1>$IconTag<a href="$thisurl?mycmd=search&myword=$percent_name">$page_name</a></h1>\n|;
    &print_toolbar($page_name);
    print &convert_html(&get_page($page_name));
    &print_footer;
}

# ページの編集
sub do_edit {
    if (not &is_editable($form{mypage})) {
        # 編集不可ページは表示のみ
        &do_read;
        return;
    }
    &editpage(&get_page($form{mypage}));
}

# ページの再編集
sub do_reedit {
    if (not &is_editable($form{mypage})) {
        # 編集不可ページは表示のみ
        &do_read;
    } else {
        &editpage($form{mymsg});
    }
}

sub editpage {
    my $page_msg = shift;
    my $page_name = $form{mypage};
    my $digest = &calc_message_digest($page_msg);
    &print_header($page_name);
    print qq|<h1>$IconTag${page_name}の編集</h1>\n|;
    &print_toolbar($page_name);
    $page_msg = &escape($page_msg);
    print <<"EOD";
<form action="$thisurl" method="post">
<input type="hidden" name="mycmd" value="preview">
<input type="hidden" name="mypage" value="$page_name">
<input type="hidden" name="mydigest" value="$digest">
<textarea cols="$cols" rows="$rows" name="mymsg" wrap="virtual">$page_msg</textarea><br>
<input type="submit" value="プレビュー">
</form>
<hr>
<h3>テキスト整形のルール</h3>

<p>通常は入力した文字がそのまま出力されますが、
以下のルールに従ってテキスト整形を行うことができます。</p>

<ul>
<li>
空行は段落の区切りとなります。

<li>
HTMLのタグは書けません。

<li>
''ボールド''のようにシングルクォート二つではさむと、ボールドになります。

<li>
'''イタリック'''のようにシングルクォート三つではさむと、イタリックになります。

<li>
----のようにマイナス4つがあると、水平線になります。

<li>
*を行頭に書くと大見出しになります。

<li>
**を行頭に書くと小見出しになります。

<li>
-を行頭に書くと箇条書きになります。- -- --- の3レベルがあります。

<li>
:を行頭に書くと用語と解説文が作れます。

<pre>
    :用語1:いろいろ書いた解説文1
    :用語2:いろいろ書いた解説文2
    :用語3:いろいろ書いた解説文3
</pre>

<li>
http://www.hyuki.com/ のようなURLは自動的にリンクになります。

<li>
YukiWikiのように大文字小文字を混ぜた英文字列を書くと、
YukiWikiのページ名になります。

<li>
[[結城浩]]のように二重の大かっこ[[ ]]でくくった文字列を書くと、
YukiWikiのページ名になります。
大かっこの中にはスペースを含めてはいけません。
日本語も使えます。

<li>
行頭がスペースで始まっていると、
その段落は整形済み扱われます。
プログラムを書き込むときに使うと便利です。

<li>
> を行頭に書くと、
引用文が書けます。
>の数が多いとインデントが深くなります（3レベルまで）。

</ul>
EOD
    &print_footer;
}

# ページの検索
sub do_search {
    if ($form{myword}) {
        &print_header('検索結果');
        print qq|<h1>$IconTag$form{myword}の検索結果</h1>\n|;
        &print_toolbar();
        print qq|<ul>\n|;
        my $count = 0;
        foreach my $page_name (sort keys %database) {    # sortするのは無謀かな
            if ($database{$page_name} =~ /\Q$form{'myword'}\E/) {
                my $encoded = &encode_percent($page_name);
                print qq|<li><a href="$thisurl?mycmd=read&mypage=$encoded">$page_name</a>\n|;
                $count++;
            }
        }
        print qq|</ul>\n|;
        if ($count > 0) {
            print qq|<p><b>$form{myword}</b>を含むページは、上に示す<b>$count</b>ページです。</p>\n|;
        } else {
            print qq|<p><b>$form{myword}</b>を含むページは見つかりません。</p>\n|;
        }
    } else {
        &print_header('単語検索');
        print qq|<h1>$IconTag単語検索</h1>\n|;
        &print_toolbar();
    }
    print <<"EOD";
<p>
<form action="$thisurl" method="post">
<input type="hidden" name="mycmd" value="search">
<input type="text" name="myword" size="20" value="$form{myword}">
<input type="submit" value="単語検索">
</form>
</p>
EOD
    &print_footer;
}

# ページの一覧
sub do_list {
    &print_header('ページ一覧');
    print qq|<h1>$IconTag ページ一覧</h1>\n|;
    &print_toolbar();
    print qq|<ul>\n|;
    foreach my $page_name (sort keys %database) {    # sortするのは無謀かな
        my $encoded = &encode_percent($page_name);
        print qq|<li><a href="$thisurl?mycmd=read&mypage=$encoded">$page_name</a>\n|
    }
    print qq|</ul>\n|;
    &print_footer;
}

# プレビュー
sub do_preview {
    my $page_name = $form{mypage};
    my $escapedmsg = &escape($form{mymsg});
    &print_header($page_name);
    print qq|<h1>$IconTag${page_name}のプレビュー</h1>\n|;
    &print_toolbar($page_name);
    # local $percent_name = &encode_percent($page_name);
    print qq|<p>以下のプレビューを確認して、よければページ下部のボタンで更新してください。</p>\n|;
    if ($form{mymsg}) {
        print qq|<table width="100%" bgcolor="$preview_color" ><tr><td>\n|;
        # print &convert_html($escapedmsg);
        print &convert_html($form{mymsg});
        print qq|</td></tr></table>\n|;
    } else {
        print qq|<p>（ページの内容は空です。更新するとこのページは<b>削除</b>されます。）</p>\n|;
    }
    &print_preview_buttons($page_name, $escapedmsg, $form{mydigest});
    &print_footer;
}

# プレビュー用のボタン表示(textareaも表示)
sub print_preview_buttons {
    my ($page_name, $escapedmsg, $digest) = @_;
    print <<"EOD";
    <form action="$thisurl" method="post">
    <textarea cols="$cols" rows="$rows" name="mymsg" wrap="virtual">$escapedmsg</textarea>
    <br />
    <input type="hidden" name="mypage" value="$page_name">
    <input type="hidden" name="mydigest" value="$digest">
    <input type="submit" name="myspecial_preview" value="再度プレビュー">
    <input type="submit" name="myspecial_write" value="ページの更新">
    </form>
EOD
}

# 書き込む
sub do_write {
    if (not &is_editable($form{mypage})) {
        # 編集不可ページは表示のみ
        &do_read;
        return;
    }

    my $page_name = $form{mypage};

    # digestを使って、更新の衝突チェック
    my $original_digest = &calc_message_digest(&get_page($page_name));
    if ($form{mydigest} ne $original_digest) {
        &print_header($page_name);
        print qq|<h1>$IconTag${page_name}で【更新の衝突】が起きました</h1>\n|;
        print <<"EOD";
<p>あなたがこのページを編集している間に、
他の人が同じページを更新してしまったようです。
</p><p>
以下に、あなたの編集したテキストがありますので、
あなたの編集内容が失われないように、
いますぐ、メモ帳などにコピー＆ペーストしてください。
</p><p>
コピー＆ペーストが済んでから、
最新の内容を見て再度編集し直してください。
最新の内容は
<a target="_blank" href="$thisurl?mycmd=read&mypage=$form{mypage}">$form{mypage}</a>
で見ることができます。
</p>
EOD
        # &print_toolbar($page_name);
        &print_preview_buttons($page_name, &escape($form{mymsg}), $form{mydigest});
        &print_footer;
        return;
    }

    # diff生成
    {
        &opendiff;
        my @msg1 = split(/\n/, &get_page($page_name));
        my @msg2 = split(/\n/, $form{mymsg});
        $msgrefA = \@msg1;
        $msgrefB = \@msg2;
        &diff_check;
        $diffbase{$form{mypage}} = $diff_text;
        $diff_text = '';
        &closediff;
    }

    &print_header($page_name);
    &set_page($page_name, $form{mymsg});
    if ($form{mymsg}) {
        print qq|<h1>$IconTag${page_name}を更新しました</h1>\n|;
        &print_toolbar($page_name);
        print &convert_html(&get_page($page_name));
    } else {
        print qq|<h1>$IconTag${page_name}を削除しました</h1>\n|;
        &print_toolbar($page_name);
        print qq|<p>${page_name}を削除しました。</p>\n|;
    }
    &print_footer;
    # 更新されたのでタッチしておく。
    if ($touchfile) {
        open(FILE, "> $touchfile");
        print FILE "\n";
        close(FILE);
    }
}

# ページの変更点
sub do_diff {
    if (not &is_editable($form{mypage})) {
        # 編集不可ページは表示のみ
        &do_read;
        return;
    }
    &opendiff;
    &print_header($form{mypage} . 'の変更点');
    print qq|<h1>$IconTag <a href="$thisurl?mycmd=read&mypage=$form{mypage}">$form{mypage}</a>の変更点</h1>\n|;
    &print_toolbar();
    $_ = &escape($diffbase{$form{mypage}});
    print <<"EOD";
<ul>
<li>追加された行は<font color="blue">青色</font>です。
<li>削除された行は<font color="red">赤色</font>です。
<li><a href="$thisurl?mycmd=read&mypage=$form{mypage}">$form{mypage}</a>へ行く。
</ul>
<hr />
EOD
    print qq|<pre>\n|;
    foreach (split(/\n/, $_)) {
        if (/^\+(.*)/) {
            print qq|<font color="blue">$1</font>\n|;
        } elsif (/^\-(.*)/) {
            print qq|<font color="red">$1</font>\n|;
        } elsif (/^\=(.*)/) {
            print qq|$1\n|;
        } else {
            print qq|??? $_\n|;
        }
    }
    print qq|</pre>\n|;
    &print_footer;
    &closediff;
}

sub opendiff {
    if ($dbmopen) {
        if (!dbmopen(%diffbase, $diffdbname, 0666)) {
            &print_error("(dbmopen) $diffdbname が作れません。");
        }
    } else {
        if (!tie(%diffbase, "YukiWikiDB", $diffdbname)) {
            &print_error("(tie error)");
        }
    }
}

sub closediff {
    if ($dbmopen) {
        dbmclose(%diffbase);
    } else {
        untie(%diffbase);
    }
}

# フォームからの情報を連想配列 %form に入れる
# &init_form('euc');
sub init_form {
    my ($charcode) = @_;
    my $query;
    if ($ENV{REQUEST_METHOD} =~ /^post$/i) {
        read(STDIN, $query, $ENV{CONTENT_LENGTH});
    } else {
        $query = $ENV{QUERY_STRING};
    }
    my @assocarray = split(/&/, $query);
    foreach my $assoc (@assocarray) {
        my ($property, $value) = split(/=/, $assoc);
        $value =~ tr/+/ /;
        $value =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
        &jcode::convert(\$value, $charcode);
        $form{$property} = $value;
    }
}

# エラーページを出力する
sub print_error {
    my ($msg) = @_;
    &print_header('Error');
    print "<h1>$IconTag$msg</h1></body></html>";
    exit(0);
}

sub escape {
    my ($line) = shift;
    $line =~ s|<|&lt;|g;
    $line =~ s|>|&gt;|g;
    $line =~ s|"|&quot;|g;
    # $line =~ s|\&|&amp;|g;
    return $line;
}

sub inline {
    my ($line) = shift;
    $line = &escape($line);
    $line =~ s|'''([^']+?)'''|<i>$1</i>|g;  # Italic
    $line =~ s|''([^']+?)''|<b>$1</b>|g;    # Bold
    $line =~ s!
                (
                    ((mailto|http|https|ftp):[\x21-\x7E]*) # Direct http://...
                        |
                    ($WikiName)                         # LocalLinkLikeThis
                        |
                    ($BracketName)                      # [[日本語リンク]]
                )
            !
                &make_link($1)
            !gex;
    return $line;
}

# ページのタイトルからページの内容を得る
sub get_page {
    my $page_name = shift;
    return $database{$page_name};
}

# ページの内容を与える
# &set_page($title, $txt)
sub set_page {
    # ページを更新する
    my $title = $_[0];
    $database{$title} = $_[1];
    # 空ページなら削除する
    unless ($database{$title}) {
        delete $database{$title};
    }
    # RecentChangesを更新する
    my $delim = ' - ';
    my @pages = split(/\n/, $database{$whatsnew});
    my $datestr = &get_current_datestr;
    unshift(@pages, qq|-$datestr$delim$title|);
    # 同一ページの更新は最新のもののみにし、
    # 存在しないページはスキップする。
    my %count;
    my @newpages;
    foreach my $line (@pages) {
        my ($prefix, $title) = split(/$delim/, $line);
        $count{$title}++;
        if ($count{$title} == 1 and exists($database{$title})) {
            push(@newpages, qq|$prefix - $title|);
        }
    }
    # ここで本当に更新
    $database{$whatsnew} = join("\n", splice(@newpages, 0, $maxnew));
}

# ページのヘッダを出力
sub print_header {
    my $title = shift;
    print <<"EOD";
Content-type: text/html

<html><head>
<title>$title</title>
<style type="text/css">
<!--
$style
-->
</style>
</head>
<body bgcolor="white">
EOD
}

# ツールバーを出力
sub print_toolbar {
    my $page_name = shift;
    my $percent_name = &encode_percent($page_name);
    my $editlink = '';
    if ($page_name ne '' and &is_editable($page_name)) {
        $editlink = <<"EOD";
<a href="$thisurl?mycmd=edit&mypage=$percent_name">編集</a> | 
<a href="$thisurl?mycmd=diff&mypage=$percent_name">差分</a> | 
EOD
    }
    print <<"EOD";
<p>
 [ 
<a href="$thisurl?mycmd=read&mypage=$toppage">トップ</a> | 
<a href="$thisurl?mycmd=list">一覧</a> | 
$editlink
<a href="$thisurl?mycmd=search">単語検索</a> | 
<a href="$thisurl?mycmd=read&mypage=$whatsnew">最終更新</a>
 ]
</p>
EOD
}

# ページのフッタを出力
sub print_footer {
    print <<"EOD";
<hr>
<p>
<a href="http://www.hyuki.com/yukiwiki/">YukiWiki</a> $version Copyright (C) 2000,2001 by <a href="http://www.hyuki.com/">Hiroshi Yuki.</a><br />
Modified by <a href="$modifierlink">$modifier</a>.<br/>
</p>
</body></html>
EOD
}

# URLやページの名前からリンクを作る
sub make_link {
    my $name = shift;
    if ($name =~ /^(http|https|ftp).*?(\.gif|\.png|\.jpeg|\.jpg)?$/) {
        if ($2) {
            return qq|<a href="$name"><img border="0" src="$name" /></a>|;
        } else {
            return qq|<a href="$name">$name</a>|;
        }
    } elsif ($name =~ /^mailto:(.*)/) {
        my $address = $1;
        return qq|<a href="$name">$address</a>|;
    } elsif ($database{$name}) {
        my $percent_name = &encode_percent($name);
        return qq|<a href="$thisurl?mycmd=read&mypage=$percent_name">$name</a>|;
    } else {
        my $percent_name = &encode_percent($name);
        return qq|$name<a href="$thisurl?mycmd=edit&mypage=$percent_name">?</a>|;
    }
}

# %xx の形式にエンコードする
# これは、
# http://www.hyuki.com/yukiwiki/yukiwiki.cgi?mycmd=read&mypage=%3C%8C%8B%8F%E9%8D_%3E
# という形式のために使われる。
# '<結城浩>' → '%3C%8C%8B%8F%E9%8D_%3E'
sub encode_percent {
    my $name = shift;
    my $encoded = '';
    foreach my $ch (split(//, $name)) {
        if ($ch =~ /[A-Za-z0-9_]/) {
            $encoded .= $ch;
        } else {
            $encoded .= '%' . sprintf("%02X", ord($ch));
        }
    }
    return $encoded;
}

# テキスト本体をHTMLに変換する
sub convert_html {
    my ($txt) = shift;
    my (@txt) = split(/\n/, $txt);
    foreach (@txt) {
        chomp;
        if (/^\*\*(.*)/) {
            push(@result, splice(@saved), '<h3>' . &inline($1) . '</h3>');
        } elsif (/^\*(.*)/) {
            push(@result, splice(@saved), '<h2>' . &inline($1) . '</h2>');
        } elsif (/^----/) {
            push(@result, splice(@saved), '<hr>');
        } elsif (/^(-{1,3})(.*)/) {
            &back_push('ul', length($1));
            push(@result, '<li>' . &inline($2) . '</li>');
        } elsif (/^:([^:]+):(.*)/) {
            &back_push('dl', 1);
            push(@result, '<dt>' . &inline($1) . '</dt>', '<dd>' . &inline($2) . '</dd>');
        } elsif (/^(>{1,3})(.*)/) {
            &back_push('blockquote', length($1));
            push(@result, &inline($2));
        } elsif (/^\s*$/) {
            push(@result, splice(@saved));
            unshift(@saved, "</p>");
            push(@result, "<p>");
        } elsif (/^(\s+.*)$/) {
            &back_push('pre', 1);
            push(@result, &escape($1)); # Not &inline, but &escape
        } else {
            push(@result, &inline($_));
        }
    }
    push(@result, splice(@saved));
    return join("\n", @result);
}

# &back_push($tag, $count)
# $tagのタグを$levelレベルまで詰める。
sub back_push {
    my ($tag, $level) = @_;
    while (@saved > $level) {
        push(@result, shift(@saved));
    }
    if ($saved[0] ne "</$tag>") {
        push(@result, splice(@saved));
    }
    while (@saved < $level) {
        unshift(@saved, "</$tag>");
        push(@result, "<$tag>");
    }
}

# 編集可能ページか？
sub is_editable {
    my ($pagename) = @_;
    foreach (@uneditable) {
        if ($pagename eq $_) {
            return 0;
        }
    }
    if (&is_valid_name($pagename)) {
        return 1;
    }
    return 0;
}

# Validな名前か？
sub is_valid_name {
    my ($pagename) = @_;
    if ($pagename =~ /^$WikiName$/) {
        return 1;
    } elsif ($pagename =~ /^$BracketName$/) {
        return 1;
    } else {
        return 0;
    }
}

# 現在時刻の文字列を得る
sub get_current_datestr {
    my (@wdays) = ( "日", "月", "火", "水", "木", "金", "土" );
    my ($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime(time);
    return sprintf("%4d-%02d-%02d (%s) %02d:%02d:%02d",
        $year + 1900, $mon + 1, $mday, $wdays[$wday], $hour, $min, $sec);
}

# URL?SomePageや、
# URL?[[結城浩]]の形式だった場合、(not yet)
# 強制的にmycmdをreadにして$formの内容を設定する。
sub normalize_form {
    foreach my $key (keys %form) {
        if ($key =~ /^$WikiName$/) {
            $form{mycmd} = 'read';
            $form{mypage} = $1;
            last;
        } elsif ($key =~ /^$BracketName$/) {
            $form{mycmd} = 'read';
            $form{mypage} = $1;
            last;
        }
    }
}

# 変換テストを行なうときのサンプル
sub print_sample {
    my $txt = &convert_html(<<"EOD");
*大見出し1
**小見出し1-1
-項目1
-項目2
-項目3
段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1
段落1段落1段落1段落1段落1段落''強調''1段落1段落1段落1段落1段落1
段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1

段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2
段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2
段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2
**小見出し1-2
:用語1:いろいろ書いた解説文1と''強調単語''
段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1
段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1
段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1
:用語2:いろいろ書いた解説文2
:用語3:いろいろ書いた解説文3
----
*大見出し2
**小見出し2-1
http://www.hyuki.com/
**小見出し2-2

[[結城浩]]

段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1段落1
段落1段落1段落1段落'''イタリック'''1段落1段落1段落1段落1段落1段落1段落1
段落1段落1段落1段落'''''イタボールド'''''1段落1段落1段落1段落1段落1段落1段落1段落1
>段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2
>段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2
>段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2段落2

レベル0レベル0レベル0レベル0レベル0レベル0

>レベル1
>レベル1
>レベル1
>>レベル2
>>レベル2
>>レベル2
>>>レベル3
-はろ1
--はろ2
ろろろろ2
---はろ3
--はろ2
---はろ3
--はろ2
---はろ3
>>>レベル3
>>>レベル3
>>>レベル3
EOD
    print $txt;
    exit;
}

sub diff_check {
    traverse_sequences(
            $msgrefA, $msgrefB,
            {
                MATCH => \&df_match,
                DISCARD_A => \&df_delete,
                DISCARD_B => \&df_add,
            }
    );
    &diff_flush;
}

sub diff_flush {
    $diff_text .= join('', map { "-$_\n" } splice(@diff_deleted));
    $diff_text .= join('', map { "+$_\n" } splice(@diff_added));
}

sub df_match {
    my ($a, $b) = @_;
    &diff_flush;
    $diff_text .= "=$msgrefA->[$a]\n";
}

sub df_delete {
    my ($a, $b) = @_;
    push(@diff_deleted, $msgrefA->[$a]);
}

sub df_add {
    my ($a, $b) = @_;
    push(@diff_added, $msgrefB->[$b]);
}

# メッセージのダイジェストを計算(書き込み衝突の検出用)
sub calc_message_digest {   # You have to use MD5...
    my $text = shift;
    my @text = split(//, $text);
    my $len = length($text);
    my $checksum = 0;
    foreach (@text) {
        $checksum += ord($_);
        $checksum = ($checksum * 2) % 65536 + (($checksum & 32768) ? 1 : 0); # 16bit rotate
    }
    return "$len:$checksum";
}

# Definition of YukiWikiDB
package YukiWikiDB;

my $debug = 1;

# Constructor
sub new {
    return shift->TIEHASH(@_);
}

# tying
sub TIEHASH {
    my ($class, $dbname) = @_;
    my $self = {
        dir => $dbname,
        keys => [],
    };
    if (not -d $self->{dir}) {
        if (!mkdir($self->{dir}, 0777)) {
            print "mkdir(" . $self->{dir} . ") fail\n" if ($debug);
            return undef;
        }
    }
    return bless($self, $class);
}

# Store
sub STORE {
    my ($self, $key, $val) = @_;
    my $file = &make_filename($self, $key);
    if (open(FILE,"> $file")) {
        binmode(FILE);
        print FILE $val;
        close(FILE);
        return $self->{$key} = $val;
    } else {
        print "$file create error.";
    }
}

# Fetch
sub FETCH {
    my ($self, $key) = @_;
    my $file = &make_filename($self, $key);
    if (open(FILE, $file)) {
        local $/;
        $self->{$key} = <FILE>;
        close(FILE);
    }
    return $self->{$key};
}

# Exists
sub EXISTS {
    my ($self, $key) = @_;
    my $file = &make_filename($self, $key);
    return -e($file);
}

# Delete
sub DELETE {
    my ($self, $key) = @_;
    my $file = &make_filename($self, $key);
    unlink $file;
    return delete $self->{$key};
}

sub FIRSTKEY {
    my ($self) = @_;
    opendir(DIR, $self->{dir}) or die $self->{dir};
    @{$self->{keys}} = grep /\.txt$/, readdir(DIR);
    foreach my $name (@{$self->{keys}}) {
        $name =~ s/\.txt$//;
        $name =~ s/[0-9A-F][0-9A-F]/pack("C", hex($&))/eg;
    }
    return shift @{$self->{keys}};
}

sub NEXTKEY {
    my ($self) = @_;
    return shift @{$self->{keys}};
}

sub make_filename {
    my ($self, $key) = @_;
    my $enkey = '';
    foreach my $ch (split(//, $key)) {
        $enkey .= sprintf("%02X", ord($ch));
    }
    return $self->{dir} . "/$enkey.txt";
}
__END__

=head1 NAME

YukiWiki - 自由にページを追加・削除・編集できるWebページ構築CGI

    Copyright (C) 2000,2001 by Hiroshi Yuki.
    結城浩 <hyuki@hyuki.com>
    http://www.hyuki.com/
    http://www.hyuki.com/yukiwiki/

=head1 SYNOPSIS

    http://www.hyuki.com/yukiwiki/yukiwiki.cgi

=head1 DESCRIPTION

YukiWiki（結城ウィキィ）は参加者が自由にページを追加・削除・編集できる
不思議なWebページ群を作るCGIです。
Webで動作する掲示板とちょっと似ていますが、
Web掲示板が単にメッセージを追加するだけなのに対して、
YukiWikiは、Webページ全体を自由に変更することができます。

YukiWikiは、Cunningham & CunninghamのWikiWikiWebの
仕様を参考にして独自に作られました。

YukiWikiはPerlで書かれたCGIスクリプトとして実現されていますので、
Perlが動作するWebサーバならば比較的容易に設置できます。

あとはdbmopenが使える環境ならば設置できます(Version 1.5.0以降ならdbmopenが使えなくても設置できます)。


YukiWikiはフリーソフトです。
ご自由にお使いください。

=head1 設置方法

=head2 入手

YukiWikiの最新版は、
http://www.hyuki.com/yukiwiki/
から入手できます。

=head2 ファイル一覧

    readme.txt      ドキュメント
    yukiwiki.cgi    YukiWiki本体
    yukiwiki.gif    ロゴ（カラー版）
    yukimono.gif    ロゴ（モノクロ版）
    jcode.pl        漢字コードライブラリ

=head2 インストール

=over 4

=item 1.

アーカイブを解きます。

=item 2.

yukiwiki.cgiのはじめの方にある設定を確認します。
通常は何もしなくてよいですが、
はじめは$touchfileを''にした方がよいでしょう。

=item 3.

yukiwiki.cgiとjcode.plを同じところに設置します。

=item 4.

Diff.pmの設置場所は、yukiwiki.cgiの始めのコメントを参照してください。

=item 5.

サイズ0のyukiwiki.dbというファイルを設置します。
（Perlシステムによってはyukiwiki.pag, yukiwiki.dir）

=item 6.

yukiwiki.cgiにブラウザからアクセスします。

=back

=head2 ファイル構成とパーミッション

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

=head1 データのバックアップ方法

$dbmopen = 1;の場合は、
データはすべてyukiwiki.db(.dir, .pag)に入る。
これをバックアップすればよい。

$dbmopen = 0;の場合は、
yukiwikiというディレクトリができるので、
これ以下をバックアップすればよい。

=head1 新しいページの作り方 

=over 4

=item 1.

まず、適当なページ（例えばFrontPage）を選び、
ページの下にある「編集」リンクをたどります。 

=item 2.

するとテキスト入力ができる状態になるので、
そこにNewPageのような単語
（大文字小文字混在している英文字列）
を書いて「保存」します。

=item 3.

保存すると、FrontPageのページが書き換わり、
あなたが書いたNewPageという文字列の後ろに ? というリンクが表示されます。 
この ? はそのページがまだ存在しないことを示す印です。 

=item 4.

その ? をクリックすると新しいページNewPageができますので、
あなたの好きな文章をその新しいページに書いて保存します。

=item 5.

NewPageページができるとFrontPageの ? は消えて、リンクとなります。 

=back

=head1 テキスト整形のルール

=over 4

=item *

連続した複数行はフィルされて表示されます。

=item *

空行は段落C<< <p> >>の区切りとなります。

=item *

HTMLのタグは書けません。

=item *

B<''ボールド''>のようにシングルクォート二つではさむと、
ボールドC<< <b> >>になります。

=item *

B<'''イタリック'''>のようにシングルクォート三つではさむと、
イタリックC<< <i> >>になります。

=item *

B<---->のようにマイナス4つがあると、
水平線C<< <hr> >>になります。

=item *

行をB<*>ではじめると、
大見出しC<< <h2> >>になります。

=item *

行をB<**>ではじめると、
小見出しC<< <h3> >>になります。

=item *

行をマイナス-ではじめると、
箇条書きC<< <ul> >>になります。
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

=item *

コロンを使うと、
用語と解説文のリストC<< <dl> >>が書けます。

    :用語1:いろいろ書いた解説文1
    :用語2:いろいろ書いた解説文2
    :用語3:いろいろ書いた解説文3

=item *

リンク

=over 4

=item *

LinkToSomePageやFrontPageのように、
英単語の最初の一文字を大文字にしたものが
二つ以上連続したものはYukiWikiのページ名となり、
それが文章中に含まれるとリンクになります。

=item *

http://www.hyuki.com/ のようなURLは自動的にリンクになります。

=item *

二重の大かっこ[[ ]]でくくった文字列も、
YukiWikiのページ名になります。
大かっこの中にはスペースを含めてはいけません。
日本語も使えます。

=back

=item *

行頭がスペースやタブで始まっていると、
それは整形済みの段落C<< <pre> >>として扱われます。
プログラムの表示などに使うと便利です。


=item *

行を > ではじめると、
引用文C<< <blockquote> >>が書けます。
>の数が多いとインデントが深くなります（3レベルまで）。

    >文章
    >文章
    >>さらなる引用
    >文章

=back

=head1 更新履歴

=over 4

=item *

2002年3月1日、Version 1.6.7。

パッケージにDiff.pmを同梱。

=item *

2001年10月20日、Version 1.6.6。

更新の衝突対策。
元ページの簡単なチェックサムを取っておき、
更新前にチェックサムを比較する。
修正個所はdigestという文字列を検索すれば分かる。
本来はMD5などでちゃんとやった方がいいのだけれど。

衝突時に表示されるメッセージなどは「極悪」さんのページを参考にした。

=item *

2001年10月17日、Version 1.6.5。

プレビュー画面で、更新ボタンを押したときに送信される
メッセージの内容をinput要素のtype="hidden"を使って埋め込むのをやめる。
代わりに、textarea要素を使う。
再プレビュー用にmyspecial_を導入。でもきれいな対策ではない。

=item *

2001年8月30日、Version 1.6.4。

URLでダイレクトにページ名を指定しても、
$WikiNameと$BracketName以外のページを作れないようにした。
(is_valid_nameとis_editable参照)。

=item *

2001年8月30日、Version 1.6.3。

RecentChangesを編集・再編集不可とした。
編集不可ページは@uneditableにページ名を入れる。

=item *

2001年2月25日、Version 1.6.1, 1.6.2。

差分機能のバグ修正。
do_previewで'>'が扱えないバグを修正
（ユーザからの指摘）。

=item *

2001年2月22日、Version 1.6.0。
差分機能を実装した。

=item *

2001年2月19日、Version 1.5.4。
画像ファイルへのリンクは画像にしてみた。

=item *

2001年2月19日、Version 1.5.3。
RecentChangesの中に削除したページがあるのをやめた。
use strict;で引っかかる部分を少し整理(完全ではない)。

=item *

2001年2月16日、Version 1.5.2。
textareaに表示およびプレビューする前に < や > を &lt; や &gt; に変換した
(do_preview, editpage, print_preview_buttons)。

=item *

2000年12月27日、Version 1.5.1。
プレビュー画面を整理した。

=item *

2000年12月22日、Version 1.5.0。
全体的にずいぶん書き直した。
一覧を別途作成するようにした(do_list)。
書き込む前に確認画面を出すようにした(do_preview)。
テキストの書き方を編集画面に入れた(do_edit, do_reedit)。
WhatsNew→RecentChanges、TopPage→FrontPageに変更した。

=item *

2000年12月20日、Version 1.1.0。
tieを利用して、dbmopenが使えない場合でも動作するように修正。
利用者の1人である「極悪」さんから
送っていただいたコードを元にしています。

=item *

2000年9月5日、Version 1.0.2。
 <body color=...> → <body bgcolor=...>
利用者からの指摘による。感謝。

=item *

2000年8月6日、Version 1.0.1を公開。
C MAGAZINE（ソフトバンクパブリッシング）
2000年10月号連載記事向け公開版。
[[ ]] の最後が「望」のようにシフトJISで
0x5Dになる場合の回避を行なった。

=item *

2000年8月5日、Version 1.0.0を公開。

=item *

2000年7月23日、Version 0.82を公開。
編集時のリンクミス。
<textarea>の属性変更。

=item *

2000年7月22日、Version 0.81を公開。
ロゴを組み込む。

=item *

2000年7月21日、Version 0.80を公開。
PODをCGI中に書き込む。

=item *

2000年7月19日、Version 0.70を公開。
'''イタリック'''や、--、---、>>、>>>などを実装。

=item *

2000年7月18日、Version 0.60を公開。
*太字*を''太字''に変更

=item *

2000年7月17日、Version 0.50を公開。

=item *

2000年7月17日、さらにいろいろ追加する。

=item *

2000年7月16日、いろいろ追加。

=item *

2000年7月15日、公開。

=back

=head1 TODO

    - テキスト表示モード
    - Charsetを明示。
    - textarea中の閉じタグ対応
    - メニューの英語表記付記
    - プレビューのボタンで、mymsgをinputのvalueに入れているが、改行をそのままvalueにいれてはいけないのではないか。
    - 「再編集」の機能はブラウザの back で充分ではないか。プレビューはもっとシンプルに。
    - ページタイトル（Wikiname）が検索にかかるようにする。
    - InterWiki風の機能「URLを隠しつつ、リンクを張る」

=head1 作者

    Copyright (C) 2000 by Hiroshi Yuki.
    結城浩 <hyuki@hyuki.com>
    http://www.hyuki.com/
    http://www.hyuki.com/yukiwiki/

質問、意見、バグ報告は hyuki@hyuki.com にメールしてください。

=head1 配布条件

YukiWikiは、
GNU General Public Licenseにて公開します。

YukiWikiはフリーソフトです。
ご自由にお使いください。
自分好みのYukiWikiが作れるようにシンプルにしてあります。

=head1 謝辞

本家のWikiWikiを作ったCunningham & Cunningham, Inc.に
感謝します。

YukiWikiを楽しんで使ってくださる
ネット上の方々に感謝します。

YukiWikiのロゴをデザインしてくださった橋本礼奈さん
http://city.hokkai.or.jp/~reina/
に感謝します。

tieを使った版の元になるコードを送ってくださった
「極悪」さんに感謝します。

=head1 参照リンク

=over 4

=item *

YukiWikiホームページ
http://www.hyuki.com/yukiwiki/

=item *

本家のWikiWiki
http://c2.com/cgi/wiki?WikiWikiWeb

=item *

本家のWikiWikiの作者(Cunningham & Cunningham, Inc.)
http://c2.com/

=item *

YukiWikiのロゴデザインをしてくださった橋本礼奈さんのページ
http://city.hokkai.or.jp/~reina/

=back

=cut
