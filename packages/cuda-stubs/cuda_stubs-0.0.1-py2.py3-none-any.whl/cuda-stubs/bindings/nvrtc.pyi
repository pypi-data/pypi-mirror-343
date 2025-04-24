from typing import *
import enum
from typing import Any, Callable, ClassVar


def __reduce_cython__(self):
    """
    nvrtcProgram.__reduce_cython__(self)
    """


def __setstate_cython__(self, __pyx_state):
    """
    nvrtcProgram.__setstate_cython__(self, __pyx_state)
    """

__test__: dict

def nvrtcAddNameExpression(prog, name_expression):
    """
    nvrtcAddNameExpression(prog, char *name_expression)
     nvrtcAddNameExpression notes the given name expression denoting the address of a global function or device/__constant__ variable.

        The identical name expression string must be provided on a subsequent
        call to nvrtcGetLoweredName to extract the lowered name.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        name_expression : bytes
            constant expression denoting the address of a global function or
            device/__constant__ variable.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_NO_NAME_EXPRESSIONS_AFTER_COMPILATION`

        See Also
        --------
        :py:obj:`~.nvrtcGetLoweredName`
    """


def nvrtcCompileProgram(prog, numOptions, options: 'Optional[Tuple[bytes] | List[bytes]]'):
    """
    nvrtcCompileProgram(prog, int numOptions, options: Optional[Tuple[bytes] | List[bytes]])
     nvrtcCompileProgram compiles the given program.

        It supports compile options listed in :py:obj:`~.Supported Compile
        Options`.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        numOptions : int
            Number of compiler options passed.
        options : List[bytes]
            Compiler options in the form of C string array.  `options` can be
            `NULL` when `numOptions` is 0.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_OUT_OF_MEMORY`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
            - :py:obj:`~.NVRTC_ERROR_INVALID_OPTION`
            - :py:obj:`~.NVRTC_ERROR_COMPILATION`
            - :py:obj:`~.NVRTC_ERROR_BUILTIN_OPERATION_FAILURE`
            - :py:obj:`~.NVRTC_ERROR_TIME_FILE_WRITE_FAILED`
            - :py:obj:`~.NVRTC_ERROR_CANCELLED`
    """


def nvrtcCreateProgram(src, name, numHeaders, headers: 'Optional[Tuple[bytes] | List[bytes]]', includeNames: 'Optional[Tuple[bytes] | List[bytes]]'):
    """
    nvrtcCreateProgram(char *src, char *name, int numHeaders, headers: Optional[Tuple[bytes] | List[bytes]], includeNames: Optional[Tuple[bytes] | List[bytes]])
     nvrtcCreateProgram creates an instance of nvrtcProgram with the given input parameters, and sets the output parameter `prog` with it.

        Parameters
        ----------
        src : bytes
            CUDA program source.
        name : bytes
            CUDA program name.  `name` can be `NULL`; `"default_program"` is
            used when `name` is `NULL` or "".
        numHeaders : int
            Number of headers used.  `numHeaders` must be greater than or equal
            to 0.
        headers : List[bytes]
            Sources of the headers.  `headers` can be `NULL` when `numHeaders`
            is 0.
        includeNames : List[bytes]
            Name of each header by which they can be included in the CUDA
            program source.  `includeNames` can be `NULL` when `numHeaders` is
            0. These headers must be included with the exact names specified
            here.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_OUT_OF_MEMORY`
            - :py:obj:`~.NVRTC_ERROR_PROGRAM_CREATION_FAILURE`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        See Also
        --------
        :py:obj:`~.nvrtcDestroyProgram`
    """


def nvrtcDestroyProgram(prog):
    """
    nvrtcDestroyProgram(prog)
     nvrtcDestroyProgram destroys the given program.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`

        See Also
        --------
        :py:obj:`~.nvrtcCreateProgram`
    """


def nvrtcGetCUBIN(prog, cubin):
    """
    nvrtcGetCUBIN(prog, char *cubin)
     nvrtcGetCUBIN stores the cubin generated by the previous compilation of `prog` in the memory pointed by `cubin`. No cubin is available if the value specified to `-arch` is a virtual architecture instead of an actual architecture.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        cubin : bytes
            Compiled and assembled result.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`

        See Also
        --------
        :py:obj:`~.nvrtcGetCUBINSize`
    """


def nvrtcGetCUBINSize(prog):
    """
    nvrtcGetCUBINSize(prog)
     nvrtcGetCUBINSize sets the value of `cubinSizeRet` with the size of the cubin generated by the previous compilation of `prog`. The value of cubinSizeRet is set to 0 if the value specified to `-arch` is a virtual architecture instead of an actual architecture.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
        cubinSizeRet : int
            Size of the generated cubin.

        See Also
        --------
        :py:obj:`~.nvrtcGetCUBIN`
    """


