NAME
    YukiWiki - ���R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���Web�y�[�W�\�zCGI

        Copyright (C) 2000,2001 by Hiroshi Yuki.
        ����_ <hyuki@hyuki.com>
        http://www.hyuki.com/
        http://www.hyuki.com/yukiwiki/

SYNOPSIS
        http://www.hyuki.com/yukiwiki/yukiwiki.cgi

DESCRIPTION
    YukiWiki�i����E�B�L�B�j�͎Q���҂����R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���
    �s�v�c��Web�y�[�W�Q�����CGI�ł��B
    Web�œ��삷��f���Ƃ�����Ǝ��Ă��܂����A
    Web�f�����P�Ƀ��b�Z�[�W��ǉ����邾���Ȃ̂ɑ΂��āA
    YukiWiki�́AWeb�y�[�W�S�̂����R�ɕύX���邱�Ƃ��ł��܂��B

    YukiWiki�́ACunningham & Cunningham��WikiWikiWeb��
    �d�l���Q�l�ɂ��ēƎ��ɍ���܂����B

    YukiWiki��Perl�ŏ����ꂽCGI�X�N���v�g�Ƃ��Ď�������Ă��܂��̂ŁA
    Perl�����삷��Web�T�[�o�Ȃ�Δ�r�I�e�Ղɐݒu�ł��܂��B

    ���Ƃ�dbmopen���g������Ȃ�ΐݒu�ł��܂�(Version
    1.5.0�ȍ~�Ȃ�dbmopen���g���Ȃ��Ă��ݒu�ł��܂�)�B

    YukiWiki�̓t���[�\�t�g�ł��B �����R�ɂ��g�����������B

�ݒu���@
  ����

    YukiWiki�̍ŐV�ł́A http://www.hyuki.com/yukiwiki/ �������ł��܂��B

  �t�@�C���ꗗ

        readme.txt      �h�L�������g
        yukiwiki.cgi    YukiWiki�{��
        yukiwiki.gif    ���S�i�J���[�Łj
        yukimono.gif    ���S�i���m�N���Łj
        jcode.pl        �����R�[�h���C�u����

  �C���X�g�[��

    1.  �A�[�J�C�u�������܂��B

    2.  yukiwiki.cgi�̂͂��߂̕��ɂ���ݒ���m�F���܂��B
        �ʏ�͉������Ȃ��Ă悢�ł����A
        �͂��߂�$touchfile��''�ɂ��������悢�ł��傤�B

    3.  yukiwiki.cgi��jcode.pl�𓯂��Ƃ���ɐݒu���܂��B

    4.  Diff.pm�̐ݒu�ꏊ�́Ayukiwiki.cgi�̎n�߂̃R�����g���Q�Ƃ��Ă��������
        B

    5.  �T�C�Y0��yukiwiki.db�Ƃ����t�@�C����ݒu���܂��B
        �iPerl�V�X�e���ɂ���Ă�yukiwiki.pag, yukiwiki.dir�j

    6.  yukiwiki.cgi�Ƀu���E�U����A�N�Z�X���܂��B

  �t�@�C���\���ƃp�[�~�b�V����

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

�f�[�^�̃o�b�N�A�b�v���@
    $dbmopen = 1;�̏ꍇ�́A �f�[�^�͂��ׂ�yukiwiki.db(.dir, .pag)�ɓ���B
    ������o�b�N�A�b�v����΂悢�B

    $dbmopen = 0;�̏ꍇ�́A yukiwiki�Ƃ����f�B���N�g�����ł���̂ŁA
    ����ȉ����o�b�N�A�b�v����΂悢�B

�V�����y�[�W�̍���
    1.  �܂��A�K���ȃy�[�W�i�Ⴆ��FrontPage�j��I�сA
        �y�[�W�̉��ɂ���u�ҏW�v�����N�����ǂ�܂��B

    2.  ����ƃe�L�X�g���͂��ł����ԂɂȂ�̂ŁA ������NewPage�̂悤�ȒP��
        �i�啶�����������݂��Ă���p������j �������āu�ۑ��v���܂��B

    3.  �ۑ�����ƁAFrontPage�̃y�[�W�����������A
        ���Ȃ���������NewPage�Ƃ���������̌��� ?
        �Ƃ��������N���\������܂��B ���� ?
        �͂��̃y�[�W���܂����݂��Ȃ����Ƃ�������ł��B

    4.  ���� ? ���N���b�N����ƐV�����y�[�WNewPage���ł��܂��̂ŁA
        ���Ȃ��̍D���ȕ��͂����̐V�����y�[�W�ɏ����ĕۑ����܂��B

    5.  NewPage�y�[�W���ł����FrontPage�� ? �͏����āA�����N�ƂȂ�܂��B

�e�L�X�g���`�̃��[��
    *   �A�����������s�̓t�B������ĕ\������܂��B

    *   ��s�͒i��`<p>'�̋�؂�ƂȂ�܂��B

    *   HTML�̃^�O�͏����܂���B

    *   ''�{�[���h''�̂悤�ɃV���O���N�H�[�g��ł͂��ނƁA
        �{�[���h`<b>'�ɂȂ�܂��B

    *   '''�C�^���b�N'''�̂悤�ɃV���O���N�H�[�g�O�ł͂��ނƁA
        �C�^���b�N`<i>'�ɂȂ�܂��B

    *   ----�̂悤�Ƀ}�C�i�X4������ƁA ������`<hr>'�ɂȂ�܂��B

    *   �s��*�ł͂��߂�ƁA �匩�o��`<h2>'�ɂȂ�܂��B

    *   �s��**�ł͂��߂�ƁA �����o��`<h3>'�ɂȂ�܂��B

    *   �s���}�C�i�X-�ł͂��߂�ƁA �ӏ�����`<ul>'�ɂȂ�܂��B
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

    *   �R�������g���ƁA �p��Ɖ�����̃��X�g`<dl>'�������܂��B

            :�p��1:���낢�돑���������1
            :�p��2:���낢�돑���������2
            :�p��3:���낢�돑���������3

    *   �����N

        *   LinkToSomePage��FrontPage�̂悤�ɁA
            �p�P��̍ŏ��̈ꕶ����啶���ɂ������̂�
            ��ȏ�A���������̂�YukiWiki�̃y�[�W���ƂȂ�A
            ���ꂪ���͒��Ɋ܂܂��ƃ����N�ɂȂ�܂��B

        *   http://www.hyuki.com/ �̂悤��URL�͎����I�Ƀ����N�ɂȂ�܂��B

        *   ��d�̑傩����[[ ]]�ł���������������A
            YukiWiki�̃y�[�W���ɂȂ�܂��B
            �傩�����̒��ɂ̓X�y�[�X���܂߂Ă͂����܂���B
            ���{����g���܂��B

    *   �s�����X�y�[�X��^�u�Ŏn�܂��Ă���ƁA
        ����͐��`�ς݂̒i��`<pre>'�Ƃ��Ĉ����܂��B
        �v���O�����̕\���ȂǂɎg���ƕ֗��ł��B

    *   �s�� > �ł͂��߂�ƁA ���p��`<blockquote>'�������܂��B
        >�̐��������ƃC���f���g���[���Ȃ�܂��i3���x���܂Łj�B

            >����
            >����
            >>����Ȃ���p
            >����

�X�V����
    *   2002�N3��1���AVersion 1.6.7�B

        �p�b�P�[�W��Diff.pm�𓯍��B

    *   2001�N10��20���AVersion 1.6.6�B

        �X�V�̏Փˑ΍�B ���y�[�W�̊ȒP�ȃ`�F�b�N�T��������Ă����A
        �X�V�O�Ƀ`�F�b�N�T�����r����B
        �C������digest�Ƃ������������������Ε�����B
        �{����MD5�Ȃǂł����Ƃ�������������̂�����ǁB

        �Փˎ��ɕ\������郁�b�Z�[�W�Ȃǂ́u�Ɉ��v����̃y�[�W���Q�l�ɂ����B

    *   2001�N10��17���AVersion 1.6.5�B

        �v���r���[��ʂŁA�X�V�{�^�����������Ƃ��ɑ��M�����
        ���b�Z�[�W�̓��e��input�v�f��type="hidden"���g���Ė��ߍ��ނ̂���߂�
        �B ����ɁAtextarea�v�f���g���B
        �ăv���r���[�p��myspecial_�𓱓��B�ł����ꂢ�ȑ΍�ł͂Ȃ��B

    *   2001�N8��30���AVersion 1.6.4�B

        URL�Ń_�C���N�g�Ƀy�[�W�����w�肵�Ă��A
        $WikiName��$BracketName�ȊO�̃y�[�W�����Ȃ��悤�ɂ����B
        (is_valid_name��is_editable�Q��)�B

    *   2001�N8��30���AVersion 1.6.3�B

        RecentChanges��ҏW�E�ĕҏW�s�Ƃ����B
        �ҏW�s�y�[�W��@uneditable�Ƀy�[�W��������B

    *   2001�N2��25���AVersion 1.6.1, 1.6.2�B

        �����@�\�̃o�O�C���B do_preview��'>'�������Ȃ��o�O���C��
        �i���[�U����̎w�E�j�B

    *   2001�N2��22���AVersion 1.6.0�B �����@�\�����������B

    *   2001�N2��19���AVersion 1.5.4�B
        �摜�t�@�C���ւ̃����N�͉摜�ɂ��Ă݂��B

    *   2001�N2��19���AVersion 1.5.3�B
        RecentChanges�̒��ɍ폜�����y�[�W������̂���߂��B use
        strict;�ň��������镔������������(���S�ł͂Ȃ�)�B

    *   2001�N2��16���AVersion 1.5.2�B
        textarea�ɕ\������уv���r���[����O�� < �� > �� &lt; �� &gt;
        �ɕϊ����� (do_preview, editpage, print_preview_buttons)�B

    *   2000�N12��27���AVersion 1.5.1�B �v���r���[��ʂ𐮗������B

    *   2000�N12��22���AVersion 1.5.0�B �S�̓I�ɂ����Ԃ񏑂��������B
        �ꗗ��ʓr�쐬����悤�ɂ���(do_list)�B
        �������ޑO�Ɋm�F��ʂ��o���悤�ɂ���(do_preview)�B
        �e�L�X�g�̏�������ҏW��ʂɓ��ꂽ(do_edit, do_reedit)�B
        WhatsNew��RecentChanges�ATopPage��FrontPage�ɕύX�����B

    *   2000�N12��20���AVersion 1.1.0�B
        tie�𗘗p���āAdbmopen���g���Ȃ��ꍇ�ł����삷��悤�ɏC���B
        ���p�҂�1�l�ł���u�Ɉ��v���񂩂�
        �����Ă����������R�[�h�����ɂ��Ă��܂��B

    *   2000�N9��5���AVersion 1.0.2�B <body color=...> �� <body bgcolor=...>
        ���p�҂���̎w�E�ɂ��B���ӁB

    *   2000�N8��6���AVersion 1.0.1�����J�B C
        MAGAZINE�i�\�t�g�o���N�p�u���b�V���O�j
        2000�N10�����A�ڋL���������J�ŁB [[ ]]
        �̍Ōオ�u�]�v�̂悤�ɃV�t�gJIS�� 0x5D�ɂȂ�ꍇ�̉�����s�Ȃ����B

    *   2000�N8��5���AVersion 1.0.0�����J�B

    *   2000�N7��23���AVersion 0.82�����J�B �ҏW���̃����N�~�X�B
        <textarea>�̑����ύX�B

    *   2000�N7��22���AVersion 0.81�����J�B ���S��g�ݍ��ށB

    *   2000�N7��21���AVersion 0.80�����J�B POD��CGI���ɏ������ށB

    *   2000�N7��19���AVersion 0.70�����J�B
        '''�C�^���b�N'''��A--�A---�A>>�A>>>�Ȃǂ������B

    *   2000�N7��18���AVersion 0.60�����J�B *����*��''����''�ɕύX

    *   2000�N7��17���AVersion 0.50�����J�B

    *   2000�N7��17���A����ɂ��낢��ǉ�����B

    *   2000�N7��16���A���낢��ǉ��B

    *   2000�N7��15���A���J�B

TODO
        - �e�L�X�g�\�����[�h
        - Charset�𖾎��B
        - textarea���̕��^�O�Ή�
        - ���j���[�̉p��\�L�t�L
        - �v���r���[�̃{�^���ŁAmymsg��input��value�ɓ���Ă��邪�A���s�����̂܂�value�ɂ���Ă͂����Ȃ��̂ł͂Ȃ����B
        - �u�ĕҏW�v�̋@�\�̓u���E�U�� back �ŏ[���ł͂Ȃ����B�v���r���[�͂����ƃV���v���ɁB
        - �y�[�W�^�C�g���iWikiname�j�������ɂ�����悤�ɂ���B
        - InterWiki���̋@�\�uURL���B���A�����N�𒣂�v

���
        Copyright (C) 2000 by Hiroshi Yuki.
        ����_ <hyuki@hyuki.com>
        http://www.hyuki.com/
        http://www.hyuki.com/yukiwiki/

    ����A�ӌ��A�o�O�񍐂� hyuki@hyuki.com �Ƀ��[�����Ă��������B

�z�z����
    YukiWiki�́A GNU General Public License�ɂČ��J���܂��B

    YukiWiki�̓t���[�\�t�g�ł��B �����R�ɂ��g�����������B
    �����D�݂�YukiWiki������悤�ɃV���v���ɂ��Ă���܂��B

�ӎ�
    �{�Ƃ�WikiWiki�������Cunningham & Cunningham, Inc.�� ���ӂ��܂��B

    YukiWiki���y����Ŏg���Ă������� �l�b�g��̕��X�Ɋ��ӂ��܂��B

    YukiWiki�̃��S���f�U�C�����Ă������������{��ނ���
    http://city.hokkai.or.jp/~reina/ �Ɋ��ӂ��܂��B

    tie���g�����ł̌��ɂȂ�R�[�h�𑗂��Ă���������
    �u�Ɉ��v����Ɋ��ӂ��܂��B

�Q�ƃ����N
    *   YukiWiki�z�[���y�[�W http://www.hyuki.com/yukiwiki/

    *   �{�Ƃ�WikiWiki http://c2.com/cgi/wiki?WikiWikiWeb

    *   �{�Ƃ�WikiWiki�̍��(Cunningham & Cunningham, Inc.) http://c2.com/

    *   YukiWiki�̃��S�f�U�C�������Ă������������{��ނ���̃y�[�W
        http://city.hokkai.or.jp/~reina/

