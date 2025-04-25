import typing, clr, abc
from System import Attribute, Exception, Array, Array_1, MulticastDelegate, IAsyncResult, AsyncCallback, Action, Decimal, IFormatProvider, Span_1, ReadOnlySpan_1, FormattableString, RuntimeTypeHandle, RuntimeFieldHandle, Delegate, ModuleHandle, Range, RuntimeMethodHandle, InvalidOperationException
from System.Threading.Tasks import Task, Task_1, ValueTask, ValueTask_1
from System.Linq.Expressions import LabelTarget, Expression, ParameterExpression, LambdaExpression, DebugInfoExpression
from System.Collections.ObjectModel import ReadOnlyCollection_1
from System.Reflection import MethodBase, MethodInfo
from System.Collections.Generic import IEnumerable_1, KeyValuePair_2, IList_1, IEnumerator_1
from System.Threading import CancellationToken
from System.Diagnostics.Contracts import ContractFailureKind
from System.Collections import IList, IDictionary
from System.Dynamic import ExpandoObject
from System.Runtime.Serialization import SerializationInfo, StreamingContext

class AccessedThroughPropertyAttribute(Attribute):
    def __init__(self, propertyName: str) -> None: ...
    @property
    def PropertyName(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...


class AsyncIteratorMethodBuilder:
    def Complete(self) -> None: ...
    @staticmethod
    def Create() -> AsyncIteratorMethodBuilder: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup
    class AwaitOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_TAwaiter = AsyncIteratorMethodBuilder.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = AsyncIteratorMethodBuilder.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup
    class AwaitUnsafeOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_TAwaiter = AsyncIteratorMethodBuilder.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = AsyncIteratorMethodBuilder.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped MoveNext due to it being static, abstract and generic.

    MoveNext : MoveNext_MethodGroup
    class MoveNext_MethodGroup:
        def __getitem__(self, t:typing.Type[MoveNext_1_T1]) -> MoveNext_1[MoveNext_1_T1]: ...

        MoveNext_1_T1 = typing.TypeVar('MoveNext_1_T1')
        class MoveNext_1(typing.Generic[MoveNext_1_T1]):
            MoveNext_1_TStateMachine = AsyncIteratorMethodBuilder.MoveNext_MethodGroup.MoveNext_1_T1
            def __call__(self, stateMachine: clr.Reference[MoveNext_1_TStateMachine]) -> None:...




class AsyncIteratorStateMachineAttribute(StateMachineAttribute):
    def __init__(self, stateMachineType: typing.Type[typing.Any]) -> None: ...
    @property
    def StateMachineType(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class AsyncMethodBuilderAttribute(Attribute):
    def __init__(self, builderType: typing.Type[typing.Any]) -> None: ...
    @property
    def BuilderType(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class AsyncStateMachineAttribute(StateMachineAttribute):
    def __init__(self, stateMachineType: typing.Type[typing.Any]) -> None: ...
    @property
    def StateMachineType(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class AsyncTaskMethodBuilder_GenericClasses(abc.ABCMeta):
    Generic_AsyncTaskMethodBuilder_GenericClasses_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('Generic_AsyncTaskMethodBuilder_GenericClasses_AsyncTaskMethodBuilder_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_AsyncTaskMethodBuilder_GenericClasses_AsyncTaskMethodBuilder_1_TResult]) -> typing.Type[AsyncTaskMethodBuilder_1[Generic_AsyncTaskMethodBuilder_GenericClasses_AsyncTaskMethodBuilder_1_TResult]]: ...

class AsyncTaskMethodBuilder(AsyncTaskMethodBuilder_0, metaclass =AsyncTaskMethodBuilder_GenericClasses): ...

class AsyncTaskMethodBuilder_0:
    @property
    def Task(self) -> Task: ...
    @staticmethod
    def Create() -> AsyncTaskMethodBuilder: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup
    class AwaitOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_TAwaiter = AsyncTaskMethodBuilder_0.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = AsyncTaskMethodBuilder_0.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup
    class AwaitUnsafeOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_TAwaiter = AsyncTaskMethodBuilder_0.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = AsyncTaskMethodBuilder_0.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup
    class Start_MethodGroup:
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_1_T1]: ...

        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_T1]):
            Start_1_TStateMachine = AsyncTaskMethodBuilder_0.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('AsyncTaskMethodBuilder_1_TResult')
class AsyncTaskMethodBuilder_1(typing.Generic[AsyncTaskMethodBuilder_1_TResult]):
    @property
    def Task(self) -> Task_1[AsyncTaskMethodBuilder_1_TResult]: ...
    @staticmethod
    def Create() -> AsyncTaskMethodBuilder_1[AsyncTaskMethodBuilder_1_TResult]: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self, result: AsyncTaskMethodBuilder_1_TResult) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup[AsyncTaskMethodBuilder_1_TResult]
    AwaitOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult')
    class AwaitOnCompleted_MethodGroup(typing.Generic[AwaitOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult]):
        AwaitOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult = AsyncTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult, AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitOnCompleted_2_AsyncTaskMethodBuilder_1_TResult')
        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_AsyncTaskMethodBuilder_1_TResult, AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_AsyncTaskMethodBuilder_1_TResult = AsyncTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_AsyncTaskMethodBuilder_1_TResult
            AwaitOnCompleted_2_TAwaiter = AsyncTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = AsyncTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup[AsyncTaskMethodBuilder_1_TResult]
    AwaitUnsafeOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitUnsafeOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult')
    class AwaitUnsafeOnCompleted_MethodGroup(typing.Generic[AwaitUnsafeOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult]):
        AwaitUnsafeOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult = AsyncTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_MethodGroup_AsyncTaskMethodBuilder_1_TResult, AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitUnsafeOnCompleted_2_AsyncTaskMethodBuilder_1_TResult')
        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_AsyncTaskMethodBuilder_1_TResult, AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_AsyncTaskMethodBuilder_1_TResult = AsyncTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_AsyncTaskMethodBuilder_1_TResult
            AwaitUnsafeOnCompleted_2_TAwaiter = AsyncTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = AsyncTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup[AsyncTaskMethodBuilder_1_TResult]
    Start_MethodGroup_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('Start_MethodGroup_AsyncTaskMethodBuilder_1_TResult')
    class Start_MethodGroup(typing.Generic[Start_MethodGroup_AsyncTaskMethodBuilder_1_TResult]):
        Start_MethodGroup_AsyncTaskMethodBuilder_1_TResult = AsyncTaskMethodBuilder_1.Start_MethodGroup_AsyncTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_MethodGroup_AsyncTaskMethodBuilder_1_TResult, Start_1_T1]: ...

        Start_1_AsyncTaskMethodBuilder_1_TResult = typing.TypeVar('Start_1_AsyncTaskMethodBuilder_1_TResult')
        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_AsyncTaskMethodBuilder_1_TResult, Start_1_T1]):
            Start_1_AsyncTaskMethodBuilder_1_TResult = AsyncTaskMethodBuilder_1.Start_MethodGroup.Start_1_AsyncTaskMethodBuilder_1_TResult
            Start_1_TStateMachine = AsyncTaskMethodBuilder_1.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




class AsyncValueTaskMethodBuilder_GenericClasses(abc.ABCMeta):
    Generic_AsyncValueTaskMethodBuilder_GenericClasses_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('Generic_AsyncValueTaskMethodBuilder_GenericClasses_AsyncValueTaskMethodBuilder_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_AsyncValueTaskMethodBuilder_GenericClasses_AsyncValueTaskMethodBuilder_1_TResult]) -> typing.Type[AsyncValueTaskMethodBuilder_1[Generic_AsyncValueTaskMethodBuilder_GenericClasses_AsyncValueTaskMethodBuilder_1_TResult]]: ...

class AsyncValueTaskMethodBuilder(AsyncValueTaskMethodBuilder_0, metaclass =AsyncValueTaskMethodBuilder_GenericClasses): ...

class AsyncValueTaskMethodBuilder_0:
    @property
    def Task(self) -> ValueTask: ...
    @staticmethod
    def Create() -> AsyncValueTaskMethodBuilder: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup
    class AwaitOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_TAwaiter = AsyncValueTaskMethodBuilder_0.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = AsyncValueTaskMethodBuilder_0.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup
    class AwaitUnsafeOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_TAwaiter = AsyncValueTaskMethodBuilder_0.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = AsyncValueTaskMethodBuilder_0.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup
    class Start_MethodGroup:
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_1_T1]: ...

        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_T1]):
            Start_1_TStateMachine = AsyncValueTaskMethodBuilder_0.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AsyncValueTaskMethodBuilder_1_TResult')