def nvrtcGetErrorString(result: 'nvrtcResult'):
    """
    nvrtcGetErrorString(result: nvrtcResult)
     nvrtcGetErrorString is a helper function that returns a string describing the given nvrtcResult code, e.g., NVRTC_SUCCESS to `"NVRTC_SUCCESS"`. For unrecognized enumeration values, it returns `"NVRTC_ERROR unknown"`.

        Parameters
        ----------
        result : :py:obj:`~.nvrtcResult`
            CUDA Runtime Compilation API result code.

        Returns
        -------
        nvrtcResult.NVRTC_SUCCESS
            nvrtcResult.NVRTC_SUCCESS
        bytes
            Message string for the given :py:obj:`~.nvrtcResult` code.
    """


def nvrtcGetLTOIR(prog, LTOIR):
    """
    nvrtcGetLTOIR(prog, char *LTOIR)
     nvrtcGetLTOIR stores the LTO IR generated by the previous compilation of `prog` in the memory pointed by `LTOIR`. No LTO IR is available if the program was compiled without `-dlto`.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        LTOIR : bytes
            Compiled result.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`

        See Also
        --------
        :py:obj:`~.nvrtcGetLTOIRSize`
    """


def nvrtcGetLTOIRSize(prog):
    """
    nvrtcGetLTOIRSize(prog)
     nvrtcGetLTOIRSize sets the value of `LTOIRSizeRet` with the size of the LTO IR generated by the previous compilation of `prog`. The value of LTOIRSizeRet is set to 0 if the program was not compiled with `-dlto`.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
        LTOIRSizeRet : int
            Size of the generated LTO IR.

        See Also
        --------
        :py:obj:`~.nvrtcGetLTOIR`
    """


def nvrtcGetLoweredName(prog, name_expression):
    """
    nvrtcGetLoweredName(prog, char *name_expression)
     nvrtcGetLoweredName extracts the lowered (mangled) name for a global function or device/__constant__ variable, and updates lowered_name to point to it. The memory containing the name is released when the NVRTC program is destroyed by nvrtcDestroyProgram. The identical name expression must have been previously provided to nvrtcAddNameExpression.

        Parameters
        ----------
        prog : nvrtcProgram
            CUDA Runtime Compilation program.
        name_expression : bytes
            constant expression denoting the address of a global function or
            device/__constant__ variable.

        Returns
        -------
        nvrtcResult
            NVRTC_SUCCESS
            NVRTC_ERROR_NO_LOWERED_NAMES_BEFORE_COMPILATION
            NVRTC_ERROR_NAME_EXPRESSION_NOT_VALID
        lowered_name : bytes
            initialized by the function to point to a C string containing the
            lowered (mangled) name corresponding to the provided name
            expression.

        See Also
        --------
        nvrtcAddNameExpression
    """


def nvrtcGetNVVM(prog, nvvm):
    """
    nvrtcGetNVVM(prog, char *nvvm)
     DEPRECATION NOTICE: This function will be removed in a future release. Please use nvrtcGetLTOIR (and nvrtcGetLTOIRSize) instead.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            None
        nvvm : bytes
            None

        Returns
        -------
        nvrtcResult
    """


def nvrtcGetNVVMSize(prog):
    """
    nvrtcGetNVVMSize(prog)
     DEPRECATION NOTICE: This function will be removed in a future release. Please use nvrtcGetLTOIRSize (and nvrtcGetLTOIR) instead.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            None

        Returns
        -------
        nvrtcResult

        nvvmSizeRet : int
            None
    """


def nvrtcGetNumSupportedArchs():
    """
    nvrtcGetNumSupportedArchs()
     nvrtcGetNumSupportedArchs sets the output parameter `numArchs` with the number of architectures supported by NVRTC. This can then be used to pass an array to :py:obj:`~.nvrtcGetSupportedArchs` to get the supported architectures.

        see :py:obj:`~.nvrtcGetSupportedArchs`

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
        numArchs : int
            number of supported architectures.
    """


def nvrtcGetOptiXIR(prog, optixir):
    """
    nvrtcGetOptiXIR(prog, char *optixir)
     nvrtcGetOptiXIR stores the OptiX IR generated by the previous compilation of `prog` in the memory pointed by `optixir`. No OptiX IR is available if the program was compiled with options incompatible with OptiX IR generation.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        optixir : bytes
            Optix IR Compiled result.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`

        See Also
        --------
        :py:obj:`~.nvrtcGetOptiXIRSize`
    """


