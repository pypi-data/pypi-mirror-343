import threading
from kmodels.models import CoreModel
from kmodels.types import OmitIfUnset, Unset, unset
from pydantic import ConfigDict, model_validator

from klocker.simple.constants import LOCK_FAILURE_T, THREAD_FAILURE_T
from klocker.simple.thread.base import SimpleBaseLocalThreadDataInterface, SimpleBaseLocalThreadDataController


class SimpleThreadFailure(CoreModel):
    model_config = ConfigDict(frozen=True, extra='forbid', arbitrary_types_allowed=True)
    exception: OmitIfUnset[BaseException | Unset] = unset

    @model_validator(mode='after')
    def reason_consistency(self):
        if self.reason == 'exception' and self.exception is unset:
            raise ValueError(f'If exception happened you have to set `exception` to the exception that happened.')
        return self


class SimpleThreadLockFailure(SimpleThreadFailure):
    reason: LOCK_FAILURE_T


class SimpleThreadExecutionFailure(SimpleThreadFailure):
    reason: THREAD_FAILURE_T


class SimpleLocalThreadState(CoreModel):
    model_config = ConfigDict(frozen=True, extra='forbid')
    acquired: bool = False
    waited: bool = False
    failure_details: OmitIfUnset[SimpleThreadFailure | Unset] = unset


class SimpleLocalThreadStateInterface(SimpleBaseLocalThreadDataInterface):
    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'state')

    @property
    def data(self) -> SimpleLocalThreadState:
        self._raise_not_initialized()
        return self._local_env.state

    @property
    def successful(self) -> bool:
        """
        Indicates whether the thread successfully acquired the resource and completed
        its operation without interruption or failure.

        Returns:
            - `True`: If the thread successfully acquired the resource (`acquired is True`) and
              no failure occurred in its context (`failure_details is Unset`).
            - `False`: If the thread encountered a failure during its operation,
              even if the resource was acquired successfully.
        """
        return self.acquired and isinstance(self.failure_details, Unset)

    @property
    def has_failed(self) -> bool:
        """
        Indicates whether the thread has encountered any failure.

        Returns:
            - `True`: If `failure_details` contains a failure of type `SimpleThreadFailure`
               (e.g., `SimpleThreadLockFailure` or `SimpleThreadExecutionFailure`).
            - `False`: If `failure_details` is `Unset` or does not represent a failure.
        """
        return not self.successful

    @property
    def acquired(self) -> bool:
        """
        Indicates whether the thread successfully acquired the lock or resource.

        Returns:
            - `True`: If the lock or resource has been acquired by the thread.
            - `False`: If the lock or resource has not been acquired.

        This property only reflects the acquisition state and does not guarantee
        that subsequent operations were successful or completed without interruptions.
        To check for a successful operation, consider using additional mechanisms
        such as the 'successful' property or manually verifying the thread's context.
        """

        return self.data.acquired

    @property
    def waited(self) -> bool:
        return self.data.waited

    @property
    def failure_details(self) -> SimpleThreadFailure | Unset:
        """
        Retrieves the details of any failure that occurred in the thread's context.

        Returns:
            - `SimpleThreadLockFailure`: If a failure occurred related to the lock
              (e.g., issues acquiring or releasing the lock).
            - `SimpleThreadExecutionFailure`: If a failure occurred during the execution
              of the function assigned to the thread.
            - `Unset`: If no failure details are present (i.e., no error occurred).

        This property allows users to detect and handle errors that occurred during thread
        operations, such as synchronization issues or exceptions raised in user logic.
        """

        return self.data.failure_details


class SimpleLocalThreadStateController(SimpleBaseLocalThreadDataController):
    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'state')

    def initialize(
            self,
            *,
            acquired: bool = False,
            waited: bool = False,
            failure_details: SimpleThreadFailure | Unset = unset
    ):
        self._raise_already_initialized()
        self._local_env.state = SimpleLocalThreadState(
            acquired=acquired, waited=waited, failure_details=failure_details
        )

    def initialize_from_state(self, state: SimpleLocalThreadState):
        return self.initialize(acquired=state.acquired, waited=state.waited, failure_details=state.failure_details)

    def get(self) -> SimpleLocalThreadState:
        return self._local_env.state

    def update(
            self,
            *,
            acquired: bool | Unset = unset,
            waited: bool | Unset = unset,
            failure_details: SimpleThreadFailure | Unset | None = None
    ):
        _acquired = acquired if not isinstance(acquired, Unset) else self._local_env.state.acquired
        _waited = waited if not isinstance(waited, Unset) else self._local_env.state.waited
        _failure_details = failure_details if failure_details is not None else self._local_env.state.failure_details

        state = SimpleLocalThreadState(acquired=_acquired, waited=_waited, failure_details=_failure_details)
        self.update_from_state(state)

    def update_from_state(self, state: SimpleLocalThreadState):
        self._local_env.state = state