class AsyncValueTaskMethodBuilder_1(typing.Generic[AsyncValueTaskMethodBuilder_1_TResult]):
    @property
    def Task(self) -> ValueTask_1[AsyncValueTaskMethodBuilder_1_TResult]: ...
    @staticmethod
    def Create() -> AsyncValueTaskMethodBuilder_1[AsyncValueTaskMethodBuilder_1_TResult]: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self, result: AsyncValueTaskMethodBuilder_1_TResult) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup[AsyncValueTaskMethodBuilder_1_TResult]
    AwaitOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult')
    class AwaitOnCompleted_MethodGroup(typing.Generic[AwaitOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult]):
        AwaitOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult = AsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult, AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult')
        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult, AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult = AsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult
            AwaitOnCompleted_2_TAwaiter = AsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = AsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup[AsyncValueTaskMethodBuilder_1_TResult]
    AwaitUnsafeOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitUnsafeOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult')
    class AwaitUnsafeOnCompleted_MethodGroup(typing.Generic[AwaitUnsafeOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult]):
        AwaitUnsafeOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult = AsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult, AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitUnsafeOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult')
        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult, AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult = AsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_AsyncValueTaskMethodBuilder_1_TResult
            AwaitUnsafeOnCompleted_2_TAwaiter = AsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = AsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup[AsyncValueTaskMethodBuilder_1_TResult]
    Start_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('Start_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult')
    class Start_MethodGroup(typing.Generic[Start_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult]):
        Start_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult = AsyncValueTaskMethodBuilder_1.Start_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_MethodGroup_AsyncValueTaskMethodBuilder_1_TResult, Start_1_T1]: ...

        Start_1_AsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('Start_1_AsyncValueTaskMethodBuilder_1_TResult')
        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_AsyncValueTaskMethodBuilder_1_TResult, Start_1_T1]):
            Start_1_AsyncValueTaskMethodBuilder_1_TResult = AsyncValueTaskMethodBuilder_1.Start_MethodGroup.Start_1_AsyncValueTaskMethodBuilder_1_TResult
            Start_1_TStateMachine = AsyncValueTaskMethodBuilder_1.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




class AsyncVoidMethodBuilder:
    @staticmethod
    def Create() -> AsyncVoidMethodBuilder: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup
    class AwaitOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_TAwaiter = AsyncVoidMethodBuilder.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = AsyncVoidMethodBuilder.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup
    class AwaitUnsafeOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_TAwaiter = AsyncVoidMethodBuilder.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = AsyncVoidMethodBuilder.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup
    class Start_MethodGroup:
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_1_T1]: ...

        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_T1]):
            Start_1_TStateMachine = AsyncVoidMethodBuilder.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




class CallConvCdecl:
    def __init__(self) -> None: ...


class CallConvFastcall:
    def __init__(self) -> None: ...


class CallConvMemberFunction:
    def __init__(self) -> None: ...


class CallConvStdcall:
    def __init__(self) -> None: ...


class CallConvSuppressGCTransition:
    def __init__(self) -> None: ...


class CallConvThiscall:
    def __init__(self) -> None: ...


class CallerArgumentExpressionAttribute(Attribute):
    def __init__(self, parameterName: str) -> None: ...
    @property
    def ParameterName(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CallerFilePathAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CallerLineNumberAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CallerMemberNameAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CallSite_GenericClasses(abc.ABCMeta):
    Generic_CallSite_GenericClasses_CallSite_1_T = typing.TypeVar('Generic_CallSite_GenericClasses_CallSite_1_T')
    def __getitem__(self, types : typing.Type[Generic_CallSite_GenericClasses_CallSite_1_T]) -> typing.Type[CallSite_1[Generic_CallSite_GenericClasses_CallSite_1_T]]: ...

class CallSite(CallSite_0, metaclass =CallSite_GenericClasses): ...

class CallSite_0:
    @property
    def Binder(self) -> CallSiteBinder: ...
    @staticmethod
    def Create(delegateType: typing.Type[typing.Any], binder: CallSiteBinder) -> CallSite: ...


CallSite_1_T = typing.TypeVar('CallSite_1_T')
class CallSite_1(typing.Generic[CallSite_1_T], CallSite_0):
    Target : CallSite_1_T
    @property
    def Binder(self) -> CallSiteBinder: ...
    @property
    def Update(self) -> CallSite_1_T: ...
    @staticmethod
    def Create(binder: CallSiteBinder) -> CallSite_1[CallSite_1_T]: ...


class CallSiteBinder(abc.ABC):
    @classmethod
    @property
    def UpdateLabel(cls) -> LabelTarget: ...
    @abc.abstractmethod
    def Bind(self, args: Array_1[typing.Any], parameters: ReadOnlyCollection_1[ParameterExpression], returnLabel: LabelTarget) -> Expression: ...
    # Skipped BindDelegate due to it being static, abstract and generic.

    BindDelegate : BindDelegate_MethodGroup
    class BindDelegate_MethodGroup:
        def __getitem__(self, t:typing.Type[BindDelegate_1_T1]) -> BindDelegate_1[BindDelegate_1_T1]: ...

        BindDelegate_1_T1 = typing.TypeVar('BindDelegate_1_T1')
        class BindDelegate_1(typing.Generic[BindDelegate_1_T1]):
            BindDelegate_1_T = CallSiteBinder.BindDelegate_MethodGroup.BindDelegate_1_T1
            def __call__(self, site: CallSite_1[BindDelegate_1_T], args: Array_1[typing.Any]) -> BindDelegate_1_T:...




class CallSiteHelpers(abc.ABC):
    @staticmethod
    def IsInternalFrame(mb: MethodBase) -> bool: ...


class CallSiteOps(abc.ABC):
    @staticmethod
    def ClearMatch(site: CallSite) -> None: ...
    @staticmethod
    def GetMatch(site: CallSite) -> bool: ...
    @staticmethod
    def SetNotMatched(site: CallSite) -> bool: ...
    # Skipped AddRule due to it being static, abstract and generic.

    AddRule : AddRule_MethodGroup
    class AddRule_MethodGroup:
        def __getitem__(self, t:typing.Type[AddRule_1_T1]) -> AddRule_1[AddRule_1_T1]: ...

        AddRule_1_T1 = typing.TypeVar('AddRule_1_T1')
        class AddRule_1(typing.Generic[AddRule_1_T1]):
            AddRule_1_T = CallSiteOps.AddRule_MethodGroup.AddRule_1_T1
            def __call__(self, site: CallSite_1[AddRule_1_T], rule: AddRule_1_T) -> None:...


    # Skipped Bind due to it being static, abstract and generic.

    Bind : Bind_MethodGroup
    class Bind_MethodGroup:
        def __getitem__(self, t:typing.Type[Bind_1_T1]) -> Bind_1[Bind_1_T1]: ...

        Bind_1_T1 = typing.TypeVar('Bind_1_T1')
        class Bind_1(typing.Generic[Bind_1_T1]):
            Bind_1_T = CallSiteOps.Bind_MethodGroup.Bind_1_T1
            def __call__(self, binder: CallSiteBinder, site: CallSite_1[Bind_1_T], args: Array_1[typing.Any]) -> Bind_1_T:...


    # Skipped CreateMatchmaker due to it being static, abstract and generic.

    CreateMatchmaker : CreateMatchmaker_MethodGroup
    class CreateMatchmaker_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateMatchmaker_1_T1]) -> CreateMatchmaker_1[CreateMatchmaker_1_T1]: ...

        CreateMatchmaker_1_T1 = typing.TypeVar('CreateMatchmaker_1_T1')
        class CreateMatchmaker_1(typing.Generic[CreateMatchmaker_1_T1]):
            CreateMatchmaker_1_T = CallSiteOps.CreateMatchmaker_MethodGroup.CreateMatchmaker_1_T1
            def __call__(self, site: CallSite_1[CreateMatchmaker_1_T]) -> CallSite_1[CreateMatchmaker_1_T]:...


    # Skipped GetCachedRules due to it being static, abstract and generic.

    GetCachedRules : GetCachedRules_MethodGroup
    class GetCachedRules_MethodGroup:
        def __getitem__(self, t:typing.Type[GetCachedRules_1_T1]) -> GetCachedRules_1[GetCachedRules_1_T1]: ...

        GetCachedRules_1_T1 = typing.TypeVar('GetCachedRules_1_T1')
        class GetCachedRules_1(typing.Generic[GetCachedRules_1_T1]):
            GetCachedRules_1_T = CallSiteOps.GetCachedRules_MethodGroup.GetCachedRules_1_T1
            def __call__(self, cache: RuleCache_1[GetCachedRules_1_T]) -> Array_1[GetCachedRules_1_T]:...


    # Skipped GetRuleCache due to it being static, abstract and generic.

    GetRuleCache : GetRuleCache_MethodGroup
    class GetRuleCache_MethodGroup:
        def __getitem__(self, t:typing.Type[GetRuleCache_1_T1]) -> GetRuleCache_1[GetRuleCache_1_T1]: ...

        GetRuleCache_1_T1 = typing.TypeVar('GetRuleCache_1_T1')
        class GetRuleCache_1(typing.Generic[GetRuleCache_1_T1]):
            GetRuleCache_1_T = CallSiteOps.GetRuleCache_MethodGroup.GetRuleCache_1_T1
            def __call__(self, site: CallSite_1[GetRuleCache_1_T]) -> RuleCache_1[GetRuleCache_1_T]:...


    # Skipped GetRules due to it being static, abstract and generic.

    GetRules : GetRules_MethodGroup
    class GetRules_MethodGroup:
        def __getitem__(self, t:typing.Type[GetRules_1_T1]) -> GetRules_1[GetRules_1_T1]: ...

        GetRules_1_T1 = typing.TypeVar('GetRules_1_T1')
        class GetRules_1(typing.Generic[GetRules_1_T1]):
            GetRules_1_T = CallSiteOps.GetRules_MethodGroup.GetRules_1_T1
            def __call__(self, site: CallSite_1[GetRules_1_T]) -> Array_1[GetRules_1_T]:...


    # Skipped MoveRule due to it being static, abstract and generic.

    MoveRule : MoveRule_MethodGroup
    class MoveRule_MethodGroup:
        def __getitem__(self, t:typing.Type[MoveRule_1_T1]) -> MoveRule_1[MoveRule_1_T1]: ...

        MoveRule_1_T1 = typing.TypeVar('MoveRule_1_T1')
        class MoveRule_1(typing.Generic[MoveRule_1_T1]):
            MoveRule_1_T = CallSiteOps.MoveRule_MethodGroup.MoveRule_1_T1
            def __call__(self, cache: RuleCache_1[MoveRule_1_T], rule: MoveRule_1_T, i: int) -> None:...


    # Skipped UpdateRules due to it being static, abstract and generic.

    UpdateRules : UpdateRules_MethodGroup
    class UpdateRules_MethodGroup:
        def __getitem__(self, t:typing.Type[UpdateRules_1_T1]) -> UpdateRules_1[UpdateRules_1_T1]: ...

        UpdateRules_1_T1 = typing.TypeVar('UpdateRules_1_T1')
        class UpdateRules_1(typing.Generic[UpdateRules_1_T1]):
            UpdateRules_1_T = CallSiteOps.UpdateRules_MethodGroup.UpdateRules_1_T1
            def __call__(self, this: CallSite_1[UpdateRules_1_T], matched: int) -> None:...




