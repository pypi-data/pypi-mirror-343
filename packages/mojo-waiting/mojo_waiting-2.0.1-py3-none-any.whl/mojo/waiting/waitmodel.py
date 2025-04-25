"""
.. module:: waitmodel
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains objects used in conjunction with waiting.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from typing import List, Optional, Protocol, Type

from types import TracebackType

import os
import threading
import time

from datetime import datetime, timedelta

from mojo.waiting.constants import (
    TimeoutState,
    MSG_TEMPL_TIME_COMPONENTS,
)


class TimeoutContext:
    """
        The :class:`TimeoutContext` object is used to store the context used to track the timeout
        of a single operations or multiple consecutive operations.
    """
    def __init__(self, timeout: float, interval: float=0, delay: float=0, doevery: int=-1,
                 what_for: Optional[str]=None):
        self._timeout = timeout
        self._interval = interval
        self._delay = delay
        self._doevery = doevery
        self._what_for = what_for

        self._loop_counter = 0
        self._now_time = None
        self._start_time = None
        self._end_time = None
        self._final_attempt = False
        self._wait_state = TimeoutState.NotStarted
        return

    @property
    def completed(self) -> bool:
        """
            Indicates the wait was successfully completed.
        """
        return self._wait_state == TimeoutState.Completed

    @property
    def end_time(self) -> datetime:
        """
            Property to retreive the current endtime
        """
        return self._end_time

    @property
    def delay(self) -> float:
        """
            Property for retreiving the delay value.
        """
        return self._delay

    @property
    def final_attempt(self) -> bool:
        """
            Property for retreiving the final_attempt marker and for monitoring and debugging
            calls to look at the final attempt marker.
        """
        return self._final_attempt

    @property
    def has_timed_out(self) -> bool:
        """
            Property indicating if the wait context reached its timeout while running.
        """
        htoval = self._wait_state != TimeoutState.Completed and self._now_time > self._end_time
        return htoval

    @property
    def interval(self) -> float:
        """
            Property for retreiving the interval value.
        """
        return self._interval

    @property
    def is_do_every_interval(self):
        dei = False
        if self._doevery > -1:
            dei = self._loop_counter % self._doevery == 0
        return dei

    @property
    def timeout(self) -> float:
        """
            Property for retreiving the timeout value.
        """
        return self._timeout

    @property
    def wait_state(self) -> TimeoutState:
        """
            Property to return the current wait state of the wait context.
        """
        return self._wait_state

    @property
    def what_for(self) -> str:
        """
            Property for retreiving the what_for value.
        """
        return self._what_for

    def continue_waiting(self):
        """
            Reset the wait context to a waiting state so we can continue waiting.
        """
        self._wait_state = TimeoutState.Running
        return

    def create_timeout(self, what_for: Optional[str]=None, detail: Optional[List[str]]=None,
                       mark_timeout: Optional[bool]=True) -> TimeoutError:
        """
            Helper method used to create detail :class:`AKitTimeoutError` exceptions
            that can be raised in the context of the looper method. 
        """
        if what_for is None:
            what_for = self._what_for

        err_msg = self.format_timeout_message(what_for, detail=detail)
        err_inst = TimeoutError(err_msg)

        if mark_timeout:
            self.mark_timeout()

        return err_inst

    def extend_timeout(self, seconds: float):
        """
            Extend the timeout of the current wait context by the specified number of seconds.

            :param seconds: The time in seconds to extend the wait period.
        """
        self._end_time = self._end_time + timedelta(seconds=seconds)
        self._wait_state = TimeoutState.Running
        self._final_attempt = False
        return

    def format_timeout_message(self, what_for: str, detail: Optional[List[str]]=None) -> str:
        """
            Helper method used to create format a detailed error message for reporting a timeout
            condition.
        """
        diff_time = self._now_time - self._start_time
        err_msg_lines = [
            "Timeout waiting for {}:".format(what_for),
            MSG_TEMPL_TIME_COMPONENTS.format(self._timeout, self._start_time, self._end_time,
                                             self._now_time, diff_time),
        ]

        if detail is not None:
            err_msg_lines.extend(detail)

        err_msg = os.linesep.join(err_msg_lines)
        return err_msg

    def mark_begin(self):
        """
            Mark the wait context as running.
        """
        self._now_time = datetime.now()
        self._start_time = self._now_time
        self._end_time = self._start_time + timedelta(seconds=self._timeout)
        self._wait_state = TimeoutState.Running
        return

    def mark_complete(self):
        """
            Mark the wait context as complete.
        """
        self._wait_state = TimeoutState.Completed
        return

    def mark_final_attempt(self):
        """
            Mark the wait context as being in the final attempt condition.
        """
        self._final_attempt = True
        return

    def mark_time(self):
        """
            Called to mark the current time in the :class:`WaitContext` instance.
        """
        self._now_time = datetime.now()
        return

    def mark_timeout(self):
        """
            Called to mark the wait context as timed out.
        """
        self._wait_state = TimeoutState.TimedOut
        return

    def reduce_delay(self, secs):
        """
            Reduce the wait start delay.
        """
        if secs > self._delay:
            self._delay = 0
        else:
            self._delay = self._delay - secs
        return

    def should_continue(self) -> bool:
        """
            Indicates if a wait condition should continue based on time specifications and context.
        """
        self._now_time = datetime.now()
        self._loop_counter += 1

        scont = True

        if self._wait_state == TimeoutState.Completed:
            scont = False
        elif self._now_time > self._end_time:
            scont = False

        return scont



class WaitCallback(Protocol):
    def __call__(self, wctx: TimeoutContext, *args, **kwargs) -> bool:
        """
            This specifies a callable object that can have variable arguments but
            that must have a final_attempt keywork arguement.  The expected behavior
            of the callback is to return false if the expected condition has not
            been meet.
        """

class WaitContext(TimeoutContext):
    """
        Place holder for differences that might arise between the base TimeoutContext and
        the WaitContext used for wait loops.
    """


class WaitGate:

    def __init__(self, gate: threading.Event, message: Optional[str]=None, timeout: Optional[float]=None,
                 timeout_args: Optional[list]=None):
        self._gate = gate
        self._message = message
        self._timeout = timeout
        self._timeout_args = timeout_args
        return

    @property
    def gate(self) -> threading.Event:
        return self._gate

    @property
    def message(self) -> str:
        return self._message

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def timeout_args(self) -> list:
        return self._timeout_args

    def clear(self):
        self._gate.clear()
        return

    def is_set(self) -> bool:
        rtnval = self._gate.is_set()
        return rtnval

    def set(self):
        self._gate.set()
        return

    def wait(self, timeout: Optional[float]=None, raise_timeout=False):

        if timeout is None:
            timeout = self._timeout

        rtnval = self._gate.wait(timeout=self._timeout)
        if not rtnval:
            errmsg = ""
            raise TimeoutError(errmsg)

        return rtnval


class WaitingScope:
    def __init__(self, gates: List[WaitGate],):
        self._gates = gates
        return

    def __enter__(self):
        for gate in self._gates:
            gate.clear()
        return
    
    def __exit__(self, ex_type: Type, ex_inst: BaseException, ex_tb: TracebackType):
        return
    
    def wait(self):

        for gate in self.gates:
            gate.wait()

        return
