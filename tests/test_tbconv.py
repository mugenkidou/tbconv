# -*- coding: utf-8 -*-
from unittest import mock

import pytest


class TestVprint(object):
    """Test for vprint()
    """
    @pytest.fixture
    def target(self):
        import tbconv
        return tbconv.vprint

    def test_one_line(self, capsys, target):
        lines = 'hoge'
        end = '\n'

        target(lines, end=end, verbose=True)

        captured = capsys.readouterr()
        assert captured.out == 'hoge\n'
        assert captured.err == ''

    def test_one_lines(self, capsys, target):
        lines = ['hoge']
        end = '\n'

        target(lines, end=end, verbose=True)

        captured = capsys.readouterr()
        assert captured.out == 'hoge\n'
        assert captured.err == ''

    def test_lines(self, capsys, target):
        lines = ['hoge', 'fuga']
        end = '\n'

        target(lines, end=end, verbose=True)

        captured = capsys.readouterr()
        assert captured.out == 'hoge\nfuga\n'
        assert captured.err == ''

    def test_end(self, capsys, target):
        lines = ['hoge', 'fuga']
        end = '*'

        target(lines, end=end, verbose=True)

        captured = capsys.readouterr()
        assert captured.out == 'hoge*fuga*'
        assert captured.err == ''


class TestGetMachineType(object):
    """Test for get_machine_type()
    """
    @property
    def machine(self):
        from tbconv import Machine
        return Machine

    @pytest.fixture
    def target(self):
        import tbconv
        return tbconv.get_machine_type

    def test_tb3(self, target):
        line = 'TRIPLET(0);'
        result = target(line)
        assert result == self.machine.TB3

    def test_tb03(self, target):
        line = 'END_STEP        = 7'
        result = target(line)
        assert result == self.machine.TB03

    def test_unknown(self, target):
        line = 'LAST_STEP(15);'
        result = target(line)
        assert result == self.machine.UNKNOWN


class ParamsMixin(object):
    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.input_file = "input_01.prm"
        self.output_file = "output_01.prm"

        self.length = 16
        self.triplet = 0

        self.note = [
            24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        ]
        self.state = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        self.slide = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        self.accent = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]

    @property
    def machine(self):
        from tbconv import Machine
        return Machine