class Closure:
    def __init__(self, constants: Array_1[typing.Any], locals: Array_1[typing.Any]) -> None: ...
    Constants : Array_1[typing.Any]
    Locals : Array_1[typing.Any]


class CompilationRelaxations(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoStringInterning : CompilationRelaxations # 8


class CompilationRelaxationsAttribute(Attribute):
    @typing.overload
    def __init__(self, relaxations: int) -> None: ...
    @typing.overload
    def __init__(self, relaxations: CompilationRelaxations) -> None: ...
    @property
    def CompilationRelaxations(self) -> int: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CompilerGeneratedAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CompilerGlobalScopeAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CompilerMarshalOverride(abc.ABC):
    pass


class ConditionalWeakTable_GenericClasses(abc.ABCMeta):
    Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TKey = typing.TypeVar('Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TKey')
    Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TValue = typing.TypeVar('Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TValue')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TKey], typing.Type[Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TValue]]) -> typing.Type[ConditionalWeakTable_2[Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TKey, Generic_ConditionalWeakTable_GenericClasses_ConditionalWeakTable_2_TValue]]: ...

ConditionalWeakTable : ConditionalWeakTable_GenericClasses

ConditionalWeakTable_2_TKey = typing.TypeVar('ConditionalWeakTable_2_TKey')
ConditionalWeakTable_2_TValue = typing.TypeVar('ConditionalWeakTable_2_TValue')
class ConditionalWeakTable_2(typing.Generic[ConditionalWeakTable_2_TKey, ConditionalWeakTable_2_TValue], IEnumerable_1[KeyValuePair_2[ConditionalWeakTable_2_TKey, ConditionalWeakTable_2_TValue]]):
    def __init__(self) -> None: ...
    def Add(self, key: ConditionalWeakTable_2_TKey, value: ConditionalWeakTable_2_TValue) -> None: ...
    def AddOrUpdate(self, key: ConditionalWeakTable_2_TKey, value: ConditionalWeakTable_2_TValue) -> None: ...
    def Clear(self) -> None: ...
    def GetOrCreateValue(self, key: ConditionalWeakTable_2_TKey) -> ConditionalWeakTable_2_TValue: ...
    def GetValue(self, key: ConditionalWeakTable_2_TKey, createValueCallback: ConditionalWeakTable_2.CreateValueCallback_2[ConditionalWeakTable_2_TKey, ConditionalWeakTable_2_TValue]) -> ConditionalWeakTable_2_TValue: ...
    def Remove(self, key: ConditionalWeakTable_2_TKey) -> bool: ...
    def TryGetValue(self, key: ConditionalWeakTable_2_TKey, value: clr.Reference[ConditionalWeakTable_2_TValue]) -> bool: ...

    CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TKey = typing.TypeVar('CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TKey')
    CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TValue = typing.TypeVar('CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TValue')
    class CreateValueCallback_GenericClasses(typing.Generic[CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TKey, CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TValue], abc.ABCMeta):
        CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TKey = ConditionalWeakTable_2.CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TKey
        CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TValue = ConditionalWeakTable_2.CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TValue
        def __call__(self) -> ConditionalWeakTable_2.CreateValueCallback_2[CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TKey, CreateValueCallback_GenericClasses_ConditionalWeakTable_2_TValue]: ...

    CreateValueCallback : CreateValueCallback_GenericClasses[ConditionalWeakTable_2_TKey, ConditionalWeakTable_2_TValue]

    CreateValueCallback_2_TKey = typing.TypeVar('CreateValueCallback_2_TKey')
    CreateValueCallback_2_TValue = typing.TypeVar('CreateValueCallback_2_TValue')
    class CreateValueCallback_2(typing.Generic[CreateValueCallback_2_TKey, CreateValueCallback_2_TValue], MulticastDelegate):
        CreateValueCallback_2_TKey = ConditionalWeakTable_2.CreateValueCallback_2_TKey
        CreateValueCallback_2_TValue = ConditionalWeakTable_2.CreateValueCallback_2_TValue
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, key: CreateValueCallback_2_TKey, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> CreateValueCallback_2_TValue: ...
        def Invoke(self, key: CreateValueCallback_2_TKey) -> CreateValueCallback_2_TValue: ...



class ConfiguredAsyncDisposable:
    def DisposeAsync(self) -> ConfiguredValueTaskAwaitable: ...


class ConfiguredCancelableAsyncEnumerable_GenericClasses(abc.ABCMeta):
    Generic_ConfiguredCancelableAsyncEnumerable_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T = typing.TypeVar('Generic_ConfiguredCancelableAsyncEnumerable_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T')
    def __getitem__(self, types : typing.Type[Generic_ConfiguredCancelableAsyncEnumerable_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T]) -> typing.Type[ConfiguredCancelableAsyncEnumerable_1[Generic_ConfiguredCancelableAsyncEnumerable_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T]]: ...

ConfiguredCancelableAsyncEnumerable : ConfiguredCancelableAsyncEnumerable_GenericClasses

