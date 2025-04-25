import typing, clr, abc
from System.Collections.Generic import IEnumerable_1
from System import Predicate_1, Attribute, Exception, EventArgs
from System.Collections import IDictionary
from System.Reflection import MethodBase
from System.Runtime.Serialization import SerializationInfo, StreamingContext

class Contract(abc.ABC):
    @staticmethod
    def EndContractBlock() -> None: ...
    # Skipped Assert due to it being static, abstract and generic.

    Assert : Assert_MethodGroup
    class Assert_MethodGroup:
        @typing.overload
        def __call__(self, condition: bool) -> None:...
        @typing.overload
        def __call__(self, condition: bool, userMessage: str) -> None:...

    # Skipped Assume due to it being static, abstract and generic.

    Assume : Assume_MethodGroup
    class Assume_MethodGroup:
        @typing.overload
        def __call__(self, condition: bool) -> None:...
        @typing.overload
        def __call__(self, condition: bool, userMessage: str) -> None:...

    # Skipped Ensures due to it being static, abstract and generic.

    Ensures : Ensures_MethodGroup
    class Ensures_MethodGroup:
        @typing.overload
        def __call__(self, condition: bool) -> None:...
        @typing.overload
        def __call__(self, condition: bool, userMessage: str) -> None:...

    # Skipped EnsuresOnThrow due to it being static, abstract and generic.

    EnsuresOnThrow : EnsuresOnThrow_MethodGroup
    class EnsuresOnThrow_MethodGroup:
        def __getitem__(self, t:typing.Type[EnsuresOnThrow_1_T1]) -> EnsuresOnThrow_1[EnsuresOnThrow_1_T1]: ...

        EnsuresOnThrow_1_T1 = typing.TypeVar('EnsuresOnThrow_1_T1')
        class EnsuresOnThrow_1(typing.Generic[EnsuresOnThrow_1_T1]):
            EnsuresOnThrow_1_TException = Contract.EnsuresOnThrow_MethodGroup.EnsuresOnThrow_1_T1
            @typing.overload
            def __call__(self, condition: bool) -> None:...
            @typing.overload
            def __call__(self, condition: bool, userMessage: str) -> None:...


    # Skipped Exists due to it being static, abstract and generic.

    Exists : Exists_MethodGroup
    class Exists_MethodGroup:
        def __getitem__(self, t:typing.Type[Exists_1_T1]) -> Exists_1[Exists_1_T1]: ...

        Exists_1_T1 = typing.TypeVar('Exists_1_T1')
        class Exists_1(typing.Generic[Exists_1_T1]):
            Exists_1_T = Contract.Exists_MethodGroup.Exists_1_T1
            def __call__(self, collection: IEnumerable_1[Exists_1_T], predicate: Predicate_1[Exists_1_T]) -> bool:...

        def __call__(self, fromInclusive: int, toExclusive: int, predicate: Predicate_1[int]) -> bool:...

    # Skipped ForAll due to it being static, abstract and generic.

    ForAll : ForAll_MethodGroup
    class ForAll_MethodGroup:
        def __getitem__(self, t:typing.Type[ForAll_1_T1]) -> ForAll_1[ForAll_1_T1]: ...

        ForAll_1_T1 = typing.TypeVar('ForAll_1_T1')
        class ForAll_1(typing.Generic[ForAll_1_T1]):
            ForAll_1_T = Contract.ForAll_MethodGroup.ForAll_1_T1
            def __call__(self, collection: IEnumerable_1[ForAll_1_T], predicate: Predicate_1[ForAll_1_T]) -> bool:...

        def __call__(self, fromInclusive: int, toExclusive: int, predicate: Predicate_1[int]) -> bool:...

    # Skipped Invariant due to it being static, abstract and generic.

    Invariant : Invariant_MethodGroup
    class Invariant_MethodGroup:
        @typing.overload
        def __call__(self, condition: bool) -> None:...
        @typing.overload
        def __call__(self, condition: bool, userMessage: str) -> None:...

    # Skipped OldValue due to it being static, abstract and generic.

    OldValue : OldValue_MethodGroup
    class OldValue_MethodGroup:
        def __getitem__(self, t:typing.Type[OldValue_1_T1]) -> OldValue_1[OldValue_1_T1]: ...

        OldValue_1_T1 = typing.TypeVar('OldValue_1_T1')
        class OldValue_1(typing.Generic[OldValue_1_T1]):
            OldValue_1_T = Contract.OldValue_MethodGroup.OldValue_1_T1
            def __call__(self, value: OldValue_1_T) -> OldValue_1_T:...


    # Skipped Requires due to it being static, abstract and generic.

    Requires : Requires_MethodGroup
    class Requires_MethodGroup:
        def __getitem__(self, t:typing.Type[Requires_1_T1]) -> Requires_1[Requires_1_T1]: ...

        Requires_1_T1 = typing.TypeVar('Requires_1_T1')
        class Requires_1(typing.Generic[Requires_1_T1]):
            Requires_1_TException = Contract.Requires_MethodGroup.Requires_1_T1
            @typing.overload
            def __call__(self, condition: bool) -> None:...
            @typing.overload
            def __call__(self, condition: bool, userMessage: str) -> None:...

        @typing.overload
        def __call__(self, condition: bool) -> None:...
        @typing.overload
        def __call__(self, condition: bool, userMessage: str) -> None:...

    # Skipped Result due to it being static, abstract and generic.

    Result : Result_MethodGroup
    class Result_MethodGroup:
        def __getitem__(self, t:typing.Type[Result_1_T1]) -> Result_1[Result_1_T1]: ...

        Result_1_T1 = typing.TypeVar('Result_1_T1')
        class Result_1(typing.Generic[Result_1_T1]):
            Result_1_T = Contract.Result_MethodGroup.Result_1_T1
            def __call__(self) -> Result_1_T:...


    # Skipped ValueAtReturn due to it being static, abstract and generic.

    ValueAtReturn : ValueAtReturn_MethodGroup
    class ValueAtReturn_MethodGroup:
        def __getitem__(self, t:typing.Type[ValueAtReturn_1_T1]) -> ValueAtReturn_1[ValueAtReturn_1_T1]: ...

        ValueAtReturn_1_T1 = typing.TypeVar('ValueAtReturn_1_T1')
        class ValueAtReturn_1(typing.Generic[ValueAtReturn_1_T1]):
            ValueAtReturn_1_T = Contract.ValueAtReturn_MethodGroup.ValueAtReturn_1_T1
            def __call__(self, value: clr.Reference[ValueAtReturn_1_T]) -> ValueAtReturn_1_T:...




class ContractAbbreviatorAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractArgumentValidatorAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractClassAttribute(Attribute):
    def __init__(self, typeContainingContracts: typing.Type[typing.Any]) -> None: ...
    @property
    def TypeContainingContracts(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractClassForAttribute(Attribute):
    def __init__(self, typeContractsAreFor: typing.Type[typing.Any]) -> None: ...
    @property
    def TypeContractsAreFor(self) -> typing.Type[typing.Any]: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractException(Exception):
    def __init__(self, kind: ContractFailureKind, failure: str, userMessage: str, condition: str, innerException: Exception) -> None: ...
    @property
    def Condition(self) -> str: ...
    @property
    def Data(self) -> IDictionary: ...
    @property
    def Failure(self) -> str: ...
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
    def Kind(self) -> ContractFailureKind: ...
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
    def UserMessage(self) -> str: ...
    def GetObjectData(self, info: SerializationInfo, context: StreamingContext) -> None: ...


class ContractFailedEventArgs(EventArgs):
    def __init__(self, failureKind: ContractFailureKind, message: str, condition: str, originalException: Exception) -> None: ...
    @property
    def Condition(self) -> str: ...
    @property
    def FailureKind(self) -> ContractFailureKind: ...
    @property
    def Handled(self) -> bool: ...
    @property
    def Message(self) -> str: ...
    @property
    def OriginalException(self) -> Exception: ...
    @property
    def Unwind(self) -> bool: ...
    def SetHandled(self) -> None: ...
    def SetUnwind(self) -> None: ...


class ContractFailureKind(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Precondition : ContractFailureKind # 0
    Postcondition : ContractFailureKind # 1
    PostconditionOnException : ContractFailureKind # 2
    Invariant : ContractFailureKind # 3
    Assert : ContractFailureKind # 4
    Assume : ContractFailureKind # 5


class ContractInvariantMethodAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractOptionAttribute(Attribute):
    @typing.overload
    def __init__(self, category: str, setting: str, enabled: bool) -> None: ...
    @typing.overload
    def __init__(self, category: str, setting: str, value: str) -> None: ...
    @property
    def Category(self) -> str: ...
    @property
    def Enabled(self) -> bool: ...
    @property
    def Setting(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> str: ...


class ContractPublicPropertyNameAttribute(Attribute):
    def __init__(self, name: str) -> None: ...
    @property
    def Name(self) -> str: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractReferenceAssemblyAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractRuntimeIgnoredAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ContractVerificationAttribute(Attribute):
    def __init__(self, value: bool) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> bool: ...


class PureAttribute(Attribute):
    def __init__(self) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...

