# -*- coding: utf-8 -*-
from unittest import mock

import pytest


class TestGetMachineType(object):
    """Test for getMachineType()
    """
    @pytest.fixture
    def target(self):
        from tbconv import getMachineType
        return getMachineType

    def test_tb3(self, target):
        line = 'TRIPLET(0);'
        result = target(line)
        assert result == 'TB-3'

    def test_tb03(self, target):
        line = 'END_STEP        = 7'
        result = target(line)
        assert result == 'TB-03'

    def test_unknown(self, target):
        line = 'LAST_STEP(15);'
        result = target(line)
        assert result == 'unknown'


class GlobalParamsMixin(object):
    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.init_params()

    def init_params(self):
        """Initialize all global params.
        """
        self.set_length(16)
        self.set_triplet(0)
        self.set_note([
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ])
        self.set_state([
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ])
        self.set_slide([
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ])
        self.set_accent([
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ])
        self.set_input_file("input_01.prm")
        self.set_output_file("output_01.prm")

    # length
    def set_length(self, val):
        import tbconv
        tbconv._set_length(val)

    def get_length(self):
        import tbconv
        return tbconv._get_length()

    # triplet
    def set_triplet(self, val):
        import tbconv
        return tbconv._set_triplet(val)

    def get_triplet(self):
        import tbconv
        return tbconv._get_triplet()

    # note
    def set_note(self, val):
        import tbconv
        return tbconv._set_note(val)

    def get_note(self):
        import tbconv
        return tbconv._get_note()

    # state
    def set_state(self, val):
        import tbconv
        return tbconv._set_state(val)

    def get_state(self):
        import tbconv
        return tbconv._get_state()

    # slide
    def set_slide(self, val):
        import tbconv
        return tbconv._set_slide(val)

    def get_slide(self):
        import tbconv
        return tbconv._get_slide()

    # accent
    def set_accent(self, val):
        import tbconv
        return tbconv._set_accent(val)

    def get_accent(self):
        import tbconv
        return tbconv._get_accent()

    # step
    def set_step(self, val):
        import tbconv
        return tbconv._set_step(val)

    def get_step(self):
        import tbconv
        return tbconv._get_step()

    # input_file
    def set_input_file(self, val):
        import tbconv
        return tbconv._set_input_file(val)

    def get_input_file(self):
        import tbconv
        return tbconv._get_input_file()

    # output_file
    def set_output_file(self, val):
        import tbconv
        return tbconv._set_output_file(val)

    def get_output_file(self):
        import tbconv
        return tbconv._get_output_file()


class TestReadParam(GlobalParamsMixin):
    """Test for readParam()
    """
    @pytest.fixture
    def target(self):
        from tbconv import readParam
        return readParam

    def test_end_length(self, target):
        line = 'END_STEP	= 7'
        machine = 'unknown'

        target(line, machine)
        assert self.get_length() == 7

    def test_last_length(self, target):
        line = 'LAST_STEP(15);'
        machine = 'unknown'

        target(line, machine)
        assert self.get_length() == 15

    def test_triplet_tb3(self, target):
        line = 'TRIPLET(2);'
        machine = 'unknown'

        target(line, machine)
        assert self.get_triplet() == 2

    def test_triplet_tb03(self, target):
        line = 'TRIPLET	= 3'
        machine = 'unknown'

        target(line, machine)
        assert self.get_triplet() == 3

    def test_steps_tb3(self, target):
        line = 'STEP8(48,2,1,3);'
        machine = 'unknown'

        target(line, machine)
        assert self.get_step() == [
            '8', '48', '2', '1', '3',
        ]
        assert self.get_note() == [
            24, 24, 24, 24, 24, 24, 24, 48,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ]
        assert self.get_slide() == [
            0, 0, 0, 0, 0, 0, 0, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert self.get_state() == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert self.get_accent() == [
            0, 0, 0, 0, 0, 0, 0, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]

    def test_steps_tb03(self, target):
        line = 'STEP 8	= STATE=1 NOTE=48 ACCENT=3 SLIDE=2'
        machine = 'unknown'

        target(line, machine)
        assert self.get_step() == [
            '8', '1', '48', '3', '2',
        ]
        assert self.get_note() == [
            24, 24, 24, 24, 24, 24, 24, 48,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
        ]
        assert self.get_slide() == [
            0, 0, 0, 0, 0, 0, 0, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert self.get_state() == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert self.get_accent() == [
            0, 0, 0, 0, 0, 0, 0, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]


class TestWriteParams(GlobalParamsMixin):
    """Test for wrtieParams()
    """
    @pytest.fixture
    def target(self):
        from tbconv import writeParams
        return writeParams

    def test_unknown(self, target):
        machine = 'unknown'

        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(machine)
        assert m.called == False
        
    def test_tb3_length_16(self, target):
        self.set_length(16)
        machine = 'TB-3'
        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(machine)

        assert m.called == True
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
        self.set_length(15)
        machine = 'TB-3'
        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(machine)

        assert m.called == True
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
        self.set_length(14)
        machine = 'TB-3'
        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(machine)

        assert m.called == True
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
        self.set_length(16)
        machine = 'TB-03'
        m = mock.mock_open()
        with mock.patch('tbconv.open', m):
            target(machine)

        assert m.called == True
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