class TestReadParam(ParamsMixin):
    """Test for read_param()
    """
    @pytest.fixture
    def target(self):
        import tbconv
        return tbconv.read_param

    def test_end_length(self, target):
        line = 'END_STEP	= 7'
        machine = self.machine.UNKNOWN

        length, triplet, note, state, slide, accent = target(line, machine)
        assert length == 7

    def test_last_length(self, target):
        line = 'LAST_STEP(15);'
        machine = self.machine.UNKNOWN

        length, triplet, note, state, slide, accent = target(line, machine)
        assert length == 15

    def test_triplet_tb3(self, target):
        line = 'TRIPLET(2);'
        machine = self.machine.UNKNOWN

        length, triplet, note, state, slide, accent = target(line, machine)
        assert triplet == 2

    def test_triplet_tb03(self, target):
        line = 'TRIPLET	= 3'
        machine = self.machine.UNKNOWN

        length, triplet, note, state, slide, accent = target(line, machine)
        assert triplet == 3

    def test_steps_tb3(self, target):
        line = 'STEP8(48,2,1,3);'
        machine = self.machine.UNKNOWN

        length, triplet, note, state, slide, accent = target(
            line, machine,
            note=self.note, state=self.state,
            slide=self.slide, accent=self.accent,
        )
        assert note == [
            24, 24, 24, 24, 24, 24, 24, 48,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ]
        assert slide == [
            0, 0, 0, 0, 0, 0, 0, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert state == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert accent == [
            0, 0, 0, 0, 0, 0, 0, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]

    def test_steps_tb03(self, target):
        line = 'STEP 8	= STATE=1 NOTE=48 ACCENT=3 SLIDE=2'
        machine = self.machine.UNKNOWN

        length, triplet, note, state, slide, accent = target(
            line, machine,
            note=self.note, state=self.state,
            slide=self.slide, accent=self.accent,
        )
        assert note == [
            24, 24, 24, 24, 24, 24, 24, 48,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ]
        assert slide == [
            0, 0, 0, 0, 0, 0, 0, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert state == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert accent == [
            0, 0, 0, 0, 0, 0, 0, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]


class TestWriteParams(ParamsMixin):
    """Test for wrtie_params()
    """
    @pytest.fixture
    def target(self):
        import tbconv
        return tbconv.write_params

    def test_unknown(self, target):
        machine = self.machine.UNKNOWN
        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(
                machine,
                self.output_file,
                self.length,
                self.triplet,
                self.note, self.state, self.slide, self.accent,
            )
        assert m.called is False

    def test_tb3_length_16(self, target):
        machine = self.machine.TB3

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(
                machine,
                self.output_file,
                self.length,
                self.triplet,
                self.note, self.state, self.slide, self.accent,
            )

        assert m.called is True
        assert m.call_count == 2

        args, kwargs = m.call_args_list[0]
        assert args == ('output_01a.prm', 'wt')

        args, kwargs = m.call_args_list[1]
        assert args == ('output_01b.prm', 'wt')

        handle = m()
        args, kwargs = handle.write.call_args_list[0]
        assert args == (
            'END_STEP	= 15\n'
            'TRIPLET	= 0\n'
            'STEP 1	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 2	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 3	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 4	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 5	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 6	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 7	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 8	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 9	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 10	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 11	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 12	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 13	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 14	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 15	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 16	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n',
        )
        assert kwargs == {}

        args, kwargs = handle.write.call_args_list[1]
        assert args == (
            'END_STEP	= 0\n'
            'TRIPLET	= 0\n'
            'STEP 1	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 2	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 3	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 4	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 5	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 6	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 7	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 8	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 9	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 10	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 11	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 12	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 13	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 14	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 15	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 16	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n',
        )
        assert kwargs == {}

    def test_tb3_length_15(self, target):
        machine = self.machine.TB3
        length = 15

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(
                machine,
                self.output_file,
                length,
                self.triplet,
                self.note, self.state, self.slide, self.accent,
            )

        assert m.called is True
        assert m.call_count == 1

        args, kwargs = m.call_args_list[0]
        assert args == ('output_01.prm', 'wt')

        handle = m()
        args, kwargs = handle.write.call_args_list[0]
        assert args == (
            'END_STEP	= 15\n'
            'TRIPLET	= 0\n'
            'STEP 1	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 2	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 3	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 4	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 5	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 6	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 7	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 8	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 9	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 10	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 11	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 12	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 13	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 14	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 15	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 16	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n',
        )
        assert kwargs == {}

    def test_tb3_length_14(self, target):
        machine = self.machine.TB3
        length = 14

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(
                machine,
                self.output_file,
                length,
                self.triplet,
                self.note, self.state, self.slide, self.accent,
            )

        assert m.called is True
        assert m.call_count == 1

        args, kwargs = m.call_args_list[0]
        assert args == ('output_01.prm', 'wt')

        handle = m()
        args, kwargs = handle.write.call_args_list[0]
        assert args == (
            'END_STEP	= 14\n'
            'TRIPLET	= 0\n'
            'STEP 1	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 2	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 3	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 4	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 5	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 6	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 7	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 8	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 9	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 10	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 11	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 12	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 13	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 14	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 15	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n'
            'STEP 16	= STATE=0 NOTE=24 ACCENT=0 SLIDE=0\n',
        )
        assert kwargs == {}

    def test_tb03_length_16(self, target):
        machine = self.machine.TB03
        length = 16

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(
                machine,
                self.output_file,
                length,
                self.triplet,
                self.note, self.state, self.slide, self.accent,
            )

        assert m.called is True
        assert m.call_count == 1

        args, kwargs = m.call_args_list[0]
        assert args == ('output_01.prm', 'wt')

        handle = m()
        handle.write.assert_called_once_with(
            'TRIPLET(0);\n'
            'LAST_STEP(16);\n'
            'GATE_WIDTH(67);\n'
            'STEP1(24,0,0,0);\n'
            'STEP2(24,0,0,0);\n'
            'STEP3(24,0,0,0);\n'
            'STEP4(24,0,0,0);\n'
            'STEP5(24,0,0,0);\n'
            'STEP6(24,0,0,0);\n'
            'STEP7(24,0,0,0);\n'
            'STEP8(24,0,0,0);\n'
            'STEP9(24,0,0,0);\n'
            'STEP10(24,0,0,0);\n'
            'STEP11(24,0,0,0);\n'
            'STEP12(24,0,0,0);\n'
            'STEP13(24,0,0,0);\n'
            'STEP14(24,0,0,0);\n'
            'STEP15(24,0,0,0);\n'
            'STEP16(24,0,0,0);\n'
            'STEP17(24,0,0,0);\n'
            'STEP18(24,0,0,0);\n'
            'STEP19(24,0,0,0);\n'
            'STEP20(24,0,0,0);\n'
            'STEP21(24,0,0,0);\n'
            'STEP22(24,0,0,0);\n'
            'STEP23(24,0,0,0);\n'
            'STEP24(24,0,0,0);\n'
            'STEP25(24,0,0,0);\n'
            'STEP26(24,0,0,0);\n'
            'STEP27(24,0,0,0);\n'
            'STEP28(24,0,0,0);\n'
            'STEP29(24,0,0,0);\n'
            'STEP30(24,0,0,0);\n'
            'STEP31(24,0,0,0);\n'
            'STEP32(24,0,0,0);\n'
            'BANK(0);\n'
            'PATCH(-1);\n'
        )


class TestMain(ParamsMixin):
    """Test for main()
    """
    @pytest.fixture
    def target(self):
        import tbconv
        return tbconv.main

    def test_no_such_file(self, capsys, target):
        m = mock.mock_open()
        with mock.patch('os.path.exists') as m_exists:
            with mock.patch('tbconv.open', m):
                m_exists.return_value = False
                target(self.input_file, self.output_file)

        assert m.called is False

        captured = capsys.readouterr()
        assert captured.out == 'No such file: input_01.prm\n'
        assert captured.err == ''