ConfiguredCancelableAsyncEnumerable_1_T = typing.TypeVar('ConfiguredCancelableAsyncEnumerable_1_T')
class ConfiguredCancelableAsyncEnumerable_1(typing.Generic[ConfiguredCancelableAsyncEnumerable_1_T]):
    def ConfigureAwait(self, continueOnCapturedContext: bool) -> ConfiguredCancelableAsyncEnumerable_1[ConfiguredCancelableAsyncEnumerable_1_T]: ...
    def GetAsyncEnumerator(self) -> ConfiguredCancelableAsyncEnumerable_1.Enumerator_1[ConfiguredCancelableAsyncEnumerable_1_T]: ...
    def WithCancellation(self, cancellationToken: CancellationToken) -> ConfiguredCancelableAsyncEnumerable_1[ConfiguredCancelableAsyncEnumerable_1_T]: ...

    Enumerator_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T = typing.TypeVar('Enumerator_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T')
    class Enumerator_GenericClasses(typing.Generic[Enumerator_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T], abc.ABCMeta):
        Enumerator_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T = ConfiguredCancelableAsyncEnumerable_1.Enumerator_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T
        def __call__(self) -> ConfiguredCancelableAsyncEnumerable_1.Enumerator_1[Enumerator_GenericClasses_ConfiguredCancelableAsyncEnumerable_1_T]: ...

    Enumerator : Enumerator_GenericClasses[ConfiguredCancelableAsyncEnumerable_1_T]

    Enumerator_1_T = typing.TypeVar('Enumerator_1_T')
    class Enumerator_1(typing.Generic[Enumerator_1_T]):
        Enumerator_1_T = ConfiguredCancelableAsyncEnumerable_1.Enumerator_1_T
        @property
        def Current(self) -> Enumerator_1_T: ...
        def DisposeAsync(self) -> ConfiguredValueTaskAwaitable: ...
        def MoveNextAsync(self) -> ConfiguredValueTaskAwaitable_1[bool]: ...



