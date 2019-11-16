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
        assert result.type == self.machine.TB3

    def test_tb03(self, target):
        line = 'END_STEP        = 7'
        result = target(line)
        assert result.type == self.machine.TB03

    def test_unknown(self, target):
        line = 'LAST_STEP(15);'
        result = target(line)
        assert result.type == self.machine.UNKNOWN


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

    @property
    def machine_unknown(self):
        from tbconv import BaseMachine
        return BaseMachine()

    @property
    def machine_tb3(self):
        from tbconv import MachineTB3
        return MachineTB3()

    @property
    def machine_tb03(self):
        from tbconv import MachineTB03
        return MachineTB03()


class TestTB3ReadParam(ParamsMixin):
    """Test for MachineTB3 read_param method
    """
    @pytest.fixture
    def target(self):
        from tbconv import MachineTB3
        return MachineTB3()

    def test_last_length(self, target):
        line = 'LAST_STEP(15);'

        target.read_param(line)
        assert target.length == 15

    def test_triplet(self, target):
        line = 'TRIPLET(2);'

        target.read_param(line)
        assert target.triplet == 2

    def test_steps(self, target):
        line = 'STEP8(48,2,1,3);'

        target.read_param(line)
        assert target.note == [
            24, 24, 24, 24, 24, 24, 24, 48,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ]
        assert target.slide == [
            0, 0, 0, 0, 0, 0, 0, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert target.state == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert target.accent == [
            0, 0, 0, 0, 0, 0, 0, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]


class TestTB03ReadParam(ParamsMixin):
    """Test for MachineTB03 read_param method
    """
    @pytest.fixture
    def target(self):
        from tbconv import MachineTB03
        return MachineTB03()

    def test_end_length(self, target):
        line = 'END_STEP	= 7'

        target.read_param(line)
        assert target.length == 7

    def test_triplet(self, target):
        line = 'TRIPLET	= 3'

        target.read_param(line)
        assert target.triplet == 3

    def test_steps(self, target):
        line = 'STEP 8	= STATE=1 NOTE=48 ACCENT=3 SLIDE=2'

        target.read_param(line)
        assert target.note == [
            24, 24, 24, 24, 24, 24, 24, 48,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ]
        assert target.slide == [
            0, 0, 0, 0, 0, 0, 0, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert target.state == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert target.accent == [
            0, 0, 0, 0, 0, 0, 0, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]


class TestTB3WriteParams(ParamsMixin):
    """Test for MachineTB3 write_params method
    """
    @pytest.fixture
    def target(self):
        from tbconv import MachineTB3
        return MachineTB3()

    def test_length_16(self, target):
        machine = self.machine_unknown
        machine.length = 16

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target.write_params(machine, self.output_file)

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

    def test_length_15(self, target):
        machine = self.machine_unknown
        machine.length = 15

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target.write_params(machine, self.output_file)

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

    def test_length_14(self, target):
        machine = self.machine_unknown
        machine.length = 14

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target.write_params(machine, self.output_file)

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


class TestTB03WriteParams(ParamsMixin):
    """Test for MachineTB03 write_params method
    """
    @pytest.fixture
    def target(self):
        from tbconv import MachineTB03
        return MachineTB03()

    def test_length_16(self, target):
        machine = self.machine_unknown
        machine.length = 16

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target.write_params(machine, self.output_file)

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
