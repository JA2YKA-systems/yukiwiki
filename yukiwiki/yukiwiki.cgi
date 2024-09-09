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
# �����@�\�̂��߂�Algorithm::Diff�Ƃ������W���[�����g���Ă��܂��B
# �t�@�C������Diff.pm�ł��B
# �ȉ���2�s�́Ayukiwiki.cgi������f�B���N�g��(.)�̉���
# Algorithm�Ƃ����f�B���N�g��������A
# ���̒���Diff.pm�Ƃ����t�@�C�������邱�Ƃ�O��Ƃ��Ă��܂��B
# YukiWiki��ݒu����T�[�o�ɂ��ł�
# Algorithm::Diff���C���X�g�[������Ă���ꍇ�ɂ́A
# �ȉ���2�s���R�����g�A�E�g���܂��B
use lib ".";
use Algorithm::Diff qw(traverse_sequences);
##############################
my $version = "1.6.7";
##############################
# �P�ƃe�X�g�̂Ƃ��ɂ� 1 �ɂ���B
my $testing = 0;
##############################
# �������C�u����
my $jcodelib = 'jcode.pl';
##############################
# �ۑ��E�\���̊����R�[�h
my $kanjicode = 'sjis';     # 'sjis' 'euc'
my $charset = 'Shift_JIS';  # 'Shift_JIS' 'EUC-JP'
##############################
# dbmopen���g����Ȃ�1�A�g���Ȃ��Ȃ�0
my $dbmopen = 0;
##############################
# �f�[�^�x�[�X���i.pag, .dir, .db�Ȃǂ͕s�v�j
# $dbmopen = 1�̂Ƃ��̓f�[�^�x�[�X���A
# $dbmopen = 0�̂Ƃ��̓f�B���N�g�����ɂȂ�B
my $dbname = './yukiwiki';
my $diffdbname = './yukidiff';
##############################
# �C���҂̎����i���R�ɕύX���Ă��������j
my $modifier = 'Hiroshi Yuki';
##############################
# �C���҂�Web�y�[�W�i���R�ɕύX���Ă��������j
my $modifierlink = 'http://www.hyuki.com/';
##############################
# ���̃y�[�W��URL
my $thisurl = 'yukiwiki.cgi';
##############################
# �J�n�y�[�W��
my $toppage = 'FrontPage';
##############################
# �ŏI�X�V�y�[�W��
my $whatsnew = 'RecentChanges';
##############################
# �ŏI�X�V�Ɍf�ڂ���y�[�W��
my $maxnew = 50;
##############################
# �A�C�R���t�@�C�����i�J���[�Łj
my $iconfile = 'yukiwiki.gif';
##############################
# �A�C�R���t�@�C�����i���m�N���Łj
# my $iconfile = 'yukimono.gif';
##############################
# �y�[�W��ύX�����Ƃ���touch����t�@�C���i''�Ȃ牽�����Ȃ��j
my $touchfile = 'touch.txt';
##############################
# �v���r���[�p�̔w�i�F
my $preview_color = '#FFCCCC';
##############################
# �S�y�[�W�̃X�^�C��
my $style = <<'EOD';
pre, dl, ul, ol, p, blockquote { line-height:120%; }
a { text-decoration: none; }
a:link { color: #0000FF; background-color: #FFFFFF; }
a:visited { color: #9900CC; background-color: #FFFFFF; }
a:hover { text-decoration: underline; }
EOD
##############################
# �e�L�X�g���͕����̑傫��
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
# �ҏW�s�y�[�W���ꗗ
my @uneditable = ( $whatsnew );
##############################
# �����N�p�̐��K�\��
# YukiWiki�̃����N��2��ނ���B
# 
# (1) WikiName (RecentChanges�Ƃ�FrontPage�̂悤�Ȃ���)
# (2) BracketName ([[����_]]�Ƃ�[[�g���u���V���[�g]]�̂悤�Ȃ���)
#
# ���V�t�gJIS��2�o�C�g�ڂɂ� ']' ��������̂ŁA
# ����']'��1�����Ƃ�悤�ɂ��Ă���B
#
my $WikiName = '([A-Z][a-z]+([A-Z][a-z]+)+)';
my $BracketName = '\[\[([^>\s]+?\]?)\]\]';

# �A�C�R�������̃^�O
my $IconTag = <<"EOD";
<a href="http://www.hyuki.com/yukiwiki/"><img src="$iconfile"
 border="0" width="80" height="80" alt="[YukiWiki]" /></a>
EOD

require "$jcodelib";

&init_form($kanjicode);

# ����e�X�g�p
if ($testing) {
    %form = (
        # 'mycmd' => 'write',
        'mycmd' => 'read',
        #'mycmd' => 'search',
        #'mycmd' => 'edit',
        'mymsg' => <<"EOD",
�͂��߂܂��āB
���ꂩ�炢�낢�돑�����݂܂��ˁB
LinkPage�����Ă��������B
TestPage�͂ǂ��ł��傤���B
�ǂ�����낵���B
http://www.hyuki.com/
[[����_]]
EOD
        'mypage' => '<����_>',
        'myword' => '��',
        # '3C8C8B8FE98D5F3E' => '',
        # 'TestPage' => '',
    );
}
&main;
exit(0);

# ���C��
sub main {
    &normalize_form;
    if ($dbmopen) {
        if (!dbmopen(%database, $dbname, 0666)) {
            &print_error("(dbmopen) $dbname �����܂���B");
        }
    } else {
        if (!tie(%database, "YukiWikiDB", $dbname)) {
            &print_error("(tie error)");
        }
    }

    # myspecial�Ή�
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

# �y�[�W�̕\��
sub do_read {
    my $page_name = $form{mypage};
    my $percent_name = &encode_percent($page_name);
    &print_header($page_name);
    print qq|<h1>$IconTag<a href="$thisurl?mycmd=search&myword=$percent_name">$page_name</a></h1>\n|;
    &print_toolbar($page_name);
    print &convert_html(&get_page($page_name));
    &print_footer;
}

# �y�[�W�̕ҏW
sub do_edit {
    if (not &is_editable($form{mypage})) {
        # �ҏW�s�y�[�W�͕\���̂�
        &do_read;
        return;
    }
    &editpage(&get_page($form{mypage}));
}

# �y�[�W�̍ĕҏW
sub do_reedit {
    if (not &is_editable($form{mypage})) {
        # �ҏW�s�y�[�W�͕\���̂�
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
    print qq|<h1>$IconTag${page_name}�̕ҏW</h1>\n|;
    &print_toolbar($page_name);
    $page_msg = &escape($page_msg);
    print <<"EOD";
<form action="$thisurl" method="post">
<input type="hidden" name="mycmd" value="preview">
<input type="hidden" name="mypage" value="$page_name">
<input type="hidden" name="mydigest" value="$digest">
<textarea cols="$cols" rows="$rows" name="mymsg" wrap="virtual">$page_msg</textarea><br>
<input type="submit" value="�v���r���[">
</form>
<hr>
<h3>�e�L�X�g���`�̃��[��</h3>

<p>�ʏ�͓��͂������������̂܂܏o�͂���܂����A
�ȉ��̃��[���ɏ]���ăe�L�X�g���`���s�����Ƃ��ł��܂��B</p>

<ul>
<li>
��s�͒i���̋�؂�ƂȂ�܂��B

<li>
HTML�̃^�O�͏����܂���B

<li>
''�{�[���h''�̂悤�ɃV���O���N�H�[�g��ł͂��ނƁA�{�[���h�ɂȂ�܂��B

<li>
'''�C�^���b�N'''�̂悤�ɃV���O���N�H�[�g�O�ł͂��ނƁA�C�^���b�N�ɂȂ�܂��B

<li>
----�̂悤�Ƀ}�C�i�X4������ƁA�������ɂȂ�܂��B

<li>
*���s���ɏ����Ƒ匩�o���ɂȂ�܂��B

<li>
**���s���ɏ����Ə����o���ɂȂ�܂��B

<li>
-���s���ɏ����Ɖӏ������ɂȂ�܂��B- -- --- ��3���x��������܂��B

<li>
:���s���ɏ����Ɨp��Ɖ���������܂��B

<pre>
    :�p��1:���낢�돑���������1
    :�p��2:���낢�돑���������2
    :�p��3:���낢�돑���������3
</pre>

<li>
http://www.hyuki.com/ �̂悤��URL�͎����I�Ƀ����N�ɂȂ�܂��B

<li>
YukiWiki�̂悤�ɑ啶�����������������p������������ƁA
YukiWiki�̃y�[�W���ɂȂ�܂��B

<li>
[[����_]]�̂悤�ɓ�d�̑傩����[[ ]]�ł�������������������ƁA
YukiWiki�̃y�[�W���ɂȂ�܂��B
�傩�����̒��ɂ̓X�y�[�X���܂߂Ă͂����܂���B
���{����g���܂��B

<li>
�s�����X�y�[�X�Ŏn�܂��Ă���ƁA
���̒i���͐��`�ς݈����܂��B
�v���O�������������ނƂ��Ɏg���ƕ֗��ł��B

<li>
> ���s���ɏ����ƁA
���p���������܂��B
>�̐��������ƃC���f���g���[���Ȃ�܂��i3���x���܂Łj�B

</ul>
EOD
    &print_footer;
}

# �y�[�W�̌���
sub do_search {
    if ($form{myword}) {
        &print_header('��������');
        print qq|<h1>$IconTag$form{myword}�̌�������</h1>\n|;
        &print_toolbar();
        print qq|<ul>\n|;
        my $count = 0;
        foreach my $page_name (sort keys %database) {    # sort����͖̂��d����
            if ($database{$page_name} =~ /\Q$form{'myword'}\E/) {
                my $encoded = &encode_percent($page_name);
                print qq|<li><a href="$thisurl?mycmd=read&mypage=$encoded">$page_name</a>\n|;
                $count++;
            }
        }
        print qq|</ul>\n|;
        if ($count > 0) {
            print qq|<p><b>$form{myword}</b>���܂ރy�[�W�́A��Ɏ���<b>$count</b>�y�[�W�ł��B</p>\n|;
        } else {
            print qq|<p><b>$form{myword}</b>���܂ރy�[�W�͌�����܂���B</p>\n|;
        }
    } else {
        &print_header('�P�ꌟ��');
        print qq|<h1>$IconTag�P�ꌟ��</h1>\n|;
        &print_toolbar();
    }
    print <<"EOD";
<p>
<form action="$thisurl" method="post">
<input type="hidden" name="mycmd" value="search">
<input type="text" name="myword" size="20" value="$form{myword}">
<input type="submit" value="�P�ꌟ��">
</form>
</p>
EOD
    &print_footer;
}

# �y�[�W�̈ꗗ
sub do_list {
    &print_header('�y�[�W�ꗗ');
    print qq|<h1>$IconTag �y�[�W�ꗗ</h1>\n|;
    &print_toolbar();
    print qq|<ul>\n|;
    foreach my $page_name (sort keys %database) {    # sort����͖̂��d����
        my $encoded = &encode_percent($page_name);
        print qq|<li><a href="$thisurl?mycmd=read&mypage=$encoded">$page_name</a>\n|
    }
    print qq|</ul>\n|;
    &print_footer;
}

# �v���r���[
sub do_preview {
    my $page_name = $form{mypage};
    my $escapedmsg = &escape($form{mymsg});
    &print_header($page_name);
    print qq|<h1>$IconTag${page_name}�̃v���r���[</h1>\n|;
    &print_toolbar($page_name);
    # local $percent_name = &encode_percent($page_name);
    print qq|<p>�ȉ��̃v���r���[���m�F���āA�悯��΃y�[�W�����̃{�^���ōX�V���Ă��������B</p>\n|;
    if ($form{mymsg}) {
        print qq|<table width="100%" bgcolor="$preview_color" ><tr><td>\n|;
        # print &convert_html($escapedmsg);
        print &convert_html($form{mymsg});
        print qq|</td></tr></table>\n|;
    } else {
        print qq|<p>�i�y�[�W�̓��e�͋�ł��B�X�V����Ƃ��̃y�[�W��<b>�폜</b>����܂��B�j</p>\n|;
    }
    &print_preview_buttons($page_name, $escapedmsg, $form{mydigest});
    &print_footer;
}

# �v���r���[�p�̃{�^���\��(textarea���\��)
sub print_preview_buttons {
    my ($page_name, $escapedmsg, $digest) = @_;
    print <<"EOD";
    <form action="$thisurl" method="post">
    <textarea cols="$cols" rows="$rows" name="mymsg" wrap="virtual">$escapedmsg</textarea>
    <br />
    <input type="hidden" name="mypage" value="$page_name">
    <input type="hidden" name="mydigest" value="$digest">
    <input type="submit" name="myspecial_preview" value="�ēx�v���r���[">
    <input type="submit" name="myspecial_write" value="�y�[�W�̍X�V">
    </form>
EOD
}

# ��������
sub do_write {
    if (not &is_editable($form{mypage})) {
        # �ҏW�s�y�[�W�͕\���̂�
        &do_read;
        return;
    }

    my $page_name = $form{mypage};

    # digest���g���āA�X�V�̏Փ˃`�F�b�N
    my $original_digest = &calc_message_digest(&get_page($page_name));
    if ($form{mydigest} ne $original_digest) {
        &print_header($page_name);
        print qq|<h1>$IconTag${page_name}�Ły�X�V�̏Փˁz���N���܂���</h1>\n|;
        print <<"EOD";
<p>���Ȃ������̃y�[�W��ҏW���Ă���ԂɁA
���̐l�������y�[�W���X�V���Ă��܂����悤�ł��B
</p><p>
�ȉ��ɁA���Ȃ��̕ҏW�����e�L�X�g������܂��̂ŁA
���Ȃ��̕ҏW���e�������Ȃ��悤�ɁA
���܂����A�������ȂǂɃR�s�[���y�[�X�g���Ă��������B
</p><p>
�R�s�[���y�[�X�g���ς�ł���A
�ŐV�̓��e�����čēx�ҏW�������Ă��������B
�ŐV�̓��e��
<a target="_blank" href="$thisurl?mycmd=read&mypage=$form{mypage}">$form{mypage}</a>
�Ō��邱�Ƃ��ł��܂��B
</p>
EOD
        # &print_toolbar($page_name);
        &print_preview_buttons($page_name, &escape($form{mymsg}), $form{mydigest});
        &print_footer;
        return;
    }

    # diff����
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
        print qq|<h1>$IconTag${page_name}���X�V���܂���</h1>\n|;
        &print_toolbar($page_name);
        print &convert_html(&get_page($page_name));
    } else {
        print qq|<h1>$IconTag${page_name}���폜���܂���</h1>\n|;
        &print_toolbar($page_name);
        print qq|<p>${page_name}���폜���܂����B</p>\n|;
    }
    &print_footer;
    # �X�V���ꂽ�̂Ń^�b�`���Ă����B
    if ($touchfile) {
        open(FILE, "> $touchfile");
        print FILE "\n";
        close(FILE);
    }
}

# �y�[�W�̕ύX�_
sub do_diff {
    if (not &is_editable($form{mypage})) {
        # �ҏW�s�y�[�W�͕\���̂�
        &do_read;
        return;
    }
    &opendiff;
    &print_header($form{mypage} . '�̕ύX�_');
    print qq|<h1>$IconTag <a href="$thisurl?mycmd=read&mypage=$form{mypage}">$form{mypage}</a>�̕ύX�_</h1>\n|;
    &print_toolbar();
    $_ = &escape($diffbase{$form{mypage}});
    print <<"EOD";
<ul>
<li>�ǉ����ꂽ�s��<font color="blue">�F</font>�ł��B
<li>�폜���ꂽ�s��<font color="red">�ԐF</font>�ł��B
<li><a href="$thisurl?mycmd=read&mypage=$form{mypage}">$form{mypage}</a>�֍s���B
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
            &print_error("(dbmopen) $diffdbname �����܂���B");
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

# �t�H�[������̏���A�z�z�� %form �ɓ����
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

# �G���[�y�[�W���o�͂���
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
                    ($BracketName)                      # [[���{�ꃊ���N]]
                )
            !
                &make_link($1)
            !gex;
    return $line;
}

# �y�[�W�̃^�C�g������y�[�W�̓��e�𓾂�
sub get_page {
    my $page_name = shift;
    return $database{$page_name};
}

# �y�[�W�̓��e��^����
# &set_page($title, $txt)
sub set_page {
    # �y�[�W���X�V����
    my $title = $_[0];
    $database{$title} = $_[1];
    # ��y�[�W�Ȃ�폜����
    unless ($database{$title}) {
        delete $database{$title};
    }
    # RecentChanges���X�V����
    my $delim = ' - ';
    my @pages = split(/\n/, $database{$whatsnew});
    my $datestr = &get_current_datestr;
    unshift(@pages, qq|-$datestr$delim$title|);
    # ����y�[�W�̍X�V�͍ŐV�̂��݂̂̂ɂ��A
    # ���݂��Ȃ��y�[�W�̓X�L�b�v����B
    my %count;
    my @newpages;
    foreach my $line (@pages) {
        my ($prefix, $title) = split(/$delim/, $line);
        $count{$title}++;
        if ($count{$title} == 1 and exists($database{$title})) {
            push(@newpages, qq|$prefix - $title|);
        }
    }
    # �����Ŗ{���ɍX�V
    $database{$whatsnew} = join("\n", splice(@newpages, 0, $maxnew));
}

# �y�[�W�̃w�b�_���o��
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

# �c�[���o�[���o��
sub print_toolbar {
    my $page_name = shift;
    my $percent_name = &encode_percent($page_name);
    my $editlink = '';
    if ($page_name ne '' and &is_editable($page_name)) {
        $editlink = <<"EOD";
<a href="$thisurl?mycmd=edit&mypage=$percent_name">�ҏW</a> | 
<a href="$thisurl?mycmd=diff&mypage=$percent_name">����</a> | 
EOD
    }
    print <<"EOD";
<p>
 [ 
<a href="$thisurl?mycmd=read&mypage=$toppage">�g�b�v</a> | 
<a href="$thisurl?mycmd=list">�ꗗ</a> | 
$editlink
<a href="$thisurl?mycmd=search">�P�ꌟ��</a> | 
<a href="$thisurl?mycmd=read&mypage=$whatsnew">�ŏI�X�V</a>
 ]
</p>
EOD
}

# �y�[�W�̃t�b�^���o��
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

# URL��y�[�W�̖��O���烊���N�����
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

# %xx �̌`���ɃG���R�[�h����
# ����́A
# http://www.hyuki.com/yukiwiki/yukiwiki.cgi?mycmd=read&mypage=%3C%8C%8B%8F%E9%8D_%3E
# �Ƃ����`���̂��߂Ɏg����B
# '<����_>' �� '%3C%8C%8B%8F%E9%8D_%3E'
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

# �e�L�X�g�{�̂�HTML�ɕϊ�����
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
# $tag�̃^�O��$level���x���܂ŋl�߂�B
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

# �ҏW�\�y�[�W���H
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

# Valid�Ȗ��O���H
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

# ���ݎ����̕�����𓾂�
sub get_current_datestr {
    my (@wdays) = ( "��", "��", "��", "��", "��", "��", "�y" );
    my ($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime(time);
    return sprintf("%4d-%02d-%02d (%s) %02d:%02d:%02d",
        $year + 1900, $mon + 1, $mday, $wdays[$wday], $hour, $min, $sec);
}

# URL?SomePage��A
# URL?[[����_]]�̌`���������ꍇ�A(not yet)
# �����I��mycmd��read�ɂ���$form�̓��e��ݒ肷��B
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

# �ϊ��e�X�g���s�Ȃ��Ƃ��̃T���v��
sub print_sample {
    my $txt = &convert_html(<<"EOD");
*�匩�o��1
**�����o��1-1
-����1
-����2
-����3
�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
�i��1�i��1�i��1�i��1�i��1�i��''����''1�i��1�i��1�i��1�i��1�i��1
�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1

�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2
�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2
�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2
**�����o��1-2
:�p��1:���낢�돑���������1��''�����P��''
�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
:�p��2:���낢�돑���������2
:�p��3:���낢�돑���������3
----
*�匩�o��2
**�����o��2-1
http://www.hyuki.com/
**�����o��2-2

[[����_]]

�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
�i��1�i��1�i��1�i��'''�C�^���b�N'''1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
�i��1�i��1�i��1�i��'''''�C�^�{�[���h'''''1�i��1�i��1�i��1�i��1�i��1�i��1�i��1�i��1
>�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2
>�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2
>�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2�i��2

���x��0���x��0���x��0���x��0���x��0���x��0

>���x��1
>���x��1
>���x��1
>>���x��2
>>���x��2
>>���x��2
>>>���x��3
-�͂�1
--�͂�2
�����2
---�͂�3
--�͂�2
---�͂�3
--�͂�2
---�͂�3
>>>���x��3
>>>���x��3
>>>���x��3
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

# ���b�Z�[�W�̃_�C�W�F�X�g���v�Z(�������ݏՓ˂̌��o�p)
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

YukiWiki - ���R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���Web�y�[�W�\�zCGI

    Copyright (C) 2000,2001 by Hiroshi Yuki.
    ����_ <hyuki@hyuki.com>
    http://www.hyuki.com/
    http://www.hyuki.com/yukiwiki/

=head1 SYNOPSIS

    http://www.hyuki.com/yukiwiki/yukiwiki.cgi

=head1 DESCRIPTION

YukiWiki�i����E�B�L�B�j�͎Q���҂����R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���
�s�v�c��Web�y�[�W�Q�����CGI�ł��B
Web�œ��삷��f���Ƃ�����Ǝ��Ă��܂����A
Web�f�����P�Ƀ��b�Z�[�W��ǉ����邾���Ȃ̂ɑ΂��āA
YukiWiki�́AWeb�y�[�W�S�̂����R�ɕύX���邱�Ƃ��ł��܂��B

YukiWiki�́ACunningham & Cunningham��WikiWikiWeb��
�d�l���Q�l�ɂ��ēƎ��ɍ���܂����B

YukiWiki��Perl�ŏ����ꂽCGI�X�N���v�g�Ƃ��Ď�������Ă��܂��̂ŁA
Perl�����삷��Web�T�[�o�Ȃ�Δ�r�I�e�Ղɐݒu�ł��܂��B

���Ƃ�dbmopen���g������Ȃ�ΐݒu�ł��܂�(Version 1.5.0�ȍ~�Ȃ�dbmopen���g���Ȃ��Ă��ݒu�ł��܂�)�B


YukiWiki�̓t���[�\�t�g�ł��B
�����R�ɂ��g�����������B

=head1 �ݒu���@

=head2 ����

YukiWiki�̍ŐV�ł́A
http://www.hyuki.com/yukiwiki/
�������ł��܂��B

=head2 �t�@�C���ꗗ

    readme.txt      �h�L�������g
    yukiwiki.cgi    YukiWiki�{��
    yukiwiki.gif    ���S�i�J���[�Łj
    yukimono.gif    ���S�i���m�N���Łj
    jcode.pl        �����R�[�h���C�u����

=head2 �C���X�g�[��

=over 4

=item 1.

�A�[�J�C�u�������܂��B

=item 2.

yukiwiki.cgi�̂͂��߂̕��ɂ���ݒ���m�F���܂��B
�ʏ�͉������Ȃ��Ă悢�ł����A
�͂��߂�$touchfile��''�ɂ��������悢�ł��傤�B

=item 3.

yukiwiki.cgi��jcode.pl�𓯂��Ƃ���ɐݒu���܂��B

=item 4.

Diff.pm�̐ݒu�ꏊ�́Ayukiwiki.cgi�̎n�߂̃R�����g���Q�Ƃ��Ă��������B

=item 5.

�T�C�Y0��yukiwiki.db�Ƃ����t�@�C����ݒu���܂��B
�iPerl�V�X�e���ɂ���Ă�yukiwiki.pag, yukiwiki.dir�j

=item 6.

yukiwiki.cgi�Ƀu���E�U����A�N�Z�X���܂��B

=back

=head2 �t�@�C���\���ƃp�[�~�b�V����

        �t�@�C��            �p�[�~�b�V����      �]�����[�h
        +--- yukiwiki.cgi    755                ASCII
        +--- yukiwiki.gif    644                BINARY
        +--- yukimono.gif    644                BINARY
        +--- jcode.pl        644                ASCII
        +--- Algorithm/      755                (�f�B���N�g���Ȃ̂œ]���Ȃ�)
             +--- Diff.pm    644                ASCII

    $dbmopen = 1; �ɂ����ꍇ:
        +--- yukiwiki.db     666                BINARY
            (yukiwiki.pag, yukiwiki.dir�̏ꍇ������j

    $dbmopen = 0; �ɂ����ꍇ: (�J�����g�f�B���N�g����777�ɂ��Ă���)
        +--- .               777                (�f�B���N�g���Ȃ̂œ]���Ȃ�)

=head1 �f�[�^�̃o�b�N�A�b�v���@

$dbmopen = 1;�̏ꍇ�́A
�f�[�^�͂��ׂ�yukiwiki.db(.dir, .pag)�ɓ���B
������o�b�N�A�b�v����΂悢�B

$dbmopen = 0;�̏ꍇ�́A
yukiwiki�Ƃ����f�B���N�g�����ł���̂ŁA
����ȉ����o�b�N�A�b�v����΂悢�B

=head1 �V�����y�[�W�̍��� 

=over 4

=item 1.

�܂��A�K���ȃy�[�W�i�Ⴆ��FrontPage�j��I�сA
�y�[�W�̉��ɂ���u�ҏW�v�����N�����ǂ�܂��B 

=item 2.

����ƃe�L�X�g���͂��ł����ԂɂȂ�̂ŁA
������NewPage�̂悤�ȒP��
�i�啶�����������݂��Ă���p������j
�������āu�ۑ��v���܂��B

=item 3.

�ۑ�����ƁAFrontPage�̃y�[�W�����������A
���Ȃ���������NewPage�Ƃ���������̌��� ? �Ƃ��������N���\������܂��B 
���� ? �͂��̃y�[�W���܂����݂��Ȃ����Ƃ�������ł��B 

=item 4.

���� ? ���N���b�N����ƐV�����y�[�WNewPage���ł��܂��̂ŁA
���Ȃ��̍D���ȕ��͂����̐V�����y�[�W�ɏ����ĕۑ����܂��B

=item 5.

NewPage�y�[�W���ł����FrontPage�� ? �͏����āA�����N�ƂȂ�܂��B 

=back

=head1 �e�L�X�g���`�̃��[��

=over 4

=item *

�A�����������s�̓t�B������ĕ\������܂��B

=item *

��s�͒i��C<< <p> >>�̋�؂�ƂȂ�܂��B

=item *

HTML�̃^�O�͏����܂���B

=item *

B<''�{�[���h''>�̂悤�ɃV���O���N�H�[�g��ł͂��ނƁA
�{�[���hC<< <b> >>�ɂȂ�܂��B

=item *

B<'''�C�^���b�N'''>�̂悤�ɃV���O���N�H�[�g�O�ł͂��ނƁA
�C�^���b�NC<< <i> >>�ɂȂ�܂��B

=item *

B<---->�̂悤�Ƀ}�C�i�X4������ƁA
������C<< <hr> >>�ɂȂ�܂��B

=item *

�s��B<*>�ł͂��߂�ƁA
�匩�o��C<< <h2> >>�ɂȂ�܂��B

=item *

�s��B<**>�ł͂��߂�ƁA
�����o��C<< <h3> >>�ɂȂ�܂��B

=item *

�s���}�C�i�X-�ł͂��߂�ƁA
�ӏ�����C<< <ul> >>�ɂȂ�܂��B
�}�C�i�X�̐���������ƃ��x����������܂��i3���x���܂Łj

    -����1
    --����1-1
    --����1-2
    -����2
    -����3
    --����3-1
    ---����3-1-1
    ---����3-1-2
    --����3-2

=item *

�R�������g���ƁA
�p��Ɖ�����̃��X�gC<< <dl> >>�������܂��B

    :�p��1:���낢�돑���������1
    :�p��2:���낢�돑���������2
    :�p��3:���낢�돑���������3

=item *

�����N

=over 4

=item *

LinkToSomePage��FrontPage�̂悤�ɁA
�p�P��̍ŏ��̈ꕶ����啶���ɂ������̂�
��ȏ�A���������̂�YukiWiki�̃y�[�W���ƂȂ�A
���ꂪ���͒��Ɋ܂܂��ƃ����N�ɂȂ�܂��B

=item *

http://www.hyuki.com/ �̂悤��URL�͎����I�Ƀ����N�ɂȂ�܂��B

=item *

��d�̑傩����[[ ]]�ł���������������A
YukiWiki�̃y�[�W���ɂȂ�܂��B
�傩�����̒��ɂ̓X�y�[�X���܂߂Ă͂����܂���B
���{����g���܂��B

=back

=item *

�s�����X�y�[�X��^�u�Ŏn�܂��Ă���ƁA
����͐��`�ς݂̒i��C<< <pre> >>�Ƃ��Ĉ����܂��B
�v���O�����̕\���ȂǂɎg���ƕ֗��ł��B


=item *

�s�� > �ł͂��߂�ƁA
���p��C<< <blockquote> >>�������܂��B
>�̐��������ƃC���f���g���[���Ȃ�܂��i3���x���܂Łj�B

    >����
    >����
    >>����Ȃ���p
    >����

=back

=head1 �X�V����

=over 4

=item *

2002�N3��1���AVersion 1.6.7�B

�p�b�P�[�W��Diff.pm�𓯍��B

=item *

2001�N10��20���AVersion 1.6.6�B

�X�V�̏Փˑ΍�B
���y�[�W�̊ȒP�ȃ`�F�b�N�T��������Ă����A
�X�V�O�Ƀ`�F�b�N�T�����r����B
�C������digest�Ƃ������������������Ε�����B
�{����MD5�Ȃǂł����Ƃ�������������̂�����ǁB

�Փˎ��ɕ\������郁�b�Z�[�W�Ȃǂ́u�Ɉ��v����̃y�[�W���Q�l�ɂ����B

=item *

2001�N10��17���AVersion 1.6.5�B

�v���r���[��ʂŁA�X�V�{�^�����������Ƃ��ɑ��M�����
���b�Z�[�W�̓��e��input�v�f��type="hidden"���g���Ė��ߍ��ނ̂���߂�B
����ɁAtextarea�v�f���g���B
�ăv���r���[�p��myspecial_�𓱓��B�ł����ꂢ�ȑ΍�ł͂Ȃ��B

=item *

2001�N8��30���AVersion 1.6.4�B

URL�Ń_�C���N�g�Ƀy�[�W�����w�肵�Ă��A
$WikiName��$BracketName�ȊO�̃y�[�W�����Ȃ��悤�ɂ����B
(is_valid_name��is_editable�Q��)�B

=item *

2001�N8��30���AVersion 1.6.3�B

RecentChanges��ҏW�E�ĕҏW�s�Ƃ����B
�ҏW�s�y�[�W��@uneditable�Ƀy�[�W��������B

=item *

2001�N2��25���AVersion 1.6.1, 1.6.2�B

�����@�\�̃o�O�C���B
do_preview��'>'�������Ȃ��o�O���C��
�i���[�U����̎w�E�j�B

=item *

2001�N2��22���AVersion 1.6.0�B
�����@�\�����������B

=item *

2001�N2��19���AVersion 1.5.4�B
�摜�t�@�C���ւ̃����N�͉摜�ɂ��Ă݂��B

=item *

2001�N2��19���AVersion 1.5.3�B
RecentChanges�̒��ɍ폜�����y�[�W������̂���߂��B
use strict;�ň��������镔������������(���S�ł͂Ȃ�)�B

=item *

2001�N2��16���AVersion 1.5.2�B
textarea�ɕ\������уv���r���[����O�� < �� > �� &lt; �� &gt; �ɕϊ�����
(do_preview, editpage, print_preview_buttons)�B

=item *

2000�N12��27���AVersion 1.5.1�B
�v���r���[��ʂ𐮗������B

=item *

2000�N12��22���AVersion 1.5.0�B
�S�̓I�ɂ����Ԃ񏑂��������B
�ꗗ��ʓr�쐬����悤�ɂ���(do_list)�B
�������ޑO�Ɋm�F��ʂ��o���悤�ɂ���(do_preview)�B
�e�L�X�g�̏�������ҏW��ʂɓ��ꂽ(do_edit, do_reedit)�B
WhatsNew��RecentChanges�ATopPage��FrontPage�ɕύX�����B

=item *

2000�N12��20���AVersion 1.1.0�B
tie�𗘗p���āAdbmopen���g���Ȃ��ꍇ�ł����삷��悤�ɏC���B
���p�҂�1�l�ł���u�Ɉ��v���񂩂�
�����Ă����������R�[�h�����ɂ��Ă��܂��B

=item *

2000�N9��5���AVersion 1.0.2�B
 <body color=...> �� <body bgcolor=...>
���p�҂���̎w�E�ɂ��B���ӁB

=item *

2000�N8��6���AVersion 1.0.1�����J�B
C MAGAZINE�i�\�t�g�o���N�p�u���b�V���O�j
2000�N10�����A�ڋL���������J�ŁB
[[ ]] �̍Ōオ�u�]�v�̂悤�ɃV�t�gJIS��
0x5D�ɂȂ�ꍇ�̉�����s�Ȃ����B

=item *

2000�N8��5���AVersion 1.0.0�����J�B

=item *

2000�N7��23���AVersion 0.82�����J�B
�ҏW���̃����N�~�X�B
<textarea>�̑����ύX�B

=item *

2000�N7��22���AVersion 0.81�����J�B
���S��g�ݍ��ށB

=item *

2000�N7��21���AVersion 0.80�����J�B
POD��CGI���ɏ������ށB

=item *

2000�N7��19���AVersion 0.70�����J�B
'''�C�^���b�N'''��A--�A---�A>>�A>>>�Ȃǂ������B

=item *

2000�N7��18���AVersion 0.60�����J�B
*����*��''����''�ɕύX

=item *

2000�N7��17���AVersion 0.50�����J�B

=item *

2000�N7��17���A����ɂ��낢��ǉ�����B

=item *

2000�N7��16���A���낢��ǉ��B

=item *

2000�N7��15���A���J�B

=back

=head1 TODO

    - �e�L�X�g�\�����[�h
    - Charset�𖾎��B
    - textarea���̕��^�O�Ή�
    - ���j���[�̉p��\�L�t�L
    - �v���r���[�̃{�^���ŁAmymsg��input��value�ɓ���Ă��邪�A���s�����̂܂�value�ɂ���Ă͂����Ȃ��̂ł͂Ȃ����B
    - �u�ĕҏW�v�̋@�\�̓u���E�U�� back �ŏ[���ł͂Ȃ����B�v���r���[�͂����ƃV���v���ɁB
    - �y�[�W�^�C�g���iWikiname�j�������ɂ�����悤�ɂ���B
    - InterWiki���̋@�\�uURL���B���A�����N�𒣂�v

=head1 ���

    Copyright (C) 2000 by Hiroshi Yuki.
    ����_ <hyuki@hyuki.com>
    http://www.hyuki.com/
    http://www.hyuki.com/yukiwiki/

����A�ӌ��A�o�O�񍐂� hyuki@hyuki.com �Ƀ��[�����Ă��������B

=head1 �z�z����

YukiWiki�́A
GNU General Public License�ɂČ��J���܂��B

YukiWiki�̓t���[�\�t�g�ł��B
�����R�ɂ��g�����������B
�����D�݂�YukiWiki������悤�ɃV���v���ɂ��Ă���܂��B

=head1 �ӎ�

�{�Ƃ�WikiWiki�������Cunningham & Cunningham, Inc.��
���ӂ��܂��B

YukiWiki���y����Ŏg���Ă�������
�l�b�g��̕��X�Ɋ��ӂ��܂��B

YukiWiki�̃��S���f�U�C�����Ă������������{��ނ���
http://city.hokkai.or.jp/~reina/
�Ɋ��ӂ��܂��B

tie���g�����ł̌��ɂȂ�R�[�h�𑗂��Ă���������
�u�Ɉ��v����Ɋ��ӂ��܂��B

=head1 �Q�ƃ����N

=over 4

=item *

YukiWiki�z�[���y�[�W
http://www.hyuki.com/yukiwiki/

=item *

�{�Ƃ�WikiWiki
http://c2.com/cgi/wiki?WikiWikiWeb

=item *

�{�Ƃ�WikiWiki�̍��(Cunningham & Cunningham, Inc.)
http://c2.com/

=item *

YukiWiki�̃��S�f�U�C�������Ă������������{��ނ���̃y�[�W
http://city.hokkai.or.jp/~reina/

=back

=cut