class ConfiguredTaskAwaitable_GenericClasses(abc.ABCMeta):
    Generic_ConfiguredTaskAwaitable_GenericClasses_ConfiguredTaskAwaitable_1_TResult = typing.TypeVar('Generic_ConfiguredTaskAwaitable_GenericClasses_ConfiguredTaskAwaitable_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_ConfiguredTaskAwaitable_GenericClasses_ConfiguredTaskAwaitable_1_TResult]) -> typing.Type[ConfiguredTaskAwaitable_1[Generic_ConfiguredTaskAwaitable_GenericClasses_ConfiguredTaskAwaitable_1_TResult]]: ...

class ConfiguredTaskAwaitable(ConfiguredTaskAwaitable_0, metaclass =ConfiguredTaskAwaitable_GenericClasses): ...

class ConfiguredTaskAwaitable_0:
    def GetAwaiter(self) -> ConfiguredTaskAwaitable.ConfiguredTaskAwaiter: ...

    class ConfiguredTaskAwaiter(ICriticalNotifyCompletion):
        @property
        def IsCompleted(self) -> bool: ...
        def GetResult(self) -> None: ...
        def OnCompleted(self, continuation: Action) -> None: ...
        def UnsafeOnCompleted(self, continuation: Action) -> None: ...



ConfiguredTaskAwaitable_1_TResult = typing.TypeVar('ConfiguredTaskAwaitable_1_TResult')
class ConfiguredTaskAwaitable_1(typing.Generic[ConfiguredTaskAwaitable_1_TResult]):
    def GetAwaiter(self) -> ConfiguredTaskAwaitable_1.ConfiguredTaskAwaiter_1[ConfiguredTaskAwaitable_1_TResult]: ...

    ConfiguredTaskAwaiter_GenericClasses_ConfiguredTaskAwaitable_1_TResult = typing.TypeVar('ConfiguredTaskAwaiter_GenericClasses_ConfiguredTaskAwaitable_1_TResult')
    class ConfiguredTaskAwaiter_GenericClasses(typing.Generic[ConfiguredTaskAwaiter_GenericClasses_ConfiguredTaskAwaitable_1_TResult], abc.ABCMeta):
        ConfiguredTaskAwaiter_GenericClasses_ConfiguredTaskAwaitable_1_TResult = ConfiguredTaskAwaitable_1.ConfiguredTaskAwaiter_GenericClasses_ConfiguredTaskAwaitable_1_TResult
        def __call__(self) -> ConfiguredTaskAwaitable_1.ConfiguredTaskAwaiter_1[ConfiguredTaskAwaiter_GenericClasses_ConfiguredTaskAwaitable_1_TResult]: ...

    ConfiguredTaskAwaiter : ConfiguredTaskAwaiter_GenericClasses[ConfiguredTaskAwaitable_1_TResult]

    ConfiguredTaskAwaiter_1_TResult = typing.TypeVar('ConfiguredTaskAwaiter_1_TResult')
    class ConfiguredTaskAwaiter_1(typing.Generic[ConfiguredTaskAwaiter_1_TResult], ICriticalNotifyCompletion):
        ConfiguredTaskAwaiter_1_TResult = ConfiguredTaskAwaitable_1.ConfiguredTaskAwaiter_1_TResult
        @property
        def IsCompleted(self) -> bool: ...
        def GetResult(self) -> ConfiguredTaskAwaiter_1_TResult: ...
        def OnCompleted(self, continuation: Action) -> None: ...
        def UnsafeOnCompleted(self, continuation: Action) -> None: ...



class ConfiguredValueTaskAwaitable_GenericClasses(abc.ABCMeta):
    Generic_ConfiguredValueTaskAwaitable_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult = typing.TypeVar('Generic_ConfiguredValueTaskAwaitable_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_ConfiguredValueTaskAwaitable_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult]) -> typing.Type[ConfiguredValueTaskAwaitable_1[Generic_ConfiguredValueTaskAwaitable_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult]]: ...

class ConfiguredValueTaskAwaitable(ConfiguredValueTaskAwaitable_0, metaclass =ConfiguredValueTaskAwaitable_GenericClasses): ...

class ConfiguredValueTaskAwaitable_0:
    def GetAwaiter(self) -> ConfiguredValueTaskAwaitable.ConfiguredValueTaskAwaiter: ...

    class ConfiguredValueTaskAwaiter(ICriticalNotifyCompletion):
        @property
        def IsCompleted(self) -> bool: ...
        def GetResult(self) -> None: ...
        def OnCompleted(self, continuation: Action) -> None: ...
        def UnsafeOnCompleted(self, continuation: Action) -> None: ...



ConfiguredValueTaskAwaitable_1_TResult = typing.TypeVar('ConfiguredValueTaskAwaitable_1_TResult')
class ConfiguredValueTaskAwaitable_1(typing.Generic[ConfiguredValueTaskAwaitable_1_TResult]):
    def GetAwaiter(self) -> ConfiguredValueTaskAwaitable_1.ConfiguredValueTaskAwaiter_1[ConfiguredValueTaskAwaitable_1_TResult]: ...

    ConfiguredValueTaskAwaiter_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult = typing.TypeVar('ConfiguredValueTaskAwaiter_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult')
    class ConfiguredValueTaskAwaiter_GenericClasses(typing.Generic[ConfiguredValueTaskAwaiter_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult], abc.ABCMeta):
        ConfiguredValueTaskAwaiter_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult = ConfiguredValueTaskAwaitable_1.ConfiguredValueTaskAwaiter_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult
        def __call__(self) -> ConfiguredValueTaskAwaitable_1.ConfiguredValueTaskAwaiter_1[ConfiguredValueTaskAwaiter_GenericClasses_ConfiguredValueTaskAwaitable_1_TResult]: ...

    ConfiguredValueTaskAwaiter : ConfiguredValueTaskAwaiter_GenericClasses[ConfiguredValueTaskAwaitable_1_TResult]

    ConfiguredValueTaskAwaiter_1_TResult = typing.TypeVar('ConfiguredValueTaskAwaiter_1_TResult')
    class ConfiguredValueTaskAwaiter_1(typing.Generic[ConfiguredValueTaskAwaiter_1_TResult], ICriticalNotifyCompletion):
        ConfiguredValueTaskAwaiter_1_TResult = ConfiguredValueTaskAwaitable_1.ConfiguredValueTaskAwaiter_1_TResult
        @property
        def IsCompleted(self) -> bool: ...
        def GetResult(self) -> ConfiguredValueTaskAwaiter_1_TResult: ...
        def OnCompleted(self, continuation: Action) -> None: ...
        def UnsafeOnCompleted(self, continuation: Action) -> None: ...



class ContractHelper(abc.ABC):
    @staticmethod
    def RaiseContractFailedEvent(failureKind: ContractFailureKind, userMessage: str, conditionText: str, innerException: Exception) -> str: ...
    @staticmethod
    def TriggerFailure(kind: ContractFailureKind, displayMessage: str, userMessage: str, conditionText: str, innerException: Exception) -> None: ...


class CppInlineNamespaceAttribute(Attribute):
    def __init__(self, dottedName: str) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CreateNewOnMetadataUpdateAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class CustomConstantAttribute(Attribute):
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> typing.Any: ...


class DateTimeConstantAttribute(CustomConstantAttribute):
    def __init__(self, ticks: int) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> typing.Any: ...


class DebugInfoGenerator(abc.ABC):
    @staticmethod
    def CreatePdbGenerator() -> DebugInfoGenerator: ...
    @abc.abstractmethod
    def MarkSequencePoint(self, method: LambdaExpression, ilOffset: int, sequencePoint: DebugInfoExpression) -> None: ...


class DecimalConstantAttribute(Attribute):
    # Constructor .ctor(scale : Byte, sign : Byte, hi : Int32, mid : Int32, low : Int32) was skipped since it collides with above method
    def __init__(self, scale: int, sign: int, hi: int, mid: int, low: int) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> Decimal: ...


class DefaultDependencyAttribute(Attribute):
    def __init__(self, loadHintArgument: LoadHint) -> None: ...
    @property
    def LoadHint(self) -> LoadHint: ...
    @property
    def TypeId(self) -> typing.Any: ...


class DefaultInterpolatedStringHandler:
    @typing.overload
    def __init__(self, literalLength: int, formattedCount: int) -> None: ...
    @typing.overload
    def __init__(self, literalLength: int, formattedCount: int, provider: IFormatProvider) -> None: ...
    @typing.overload
    def __init__(self, literalLength: int, formattedCount: int, provider: IFormatProvider, initialBuffer: Span_1[str]) -> None: ...
    def AppendLiteral(self, value: str) -> None: ...
    def ToString(self) -> str: ...
    def ToStringAndClear(self) -> str: ...
    # Skipped AppendFormatted due to it being static, abstract and generic.

    AppendFormatted : AppendFormatted_MethodGroup
    class AppendFormatted_MethodGroup:
        def __getitem__(self, t:typing.Type[AppendFormatted_1_T1]) -> AppendFormatted_1[AppendFormatted_1_T1]: ...

        AppendFormatted_1_T1 = typing.TypeVar('AppendFormatted_1_T1')
        class AppendFormatted_1(typing.Generic[AppendFormatted_1_T1]):
            AppendFormatted_1_T = DefaultInterpolatedStringHandler.AppendFormatted_MethodGroup.AppendFormatted_1_T1
            @typing.overload
            def __call__(self, value: AppendFormatted_1_T) -> None:...
            @typing.overload
            def __call__(self, value: AppendFormatted_1_T, alignment: int) -> None:...
            @typing.overload
            def __call__(self, value: AppendFormatted_1_T, format: str) -> None:...
            @typing.overload
            def __call__(self, value: AppendFormatted_1_T, alignment: int, format: str) -> None:...

        @typing.overload
        def __call__(self, value: ReadOnlySpan_1[str]) -> None:...
        @typing.overload
        def __call__(self, value: str) -> None:...
        @typing.overload
        def __call__(self, value: ReadOnlySpan_1[str], alignment: int = ..., format: str = ...) -> None:...
        @typing.overload
        def __call__(self, value: str, alignment: int = ..., format: str = ...) -> None:...
        @typing.overload
        def __call__(self, value: typing.Any, alignment: int = ..., format: str = ...) -> None:...



class DependencyAttribute(Attribute):
    def __init__(self, dependentAssemblyArgument: str, loadHintArgument: LoadHint) -> None: ...
    @property
    def DependentAssembly(self) -> str: ...
    @property
    def LoadHint(self) -> LoadHint: ...
    @property
    def TypeId(self) -> typing.Any: ...


class DisablePrivateReflectionAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class DiscardableAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class DynamicAttribute(Attribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, transformFlags: Array_1[bool]) -> None: ...
    @property
    def TransformFlags(self) -> IList_1[bool]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class EnumeratorCancellationAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ExtensionAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class FixedAddressValueTypeAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class FixedBufferAttribute(Attribute):
    def __init__(self, elementType: typing.Type[typing.Any], length: int) -> None: ...
    @property
    def ElementType(self) -> typing.Type[typing.Any]: ...
    @property
    def Length(self) -> int: ...
    @property
    def TypeId(self) -> typing.Any: ...


class FormattableStringFactory(abc.ABC):
    @staticmethod
    def Create(format: str, arguments: Array_1[typing.Any]) -> FormattableString: ...


class HasCopySemanticsAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class IAsyncStateMachine(typing.Protocol):
    @abc.abstractmethod
    def MoveNext(self) -> None: ...
    @abc.abstractmethod
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...


class ICastable(typing.Protocol):
    @abc.abstractmethod
    def GetImplType(self, interfaceType: RuntimeTypeHandle) -> RuntimeTypeHandle: ...
    @abc.abstractmethod
    def IsInstanceOfInterface(self, interfaceType: RuntimeTypeHandle, castError: clr.Reference[Exception]) -> bool: ...


class ICriticalNotifyCompletion(INotifyCompletion, typing.Protocol):
    @abc.abstractmethod
    def UnsafeOnCompleted(self, continuation: Action) -> None: ...


class IDispatchConstantAttribute(CustomConstantAttribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> typing.Any: ...


class IndexerNameAttribute(Attribute):
    def __init__(self, indexerName: str) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class INotifyCompletion(typing.Protocol):
    @abc.abstractmethod
    def OnCompleted(self, continuation: Action) -> None: ...


class InternalsVisibleToAttribute(Attribute):
    def __init__(self, assemblyName: str) -> None: ...
    @property
    def AllInternalsVisible(self) -> bool: ...
    @AllInternalsVisible.setter
    def AllInternalsVisible(self, value: bool) -> bool: ...
    @property
    def AssemblyName(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...


class InterpolatedStringHandlerArgumentAttribute(Attribute):
    @typing.overload
    def __init__(self, argument: str) -> None: ...
    @typing.overload
    def __init__(self, arguments: Array_1[str]) -> None: ...
    @property
    def Arguments(self) -> Array_1[str]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class InterpolatedStringHandlerAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class IRuntimeVariables(typing.Protocol):
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> typing.Any: ...
    @Item.setter
    def Item(self, value: typing.Any) -> typing.Any: ...


class IsBoxed(abc.ABC):
    pass


class IsByRefLikeAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class IsByValue(abc.ABC):
    pass


class IsConst(abc.ABC):
    pass


class IsCopyConstructed(abc.ABC):
    pass


class IsExplicitlyDereferenced(abc.ABC):
    pass


class IsExternalInit(abc.ABC):
    pass


class IsImplicitlyDereferenced(abc.ABC):
    pass


class IsJitIntrinsic(abc.ABC):
    pass


class IsLong(abc.ABC):
    pass


class IsPinned(abc.ABC):
    pass


class IsReadOnlyAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class IsSignUnspecifiedByte(abc.ABC):
    pass


class IStrongBox(typing.Protocol):
    @property
    def Value(self) -> typing.Any: ...
    @Value.setter
    def Value(self, value: typing.Any) -> typing.Any: ...


class IsUdtReturn(abc.ABC):
    pass


class IsVolatile(abc.ABC):
    pass


class IteratorStateMachineAttribute(StateMachineAttribute):
    def __init__(self, stateMachineType: typing.Type[typing.Any]) -> None: ...
    @property
    def StateMachineType(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ITuple(typing.Protocol):
    @property
    def Item(self) -> typing.Any: ...
    @property
    def Length(self) -> int: ...


class IUnknownConstantAttribute(CustomConstantAttribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> typing.Any: ...


class LoadHint(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : LoadHint # 0
    Always : LoadHint # 1
    Sometimes : LoadHint # 2


class MethodCodeType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    IL : MethodCodeType # 0
    Native : MethodCodeType # 1
    OPTIL : MethodCodeType # 2
    Runtime : MethodCodeType # 3


class MethodImplAttribute(Attribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, methodImplOptions: MethodImplOptions) -> None: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    MethodCodeType : MethodCodeType
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> MethodImplOptions: ...


class MethodImplOptions(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unmanaged : MethodImplOptions # 4
    NoInlining : MethodImplOptions # 8
    ForwardRef : MethodImplOptions # 16
    Synchronized : MethodImplOptions # 32
    NoOptimization : MethodImplOptions # 64
    PreserveSig : MethodImplOptions # 128
    AggressiveInlining : MethodImplOptions # 256
    AggressiveOptimization : MethodImplOptions # 512
    InternalCall : MethodImplOptions # 4096


class ModuleInitializerAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class NativeCppClassAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class PoolingAsyncValueTaskMethodBuilder_GenericClasses(abc.ABCMeta):
    Generic_PoolingAsyncValueTaskMethodBuilder_GenericClasses_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('Generic_PoolingAsyncValueTaskMethodBuilder_GenericClasses_PoolingAsyncValueTaskMethodBuilder_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_PoolingAsyncValueTaskMethodBuilder_GenericClasses_PoolingAsyncValueTaskMethodBuilder_1_TResult]) -> typing.Type[PoolingAsyncValueTaskMethodBuilder_1[Generic_PoolingAsyncValueTaskMethodBuilder_GenericClasses_PoolingAsyncValueTaskMethodBuilder_1_TResult]]: ...

class PoolingAsyncValueTaskMethodBuilder(PoolingAsyncValueTaskMethodBuilder_0, metaclass =PoolingAsyncValueTaskMethodBuilder_GenericClasses): ...

class PoolingAsyncValueTaskMethodBuilder_0:
    @property
    def Task(self) -> ValueTask: ...
    @staticmethod
    def Create() -> PoolingAsyncValueTaskMethodBuilder: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup
    class AwaitOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_TAwaiter = PoolingAsyncValueTaskMethodBuilder_0.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = PoolingAsyncValueTaskMethodBuilder_0.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup
    class AwaitUnsafeOnCompleted_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_TAwaiter = PoolingAsyncValueTaskMethodBuilder_0.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = PoolingAsyncValueTaskMethodBuilder_0.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup
    class Start_MethodGroup:
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_1_T1]: ...

        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_T1]):
            Start_1_TStateMachine = PoolingAsyncValueTaskMethodBuilder_0.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('PoolingAsyncValueTaskMethodBuilder_1_TResult')
class PoolingAsyncValueTaskMethodBuilder_1(typing.Generic[PoolingAsyncValueTaskMethodBuilder_1_TResult]):
    @property
    def Task(self) -> ValueTask_1[PoolingAsyncValueTaskMethodBuilder_1_TResult]: ...
    @staticmethod
    def Create() -> PoolingAsyncValueTaskMethodBuilder_1[PoolingAsyncValueTaskMethodBuilder_1_TResult]: ...
    def SetException(self, exception: Exception) -> None: ...
    def SetResult(self, result: PoolingAsyncValueTaskMethodBuilder_1_TResult) -> None: ...
    def SetStateMachine(self, stateMachine: IAsyncStateMachine) -> None: ...
    # Skipped AwaitOnCompleted due to it being static, abstract and generic.

    AwaitOnCompleted : AwaitOnCompleted_MethodGroup[PoolingAsyncValueTaskMethodBuilder_1_TResult]
    AwaitOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult')
    class AwaitOnCompleted_MethodGroup(typing.Generic[AwaitOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult]):
        AwaitOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult = PoolingAsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitOnCompleted_2_T1], typing.Type[AwaitOnCompleted_2_T2]]) -> AwaitOnCompleted_2[AwaitOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult, AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]: ...

        AwaitOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult')
        AwaitOnCompleted_2_T1 = typing.TypeVar('AwaitOnCompleted_2_T1')
        AwaitOnCompleted_2_T2 = typing.TypeVar('AwaitOnCompleted_2_T2')
        class AwaitOnCompleted_2(typing.Generic[AwaitOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult, AwaitOnCompleted_2_T1, AwaitOnCompleted_2_T2]):
            AwaitOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult = PoolingAsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult
            AwaitOnCompleted_2_TAwaiter = PoolingAsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T1
            AwaitOnCompleted_2_TStateMachine = PoolingAsyncValueTaskMethodBuilder_1.AwaitOnCompleted_MethodGroup.AwaitOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitOnCompleted_2_TStateMachine]) -> None:...


    # Skipped AwaitUnsafeOnCompleted due to it being static, abstract and generic.

    AwaitUnsafeOnCompleted : AwaitUnsafeOnCompleted_MethodGroup[PoolingAsyncValueTaskMethodBuilder_1_TResult]
    AwaitUnsafeOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitUnsafeOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult')
    class AwaitUnsafeOnCompleted_MethodGroup(typing.Generic[AwaitUnsafeOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult]):
        AwaitUnsafeOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult = PoolingAsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Tuple[typing.Type[AwaitUnsafeOnCompleted_2_T1], typing.Type[AwaitUnsafeOnCompleted_2_T2]]) -> AwaitUnsafeOnCompleted_2[AwaitUnsafeOnCompleted_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult, AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]: ...

        AwaitUnsafeOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('AwaitUnsafeOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult')
        AwaitUnsafeOnCompleted_2_T1 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T1')
        AwaitUnsafeOnCompleted_2_T2 = typing.TypeVar('AwaitUnsafeOnCompleted_2_T2')
        class AwaitUnsafeOnCompleted_2(typing.Generic[AwaitUnsafeOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult, AwaitUnsafeOnCompleted_2_T1, AwaitUnsafeOnCompleted_2_T2]):
            AwaitUnsafeOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult = PoolingAsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_PoolingAsyncValueTaskMethodBuilder_1_TResult
            AwaitUnsafeOnCompleted_2_TAwaiter = PoolingAsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T1
            AwaitUnsafeOnCompleted_2_TStateMachine = PoolingAsyncValueTaskMethodBuilder_1.AwaitUnsafeOnCompleted_MethodGroup.AwaitUnsafeOnCompleted_2_T2
            def __call__(self, awaiter: clr.Reference[AwaitUnsafeOnCompleted_2_TAwaiter], stateMachine: clr.Reference[AwaitUnsafeOnCompleted_2_TStateMachine]) -> None:...


    # Skipped Start due to it being static, abstract and generic.

    Start : Start_MethodGroup[PoolingAsyncValueTaskMethodBuilder_1_TResult]
    Start_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('Start_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult')
    class Start_MethodGroup(typing.Generic[Start_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult]):
        Start_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult = PoolingAsyncValueTaskMethodBuilder_1.Start_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult
        def __getitem__(self, t:typing.Type[Start_1_T1]) -> Start_1[Start_MethodGroup_PoolingAsyncValueTaskMethodBuilder_1_TResult, Start_1_T1]: ...

        Start_1_PoolingAsyncValueTaskMethodBuilder_1_TResult = typing.TypeVar('Start_1_PoolingAsyncValueTaskMethodBuilder_1_TResult')
        Start_1_T1 = typing.TypeVar('Start_1_T1')
        class Start_1(typing.Generic[Start_1_PoolingAsyncValueTaskMethodBuilder_1_TResult, Start_1_T1]):
            Start_1_PoolingAsyncValueTaskMethodBuilder_1_TResult = PoolingAsyncValueTaskMethodBuilder_1.Start_MethodGroup.Start_1_PoolingAsyncValueTaskMethodBuilder_1_TResult
            Start_1_TStateMachine = PoolingAsyncValueTaskMethodBuilder_1.Start_MethodGroup.Start_1_T1
            def __call__(self, stateMachine: clr.Reference[Start_1_TStateMachine]) -> None:...




class PreserveBaseOverridesAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ReadOnlyCollectionBuilder_GenericClasses(abc.ABCMeta):
    Generic_ReadOnlyCollectionBuilder_GenericClasses_ReadOnlyCollectionBuilder_1_T = typing.TypeVar('Generic_ReadOnlyCollectionBuilder_GenericClasses_ReadOnlyCollectionBuilder_1_T')
    def __getitem__(self, types : typing.Type[Generic_ReadOnlyCollectionBuilder_GenericClasses_ReadOnlyCollectionBuilder_1_T]) -> typing.Type[ReadOnlyCollectionBuilder_1[Generic_ReadOnlyCollectionBuilder_GenericClasses_ReadOnlyCollectionBuilder_1_T]]: ...

ReadOnlyCollectionBuilder : ReadOnlyCollectionBuilder_GenericClasses

ReadOnlyCollectionBuilder_1_T = typing.TypeVar('ReadOnlyCollectionBuilder_1_T')
class ReadOnlyCollectionBuilder_1(typing.Generic[ReadOnlyCollectionBuilder_1_T], IList_1[ReadOnlyCollectionBuilder_1_T], IList):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, capacity: int) -> None: ...
    @typing.overload
    def __init__(self, collection: IEnumerable_1[ReadOnlyCollectionBuilder_1_T]) -> None: ...
    @property
    def Capacity(self) -> int: ...
    @Capacity.setter
    def Capacity(self, value: int) -> int: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ReadOnlyCollectionBuilder_1_T: ...
    @Item.setter
    def Item(self, value: ReadOnlyCollectionBuilder_1_T) -> ReadOnlyCollectionBuilder_1_T: ...
    def Add(self, item: ReadOnlyCollectionBuilder_1_T) -> None: ...
    def Clear(self) -> None: ...
    def Contains(self, item: ReadOnlyCollectionBuilder_1_T) -> bool: ...
    def CopyTo(self, array: Array_1[ReadOnlyCollectionBuilder_1_T], arrayIndex: int) -> None: ...
    def GetEnumerator(self) -> IEnumerator_1[ReadOnlyCollectionBuilder_1_T]: ...
    def IndexOf(self, item: ReadOnlyCollectionBuilder_1_T) -> int: ...
    def Insert(self, index: int, item: ReadOnlyCollectionBuilder_1_T) -> None: ...
    def Remove(self, item: ReadOnlyCollectionBuilder_1_T) -> bool: ...
    def RemoveAt(self, index: int) -> None: ...
    def ToArray(self) -> Array_1[ReadOnlyCollectionBuilder_1_T]: ...
    def ToReadOnlyCollection(self) -> ReadOnlyCollection_1[ReadOnlyCollectionBuilder_1_T]: ...
    # Skipped Reverse due to it being static, abstract and generic.

    Reverse : Reverse_MethodGroup[ReadOnlyCollectionBuilder_1_T]
    Reverse_MethodGroup_ReadOnlyCollectionBuilder_1_T = typing.TypeVar('Reverse_MethodGroup_ReadOnlyCollectionBuilder_1_T')
    class Reverse_MethodGroup(typing.Generic[Reverse_MethodGroup_ReadOnlyCollectionBuilder_1_T]):
        Reverse_MethodGroup_ReadOnlyCollectionBuilder_1_T = ReadOnlyCollectionBuilder_1.Reverse_MethodGroup_ReadOnlyCollectionBuilder_1_T
        @typing.overload
        def __call__(self) -> None:...
        @typing.overload
        def __call__(self, index: int, count: int) -> None:...