def nvrtcGetOptiXIRSize(prog):
    """
    nvrtcGetOptiXIRSize(prog)
     nvrtcGetOptiXIRSize sets the value of `optixirSizeRet` with the size of the OptiX IR generated by the previous compilation of `prog`. The value of nvrtcGetOptiXIRSize is set to 0 if the program was compiled with options incompatible with OptiX IR generation.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
        optixirSizeRet : int
            Size of the generated LTO IR.

        See Also
        --------
        :py:obj:`~.nvrtcGetOptiXIR`
    """


def nvrtcGetPCHCreateStatus(prog):
    """
    nvrtcGetPCHCreateStatus(prog)
     returns the PCH creation status.

        NVRTC_SUCCESS indicates that the PCH was successfully created.
        NVRTC_ERROR_NO_PCH_CREATE_ATTEMPTED indicates that no PCH creation was
        attempted, either because PCH functionality was not requested during
        the preceding nvrtcCompileProgram call, or automatic PCH processing was
        requested, and compiler chose not to create a PCH file.
        NVRTC_ERROR_PCH_CREATE_HEAP_EXHAUSTED indicates that a PCH file could
        potentially have been created, but the compiler ran out space in the
        PCH heap. In this scenario, the
        :py:obj:`~.nvrtcGetPCHHeapSizeRequired()` can be used to query the
        required heap size, the heap can be reallocated for this size with
        :py:obj:`~.nvrtcSetPCHHeapSize()` and PCH creation may be reattempted
        again invoking :py:obj:`~.nvrtcCompileProgram()` with a new NVRTC
        program instance. NVRTC_ERROR_PCH_CREATE indicates that an error
        condition prevented the PCH file from being created.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_NO_PCH_CREATE_ATTEMPTED`
            - :py:obj:`~.NVRTC_ERROR_PCH_CREATE`
            - :py:obj:`~.NVRTC_ERROR_PCH_CREATE_HEAP_EXHAUSTED`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
    """


def nvrtcGetPCHHeapSize():
    """
    nvrtcGetPCHHeapSize()
     retrieve the current size of the PCH Heap.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
        ret : int
            pointer to location where the size of the PCH Heap will be stored
    """


def nvrtcGetPCHHeapSizeRequired(prog):
    """
    nvrtcGetPCHHeapSizeRequired(prog)
     retrieve the required size of the PCH heap required to compile the given program.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT` The size retrieved using this function is only valid if :py:obj:`~.nvrtcGetPCHCreateStatus()` returned NVRTC_SUCCESS or NVRTC_ERROR_PCH_CREATE_HEAP_EXHAUSTED
        size : int
            pointer to location where the required size of the PCH Heap will be
            stored
    """


def nvrtcGetPTX(prog, ptx):
    """
    nvrtcGetPTX(prog, char *ptx)
     nvrtcGetPTX stores the PTX generated by the previous compilation of `prog` in the memory pointed by `ptx`.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        ptx : bytes
            Compiled result.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`

        See Also
        --------
        :py:obj:`~.nvrtcGetPTXSize`
    """


def nvrtcGetPTXSize(prog):
    """
    nvrtcGetPTXSize(prog)
     nvrtcGetPTXSize sets the value of `ptxSizeRet` with the size of the PTX generated by the previous compilation of `prog` (including the trailing `NULL`).

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
        ptxSizeRet : int
            Size of the generated PTX (including the trailing `NULL`).

        See Also
        --------
        :py:obj:`~.nvrtcGetPTX`
    """


def nvrtcGetProgramLog(prog, log):
    """
    nvrtcGetProgramLog(prog, char *log)
     nvrtcGetProgramLog stores the log generated by the previous compilation of `prog` in the memory pointed by `log`.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        log : bytes
            Compilation log.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`

        See Also
        --------
        :py:obj:`~.nvrtcGetProgramLogSize`
    """


def nvrtcGetProgramLogSize(prog):
    """
    nvrtcGetProgramLogSize(prog)
     nvrtcGetProgramLogSize sets `logSizeRet` with the size of the log generated by the previous compilation of `prog` (including the trailing `NULL`).

        Note that compilation log may be generated with warnings and
        informative messages, even when the compilation of `prog` succeeds.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
        logSizeRet : int
            Size of the compilation log (including the trailing `NULL`).

        See Also
        --------
        :py:obj:`~.nvrtcGetProgramLog`
    """


def nvrtcGetSupportedArchs():
    """
    nvrtcGetSupportedArchs()
     nvrtcGetSupportedArchs populates the array passed via the output parameter `supportedArchs` with the architectures supported by NVRTC. The array is sorted in the ascending order. The size of the array to be passed can be determined using :py:obj:`~.nvrtcGetNumSupportedArchs`.

        see :py:obj:`~.nvrtcGetNumSupportedArchs`

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
        supportedArchs : List[int]
            sorted array of supported architectures.
    """