class ReferenceAssemblyAttribute(Attribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, description: str) -> None: ...
    @property
    def Description(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...


class RequiredAttributeAttribute(Attribute):
    def __init__(self, requiredContract: typing.Type[typing.Any]) -> None: ...
    @property
    def RequiredContract(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class RuleCache_GenericClasses(abc.ABCMeta):
    Generic_RuleCache_GenericClasses_RuleCache_1_T = typing.TypeVar('Generic_RuleCache_GenericClasses_RuleCache_1_T')
    def __getitem__(self, types : typing.Type[Generic_RuleCache_GenericClasses_RuleCache_1_T]) -> typing.Type[RuleCache_1[Generic_RuleCache_GenericClasses_RuleCache_1_T]]: ...

RuleCache : RuleCache_GenericClasses

RuleCache_1_T = typing.TypeVar('RuleCache_1_T')
class RuleCache_1(typing.Generic[RuleCache_1_T]):
    pass


class RuntimeCompatibilityAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def WrapNonExceptionThrows(self) -> bool: ...
    @WrapNonExceptionThrows.setter
    def WrapNonExceptionThrows(self, value: bool) -> bool: ...


class RuntimeFeature(abc.ABC):
    CovariantReturnsOfClasses : str
    DefaultImplementationsOfInterfaces : str
    PortablePdb : str
    UnmanagedSignatureCallingConvention : str
    VirtualStaticsInInterfaces : str
    @classmethod
    @property
    def IsDynamicCodeCompiled(cls) -> bool: ...
    @classmethod
    @property
    def IsDynamicCodeSupported(cls) -> bool: ...
    @staticmethod
    def IsSupported(feature: str) -> bool: ...


class RuntimeHelpers(abc.ABC):
    @classmethod
    @property
    def OffsetToStringData(cls) -> int: ...
    @staticmethod
    def AllocateTypeAssociatedMemory(type: typing.Type[typing.Any], size: int) -> int: ...
    @staticmethod
    def EnsureSufficientExecutionStack() -> None: ...
    @staticmethod
    def ExecuteCodeWithGuaranteedCleanup(code: RuntimeHelpers.TryCode, backoutCode: RuntimeHelpers.CleanupCode, userData: typing.Any) -> None: ...
    @staticmethod
    def GetObjectValue(obj: typing.Any) -> typing.Any: ...
    @staticmethod
    def GetUninitializedObject(type: typing.Type[typing.Any]) -> typing.Any: ...
    @staticmethod
    def InitializeArray(array: Array, fldHandle: RuntimeFieldHandle) -> None: ...
    @staticmethod
    def PrepareConstrainedRegions() -> None: ...
    @staticmethod
    def PrepareConstrainedRegionsNoOP() -> None: ...
    @staticmethod
    def PrepareContractedDelegate(d: Delegate) -> None: ...
    @staticmethod
    def PrepareDelegate(d: Delegate) -> None: ...
    @staticmethod
    def ProbeForSufficientStack() -> None: ...
    @staticmethod
    def RunClassConstructor(type: RuntimeTypeHandle) -> None: ...
    @staticmethod
    def RunModuleConstructor(module: ModuleHandle) -> None: ...
    @staticmethod
    def TryEnsureSufficientExecutionStack() -> bool: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...
        @typing.overload
        def __call__(self, o1: typing.Any, o2: typing.Any) -> bool:...

    # Skipped GetHashCode due to it being static, abstract and generic.

    GetHashCode : GetHashCode_MethodGroup
    class GetHashCode_MethodGroup:
        @typing.overload
        def __call__(self) -> int:...
        @typing.overload
        def __call__(self, o: typing.Any) -> int:...

    # Skipped GetSubArray due to it being static, abstract and generic.

    GetSubArray : GetSubArray_MethodGroup
    class GetSubArray_MethodGroup:
        def __getitem__(self, t:typing.Type[GetSubArray_1_T1]) -> GetSubArray_1[GetSubArray_1_T1]: ...

        GetSubArray_1_T1 = typing.TypeVar('GetSubArray_1_T1')
        class GetSubArray_1(typing.Generic[GetSubArray_1_T1]):
            GetSubArray_1_T = RuntimeHelpers.GetSubArray_MethodGroup.GetSubArray_1_T1
            def __call__(self, array: Array_1[GetSubArray_1_T], range: Range) -> Array_1[GetSubArray_1_T]:...


    # Skipped IsReferenceOrContainsReferences due to it being static, abstract and generic.

    IsReferenceOrContainsReferences : IsReferenceOrContainsReferences_MethodGroup
    class IsReferenceOrContainsReferences_MethodGroup:
        def __getitem__(self, t:typing.Type[IsReferenceOrContainsReferences_1_T1]) -> IsReferenceOrContainsReferences_1[IsReferenceOrContainsReferences_1_T1]: ...

        IsReferenceOrContainsReferences_1_T1 = typing.TypeVar('IsReferenceOrContainsReferences_1_T1')
        class IsReferenceOrContainsReferences_1(typing.Generic[IsReferenceOrContainsReferences_1_T1]):
            IsReferenceOrContainsReferences_1_T = RuntimeHelpers.IsReferenceOrContainsReferences_MethodGroup.IsReferenceOrContainsReferences_1_T1
            def __call__(self) -> bool:...


    # Skipped PrepareMethod due to it being static, abstract and generic.

    PrepareMethod : PrepareMethod_MethodGroup
    class PrepareMethod_MethodGroup:
        @typing.overload
        def __call__(self, method: RuntimeMethodHandle) -> None:...
        @typing.overload
        def __call__(self, method: RuntimeMethodHandle, instantiation: Array_1[RuntimeTypeHandle]) -> None:...


    class CleanupCode(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, userData: typing.Any, exceptionThrown: bool, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> None: ...
        def Invoke(self, userData: typing.Any, exceptionThrown: bool) -> None: ...


    class TryCode(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, userData: typing.Any, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> None: ...
        def Invoke(self, userData: typing.Any) -> None: ...



class RuntimeOps(abc.ABC):
    @staticmethod
    def ExpandoCheckVersion(expando: ExpandoObject, version: typing.Any) -> bool: ...
    @staticmethod
    def ExpandoPromoteClass(expando: ExpandoObject, oldClass: typing.Any, newClass: typing.Any) -> None: ...
    @staticmethod
    def ExpandoTryDeleteValue(expando: ExpandoObject, indexClass: typing.Any, index: int, name: str, ignoreCase: bool) -> bool: ...
    @staticmethod
    def ExpandoTryGetValue(expando: ExpandoObject, indexClass: typing.Any, index: int, name: str, ignoreCase: bool, value: clr.Reference[typing.Any]) -> bool: ...
    @staticmethod
    def ExpandoTrySetValue(expando: ExpandoObject, indexClass: typing.Any, index: int, value: typing.Any, name: str, ignoreCase: bool) -> typing.Any: ...
    @staticmethod
    def MergeRuntimeVariables(first: IRuntimeVariables, second: IRuntimeVariables, indexes: Array_1[int]) -> IRuntimeVariables: ...
    @staticmethod
    def Quote(expression: Expression, hoistedLocals: typing.Any, locals: Array_1[typing.Any]) -> Expression: ...
    # Skipped CreateRuntimeVariables due to it being static, abstract and generic.

    CreateRuntimeVariables : CreateRuntimeVariables_MethodGroup
    class CreateRuntimeVariables_MethodGroup:
        @typing.overload
        def __call__(self) -> IRuntimeVariables:...
        @typing.overload
        def __call__(self, data: Array_1[typing.Any], indexes: Array_1[int]) -> IRuntimeVariables:...



class RuntimeWrappedException(Exception):
    def __init__(self, thrownObject: typing.Any) -> None: ...
    @property
    def Data(self) -> IDictionary: ...
    @property
    def HelpLink(self) -> str: ...
    @HelpLink.setter
    def HelpLink(self, value: str) -> str: ...
    @property
    def HResult(self) -> int: ...
    @HResult.setter
    def HResult(self, value: int) -> int: ...
    @property
    def InnerException(self) -> Exception: ...
    @property
    def Message(self) -> str: ...
    @property
    def Source(self) -> str: ...
    @Source.setter
    def Source(self, value: str) -> str: ...
    @property
    def StackTrace(self) -> str: ...
    @property
    def TargetSite(self) -> MethodBase: ...
    @property
    def WrappedException(self) -> typing.Any: ...
    def GetObjectData(self, info: SerializationInfo, context: StreamingContext) -> None: ...


class ScopelessEnumAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class SkipLocalsInitAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class SpecialNameAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class StateMachineAttribute(Attribute):
    def __init__(self, stateMachineType: typing.Type[typing.Any]) -> None: ...
    @property
    def StateMachineType(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class StringFreezingAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class StrongBox_GenericClasses(abc.ABCMeta):
    Generic_StrongBox_GenericClasses_StrongBox_1_T = typing.TypeVar('Generic_StrongBox_GenericClasses_StrongBox_1_T')
    def __getitem__(self, types : typing.Type[Generic_StrongBox_GenericClasses_StrongBox_1_T]) -> typing.Type[StrongBox_1[Generic_StrongBox_GenericClasses_StrongBox_1_T]]: ...

StrongBox : StrongBox_GenericClasses

StrongBox_1_T = typing.TypeVar('StrongBox_1_T')
class StrongBox_1(typing.Generic[StrongBox_1_T], IStrongBox):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, value: StrongBox_1_T) -> None: ...
    Value : StrongBox_1_T


class SuppressIldasmAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class SwitchExpressionException(InvalidOperationException):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, innerException: Exception) -> None: ...
    @typing.overload
    def __init__(self, message: str) -> None: ...
    @typing.overload
    def __init__(self, message: str, innerException: Exception) -> None: ...
    @typing.overload
    def __init__(self, unmatchedValue: typing.Any) -> None: ...
    @property
    def Data(self) -> IDictionary: ...
    @property
    def HelpLink(self) -> str: ...
    @HelpLink.setter
    def HelpLink(self, value: str) -> str: ...
    @property
    def HResult(self) -> int: ...
    @HResult.setter
    def HResult(self, value: int) -> int: ...
    @property
    def InnerException(self) -> Exception: ...
    @property
    def Message(self) -> str: ...
    @property
    def Source(self) -> str: ...
    @Source.setter
    def Source(self, value: str) -> str: ...
    @property
    def StackTrace(self) -> str: ...
    @property
    def TargetSite(self) -> MethodBase: ...
    @property
    def UnmatchedValue(self) -> typing.Any: ...
    def GetObjectData(self, info: SerializationInfo, context: StreamingContext) -> None: ...


class TaskAwaiter_GenericClasses(abc.ABCMeta):
    Generic_TaskAwaiter_GenericClasses_TaskAwaiter_1_TResult = typing.TypeVar('Generic_TaskAwaiter_GenericClasses_TaskAwaiter_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_TaskAwaiter_GenericClasses_TaskAwaiter_1_TResult]) -> typing.Type[TaskAwaiter_1[Generic_TaskAwaiter_GenericClasses_TaskAwaiter_1_TResult]]: ...

class TaskAwaiter(TaskAwaiter_0, metaclass =TaskAwaiter_GenericClasses): ...

class TaskAwaiter_0(ICriticalNotifyCompletion):
    @property
    def IsCompleted(self) -> bool: ...
    def GetResult(self) -> None: ...
    def OnCompleted(self, continuation: Action) -> None: ...
    def UnsafeOnCompleted(self, continuation: Action) -> None: ...


TaskAwaiter_1_TResult = typing.TypeVar('TaskAwaiter_1_TResult')
class TaskAwaiter_1(typing.Generic[TaskAwaiter_1_TResult], ICriticalNotifyCompletion):
    @property
    def IsCompleted(self) -> bool: ...
    def GetResult(self) -> TaskAwaiter_1_TResult: ...
    def OnCompleted(self, continuation: Action) -> None: ...
    def UnsafeOnCompleted(self, continuation: Action) -> None: ...


class TupleElementNamesAttribute(Attribute):
    def __init__(self, transformNames: Array_1[str]) -> None: ...
    @property
    def TransformNames(self) -> IList_1[str]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class TypeForwardedFromAttribute(Attribute):
    def __init__(self, assemblyFullName: str) -> None: ...
    @property
    def AssemblyFullName(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...


class TypeForwardedToAttribute(Attribute):
    def __init__(self, destination: typing.Type[typing.Any]) -> None: ...
    @property
    def Destination(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class UnsafeValueTypeAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ValueTaskAwaiter_GenericClasses(abc.ABCMeta):
    Generic_ValueTaskAwaiter_GenericClasses_ValueTaskAwaiter_1_TResult = typing.TypeVar('Generic_ValueTaskAwaiter_GenericClasses_ValueTaskAwaiter_1_TResult')
    def __getitem__(self, types : typing.Type[Generic_ValueTaskAwaiter_GenericClasses_ValueTaskAwaiter_1_TResult]) -> typing.Type[ValueTaskAwaiter_1[Generic_ValueTaskAwaiter_GenericClasses_ValueTaskAwaiter_1_TResult]]: ...

class ValueTaskAwaiter(ValueTaskAwaiter_0, metaclass =ValueTaskAwaiter_GenericClasses): ...

class ValueTaskAwaiter_0(ICriticalNotifyCompletion):
    @property
    def IsCompleted(self) -> bool: ...
    def GetResult(self) -> None: ...
    def OnCompleted(self, continuation: Action) -> None: ...
    def UnsafeOnCompleted(self, continuation: Action) -> None: ...


ValueTaskAwaiter_1_TResult = typing.TypeVar('ValueTaskAwaiter_1_TResult')
class ValueTaskAwaiter_1(typing.Generic[ValueTaskAwaiter_1_TResult], ICriticalNotifyCompletion):
    @property
    def IsCompleted(self) -> bool: ...
    def GetResult(self) -> ValueTaskAwaiter_1_TResult: ...
    def OnCompleted(self, continuation: Action) -> None: ...
    def UnsafeOnCompleted(self, continuation: Action) -> None: ...


class YieldAwaitable:
    def GetAwaiter(self) -> YieldAwaitable.YieldAwaiter: ...

    class YieldAwaiter(ICriticalNotifyCompletion):
        @property
        def IsCompleted(self) -> bool: ...
        def GetResult(self) -> None: ...
        def OnCompleted(self, continuation: Action) -> None: ...
        def UnsafeOnCompleted(self, continuation: Action) -> None: ...