def nvrtcSetFlowCallback(prog, callback, payload):
    """
    nvrtcSetFlowCallback(prog, callback, payload)
     nvrtcSetFlowCallback registers a callback function that the compiler will invoke at different points during a call to nvrtcCompileProgram, and the callback function can decide whether to cancel compilation by returning specific values.

        The callback function must satisfy the following constraints:

        (1) Its signature should be:

        **View CUDA Toolkit Documentation for a C++ code example**

        When invoking the callback, the compiler will always pass `payload` to
        param1 so that the callback may make decisions based on `payload` .
        It'll always pass NULL to param2 for now which is reserved for future
        extensions.

        (2) It must return 1 to cancel compilation or 0 to continue. Other
        return values are reserved for future use.

        (3) It must return consistent values. Once it returns 1 at one point,
        it must return 1 in all following invocations during the current
        nvrtcCompileProgram call in progress.

        (4) It must be thread-safe.

        (5) It must not invoke any nvrtc/libnvvm/ptx APIs.

        Parameters
        ----------
        prog : :py:obj:`~.nvrtcProgram`
            CUDA Runtime Compilation program.
        callback : Any
            the callback that issues cancellation signal.
        payload : Any
            to be passed as a parameter when invoking the callback.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_PROGRAM`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
    """


def nvrtcSetPCHHeapSize(size):
    """
    nvrtcSetPCHHeapSize(size_t size)
     set the size of the PCH Heap.

        The requested size may be rounded up to a platform dependent alignment
        (e.g. page size). If the PCH Heap has already been allocated, the heap
        memory will be freed and a new PCH Heap will be allocated.

        Parameters
        ----------
        size : size_t
            requested size of the PCH Heap, in bytes

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
    """


def nvrtcVersion():
    """
    nvrtcVersion()
     nvrtcVersion sets the output parameters `major` and `minor` with the CUDA Runtime Compilation version number.

        Returns
        -------
        nvrtcResult
            - :py:obj:`~.NVRTC_SUCCESS`
            - :py:obj:`~.NVRTC_ERROR_INVALID_INPUT`
        major : int
            CUDA Runtime Compilation major version number.
        minor : int
            CUDA Runtime Compilation minor version number.
    """


def sizeof(objType):
    """
    sizeof(objType)
     Returns the size of provided CUDA Python structure in bytes

        Parameters
        ----------
        objType : Any
            CUDA Python object

        Returns
        -------
        lowered_name : int
            The size of `objType` in bytes
    """


class nvrtcProgram:
    def __init__(self, *args, **kwargs) -> Any:
        """Initialize self.  See help(type(self)) for accurate signature."""
    def getPtr(self) -> Any:
        """nvrtcProgram.getPtr(self)"""
    def __index__(self) -> int:
        """Return self converted to an integer, if self is suitable for use as an index into a list."""
    def __int__(self) -> int:
        """int(self)"""
    def __reduce__(self):
        """nvrtcProgram.__reduce_cython__(self)"""

class nvrtcResult(enum.IntEnum):
    __new__: ClassVar[Callable] = ...
    NVRTC_ERROR_BUILTIN_OPERATION_FAILURE: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_CANCELLED: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_COMPILATION: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_INTERNAL_ERROR: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_INVALID_INPUT: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_INVALID_OPTION: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_INVALID_PROGRAM: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_NAME_EXPRESSION_NOT_VALID: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_NO_LOWERED_NAMES_BEFORE_COMPILATION: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_NO_NAME_EXPRESSIONS_AFTER_COMPILATION: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_NO_PCH_CREATE_ATTEMPTED: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_OUT_OF_MEMORY: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_PCH_CREATE: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_PCH_CREATE_HEAP_EXHAUSTED: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_PROGRAM_CREATION_FAILURE: ClassVar[nvrtcResult] = ...
    NVRTC_ERROR_TIME_FILE_WRITE_FAILED: ClassVar[nvrtcResult] = ...
    NVRTC_SUCCESS: ClassVar[nvrtcResult] = ...
    _generate_next_value_: ClassVar[Callable] = ...
    _member_map_: ClassVar[dict] = ...
    _member_names_: ClassVar[list] = ...
    _member_type_: ClassVar[type[int]] = ...
    _unhashable_values_: ClassVar[list] = ...
    _use_args_: ClassVar[bool] = ...
    _value2member_map_: ClassVar[dict] = ...
    def __format__(self, *args, **kwargs) -> str:
        """Convert to a string according to format_spec."""