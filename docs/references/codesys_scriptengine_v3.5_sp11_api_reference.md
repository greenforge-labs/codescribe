# Entry points

## ArchiveCategories

Type: [ScriptProjectArchiveCategories](#scriptprojectarchivecategories)

## ImplementationLanguages

Type: [ScriptImplementationLanguages](#scriptimplementationlanguages)

## SV_DEV

= Guid('d9b2b2cc-ea99-4c3b-aa42-1e5c49e65b84')

## SV_POU

= Guid('21af5390-2942-461a-bf89-951aaf6999f1')

## device_repository

Type: [ScriptDeviceRepository](#scriptdevicerepository)

## librarymanager

Type: [LibManager](#libmanager)

## modulerepository

Type: [ScriptModuleRepository](#scriptmodulerepository)

## online

Type: [ScriptOnline](#scriptonline)

## projects

Type: [ScriptProjects](#scriptprojects)

## system

Type: [SystemImpl](#systemimpl)

# Enumerations

## AccessRight

Base: enum.Enum

Defines access rights on a parameter

`None`

:   Value: 0

```
The element is not accessible.
```

`Read`

:   Value: 1

```
Specifies that the element may be read.
```

`Write`

:   Value: 2

```
Specifies that it is allowed to write to the element
```

`ReadWrite`

:   Value: 3

```
Combination of read and write access: The element may be written
and read.
```

## AdditionalDirInfo

Base: enum.Enum

Flags to get additional information about a file or directory.

`None`

:   Value: 0

```
No information available
```

`PlaceholderDirectory`

:   Value: 1

```
The directory is defined as a placeholder directory (e.g.
\$PlcLogic\$) on the PLC.
```

`RedundantDirectory`

:   Value: 2

```
The directory is a shortcut to another directory (e.g. links to a
subdirectory in the default path)
```

## AlwaysUpdateVariablesMode

Base: enum.Enum

Defines always mapping modes on a parameter or connectors

`Disabled`

:   Value: 0

```
Disable the alway update of the variables.
```

`OnlyIfUnused`

:   Value: 1

```
The io channel is mapped in the bus cycle task if no other task is
using it. If it used in an task then alwaysmapping is ignored,
because it is updated in the used task only.
```

`AlwaysInBusCycle`

:   Value: 2

```
AlwaysInBusCycle: The io channel is always updated in the bus
cycle task independent of the real task usage. Therefore task
consistency is not guaranteed.
```

## ApplicationState

Base: enum.Enum

Execution state of an application

`none`

:   Value: 0

```
No valid application state (eg. not loaded).
```

`run`

:   Value: 1

```
Application is running.
```

`stop`

:   Value: 2

```
Application is stopped
```

`halt_on_bp`

:   Value: 3

```
Halted on a breakpoint.
```

`debug_step`

:   Value: 4

```
Executing a single step in the debugger.
```

`single_cycle`

:   Value: 5

```
Executing a single cycle in the debugger.
```

`system_application`

:   Value: 255

```
TOCHECK maybe to delete, a special flag indicating a system
application (only possible state is stop)
```

`unknown`

:   Value: 4294967295

```
Unknown application state.
```

## AutoUpdateMode

Base: enum.Enum

This enumeration is used to control how changes in a physical file are
reflected to the embedded data of a \[IFileReference\].

`Always`

:   Value: 0

```
Changes on the physical file are automatically reflected in the
embedded data.
```

`Prompt`

:   Value: 1

```
When the physical file changes, an event will be triggered in
order to obtain information whether to automatically update the
embedded data or not.
```

`Never`

:   Value: 2

```
Changes on the physical file are not automatically reflected in
the embedded data.
```

## BlockDriverType

Base: enum.Enum

An enumeration to specify the type of Block Driver used on the runtime
system

`Generic`

:   Value: 0

```
Any of the regular block drivers without special treatment or
unknown
```

`CmpBlkDrvTcp`

:   Value: 1

```
The Block Driver TCP in the runtime system
```

`CmpBlkDrvCom`

:   Value: 2

```
The Block Driver COM in the runtime system
```

`CmpBlkDrvUsb`

:   Value: 3

```
The Block Driver UDP in the runtime system
```

`CmpBlkDrvShm`

:   Value: 4

```
The Block Driver Shared Memory in the runtime system
```

`CmpBlkDrvUdp`

:   Value: 5

```
The Block Driver UDP in the runtime system
```

`CmpBlkDrvCanClient`

:   Value: 6

```
The Block Driver CAN Client in the runtime system
```

`CmpBlkDrvCanServer`

:   Value: 7

```
The Block Driver CAN Server in the runtime system
```

`CmpBlkDrvDirectCall`

:   Value: 8

```
The Block Driver Direct Call in the runtime system
```

## ChannelType

Base: enum.Enum

Defines the types of a channel.

`None`

:   Value: 0

```
Not a channel.
```

`Input`

:   Value: 1

```
An input channel.
```

`Output`

:   Value: 2

```
An output channel.
```

`OutputReadOnly`

:   Value: 3

```
An readonly output channel.
```

## ConflictResolve

Base: enum.Enum

Possible resolvements in the case that importing a specific PLCopenXML
object leads to conflicts with an already existing object.

`Replace`

:   Value: 0

```
The existing object is replaced by the imported object.
```

`Copy`

:   Value: 1

```
The existing object remains with its original name, and the
imported object is renamed so that is does not conflict any more.
```

`Skip`

:   Value: 2

```
The object to be imported is skipped.
```

## ConnectorRole

Base: enum.Enum

Describes the role of a connector

`Parent`

:   Value: 0

```
The connector allows other devices to be connected to the
connectors device
```

`Child`

:   Value: 1

```
The connector allows its device to be connectoed to another
device.
```

## CredentialSourceKind

Base: enum.Enum

The kinds of authentication allowed for the fallback to the default
handler.

`None`

:   Value: 0

```
No credential source kind allowed.
```

`CurrentProjectSession`

:   Value: 1

```
Tries a device login via the current project login credentials (if
logged in).
```

`Interactive`

:   Value: 2

```
Queries the user interactively for the credentials. Disabling this
bit can be useful for test scripts or python scripts, when no
interactive prompt is wanted.
```

`All`

:   Value: -1

```
All source kinds are allowed. (This is the default value when no
[ITemporaryLoginCredentialsContext] is set.)
```

## DeviceUserManagementFlags

Base: enum.Enum

Flags for the entire \[IDeviceUserList\], the
entire \[IDeviceGroupList\], a single
\[IDeviceUser\], or a single \[IDeviceGroup\].

`Edit`

:   Value: 1

```
If set, the particular [IDeviceUser] or
[IDeviceGroup] can be edited.
```

`AddMember`

:   Value: 2

```
If set, users or groups can be added to the particular
[IDeviceGroup].
```

`RemoveMember`

:   Value: 4

```
If set, users or groups can be removed from the particular
[IDeviceGroup].
```

`Create`

:   Value: 8

```
If set, new users can be created in the particular
[IDeviceUserList], or new groups can be
created in the particular [IDeviceGroupList].
```

`Delete`

:   Value: 16

```
If set, existing users can be deleted from the particular
[IDeviceUserList], or existing groups can be
deleted from the particular [IDeviceGroupList]
```

`RemoveAllMembers`

:   Value: 32

```
If set, all existing users can be removed from the particular
[IDeviceUserList]. If not set, at least one
user must be available in this group.
```

`EditRights`

:   Value: 64

```
If set, permissions for the particular [IDeviceGroup] can be changed
```

`Owner`

:   Value: 128

```
If set, the particular [IDeviceGroup] is the
owner group
```

`NameEditable`

:   Value: 256

```
If set, the name of the particular [IDeviceUser] or [IDeviceGroup] is editable.
```

`All`

:   Value: 4294967167

```
All flags together except flag Owner
```

## DiagType

Base: enum.Enum

Describes the function of a parameter in respect to module diagnosis.

`None`

:   Value: 0

```
No diagnostic meaning
```

`Diagnosis`

:   Value: 1

```
Provides the diagnostic message
```

`Acknowledge`

:   Value: 2

```
Acknowledge for current diagnostic message
```

## DirectIoAccessObstacles

Base: enum.Enum

This enum shows the obstacles which prevent the Direct IO access from
taking place.

`None`

:   Value: 0

```
Direct I/O access is possible.
```

`OldCompilerVersion`

:   Value: 1

```
The compiler version is to old.
```

`TargetSettingSeparateApplication`

:   Value: 2

```
The symbol configuration is configured as a child object.
```

## DutType

Base: enum.Enum

Defines the type of the DUT which is to be created.

`Structure`

:   Value: 1

```
A structure.
```

`Enumeration`

:   Value: 2

```
An enumeration.
```

`Alias`

:   Value: 3

```
An alias.
```

`Union`

:   Value: 4

```
An union.
```

`EnumerationWithTextList`

:   Value: 5

```
An enumeration with integrated text list support.
```

## ImageLinkType

Base: enum.Enum

This enumeration represents the way an image is embedded or linked
into a project.

`Linked`

:   Value: 0

```
This value means that the image is linked from the project only.
```

`EmbeddedAndLinked`

:   Value: 1

```
This value means that the image is embedded within the project
while still linked to the according file in the filesystem and
thus allowing automatic updates if changed on disk.
```

`Embedded`

:   Value: 2

```
This value means that the image is embedded within the project.
```

## KindOfTask

Base: enum.Enum

`Cyclic`

:   Value: 1

`Freewheeling`

:   Value: 2

`Event`

:   Value: 3

`ExternalEvent`

:   Value: 4

`Status`

:   Value: 5

`ParentSynchron`

:   Value: 6

## NativeImportResolve

Base: enum.Enum

How to resolve a conflict.

`replace`

:   Value: 1

```
Replace the object.
```

`skip`

:   Value: 2

```
Skip the object.
```

`cancel`

:   Value: 3

```
Cancel the import.
```

## NativeImportResult

Base: enum.Enum

Enum für das Ergebnis eines Importvorgangs.

`no_changes`

:   Value: 1

```
The import did not change anything at all.
```

`ok`

:   Value: 2

```
The import was okay.
```

`skipped`

:   Value: 3

```
The import skipped some entries.
```

`errors`

:   Value: 4

```
Errors happened during the import.
```

## ObjectPermissionKind

Base: enum.Enum

This enumeration contains the various possibilites to access an object
from the viewpoint of the User Management.

`View`

:   Value: 0

```
The permission to view an object.
```

`Modify`

:   Value: 1

```
The permission to modify an object.
```

`Remove`

:   Value: 2

```
The permission to remove an object.
```

`AddRemoveChildren`

:   Value: 3

```
The permission to add or remove a child to or from an object.
```

## OnlineChangeOption

Base: enum.Enum

Online change options used for multiple download.

`Never`

:   Value: 0

```
Online change shall never be performed. In that case a full
download is forced.
```

`Try`

:   Value: 1

```
Online change shall be tried. If not possible, a full download
shall be performed.
```

`Force`

:   Value: 2

```
Online change shall be forced. If not possible, the action is
terminated with no change.
```

## OperatingState

Base: enum.Enum

The global state of an application. Although not defined as such, this
enumeration is treated like a flags field, so the effective value may
be a combination of more of these values.

`none`

:   Value: 0

```
No application loaded.
```

`program_loaded`

:   Value: 1

```
Program code is loaded (ready to execute)
```

`download`

:   Value: 2

```
A download is in progress.
```

`online_change`

:   Value: 4

```
Performing an online change.
```

`store_bootproject`

:   Value: 8

```
Storing the bootproject.
```

`force_active`

:   Value: 16

```
There are currently forced values for this application.
```

`exception`

:   Value: 32

```
Application stopped since an exception occurred. A reset is
required to restart the application.
```

`run_after_download`

:   Value: 64

```
Download code at the end of download is in progress
(initialization of the application)
```

`store_bootproject_only`

:   Value: 128

```
Only the bootproject is stored at download
```

`exit`

:   Value: 256

```
Application exit is still executed (application is no longer
active)
```

`delete`

:   Value: 512

```
Application is deleted (object is available, but the content is
stil deleted)
```

`reset`

:   Value: 1024

```
Application reset is in progress
```

`retain_mismatch`

:   Value: 2048

```
Retain mismatch occurred during loading the bootproject (retain
data does not match to the application)
```

`bootproject_valid`

:   Value: 4096

```
Bootproject available (bootproject matched to running application
in RAM)
```

`load_bootproject`

:   Value: 8192

```
Loading bootproject in progress
```

`flow_active`

:   Value: 16384

```
flow control is active
```

`run_in_flash`

:   Value: 32768

```
Application is running in flash only
```

`core_dump_loaded`

:   Value: 131072

```
A Core-Dump for this application is loaded
```

`executionpoints_active`

:   Value: 262144

```
there are Executionpoints active in the application
```

`core_dump_creating`

:   Value: 524288

```
there are Executionpoints active in the application
```

## ParamType

Base: enum.Enum

Enumeration defining allowed types for a gateway parameter. The types
match the equally named .NET types.

`SByte`

:   Value: 17

```
8 bit signed byte
```

`Byte`

:   Value: 18

```
Unsigned byte (8 bit)
```

`Int16`

:   Value: 19

```
16 bit signed integer
```

`UInt16`

:   Value: 20

```
16 bit unsigned integer
```

`Int32`

:   Value: 21

```
32 bit signed integer
```

`UInt32`

:   Value: 22

```
32 bit unsigned integer
```

`Int64`

:   Value: 23

```
64 bit signed integer
```

`UInt64`

:   Value: 24

```
64 bit unsigned integer
```

`Char`

:   Value: 25

```
A single character
```

`Single`

:   Value: 26

```
Single precission FloatingPoint value
```

`Double`

:   Value: 27

```
Double precission FloatingPoint value
```

`Boolean`

:   Value: 28

```
Boolean value (true or false)
```

`StringAnsi`

:   Value: 29

```
ASCII coded string
```

`StringUnicode`

:   Value: 30

```
Unicode coded string.
```

## PermissionState

Base: enum.Enum

The permission state, either "granted", "denied", or "default".

`Granted`

:   Value: 0

```
The corresponding permission is explicitely granted to a certain
group.
```

`Denied`

:   Value: 1

```
The corresponding permission is explicitely denied to a certain
group.
```

`Default`

:   Value: 2

```
The corresponding permission is not explicitely set for a certain
group.
```

## PouType

Base: enum.Enum

Defines the type of the POU which is to be created.

`Program`

:   Value: 1

```
A program.
```

`FunctionBlock`

:   Value: 2

```
A function block.
```

`Function`

:   Value: 3

```
A function.
```

## PromptChoice

Base: enum.Enum

This enumeration denotes possible prompt options for
\[IMessageService\] methods.

`OK`

:   Value: 0

```
The user can choose "OK".
```

`OKCancel`

:   Value: 1

```
The user can choose "OK" or "Cancel".
```

`YesNo`

:   Value: 2

```
The user can choose "Yes" and "No".
```

`YesNoCancel`

:   Value: 3

```
The user can choose "Yes", "No", and "Cancel".
```

`RetryCancel`

:   Value: 4

```
The user can choose "Retry" or "Cancel".
```

`AbortRetryIgnore`

:   Value: 5

```
The user can choose "Abort", "Retry", and "Ignore".
```

## PromptHandling

Base: enum.Enum

Definition flags for prompt handling. Prompts are standard dialog
boxes issued by plugins to inform or query the user.

:::
Note

Simple prompts are those which have only a single button (like a
single OK button) and don't leave any choices to the user. Simple
prompt handling also applies to prompts with or without message keys,
but prompts actually caught by message keys defined in
\[ISystem.prompt_answers\] are not subject to
simple prompt handling.

This enum may be extended in future releases.

Currently, all handling choices are cumulative, so you can set
\[PromptHandling.ForwardSimplePrompts\] and
\[PromptHandling.LogSimplePrompts\] at the same
time.
:::

`None`

:   Value: 0

```
None of the flags are set. This implies that "simple" prompts are
silently suppressed.
```

`ForwardSimplePrompts`

:   Value: 1

```
Handle simple prompts in their original way. Usually, this means,
the user is queried with a dialog box. (However, other plugins may
modify that behaviour.) This flag is set by default in UI mode. If
you disable this flag, simple promts are not processed in any way.
```

`LogSimplePrompts`

:   Value: 2

```
Print simple prompts as a log message, similar to
[ISystem.write_message]. Log the prompts to
the message view with appropriate priority. This is set by default
in Non-UI mode.
```

`EnableTextPrompts`

:   Value: 4

```
Enables a basic text mode message service implementation in --noUI
mode. By default, this flag is not set for compatibility reasons
with old scripts, and it is ignored if [ISystem.ui_present] is true.

:::
Note

If this flag is not set, all MessageServicePrompts which ought to
query the user simply return the default value, while
[IScriptUI.open_file_dialog],
[IScriptUI.save_file_dialog],
[IScriptUI.browse_directory_dialog],
[IScriptUI.query_string],
[IScriptUI.query_password] and
[IScriptUI.query_credentials] simply pop up
the standard graphical dialogs.
:::
```

`ProcessScriptPrompts`

:   Value: 8

```
If this flag is set, prompts issued by the Script itself via
[ISystem.ui] are also subject to the
[ISystem.prompt_handling]and
[ISystem.prompt_answers] processing /
filtering. This flag is not set by default.
```

`LogMessageKeys`

:   Value: 16

```
Logs all MessageService calls with their message key to the
message store. Use this to catch the message keys you need for
[ISystem.prompt_answers].

:::
Note

Calls without a message key are logged with the key "\<\<No
Key\>\>", calls which got passed None as message key are logged
with "\<\<None\>\>"
:::
```

## PromptResult

Base: enum.Enum

This enumeration denotes possible prompt results from
\[IMessageService\]methods.

`OK`

:   Value: 0

```
The user has selected "OK".
```

`Cancel`

:   Value: 1

```
The user has selected "Cancel".
```

`Yes`

:   Value: 2

```
The user has selected "Yes".
```

`No`

:   Value: 3

```
The user has selected "No".
```

`Retry`

:   Value: 4

```
The user has selected "Retry".
```

`Abort`

:   Value: 5

```
The user has selected "Abort".
```

`Ignore`

:   Value: 6

```
The user has selected "Ignored".
```

## ReferenceMode

Base: enum.Enum

`Link`

:   Value: 0

`LinkAndEmbed`

:   Value: 1

`Embed`

:   Value: 2

## ResetOption

Base: enum.Enum

This enum defines the different kinds of reset (warm, cold, origin)

`Warm`

:   Value: 0

```
Warm reset of the application - keep retain variables.
```

`Cold`

:   Value: 1

```
"Cold" reset - keep persistent variables and applications
```

`Original`

:   Value: 2

```
Reset "original" - erase all variables, applications, etc.
```

## Severity

Base: enum.Enum

Describes the severity of an \[IMessage\].

`FatalError`

:   Value: 1

```
Indicates that the corresponding message is a fatal error.
```

`Error`

:   Value: 2

```
Indicates that the corresponding message is an error.
```

`Warning`

:   Value: 4

```
Indicates that the corresponding message is a warning.
```

`Information`

:   Value: 8

```
Indicates that the corresponding message is an information.
```

`Text`

:   Value: 16

```
Indicates that the corresponding message is an informational text
without corresponding source code position.
```

## StopResetBehaviour

Base: enum.Enum

`KeepCurrentValues`

:   Value: 0

```
The outputs kepp the last current values
```

`SetToDefault`

:   Value: 1

```
The outputs are set to the default values
```

`ExecuteProgram`

:   Value: 2

```
A user defined program is executed
```

## SymbolAccess

Base: enum.Enum

Describing the access rights of a symbol config node.

:::
Note

The order of the elements and the numeric values between None and
ReadWrite must not be changed because it is accessed with the numeric
values. Its members must be synchronized with the AccessRights enum in
the IecVarAccess2_Itfs.library. Its values must not use more than 8
bit because it's stored in a byte in the SymbolicVarsBase.library. For
historical reasons, this enum is not marked with the
\[FlagsAttribute\], but the bit patterns are
defined in a way which allows bitwise ORing and ANDing of
\[SymbolAccess.Read\], \[SymbolAccess.Write\]and \[SymbolAccess.Execute\].
:::

`None`

:   Value: 0

```
No access permitted.
```

`Read`

:   Value: 1

```
Read access permitted.
```

`Write`

:   Value: 2

```
Write access permitted.
```

`ReadWrite`

:   Value: 3

```
Read and write access permitted.

:::
Note

This value happens to be the bitwise or of
[SymbolAccess.Read] and
[SymbolAccess.Write], althought this enum is
currently not marked with the [FlagsAttribute] for backwards compatibility reasons.
:::
```

`Void`

:   Value: 4

```
Unspecified access (fall back to the default values).

:::
Note

This value is currently not defined in the runtime, as it's only
used in the configuration settings.
:::
```

`Execute`

:   Value: 8

```
Future extension: Execute access (for methods, FBs, Functions).
(not yet supported in V3.5 SP9)
```

`ReadExecute`

:   Value: 9

```
Future extension: Combination of read / execute. (not yet
supported in V3.5 SP9)
```

`WriteExecute`

:   Value: 10

```
Future extension: Combination of write / execute. (not yet
supported in V3.5 SP9)
```

`ReadWriteExecute`

:   Value: 11

```
Future extension: Combination of read / write / execute. (not yet
supported in V3.5 SP9)
```

## SymbolAttributeFilterTypes

Base: enum.Enum

Definition of the attribute matching type

`None`

:   Value: 0

```
No attributes or not configured.
```

`All`

:   Value: 1

```
All attributes are included.
```

`SimpleIdentifiers`

:   Value: 2

```
Match all simple identifiers without fullstop (non-hierarchical
attributes).

:::
Note

This is mainly here for backwards compatibility.
:::
```

`Prefix`

:   Value: 3

```
Prefix matching of attributes
```

`Regex`

:   Value: 4

```
Regex matching of attributes
```

## SymbolCommentFilterType

Base: enum.Enum

Defines which comments are included in the XML file or symbol tables.

`None`

:   Value: 0

```
No comments are included at all, or not configured.
```

`NormalComments`

:   Value: 1

```
Only normal comments are included, those delimited with // or
(\\\* \\\*).
```

`DocuComments`

:   Value: 2

```
Only docu comments are included, those delimited with ///.
```

`Both`

:   Value: 3

`PreferNormalComments`

:   Value: 4

```
Prefer the normal comments, docu comment is used when no normal
comment is there.

:::
Note

This implies [SymbolCommentFilterType.NormalComments] and [SymbolCommentFilterType.DocuComments].
:::
```

`PreferDocuComments`

:   Value: 5

## SymbolConfigContentFeatureFlags

Base: enum.Enum

The feature flags describing the contents of the symbol tables and XML
files. (Introduced in V3.5.8.30, more broadly supported in V3.5.9.0.)

`None`

:   Value: 0

```
Nothing configured.
```

`SupportOPCUA`

:   Value: 1

```
Support OPC UA features (flag supported since V3.5.8.30). This is
equal to the [ISymbolConfigObject6.SupportOPCUA] property.

:::
Note

This is required for
[SymbolConfigContentFeatureFlags.IncludeComments],
[SymbolConfigContentFeatureFlags.IncludeAttributes] and
[SymbolConfigContentFeatureFlags.IncludeTypeNodeAttributes]. In compiler versions V3.5.5.0 to V3.5.7.X, this
implied [SymbolConfigContentFeatureFlags.IncludeAttributes] with a filter matching only single IEC identifiers.
In compiler versions V3.5.8.X, this implied
[SymbolConfigContentFeatureFlags.IncludeAttributes] with a filter matching IEC identifier pathes (e. G.
foo.bar.baz).
:::
```

`IncludeComments`

:   Value: 2

```
Include comments (flag supported since V3.5.9.0).
```

`IncludeAttributes`

:   Value: 4

```
Include attributes (flag supported since V3.5.9.0).
```

`IncludeTypeNodeAttributes`

:   Value: 8

```
Also include comments / attributes for type nodes (flag supported
since V3.5.9.0).
```

`IncludeExecutables`

:   Value: 16

```
Future extension: Inclusion of executable members (flag not yet
supported in V3.5.9.0, allows calling of programs, functions, FBs
and methods, requires OPC UA).

:::
Note

If this flag is set, the list of available signatures will also
include callables.
:::
```

`MaskRuntime`

:   Value: 65535

```
The runtime feature bit mask (also relevant for CRC calculation).
```

`XmlIncludeNodeFlags`

:   Value: 65536

```
Include the node flags in the XML file (flag supported since
V3.5.8.30).

:::
Note

This was implied in compiler version V3.5.8.0, and is configurable
using this flag since V3.5.8.30 due to backwards compatibility
problems with various XML parsers.
:::
```

`XmlIncludeComments`

:   Value: 131072

```
Include comments in the XML file (flag supported since V3.5.8.30),
equal to [ISymbolConfigObject5.ExportCommentsInXML] flag.

:::
Note

In compiler versions 3.5.5.X to 3.5.8.X, this implied
[SymbolCommentFilterType.PreferDocuComments].
:::
```

`XmlIncludeAttributes`

:   Value: 262144

```
Include the attributes in XML (flag supported since V3.5.9.0).
```

`XmlIncludeTypeNodeAttributes`

:   Value: 524288

```
Also include comments / attributes for type nodes (flag supported
since V3.5.9.0).
```

`XmlIncludeExecutables`

:   Value: 1048576

```
Future extension: Inclusion of executable members (flag not yet
supported in V3.5.9.0, allows calling of programs, functions, FBs
and methods, requires OPC UA).

:::
Note

This requires
[SymbolConfigContentFeatureFlags.IncludeExecutables] to be active - settingt his flag to false allows to
suppress the executables in the for backwards compatibility.
:::
```

`MaskXml`

:   Value: 4294901760

```
The XML feature bit mask (not relevant for CRC calculation).
```

## VersionUpdateFlags

Base: enum.Enum

Flags for the
\[IVersionCompatibilityManager2.SetVersionUpdateFlags\]method.

`Regular`

:   Value: 0

```
The [IVersionCompatibilityManager] checks for
updates when opening a project and displays a related dialog for
the user to manually update the versions.
```

`NoUpdates`

:   Value: 1

```
The [IVersionCompatibilityManager] will not
check for updates when the next project will be opened. Therefore,
there will be no dialog.
```

`SilentMode`

:   Value: 2

```
Determines if a dialog for user interaction is shown or not. If
this flag is set, there will be no dialog.

:::
Note

This flag is often combined with one of the **Update\...** flags.
:::
```

`UpdateAllCustomProviders`

:   Value: 4

```
The [IVersionCompatibilityManager] will
automatically update all items to the newest available version
when the next project will be opened. To avoid a dialog, combine
this flag with the [VersionUpdateFlags.SilentMode] flag.
```

`UpdateLibraries`

:   Value: 8

```
The [IVersionCompatibilityManager] will
automatically update all libraries to the newest available version
when the next project will be opened. To avoid a dialog, combine
this flag with the [VersionUpdateFlags.SilentMode] flag.
```

`UpdateCompiler`

:   Value: 16

```
The [IVersionCompatibilityManager] will
automatically update the compiler version to the newest available
version when the next project will be opened. To avoid a dialog,
combine this flag with the [VersionUpdateFlags.SilentMode] flag.
```

`UpdateVisualisation`

:   Value: 32

```
The [IVersionCompatibilityManager] will
automatically update the visualisation profile to the newest
available version when the next project will be opened. To avoid a
dialog, combine this flag with the
[VersionUpdateFlags.SilentMode] flag.
```

`UpdateDevices`

:   Value: 64

```
The [IVersionCompatibilityManager] will
automatically update the device profile to the newest available
version when the next project will be opened. To avoid a dialog,
combine this flag with the [VersionUpdateFlags.SilentMode] flag.
```

`UpdateVisualisationStyles`

:   Value: 128

```
The [IVersionCompatibilityManager] will
automatically update the used visualization styles to the newest
available versions when the next project will be opened. To avoid
a dialog, combine this flag with the
[VersionUpdateFlags.SilentMode] flag.
```

`UpdateAll`

:   Value: 65532

```
The [IVersionCompatibilityManager] will
automatically update all items to the newest available version
when the next project will be opened. To avoid a dialog, combine
this flag with the [VersionUpdateFlags.SilentMode] flag.

:::
Note

Please note that this enum value sets all bits in the range of 2
to 15 to "1".
:::
```

# Interfaces

## ExportReporter

Base: object

python classes can implement their own export_xml reporter here. This
interface is exposed under the name ExportReporter.

`aborting`

:   This allows abortion when we report non-exportable objects.

`error`(*obj*, *message*)

:   This method is called when an error has occurred during
export_xml.

```
**Parameter**: obj (IScriptObject)
:   The obj which caused the error.

**Parameter**: message (str)
:   The message describing the problem.
```

`nonexportable`(*obj*)

:   This method is called when we find out that a given object is not
exportable. (This is only called for objects given directly as
parameters - non-exportable children are silently ignored.) The
script can decide to abort the export by setting aborting to true
during this phase.

```
:::
Note

This method will be called for all non-exportable objects even
when aborting is set to true. The flag will be checked after all
objects have been checked for exportability, just before the
actual export is going to start (and thus before the destination
file is opened). This allows scripts to find out about all
non-exportable objects in one run.
:::

**Parameter**: obj (IScriptObject)
:   The object which is not exportable
```

`warning`(*obj*, *message*)

:   This method is called when an warning has occurred during
export_xml.

```
**Parameter**: obj (IScriptObject)
:   The obj which caused the warning.

**Parameter**: message (str)
:   The message describing the problem.
```

## ILibCategory

Base: object

Information about a library category.

`default_name`

:   Gets the default name.

`guid`

:   Gets the guid identifying the category.

`localized_name`

:   Gets the localized name for the current UI culture.

`name`

:   Gets the localized name, or the default name if no localized name
is available.

`parent`

:   Gets the parent category, or None if the category is top level.

`version`

:   Gets the version.

## ILibRepository

Base: object

Description class for a library repository.

`editable`

:   Gets a value indicating whether this [ILibRepository](#ilibrepository) is editable. The
default system library repository is not editable - that means, it
cannot be removed from the list of repositories.

`name`

:   Gets the name of the repository.

`root_folder`

:   Gets the root folder of the repository.

## IManagedLib

Base: object

Description class for a managed library.

`categories`

:   Gets the categories (list of [ILibCategory](#ilibcategory)).

`company`

:   Gets the company.

`default_namespace`

:   Gets the default_namespace.

`dependencies`

:   Gets the dependencies as a list of \[String\]s.

`displayname`

:   Gets the displayname.

`title`

:   Gets the title.

`version`

:   Gets the version.

## IModuleId

Base: object

Unique identification for a module.

:::
Note

A module is a special type of device, that is only available within
the context of a certain device. The module is identified by the same
values as each owning device, with an additional module id, to
distinguish it from other modules of the same device.

Examples for modules are device local io modules and similar nodes.
:::

`id`

:   Id of the device. The format for this id is specified for each
type. The id is unique within the class of devices of one type.

`module_id`

:   Id of the module.

```
:::
Note

Id of the module. The format for this id is specified for each
type. The id is unique within the class of devices of one type.
:::
```

`type`

:   Type of the device.

`version`

:   The version of the device. The format for the version string is
specified for each type.

## IScriptApplication

Base: object

Extension interface of [IScriptApplication](#iscriptapplication) since V3.5.10.0.

`build`()

:   Builds the application.

```
:::
Note

You can use the [ISystem.get_messages] and
[ISystem.get_message_objects] calls to check
whether any messages were added.

This method only works for applications in the primary project.
:::
```

`clean`()

:   Cleans the application.

```
:::
Note

You can use the [ISystem.get_messages] and
[ISystem.get_message_objects] calls to check
whether any messages were added.

This method only works for applications in the primary project.
:::
```

`create_boot_application`(*output_filename*)

:   Creates the offline boot project at the specified outputpath.

```
**Parameter**: output_filename (str)
:   The filename to write the boot application to.

:::
Note

Relative output filenames are interpreted relative to the location
of the project. If you pass None or the empty string,
applicationname.app is used.

This method only works for applications in the primary project.
:::
```

`create_boot_application`(*output_filename*, *update_compile_info*, *write_visu_files*)

:   Creates the offline boot project at the specified outputpath.

```
**Parameter**: output_filename (str)
:   The filename to write the boot application to.

**Parameter**: update_compile_info (bool)
:   if set to **True**, also writes the compile information
    (compiler reference context) to the project directory. (This
    may break online change, see below). This parameter is
    optional, the default is false. (The compile information is
    updated in the directory where the project resides, not the
    output directory.)

**Parameter**: write_visu_files (bool)
:   if set to **True**, also writes the visualization files into
    the output directory. This parameter is optional, the default
    is false. It will be silently ignored when this application
    does not contain a visualization manager.

:::
Note

If the project was changed since the last download or online
change to a PLC, and you create a boot application with
**update_compile_info** set to **True**, this will overwrite the
current compiler reference context with the one matching the boot
project (which no longer matches the one on the PLC). Thus, a
direct conline change to the PLC will no longer work. On the other
hand, the reference context now matches the created boot
application, so you can login to any PLC on which you deploy the
generated boot application. This updated compile context is also
the one to be included into a project archive.

Relative output filenames are interpreted relative to the location
of the project. If you pass None or the empty string,
applicationname.app is used.

This method only works for applications in the primary project.
:::
```

`create_task_configuration`()

:   Add the task configuration object to an application.

```
**Returns**: (IScriptObject)
:   Script object of the task configuration object
```

`generate_code`()

:   Generates the code for the application.

```
:::
Note

You can use the [ISystem.get_messages] and
[ISystem.get_message_objects] calls to check
whether any messages were added.

This method only works for applications in the primary project.
:::
```

`is_active_application`

:   Gets a value indicating whether this [IScriptApplication](#iscriptapplication) is the
active application.

```
:::
Note

The active application is always in the primary project, so this
property will always return false for non-primary projects.
:::
```

`is_application`

:   Gets a value indicating whether this
[IScriptApplicationMarker](#iscriptapplicationmarker) is an
application.

`rebuild`()

:   Rebuilds the application.

```
:::
Note

You can use the [ISystem.get_messages] and
[ISystem.get_message_objects] calls to check
whether any messages were added.

This method only works for applications in the primary project.
:::
```

## IScriptApplicationMarker

Base: object

Marker object to check whether an IScriptObject is an application
object. (Since V3.5.2.0)

`is_application`

:   Gets a value indicating whether this
[IScriptApplicationMarker](#iscriptapplicationmarker) is an
application.

## IScriptApplicationSymbolConfigExtension

Base: object

Extension provider for IApplicationObject instances.

`create_symbol_config`(*export_comments_to_xml*, *support_opc_ua*, *client_side_layout_calculator*)

:   Add the symbol configuration object to an application.

```
**Parameter**: export_comments_to_xml (bool)

**Parameter**: support_opc_ua (bool)

**Parameter**: client_side_layout_calculator (Guid)

**Returns**: (IScriptObject)
:   Script object of the symbol config object
```

## IScriptClientSideLayoutCalculatorDescription

Base: object

Description of an client side layout calculator.

:::
Note

Currently, two different values are allowed: \[Guid.Empty\] to use the compatibility layout calculator which is always
available. And **Guid("{0141eb75-141b-4ea1-9a8c-75f952b22a6c}")** to
use the optimized layout calculator, which is new with V3.5.7.0 and
also requires the compiler version 3.5.7.0 (see
[http://jira.3s-software.com/browse/CDS-41816](http://jira.3s-software.com/browse/CDS-41816)). This scheme may be extended to allow more offset
calculators in the future.
:::

`description`

:   A longer description of the output layout calculator.

```
:::
Note

This may be shown in a tooltip, and should give some detailed
explanation of the calculator, and e. G. the conditions under
which the calculator is valid.
:::
```

`name`

:   The name of the output layout calculator - human readable and
localized.

`type_guid`

:   The unique ID of the output layout calculator.

## IScriptClientSideLayoutCalculatorDescriptionCollection

Base: object

Descriptions of the client side layout calculators.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`__len__`()

:   Gets the length (number of calculator descriptions).

```
**Returns**: (int)
:   The number of calculator descriptions.
```

## IScriptCommand

Base: object

Represents a CoDeSys command (Menu, Toolbar, Context Menu).

`description`

:   Gets the description for this command. This string is used as
statusbar text and usually is localized.

`guid`

:   Gets the GUID.

`name`

:   Gets the display text of this command. This string is used as menu
item label and usually is localized.

`tokens`

:   Gets the tokens which introduce a corresponding batch instruction.
For example, a batch command which opens a project file would
probably return the two tokens "file" and "open" here.

## IScriptCommands

Base: object

A sequence of all known Commands in CoDeSys.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

## IScriptConnector

Base: object

Extension interfaces for IScriptConnector since V3.5.6.0.

`additional_interfaces`

:   Gets the additional interfaces of the connector. This may be
useful to find out which child connector of the current parent
connector is actually valid.

`connector_id`

:   The unique connector id.

`connector_role`

:   Get whether this connector is a parent or child connector.

`get_device_object`()

:   Get an instance of the device object this connector belongs to.

```
**Returns**: (IScriptObject)
:   Returns the device object
```

`host_parameters`

:   Get the host parameter set of this connector.

```
:::
Note

The returned list is read-only which means you can't add, insert
or remove parameters or clear it. The list of available parameters
is defined in the device description.
:::
```

`host_path`

:   Get the id of the next connector towards the host. **-1**, if the
attached device is the controlling host.

`interface`

:   The unique typename of a connector, eg. "Common.PCI". A parent
connector may be connected to a child connector, if this connector
type matches.

`interface_name`

:   Get an internationalized version of the interface name for
presentation purposes.

`is_explicit`

:   Get whether a separate node should be shown in the user interface
for this connector.

`module_type`

:   Id of the connector. This id is used by the driver on the runtime
system.

```
:::
Note

The Id's of matching parent and child connectors are different.
Therefore in order to find a matching device for a given parent
connector use the [('Unknown', u'ConnectorType')]Property instead.
:::
```

## IScriptDataElement

Base: object

Extension to [IScriptDataElement](#iscriptdataelement) since V3.5.8.0.

`bit_size`

:   Get the size of this parameters value in bits.

`can_access_online`

:   Gets a value indicating whether this [IScriptDataElement](#iscriptdataelement) can be read
online.

```
:::
Note

If this is true, the element additionally implements
[IScriptValueDataElement].
:::
```

`description`

:   Internationalized description of the data element.

`has_sub_elements`

:   Get information whether this element is a compound type.

```
:::
Note

True for structs, arrays, bitfields, \... - in this case, the
element implements [IScriptCompoundDataElement]. If this is False, the element implements
IScriptPrimitiveTypeDataElement. The properties
[IScriptDataElement.is_enumeration] and
[IScriptDataElement.has_sub_elements] are
mutually exclusive, only one of them can be true at the same time.
:::
```

`identifier`

:   Unique identifier of this data element within it's parent element.

`io_mapping`

:   Gets the io mapping of this data element.

`is_enumeration`

:   True if this element is defined as an enumeration. It then also
implements \[IScriptEnumerationDataElement\].

```
:::
Note

The properties [IScriptDataElement.is_enumeration] and [IScriptDataElement.has_sub_elements] are mutually exclusive, only one of them can be true at
the same time.
:::
```

`is_mappable_io`

:   Gets a value indicating whether this [IScriptDataElement](#iscriptdataelement) is a
mappable input or output.

`is_range_type`

:   True, if the elements value must be within a certain range.

```
:::
Note

If this is true, the element implements the
[IScriptRangeDataElement] interface.
:::
```

`is_union`

:   Gets a value indicating whether this [IScriptDataElement](#iscriptdataelement) is an union.

`parameter`

:   Gets the parameter defining this data element. (This will return
the same instance if called on the [IScriptDeviceParameter](#iscriptdeviceparameter).

`parent`

:   Gets the parent.

```
:::
Note

This property returns either the parent [IScriptDataElement](#iscriptdataelement) (which may
be the [IScriptDeviceParameter](#iscriptdeviceparameter)), or the
[IScriptDeviceParameterSet](#iscriptdeviceparameterset) if
the current element is the device parameter.
:::
```

`unit`

:   Internationalized unit of the data element. To be used by the
presentation layer.

`user_comment`

:   Get or set a user specified comment.

`visible_name`

:   Internationalized name of the data element (this is the name used
in the user interface).

## IScriptDeviceCategory

Base: object

Category of devices.

:::
Note

Devices can be grouped into categories by means of the
**DeviceDescription/Device/DeviceInfo/Category** tags of the device
description file. One can implement a corresponding class of this
interface to display these types in a user-friendly way.
:::

`category_id`

:   Id of the category.

`description`

:   Gets a user-friendly description for this device category. This
string should be localized.

`name`

:   Gets a user-friendly display name for this device category. This
string should be localized.

`parent_category`

:   The type GUID of the parent device category implementation, or
**Guid.Empty**, if this device implementation is top-level.

## IScriptDeviceCollection

Base: object

A collection of [IScriptDeviceDescription](#iscriptdevicedescription) objects.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`__len__`()

:   Gets the length (number of device descriptions).

```
**Returns**: (int)
:   The number of device descriptions.
```

`get_devices_of_vendor`(*vendor*)

:   Get all devices in the list which match the specified vendor.

```
**Parameter**: vendor (str)
:   Vendor name.

**Returns**: (IScriptDeviceCollection)
:   A collection of devices from one vendor.
```

`vendors`

:   Get the list of all vendors in the collection.

## IScriptDeviceDescription

Base: object

Description of a device.

`device_id`

:   Get the identification object of the device.

`device_info`

:   Get information about the device.

## IScriptDeviceFamily

Base: object

Device family.

`description`

:   Description of the family.

`family_id`

:   Family Id.

`name`

:   Family name.

`parent_family`

:

`sub_families`

:   Sub families of the family.

## IScriptDeviceInfo

Base: object

Provides information about a device.

`categories`

:   Gets a list of categories this device belongs to.

`custom`

:   Get vendor specific information for the device.

```
:::
Note

This property may contain all kinds of information not defined by
the specification, structured as an XML-Fragment with root node
"Custom".
:::

Example:
:   \<Custom\>\<MaxTemp\>30\</MaxTemp\>\</Custom\>
```

`default_instance_name`

:

`description`

:   Internationalized description for the device

`families`

:   Gets a list of vendor-specific families this device belongs to.
Each string has got the format **VendorId:FamilyId**.

`name`

:   Internationalized name of the device

`order_number`

:   Vendor specific ordernumber for this device.

`vendor`

:   Internationalized name of the device

## IScriptDeviceObject

Base: object

Extension interface for device objects since V3.5.10.0

`add`(*name*, *device*, *module*)

:   Adds the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`add`(*name*, *type*, *id*, *version*, *module*)

:   Adds the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`allow_symbolic_var_access_in_sync_with_iec_cycle`

:   Property used by the symbol configuration to determine if symbolic
variable access is allowed to be synchronized with the IEC cycle.
The default is **False** and should be kept for most use cases.
Setting this to **True** may increase the jitter for all
applications running on the device because the task accessing the
variables may block other tasks.

```
:::
Note

The device object has to support IDeviceObject15 to access the
value.
:::
```

`allowed_interfaces_at`(*index*)

:   Get the name of the child interfaces that this device object can
accept at the specified insert position.

```
**Parameter**: index (int)
:   The child index where a device should be inserted.

**Returns**: (list)
:   A list of possible interface names or null if no device can be
    inserted at that position.
```

`connectors`

:   Gets the connectors.

`device_parameters`

:   Gets the set of device parameters.

```
:::
Note

Since V3.5.8.0, this actually is a
[IScriptMappableDeviceParameterSet].
:::
```

`disable`()

:   Marks this device as disabled during download.

`driver_info`

:   Get the driver info of the device.

`enable`()

:   Marks this device as enabled during download.

`export_io_mappings_as_csv`(*file_path*)

:   Export the io mappings as a CSV file to the specified absolute
path.

```
**Parameter**: file_path (str)
:   The absolute path of the file to export.
```

`get_address`()

:   Gets the address of the device.

```
**Returns**: (str)
:   The device address in the bus independent CODESYS format.

:::
Note

**See also:**
[IScriptDeviceObject.get_device_communication_settings]
:::
```

`get_device_communication_settings`()

:   Reads the communication settings of the device.

`get_device_identification`()

:   Gets the device identification.

```
**Returns**: (IDeviceId)
:   The device identification object.
```

`get_gateway`()

:   Gets the gateway.

```
**Returns**: (Guid)
:   The guid of the Gateway.

:::
Note

**See also:**
[IScriptDeviceObject.get_device_communication_settings]
:::
```

`get_module_identification`()

:   Returns the unique identification of a module.

```
:::
Note

A module is a special type of device, that is only available
within the context of a certain device. The module is identified
by the same values as each owning device, with an additional
module id, to distinguish it from other modules of the same
device.

Examples for modules are device local io modules and similar
nodes.
:::

**Returns**: (str)
:   The module identification, or an empty string if this module
    has no module identification.
```

`get_simulation_mode`()

:   Gets the simulation mode.

```
**Returns**: (bool)
:   True if simulation is enabled.
```

`import_io_mappings_from_csv`(*file_path*)

:   Imports the io mappings from a CSV file at the specified absolute
path.

```
**Parameter**: file_path (str)
:   The absolute path of the file to export.
```

`insert`(*name*, *index*, *device*, *module*)

:   Inserts the specified device at the specified index.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: index (int)
:   index where to insert the device.

**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`insert`(*name*, *index*, *type*, *id*, *version*, *module*)

:   Inserts the specified device at the specified index.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: index (int)
:   index where to insert the device.

**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`is_device`

:   Gets a value indicating whether this instance is a device object.

`is_enabled`()

:   Determines whether this instance is enabled during download.

```
**Returns**: (bool)
:   **True** if this instance is enabled during download;
    otherwise, **False**.
```

`plug`(*name*, *device*, *module*)

:   Plugs the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`plug`(*name*, *type*, *id*, *version*, *module*)

:   Plugs the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`set_gateway_and_address`(*gateway*, *address*)

:   Sets the gateway and address.

```
**Parameter**: gateway (Guid)
:   The gateway Guid.

**Parameter**: address (str)
:   The address in the bus independent CODESYS format.

:::
Note

If you pass the emty guid and an empty address, the gateway
address will be cleared. You can use one of the overloads
[IScriptGateway.find_address_by_ip] or
[IScriptGateway.find_address_by_ip] to search
the CODESYS address when you know the ip address or hostname.
:::
```

`set_gateway_and_address`(*gateway*, *address*)

:   Sets the gateway and address.

```
**Parameter**: gateway (IScriptGateway)
:   The gateway.

**Parameter**: address (str)
:   The address in the bus independent CODESYS format.

:::
Note

If you pass null as gateway an empty address, the gateway address
will be cleared. You can use one of the overloads
[IScriptGateway.find_address_by_ip] or
[IScriptGateway.find_address_by_ip] to search
the CODESYS address when you know the ip address or hostname.
:::
```

`set_gateway_and_address`(*stGateway*, *address*)

:   Sets the gateway and address.

```
**Parameter**: stGateway (str)
:   The gateway Guid (string representation), or (since V3.5.8.0)
    the name of the gateway, if unique.

**Parameter**: address (str)
:   The address in the bus independent CODESYS format.

:::
Note

If you pass None or empty Strings for both parameters (or the
empty guid), the gateway and address will be cleared. You can use
one of the overloads [IScriptGateway.find_address_by_ip] or [IScriptGateway.find_address_by_ip] to search the CODESYS address when you know the ip
address or hostname.
:::

**Exception**: InvalidOperationException
:   If several gateways have the same name, an exception is
    thrown.
```

`set_gateway_and_device_name`(*gateway_guid*, *device_name*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway_guid (Guid)
:   The gateway guid .

**Parameter**: device_name (str)
:   The device name.

:::
Note

If you pass the emty guid and an empty address, the gateway
address will be cleared. The device will be tracked by its device
name - when trying to go online, a quick online scan will be made
and the first device with the given name will be selected.
:::
```

`set_gateway_and_device_name`(*gateway*, *device_name*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (IScriptGateway)
:   The gateway.

**Parameter**: device_name (str)
:   The device name.

:::
Note

If you pass the emty guid and an empty address, the gateway
address will be cleared. The device will be tracked by its device
name - when trying to go online, a quick online scan will be made
and the first device with the given name will be selected.
:::
```

`set_gateway_and_device_name`(*gateway*, *device_name*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (str)
:   The gateway guid (as string) or name.

**Parameter**: device_name (str)
:   The device name.

:::
Note

If you pass the emty guid and an empty address, the gateway
address will be cleared. The device will be tracked by its device
name - when trying to go online, a quick online scan will be made
and the first device with the given name will be selected.
:::

**Exception**: InvalidOperationException
:   If several gateways have the same name, an exception is
    thrown.
```

`set_gateway_and_ip_address`(*gateway_guid*, *ip_address*, *port*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway_guid (Guid)
:   The gateway.

**Parameter**: ip_address (System.Net.IPAddress)
:   The ip address.

**Parameter**: port (int)
:   The port (if you omit the port, the default of 11740 will be
    used).

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::
```

`set_gateway_and_ip_address`(*gateway_guid*, *ip_address*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway_guid (Guid)
:   The gateway.

**Parameter**: ip_address (str)
:   The ip address as a string (e. G. "127.0.0.1"), and optionally
    the port separated with a colon (e. G. "127.0.0.1:11740") if
    you don't want the default value of 11740.

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::
```

`set_gateway_and_ip_address`(*gateway_guid*, *ip_address*, *port*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway_guid (Guid)
:   The gateway.

**Parameter**: ip_address (str)
:   The ip address as a string (e. G. "127.0.0.1").

**Parameter**: port (int)
:   The port (if you don't use the default of 11740).

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::
```

`set_gateway_and_ip_address`(*gateway*, *ip_address*, *port*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (IScriptGateway)
:   The gateway.

**Parameter**: ip_address (System.Net.IPAddress)
:   The ip address.

**Parameter**: port (int)
:   The port (if you omit the port, the default of 11740 will be
    used).

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::
```

`set_gateway_and_ip_address`(*gateway*, *ip_address*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (IScriptGateway)
:   The gateway.

**Parameter**: ip_address (str)
:   The ip address as a string (e. G. "127.0.0.1"), and optionally
    the port separated with a colon (e. G. "127.0.0.1:11740") if
    you don't want the default value of 11740.

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::
```

`set_gateway_and_ip_address`(*gateway*, *ip_address*, *port*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (IScriptGateway)
:   The gateway.

**Parameter**: ip_address (str)
:   The ip address as a string (e. G. "127.0.0.1").

**Parameter**: port (int)
:   The port (if you don't use the default of 11740).

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::
```

`set_gateway_and_ip_address`(*gateway*, *ip_address*, *port*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (str)
:   The gateway guid (as string) or name.

**Parameter**: ip_address (System.Net.IPAddress)
:   The ip address.

**Parameter**: port (int)
:   The port (if you omit the port, the default of 11740 will be
    used).

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::

**Exception**: InvalidOperationException
:   If several gateways have the same name, an exception is
    thrown.
```

`set_gateway_and_ip_address`(*gateway*, *ip_address*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (str)
:   The gateway guid (as string) or name.

**Parameter**: ip_address (str)
:   The ip address as a string (e. G. "127.0.0.1"), and optionally
    the port separated with a colon (e. G. "127.0.0.1:11740") if
    you don't want the default value of 11740.

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::

**Exception**: InvalidOperationException
:   If several gateways have the same name, an exception is
    thrown.
```

`set_gateway_and_ip_address`(*gateway*, *ip_address*, *port*)

:   Sets the gateway and device name for communicaiton.

```
**Parameter**: gateway (str)
:   The gateway guid (as string) or name.

**Parameter**: ip_address (str)
:   The ip address as a string (e. G. "127.0.0.1").

**Parameter**: port (int)
:   The port (if you don't use the default of 11740).

:::
Note

If you pass the emty guid and a null address, the gateway address
will be cleared. The device will be tracked by its ip address -
when trying to go online, a quick online scan will be made to
check for the device with the given ip and port.
:::

**Exception**: InvalidOperationException
:   If several gateways have the same name, an exception is
    thrown.
```

`set_simulation_mode`(*simulation*)

:   Sets the simulation mode.

```
**Parameter**: simulation (bool)
:   if set to **True**, simulation is enabled.
```

`unplug`()

:   Unplugs the specified device.

`update`(*device*, *module*)

:   Updates the specified device.

```
**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`update`(*type*, *id*, *version*, *module*)

:   Updates the specified device.

```
**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

## IScriptDeviceObjectMarker

Base: object

Every IScriptObject instance will be extended with this method.

This interface is exported to python, and thus adheres to python
naming standards.

`is_device`

:   Gets a value indicating whether this instance is a device object.

## IScriptDeviceParameter

Base: object

A device parameter.

:::
Note

This interface is exported to python, and thus adheres to python
naming standards.
:::

`bit_size`

:   Get the size of this parameters value in bits.

`can_access_online`

:   Gets a value indicating whether this [IScriptDataElement](#iscriptdataelement) can be read
online.

```
:::
Note

If this is true, the element additionally implements
[IScriptValueDataElement].
:::
```

`channel_type`

:   If this parameter represents an IO channel, returns whether it is
an input or an output channel. Otherwise this property returns
\[ChannelType.None\]

`description`

:   Internationalized description of the data element.

`diagnostic_type`

:   Get or set the diagnostic type of this parameter.

`downloaded_with_ioconfig`

:   Get whether this parameter will be downloaded with the IO-Config

`get_device_object`()

:   Gets the device object associated with this parameter.

`has_sub_elements`

:   Get information whether this element is a compound type.

```
:::
Note

True for structs, arrays, bitfields, \... - in this case, the
element implements [IScriptCompoundDataElement]. If this is False, the element implements
IScriptPrimitiveTypeDataElement. The properties
[IScriptDataElement.is_enumeration] and
[IScriptDataElement.has_sub_elements] are
mutually exclusive, only one of them can be true at the same time.
:::
```

`id`

:   Each parameter has a unique id within it's parameter list. This is
also returned as the identifier in the underlying IDataElement.

`identifier`

:   Unique identifier of this data element within it's parent element.

`iec_type`

:   Gets the iec type of this parameter, or None if none is defined.

`is_enumeration`

:   True if this element is defined as an enumeration. It then also
implements \[IScriptEnumerationDataElement\].

```
:::
Note

The properties [IScriptDataElement.is_enumeration] and [IScriptDataElement.has_sub_elements] are mutually exclusive, only one of them can be true at
the same time.
:::
```

`is_range_type`

:   True, if the elements value must be within a certain range.

```
:::
Note

If this is true, the element implements the
[IScriptRangeDataElement] interface.
:::
```

`is_union`

:   Gets a value indicating whether this [IScriptDataElement](#iscriptdataelement) is an union.

`name`

:   Internationalized name of the data element. To be used by the
presentation layer.

`offline_access_rights`

:   Get the allowed access to this parameter in offline mode

```
**Returns**:
:   The allowed access on this parameter.
```

`online_access_rights`

:   Get the allowed access to this parameter in online mode

```
**Returns**:
:   The allowed access on this parameter.
```

`param_type`

:   get information about the original paramtype (e.g. "std:uint" or
"localtypes:struct"

```
:::
Note

Usually, this is the best method to describe the type of an
parameter - however, in old projects, this value might not be
accurate or even empty.
:::
```

`parameter`

:   Gets the parameter defining this data element. (This will return
the same instance if called on the [IScriptDeviceParameter](#iscriptdeviceparameter).

`parent`

:   Gets the parent.

```
:::
Note

This property returns either the parent [IScriptDataElement](#iscriptdataelement) (which may
be the [IScriptDeviceParameter](#iscriptdeviceparameter)), or the
[IScriptDeviceParameterSet](#iscriptdeviceparameterset) if
the current element is the device parameter.
:::
```

`section`

:   Gets the section of the parameter. (The sections are purely
informative and help to structure the device parameters in user
interfaces.)

`type_string`

:   Returns a string which fully describes the type.

`unit`

:   Internationalized unit of the data element. To be used by the
presentation layer.

`user_comment`

:   Get or set a user specified comment.

`visible_name`

:   Internationalized name of the data element (this is the name used
in the user interface).

## IScriptDeviceParameterSet

Base: object

A device parameter set.

:::
Note

The list is read-only which means you can't add, insert or remove
parameters or clear it. The list of available parameters is defined in
the device description.
:::

`Add`(*item*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.Add for more information!

`Clear`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.Clear for more information!

`Contains`(*item*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.Contains for more information!

`CopyTo`(*array*, *arrayIndex*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.CopyTo for more information!

`Count`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.Count for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`IsReadOnly`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.IsReadOnly for more information!

`Item`

:

`Remove`(*item*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).ICollection\`1.Remove for more information!

`by_id`(*id*)

:   Gets the [IScriptDeviceParameter](#iscriptdeviceparameter) with the
specified id.

`contains`(*parameter*)

:   Determines whether it contains the specified
[IScriptDeviceParameter](#iscriptdeviceparameter).

```
**Parameter**: parameter (IScriptDeviceParameter)
:   The parameter.

**Returns**: (bool)
:   **True** if contains the specified
    [IScriptDeviceParameter](#iscriptdeviceparameter);
    otherwise, **False**.

:::
Note

This class also contains an appropriate **\_\_contains\_\_**
overload for the **in** operator.
:::
```

`contains`(*id*)

:   Determines whether it contains a [IScriptDeviceParameter](#iscriptdeviceparameter) with the
specified id.

```
**Parameter**: id (int)
:   The id.

**Returns**: (bool)
:   **True** if contains a [IScriptDeviceParameter](#iscriptdeviceparameter) with
    the specified id; otherwise, **False**.

:::
Note

This class also contains an appropriate **\_\_contains\_\_**
overload for the **in** operator.
:::
```

`contains`(*name*)

:   Determines whether it contains a [IScriptDeviceParameter](#iscriptdeviceparameter) with the
specified name.

```
**Parameter**: name (str)
:   The name.

**Returns**: (bool)
:   **True** if contains a [IScriptDeviceParameter](#iscriptdeviceparameter) with
    the specified name; otherwise, **False**.

:::
Note

This class also contains an appropriate **\_\_contains\_\_**
overload for the **in** operator.
:::
```

`get_device_object`()

:   Gets the device object or explicit connector object defining this
parameter set.

`parent`

:   Gets the parent.

```
:::
Note

This is either a device object, a connector object, or an explicit
connector object.
:::
```

## IScriptExplicitConnectorObject

Base: object

Extension interface for [IScriptExplicitConnectorObject](#iscriptexplicitconnectorobject)
since V3.5.8.0.

`add`(*name*, *device*, *module*)

:   Adds the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`add`(*name*, *type*, *id*, *version*, *module*)

:   Adds the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`allowed_interfaces_at`(*index*)

:   Get the name of the child interfaces that this device object can
accept at the specified insert position.

```
**Parameter**: index (int)
:   The child index where a device should be inserted.

**Returns**: (list)
:   A list of possible interface names or null if no device can be
    inserted at that position.
```

`connector_id`

:   The unique connector id.

`connector_role`

:   Get whether this connector is a parent or child connector.

`export_io_mappings_as_csv`(*file_path*)

:   Export the io mappings as a CSV file to the specified absolute
path.

```
**Parameter**: file_path (str)
:   The absolute path of the file to export.
```

`get_device_object`()

:   Get an instance of the device object this connector belongs to.

```
**Returns**: (IScriptObject)
:   Returns the device object
```

`host_parameters`

:   Get the host parameter set of this connector.

```
:::
Note

The returned list is read-only which means you can't add, insert
or remove parameters or clear it. The list of available parameters
is defined in the device description.
:::
```

`host_path`

:   Get the id of the next connector towards the host. **-1**, if the
attached device is the controlling host.

`import_io_mappings_from_csv`(*file_path*)

:   Imports the io mappings from a CSV file at the specified absolute
path.

```
**Parameter**: file_path (str)
:   The absolute path of the file to export.
```

`insert`(*name*, *index*, *device*, *module*)

:   Inserts the specified device at the specified index.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: index (int)
:   index where to insert the device.

**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`insert`(*name*, *index*, *type*, *id*, *version*, *module*)

:   Inserts the specified device at the specified index.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: index (int)
:   index where to insert the device.

**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`interface`

:   The unique typename of a connector, eg. "Common.PCI". A parent
connector may be connected to a child connector, if this connector
type matches.

`interface_name`

:   Get an internationalized version of the interface name for
presentation purposes.

`is_explicit`

:   Get whether a separate node should be shown in the user interface
for this connector.

`is_explicit_connector`

:   Gets a value indicating whether this instance is a device object.

`module_type`

:   Id of the connector. This id is used by the driver on the runtime
system.

```
:::
Note

The Id's of matching parent and child connectors are different.
Therefore in order to find a matching device for a given parent
connector use the [('Unknown', u'ConnectorType')]Property instead.
:::
```

## IScriptExplicitConnectorObjectMarker

Base: object

Decorator for marking an object as explicit connector or not. All
objects within a project are decorated with this marker since
V3.5.4.0.

`is_explicit_connector`

:   Gets a value indicating whether this instance is a device object.

## IScriptExternalFileObject

Base: object

Provides the actual functionality of the external file objects.

`auto_update_mode`

:   Gets or sets the auto update mode.

`calculate_checksum`()

:   Calculates the checksum of the data.

```
**Returns**: (int)
:   The CRC 32 value of the data.
```

`change_modes`(*reference_mode*, *auto_update_mode*)

:   Changes the modes of the external file object.

```
**Parameter**: reference_mode (ReferenceMode)
:   The reference mode.

**Parameter**: auto_update_mode (AutoUpdateMode)
:   The auto update mode. This is optional, and only makes sense
    if **reference_mode** is set to
    [ReferenceMode.LinkAndEmbed].
```

`create_edit_path`()

:   Gets the absolute path where this file reference is edited. This
is the absolute path itself if the file reference is linked to a
file system object, or a temporary path if it is embedded into a
project.

```
**Returns**: (str)
:   The edit path of this file reference.
```

`file_path`

:   Gets the file path.

`get_data`(*stream*)

:   Gets the data by writing it into the given stream.

```
**Parameter**: stream (Stream)
:   The stream.
```

`get_data`(*filename*)

:   Gets the data by writing it to the specified filename.

```
**Parameter**: filename (str)
:   The filename.
```

`get_data`()

:   Gets the data as a byte array.

```
**Returns**: (Byte\[\])
:   The data as a byte array.
```

`is_external_file_object`

:   Gets a value indicating whether this [IScriptObject](#iscriptobject) is is an external
file object.

`last_modification`

:   Gets the last modification date.

`length`

:   Gets the length of the data in bytes.

`may_contain_external_file_objects`

:   Gets a value indicating whether this [IScriptObject](#iscriptobject) or
[IScriptProject](#iscriptproject) may contain external file objects.

```
:::
Note

The project root may always contain external file objects, those
are not downloaded to the devices. Devices and Applications may
contain files which are synchronized to the runtime, depending on
the device description and settings.
:::
```

`reference_mode`

:   Gets or sets the reference mode.

`update`()

:   Updates this instance.

## IScriptExternalFileObjectContainer

Base: object

This interface is implemented by the project root, and by objects
which can contain synchable external file objects.

:::
Note

The project root may always contain external file objects, those are
not downloaded to the devices. Devices and Applications may contain
files which are synchronized to the runtime, depending on the device
description and settings.
:::

`create_external_file_object`(*file_path*, *name*, *reference_mode*, *auto_update_mode*)

:   Creates an external file objects with the specified name.

```
**Parameter**: file_path (str)
:   The file path with the contents of the external file object.

**Parameter**: name (str)
:   The name. This is optional, if it is omitted, the filename
    will be extracted from the path.

**Parameter**: reference_mode (ReferenceMode)
:   The reference mode.

**Parameter**: auto_update_mode (AutoUpdateMode)
:   The automatic update mode.

**Returns**: (IScriptObject)
:   The newly created external file object.
```

`is_external_file_object`

:   Gets a value indicating whether this [IScriptObject](#iscriptobject) is is an external
file object.

`may_contain_external_file_objects`

:   Gets a value indicating whether this [IScriptObject](#iscriptobject) or
[IScriptProject](#iscriptproject) may contain external file objects.

```
:::
Note

The project root may always contain external file objects, those
are not downloaded to the devices. Devices and Applications may
contain files which are synchronized to the runtime, depending on
the device description and settings.
:::
```

## IScriptExternalFileObjectMarker

Base: object

Determines whether this object is an external file object or can
contain them.

`is_external_file_object`

:   Gets a value indicating whether this [IScriptObject](#iscriptobject) is is an external
file object.

`may_contain_external_file_objects`

:   Gets a value indicating whether this [IScriptObject](#iscriptobject) or
[IScriptProject](#iscriptproject) may contain external file objects.

```
:::
Note

The project root may always contain external file objects, those
are not downloaded to the devices. Devices and Applications may
contain files which are synchronized to the runtime, depending on
the device description and settings.
:::
```

## IScriptGateway

Base: object

Script engine representation of a configured gateway for runtime
connections.

:::
Note

Since V3.5.8.0
:::

`config_params`

:   Gets a python dictionary with a copy of the current configuration
of the gateway, using the
\[IScriptGatewayParameterDescription.id\] as
keys and the parameter values as values.

`find_address_by_ip`(*address*, *port*)

:   Finds an CODESYS address by scanning the network by IP or
Hostname.

```
**Parameter**: address (System.Net.IPAddress)
:   The IP address.

**Parameter**: port (int)
:   The port (11740 by default).

**Returns**: (str)
:   The CODESYS address.

:::
Note

Currently, only IPv4 addresses are supported. This method blocks
until either the device responded or the timeout for network scans
is reached. Any exceptions coming form the communication layer
will be thrown (e.g. if the Gateway is not running).
:::

**Exception**: TimeoutException
:   Thrown in case no device replies.

**Exception**: Exception
:   Any other exception forwarded from the communication layer.
```

`find_address_by_ip`(*ip_or_name*, *port*)

:   Finds an CODESYS address by scanning the network by IP or device.

```
**Parameter**: ip_or_name (str)
:   The IP address or device name.

**Parameter**: port (int)
:   The port (11740 by default) - will be ignored when scanning
    for the device name.

**Returns**: (str)
:   The CODESYS address.

:::
Note

Currently, only IPv4 addresses are supported. This method blocks
until either the device responded or the timeout for network scans
is reached. Any exceptions coming form the communication layer
will be thrown (e.g. if the Gateway is not running).
:::

**Exception**: TimeoutException
:   Thrown in case no device replies.

**Exception**: Exception
:   Any other exception forwarded from the communication layer.
```

`gateway_driver`

:   Gets the gateway protcol driver used for this gateway.

`get_cached_network_scan_result`()

:   Gets the cached result of the last network scan on this gateway.

```
**Returns**: (IEnumerable\`1)
:   The list of devices which were found.
```

`guid`

:   Gets the unique identifier of the gateway.

`name`

:   Gets the name of the gateway.

```
:::
Note

For backwards compatibility reasons, the gateway names are not
guaranteed to be unique - several gateways with the same name may
exist.
:::
```

`perform_network_scan`()

:   Performs a network scan on this gateway.

```
**Returns**: (IEnumerable\`1)
:   The list of devices which were found.

:::
Note

This method will block at least for the duration of the network
scan timeout period.
:::

**Exception**: Exception
:   Any exceptions occurring durint the network scan.
```

## IScriptGatewayDriver

Base: object

Script engine representation of a gateway driver.

:::
Note

Since V3.5.8.0
:::

`gateway_parameters`

:   Gets the gateway parameter descriptions - those are used when a
new gateway with this driver is created.

`guid`

:   A Guid that uniquely identifies the driver type.

```
:::
Note

Each implementation for a gateway driver is identified by a Guid.
:::
```

`name`

:   Get the user-readable name of this gateway driver.

## IScriptGatewayDrivers

Base: object

Represents a list of script gateway drivers.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`default_driver`

:   Gets the default gateway driver (currently bound to TCP/IP on
standard CODESYS and most derivates).

`find_with_name`(*name*)

:   Finds all gateway drivers with the name.

```
**Parameter**: name (str)
:   The name.

**Returns**: (IEnumerable\`1)
:   A (possibly empty) sequence of all gateway drivers with the
    name.
```

## IScriptGatewayParameterDescription

Base: object

Description of parameters for a gateway driver - those are used when a
new gateway with this driver is created.

`default_value`

:   Default value of the parameter. May be null.

`description`

:   Human readable string describing the parameter.

`id`

:   The id of the parameter.

```
:::
Note

The id is unique for any particular gateway driver.
:::
```

`name`

:   Human readable string, givin the name of the parameter.

`parameter_type`

:   The type of the parameter value.

```
:::
Note

The types here have finer granularity than the types available in
python. However, users don't need to cast to the corresponding
.NET types, this will be done by the script engine as long as the
generic type kind is matching - e. G. a python integer is ok for
all integer param types, or a single-character python string is ok
for [ParamType.Char].
:::
```

`validate`(*value*)

:   Check whether the provided object is a valid value for this
parameter.

```
**Parameter**: value (object)
:   The value to check.

**Exception**: Exception
:   If the object is not valid.

:::
Note

You can use the [IScriptGateways.convert_gateway_parameter] method to convert the parameter to the
corresponding type.
:::
```

## IScriptGatewayParameterDescriptions

Base: object

A collection of script gateway parameters.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

## IScriptGateways

Base: object

A collection of gateways currently configured in CODESYS.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`add_new_gateway`(*name*, *parameters*, *driver*, *gateway_guid*)

:

`convert_gateway_parameter`(*parameter*, *paramType*)

:   Converts an object to the specified gateway parameter type.

```
**Parameter**: parameter (object)
:   The parameter.

**Parameter**: paramType (ParamType)
:   Type of the parameter.

**Returns**: (object)
:   The object converted to the specified [ParamType](#paramtype).
```

`find_with_name`(*name*)

:   Finds all gateways with the name.

```
**Parameter**: name (str)
:   The name.

**Returns**: (IEnumerable\`1)
:   A (possibly empty) sequence of all gateways with the name.
```

`remove_gateway`(*guid*)

:   Removes the specified gateway.

```
**Parameter**: guid (Guid)
:   The guid of the gateway to remove.

:::
Note

If the specified one is the default one, the next one (if any)
will be the new default.
:::
```

`remove_gateway`(*gateway*)

:   Removes the specified gateway.

```
**Parameter**: gateway (IScriptGateway)
:   The gateway.

:::
Note

If the specified one is the default one, the next one (if any)
will be the new default.
:::
```

## IScriptIecLanguageMemberContainer

Base: object

This allows objects to create POU like member objects, the methods
will be availabe on POUs, Interfaces, GVLs, and folders below them.

:::
Note

The extended settings and specializations which are available in the
"Add Object" dialog, but not available in this interface, can be
implemented by direct access of the textual declaration part via
\[IScriptObjectWithTextualDeclaration\] - for
example, setting derived interfaces, or persistent or constant GVLs.

This interface is available since V3.5.9.0.
:::

`create_action`(*name*, *language*)

:

`create_method`(*name*, *return_type*, *language*)

:

`create_property`(*name*, *return_type*, *language*)

:

`create_transition`(*name*, *language*)

:

## IScriptIecLanguageObjectContainer

Base: object

This allows objects to create POU like objects, the methods will be
availabe in the project root as well as applications, and folders
below them.

:::
Note

The extended settings and specializations which are available in the
"Add Object" dialog, but not available in this interface, can be
implemented by direct access of the textual declaration part via
\[IScriptObjectWithTextualDeclaration\] - for
example, setting derived interfaces, or persistent or constant GVLs.

This interface is available since V3.5.9.0.
:::

`create_dut`(*name*, *type*, *baseType*)

:   Creates a DUT with the specified name and type.

```
**Parameter**: name (str)
:   The name.

**Parameter**: type (DutType)
:   The type. Optional, the default is a structure.

**Parameter**: baseType (str)
:   The base type. This optional parameter is necessary for for
    Alias types, optional for STRUCTs and enums, and currently not
    allowed for unions.

**Returns**: (IScriptObject)
:   The [IScriptObject](#iscriptobject) of the newly
    created POU.

**Exception**: Exception
:   Any exception which might occur (e. G. if the name is not an
    IEC identifier, or an object with the same name already exists
    within the same namespace, or the object cannot be created
    under this parent

:::
Note

As with manual object creation in the UI, enums will get the
attribute 'strict' with compiler versions \>= 3.5.7.0, and
additionally the attribute 'qualified_only' with compiler version
3.5.8.0.
:::
```

`create_gvl`(*name*)

:   Creates a GVL with the specified name.

```
**Parameter**: name (str)
:   The name.

**Returns**: (IScriptObject)
:   The [IScriptObject](#iscriptobject) of the newly
    created POU.

**Exception**: Exception
:   Any exception which might occur (e. G. if the name is not an
    IEC identifier, or an object with the same name already exists
    within the same namespace, or the object cannot be created
    under this parent.
```

`create_interface`(*name*, *baseInterfaces*)

:   Creates an interface with the specified name .

```
**Parameter**: name (str)
:   The name.

**Parameter**: baseInterfaces (str)
:   The base interfaces (comma separated). The default is
    "\_\_System.IQueryInterface".

**Returns**: (IScriptObject)
:   The [IScriptObject](#iscriptobject) of the newly
    created POU.

**Exception**: Exception
:   Any exception which might occur (e. G. if the name is not an
    IEC identifier, or an object with the same name already exists
    within the same namespace, or the object cannot be created
    under this parent.
```

`create_pou`(*name*, *type*, *language*, *return_type*, *base_type*, *interfaces*)

:

## IScriptImagePoolItem

Base: object

An item (in fact like a line) within an [IScriptImagePoolObject](#iscriptimagepoolobject).

`filepath`

:   The path of the referenced image. Relevant only if
\[IScriptImagePoolItem.linktype\] yields
\[ImageLinkType.Linked\] or
\[ImageLinkType.EmbeddedAndLinked\]

`id`

:   The identification of the image that can be accessed in the
visualization too

```
**Exception**: ArgumentException
:   Thrown when the id is being set and the new id is already
    contained in the imagepool
```

`linktype`

:   The way the image is referenced.

`updatemode`

:   The way the image is updated automatically while the project is
open. Relevant only if \[IScriptImagePoolItem.linktype\] yields \[ImageLinkType.EmbeddedAndLinked\]

## IScriptImagePoolItems

Base: object

The items currently managed by the imagepool object

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`__len__`()

:   Gets the current number of items in this imagepool.

```
**Returns**: (int)
:   The number of items.
```

`add`(*id*, *path*, *linktype*, *updateMode*)

:   Adds a new image to the current image pool and returns the newly
created [IScriptImagePoolItem](#iscriptimagepoolitem)

```
**Parameter**: id (str)
:   The id to assign to the newly inserted image. Must not yet be
    existing.

**Parameter**: path (str)
:   The file path to reference by the new image item.

**Parameter**: linktype (ImageLinkType)
:   The way the new image item references the according file.

**Parameter**: updateMode (AutoUpdateMode)
:   The way the image item is updated automatically, relevant only
    in case of **linktype** is
    [ImageLinkType.EmbeddedAndLinked]

**Returns**: (IScriptImagePoolItem)
:   The newly created [IScriptImagePoolItem](#iscriptimagepoolitem)

**Exception**: ArgumentException
:   Thrown when an item with the according **id** is already
    existing.
```

`move`(*indexSrc*, *indexDst*)

:   Moves an [IScriptImagePoolItems](#iscriptimagepoolitems) in the
list of items.

```
**Parameter**: indexSrc (int)
:   The index of the item that should be moved.

**Parameter**: indexDst (int)
:   The index where the item should be located afterwards.

**Exception**: ArgumentOutOfRangeException
:   Thrown when the given indices are out of range.
```

`remove`(*id*)

:   Removes the [IScriptImagePoolItem](#iscriptimagepoolitem) with the
given **id**

```
**Parameter**: id (str)
:   The id of the item to remove.

**Exception**: KeyNotFoundException
:   Thrown when no entry with the given id exists.
```

## IScriptImagePoolMarker

Base: object

Marker object to check whether an IScriptObject is an imagepool
object. (Since V3.5.9.0)

`is_imagepool`

:   Gets a value indicating whether this
[IScriptApplicationMarker](#iscriptapplicationmarker) is an
imagepool.

## IScriptImagePoolObject

Base: object

IScriptObjects which are an imagepool object are extended with this
interface. (Since V3.5.9.0)

`download_only_used_images`

:   Gets or sets a value whether all images or only the explicitly
referenced ones should be downloaded to PLCs.

`imagepool_is_internal`

:   Gets or sets a value whether this image pool is visible for
projects embedding the current one as a library. This is not
relevant when working on a project itself.

`images`

:   Gets the collection of the items currently configured within this
imagepool.

`is_imagepool`

:   Gets a value indicating whether this
[IScriptApplicationMarker](#iscriptapplicationmarker) is an
imagepool.

`symboltextlist`

:   Gets and sets the name of the text list for translation of the
symbols in this image pool.

## IScriptImagePoolObjectContainer

Base: object

Projects and Application Objects are extended with this interface
since CoDeSys V3.5.9.0

`create_imagepool`(*name*)

:   Creates a new image pool object in the current context (either
application or project global).

```
**Parameter**: name (str)
:   The name of the new imagepool object. In case of **None**, a
    default name will be generated.

**Returns**: (IScriptObject)
:   The newly created imagepool object.

**Exception**: ArgumentException
:   Thrown when an image pool with the given name already exists
    within the current context.
```

`get_global_imagepool`()

:   Returns the global image pool object or creates a new one if not
yet existing.

```
:::
Note

Typically this method can be called on projects only. Only in case
of special customizations of the programming system, it is allowed
to call this on an application too.
:::

**Returns**: (IScriptObject)
:   The global imagepool

**Exception**: InvalidOperationException
:   Thrown when called on applications when this is not allowed.
```

`has_global_imagepool`

:   Checks whether there is already a globalimagepool in the current
location.

```
:::
Note

Only in case of special customizations of the programming system,
it is allowed to call this on an application too.
:::

**Exception**: InvalidOperationException
:   Thrown when called on applications when this is not allowed.
```

## IScriptLibManObject

Base: object

Extension interface for lib man objects since V3.5.5.0.

`add_library`(*library*)

:   Adds a reference to the specified library.

```
**Parameter**: library (IManagedLib)
:   The library.
```

`add_library`(*name*)

:   Adds the library with the specified name.

```
**Parameter**: name (str)
:   The name.
```

`add_placeholder`(*name*, *default_resolution*)

:   Adds a placeholder with the specified default resolution..

```
**Parameter**: name (str)
:   The name.

**Parameter**: default_resolution (IManagedLib)
:   The default_resolution.
```

`add_placeholder`(*name*, *default_resolution*)

:   Adds the placeholder for a library with the specified name.

```
**Parameter**: name (str)
:   The name.

**Parameter**: default_resolution (str)
:   The default_resolution.
```

`get_libraries`(*recursive*)

:   Returns a list of all libraries.

```
**Parameter**: recursive (bool)
:   If set to **True**, sublibraries are also queried recursively.
    (This parameter is optional, default is False.)

**Returns**: (list)
:   The list of library names.
```

`is_libman`

:   Gets a value indicating whether this instance is a lib man object.

`references`

:   Gets the collection of the references currently configured within
this library manager.

`remove_library`(*name*)

:   Removes the librariy with the specified name.

```
**Parameter**: name (str)
:   The name.
```

## IScriptLibManObjectContainer

Base: object

Projects and Application Objects are extended with this interface
since CoDeSys V3.5.2.0

`get_library_manager`()

:   Gets the library manager for this application or project,
implicitly creating one if none is existing yet.

```
**Returns**: (IScriptObject)
:   The library manager object.
```

`has_library_manager`

:   Gets a value indicating whether this
[IScriptLibManObjectContainer](#iscriptlibmanobjectcontainer)
has a library manager.

## IScriptLibManObjectMarker

Base: object

Every IScriptObject instance will be extended with this method.

This interface is exported to python, and thus adheres to python
naming standards.

`is_libman`

:   Gets a value indicating whether this instance is a lib man object.

## IScriptModule

Base: object

Interface providing necessary information and functionalities dealing
with Modules in Python (equalling the type IModule in the application
composer interface collection).

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`Extender`

:   Gets the Extender instance for the current object.

`iec_declaration`

:   Gets the declaration of the corresponding Module-IEC-FB.

`inst_refs`

:   Gets all Module-InstanceReferences

`ios`

:   Gets all Module-IOs

`is_param_page_disabled`

:   Whether the Editors Parameters-Page is dissabled or not.

`is_toplevel_page_disabled`

:   Whether the Editors Toplevel-Page is dissabled or not.

`meta_data`

:   Gets the Module-MetaData. Returns null if module is not toplevel.

`name`

:   Gets the name of the Module

`parameters`

:   Gets all Module-Parameters

`proxies`

:   Gets all Module-Proxies.

`qualified_name`

:   Gets the fully qualified Name (namespace.modulename) of the Module

`slots`

:   Gets all Module-Slots

`toplevel_info`

:   Gets the Module-ToplevelInfo. Returns null if module is not
toplevel.

`var_arrays`

:   Gets all Module-VarArrays

## IScriptModuleIECDecl

Base: object

Interface providing necessary information and functionallities for
dealing with module-bound Declarations in Python.

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`is_fb`

:   Whether this declaration is an FB or not.

`is_interface`

:   Whether this declaration is an interface or not.

`is_method`

:   Whether this declaration is a method or not.

`is_other`

:   Whether this declaration is of an other type or not.

`is_struct`

:   Whether this declaration is a struct or not.

`is_union`

:   Whether this declaration is a union or not.

`name`

:   Gets the name of the declaration object.

## IScriptModuleMetaData

Base: object

Interface providing necessary information and functionalitties for
dealing with Module-MetaData in Python.

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`category`

:   The hierarchic category of the module. The components are
separated by '|'.

`default_inst_name`

:   Returns the default name for instances of this module type.

`description`

:   Localized (multi-lingual) description of the module.

`inst_prefix`

:   An optional, default instance prefix that is prepended to the name
of the FB-instance variables of submodules and to the names of
VarArray variables. "" is a possible value. If no prefix is given,
'inst_prefix' is null.

## IScriptModuleSlot

Base: object

Interface providing necessary information and functionallities for
dealing with Module-Slots in Python.

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`default_inst_name`

:   Gets the default name for module instances, which are connected to
this Slot. If no default name is defined an empty string is
returned.

`id`

:   Id of the Slot. The Id is unique among all Slots of a module.

`inst_prefix`

:   Gets the optional prefix, that is prepended to the name of the FB
instance variables of submodules. This string can either have a
value or is empty, what indicates a prefix, or that no prefix is
wished. When this string is null no prefix wishes at all are
given.

`is_multi`

:   Returns whether the Slot is a Multi-Slot, which can hold multiple
instances, or not.

`is_reference_slot`

:   Returns whether the Slot is meant to hold references to modules or
not.

`is_single`

:   Returns whether the Slot is a Single-Slot, which only can hold one
instance, or not.

`is_submodule_slot`

:   Returns whether the Slot is meant to hold submodules or not.

`max_connections`

:   Gets the number of the maximum of submodules or references, that
can be connected to this Slot.

`min_connections`

:   Gets the number of the minimum of submodules or references, that
have to be connected to this Slot.

`pragmas`

:   Returns the compiler-pragmas, that are to be inserted before
instances of submodule function blocks.

`role`

:   Localized (multi-lingual) description of the slot role.

`type`

:   Gets the interface type of this Slot (corresponding to the
interface, that FBs have to implement, when they shall be
connectable to this slot).

`var_array_size_path`

:   For Multi-Slots the instance path of the variable, which holds the
number of connected submodules or references, relative to the FB
instance of the module. For Single-Slots an empty string is
returned.

`var_path`

:   The IEC instance path of the slot variable relative to the FB
instance of the module.

## IScriptModuleStdTaskInfo

Base: object

Interface providing all necessary information and functionallities for
dealing with a StandardTaskInfo.

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`description`

:   Localized (multi-lingual) description of the task.

`is_create_if_missing`

:   Whether the task is created, if it did not exist yet, or not.

`is_readonly`

:   Whether the name can be changed by the user or not.

`is_update_ios`

:   Whether module IOs that are directly mapped (i.e. not mapped to
physical IOs) are read and written in this task or not

`name`

:   The name of the task.

## IScriptModuleToplevelInfo

Base: object

Interface providing all neccessary information and functionallities
for dealing with Module-ToplevelInfo.

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`custom_tasks`

:   Returns all defined custom tasks.

`get_home`()

:   Gets the home location of a toplevel module where the composer
generates the applications. It has the form "Device.AppName" or
holds the special string "POU Pool".

`get_standard_task_high`()

:   Returns the standard task info for the high priority task, or null
if this task was not enabled.

`get_standard_task_low`()

:   Returns the standard task info for the low priority task, or null
if this task was not enabled.

`get_standard_task_medium`()

:   Returns the standard task info for the medium priority task, or
null if this task was not enabled.

`gvl_name`

:   Gets the name of the global variable list where the module
instances will be declared.

`pragmas`

:   Returns the compiler pragmas that are to be inserted before
instances of the module function block.

## IScriptObject

Base: object

Extension interface for IScriptObjects since CODESYS V3.5 SP7.

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`Extender`

:   Gets the Extender instance for the current object.

`build_properties`

:   Gets the build properties of the object, or None.

```
:::
Note

Not all objects have editable build properties - this method
returns None when the object does not have any build properties.
:::
```

`create_folder`(*foldername*)

:   Creates a folder with the specified foldername in the structured
view of the parent node.

```
**Parameter**: foldername (str)
:   The foldername.

:::
Note

The Modules View currently does not support folders, so creating
folders below module objects is not supported.
:::
```

`effectively_excluded_from_build`

:   Gets a boolean indicating whether this object is effectively
excluded from the build.

```
:::
Note

An object is effectively excluded if either the object itsself or
any of its parents has the
[IScriptBuildProperties.exclude_from_build]
flag set.
:::
```

`embedded_object_types`

:   Gets the embedded object types.

`exclusion_from_build_is_inherited`

:   Gets a boolean indicating whether the build exclusion is inherited
from a parent object.

`export_native`(*destination*, *recursive*, *profile_name*, *reporter*)

:   Export the specified objects in the CoDeSys native export format.

```
**Parameter**: destination (str)
:   The destination file.

**Parameter**: recursive (bool)
:   if set to **True**, the chilren are included recursively. This
    parameter is optional, the default is true.

**Parameter**: profile_name (str)
:   The profile_name, or null for the default profile. This
    parameter is optional.

**Parameter**: reporter (NativeExportReporter)
:   The reporter. You can pass null for no reporting at all. This
    parameter is optional.
```

`export_xml`(*reporter*, *path*, *recursive*)

:   Exports the ScriptObject in PLCopenXML format into a string, or a
file at the given path. This method internally eliminates
duplicates, and all non-exportable objects are reported as error.

```
**Parameter**: reporter (ExportReporter)
:   The IExportReporter instance.

**Parameter**: path (str)
:   The path of the file we export into. If omitted, we export
    into a string and return that string. (This parameter is
    optional.)

**Parameter**: recursive (bool)
:   if set to **True**, all exportable children of the objects are
    also exported. (This parameter is optional, default is false.)

**Returns**: (str)
:   The exported XML as string, or null if a filepath is given.
```

`export_xml`(*reporter*, *path*, *recursive*, *export_folder_structure*)

:   Exports the ScriptObject in PLCopenXML format into a string, or a
file at the given path. This method internally eliminates
duplicates, and all non-exportable objects are reported as error.

```
**Parameter**: reporter (ExportReporter)
:   The IExportReporter instance.

**Parameter**: path (str)
:   The path of the file we export into. If omitted, we export
    into a string and return that string. (This parameter is
    optional.)

**Parameter**: recursive (bool)
:   if set to **True**, all exportable children of the objects are
    also exported. (This parameter is optional, default is false.)

**Parameter**: export_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also exported. This is a proprietary extension to the default
    schema.

**Returns**: (str)
:   The exported XML as string, or null if a filepath is given.
```

`export_xml`(*reporter*, *path*, *recursive*, *export_folder_structure*, *declarations_as_plaintext*)

:   Exports the ScriptObject in PLCopenXML format into a string, or a
file at the given path. This method internally eliminates
duplicates, and all non-exportable objects are reported as error.

```
**Parameter**: reporter (ExportReporter)
:   The IExportReporter instance.

**Parameter**: path (str)
:   The path of the file we export into. If omitted, we export
    into a string and return that string. (This parameter is
    optional.)

**Parameter**: recursive (bool)
:   if set to **True**, all exportable children of the objects are
    also exported. (This parameter is optional, default is false.)

**Parameter**: export_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also exported. This is a proprietary extension to the default
    schema.

**Parameter**: declarations_as_plaintext (bool)
:   if set to **True**, the declaration parts will be additionally
    exported as plain text (which is lossless in contrast to the
    default schema). This is a proprietary extension to the
    default schema. (Import will automatically recognize and
    prefer the plain text format if present.)

**Returns**: (str)
:   The exported XML as string, or null if a filepath is given.
```

`export_xml`(*path*, *recursive*, *export_folder_structure*, *declarations_as_plaintext*)

:   Exports the ScriptObject in PLCopenXML format into a string, or a
file at the given path. This method internally eliminates
duplicates, and all non-exportable objects are reported as error.

```
**Parameter**: path (str)
:   The path of the file we export into. If omitted, we export
    into a string and return that string. (This parameter is
    optional.)

**Parameter**: recursive (bool)
:   if set to **True**, all exportable children of the objects are
    also exported. (This parameter is optional, default is false.)

**Parameter**: export_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also exported. This is a proprietary extension to the default
    schema.

**Parameter**: declarations_as_plaintext (bool)
:   if set to **True**, the declaration parts will be additionally
    exported as plain text (which is lossless in contrast to the
    default schema). This is a proprietary extension to the
    default schema. (Import will automatically recognize and
    prefer the plain text format if present.)

**Returns**: (str)
:   The exported XML as string, or null if a filepath is given.

:::
Note

This method will report all exportable objects, report everything
on progress, and throw exceptions on critical errors.
:::
```

`find`(*names*)

:   Finds objects matching the given path.

```
:::
Note

Names are not unique in the tree, so several Objects can be
delivered. The search is against the nonlocalized name and
non-recursive.
:::

**Parameter**: names (String\[\])
:   The path of names to follow.

**Returns**: (list)
:   The collection of objects.
```

`find`(*name*, *recursive*)

:   Finds objects matching the given name.

```
:::
Note

Names are not unique in the tree, so several Objects can be
delivered. The search is against the nonlocalized name.
:::

**Parameter**: name (str)
:   The name.

**Parameter**: recursive (bool)
:   Whether we search recursively (This parameter is optional,
    default = false).

**Returns**: (list)
:   The collection of objects.
```

`get_children`(*recursive*)

:   Gets the children of our object.

```
**Parameter**: recursive (bool)
:   If set to **True**, we work recursive (This parameter is
    optional, default = false).

**Returns**: (list)
:   All child objects.
```

`get_name`(*resolve_localized_display_name*)

:   Gets the name of the object.

```
**Parameter**: resolve_localized_display_name (bool)
:   if set to **True**, the name is localized. (This parameter is
    optional, default = false)

**Returns**: (str)
:   The name of the object.
```

`get_signature_crc`(*application*, *default_value*)

:   Gets the signature CRC of the specified pou. A successfull build
is needed for this method to work.

```
**Parameter**: application (object)
:   The application which the POU is referenced, if necessary (see
    remarks). This parameter accepts the application object or its
    guid.

**Parameter**: default_value (str)
:   If you pass a value here, this is returned instead of throwing
    an exception when no CRC is found.

**Returns**: (str)
:   The string representation of the CRC, or the default value
    when no CRC was found.

**Exception**: InvalidOperationException
:   No compile context found for the object - maybe the
    application was not compiled?

**Exception**: NotSupportedException
:   No compiled signature found for the object - maybe the object
    is no POU.

**Exception**: KeyNotFoundException
:   No CRC Attribute found for the object.

**Exception**: ArgumentException
:   You did pass an invalid object for the application.

:::
Note

For POUs which are defined below an application, compile the
application via [IScriptApplication.build].
You can omit **application**, and the parent application will be
found automatically.

For POUs which are in the pool of a library projuect, compile the
application via [IScriptProject.check_all_pool_objects]. The pool application guid ([Guid.Empty]) will be used automatically in this case, so you can
omit **application**.

For pous which are defined in the pool of a project, but
referenced from within an application, compile the application via
[IScriptApplication.build] and explicitly
pass that application (or its guid) as **application** parameter.
:::
```

`guid`

:   Gets the GUID of the object.

`handle`

:   Gets the internal Automation Platform handle of the Project.

```
:::
Note

This handle is primarily useful for other Atomation Platform
plugins which provide functionality for scripts via IScriptDriver.
When they consume IScriptProjects as their parameters, they can
use the handle to gain access to the underlying Automation
Platform object.
:::
```

`import_native`(*filenames*, *filter*, *handler*)

:

`import_native`(*filename*, *filter*, *handler*)

:   Imports the specified files in the native xml format in under the
current node.

```
**Parameter**: filename (str)
:   The filename.

**Parameter**: filter (NativeImportFilter)
:   The filter - if null is passed, all files are imported.

**Parameter**: handler (NativeImportHandler)
:   The handler - if null passed, the default handler is used.
```

`import_xml`(*conflictResolve*, *dataOrPath*, *import_folder_structure*)

:   Imports the contents of the specified PLCopenXML file als children
of the current object.

```
:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML. This heuristics may be replaced by a more
sophisticated heuristics in the future.
:::

**Parameter**: conflictResolve (ConflictResolve)
:   The conflict resolution strategy.

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Parameter**: import_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also imported.
```

`import_xml`(*reporter*, *dataOrPath*)

:   Imports the contents of the specified PLCopenXML file als children
of the current object.

```
:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML. This heuristics may be replaced by a more
sophisticated heuristics in the future.
:::

**Parameter**: reporter (ImportReporter)
:   The import reporter.

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Returns**:
:   Counts of errors and warnings.
```

`import_xml`(*reporter*, *dataOrPath*, *import_folder_structure*)

:   Imports the contents of the specified PLCopenXML file als children
of the current object.

```
:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML. This heuristics may be replaced by a more
sophisticated heuristics in the future.
:::

**Parameter**: reporter (ImportReporter)
:   The import reporter.

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Parameter**: import_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also imported.
```

`import_xml`(*dataOrPath*, *import_folder_structure*)

:   Imports the contents of the specified PLCopenXML file als children
of the current object.

```
:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML. This heuristics may be replaced by a more
sophisticated heuristics in the future. This method will apply
[ConflictResolve.Copy] as strategy.
:::

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Parameter**: import_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also imported.
```

`index`

:   Gets the index.

`is_folder`

:   Gets a value indicating whether this instance is a folder.

`is_root`

:   Gets a value indicating whether this instance is the root of the
object tree. This returns true for all ScriptProject instances,
and false for all ScriptObject instances.

`move`(*new_parent*, *new_index*)

:   Moves the object to the specified new parent.

```
**Parameter**: new_parent (IScriptObject)
:   The new parent.

**Parameter**: new_index (int)
:   New index in the new parent. (This parameter is optional.)
```

`move`(*new_parent*, *new_index*)

:   Moves the object to the specified new parent.

```
**Parameter**: new_parent (IScriptProject)
:   The new parent.

**Parameter**: new_index (int)
:   New index in the new parent. (This parameter is optional.)
```

`parent`

:   Gets the parent ScriptObject, or the Project if we are top-level.

```
:::
Note

You can use the is_root property implemented by objects and
projects to distinct between the two.
:::
```

`project`

:   Gets the project.

```
:::
Note

This returns "this" rsp. "self" if called on Projects.
:::
```

`remove`()

:   Removes this instance.

`rename`(*stNewName*)

:   Renames the object to the new name.

```
**Parameter**: stNewName (str)
:   New name of the object.
```

`type`

:   Gets the type guid.

## IScriptObjectFactories

Base: object

A sequence of all known object factories.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`search_factories_for`(*typeguid*)

:   Returns all known object factories for a given object type.

```
**Parameter**: typeguid (Guid)
:   The typeguid.

**Returns**: (IEnumerable\`1)
:   A (possibly empty) sequence of object factories.

:::
Note

The list is ordered, so that perfect matches (which produce
exactly the queried type) come before factories which produce
subclasses of the queried type. For object permission management,
permissions are tested for the first factory of that list which
produces that actual type.
:::
```

## IScriptObjectFactory

Base: object

An Object factory.

`description`

:   Gets the description for this object factory. This string should
be localized.

`guid`

:   Gets the GUID of the object factory.

`name`

:   Gets the display text of this object factory. This string should
be localized.

`object_namespace`

:   Gets a GUID identifying the namespace the created object will
belong to.

`object_type`

:   Gets the guid of the produced object type.

## IScriptOnlineApplication

Base: object

Extension interface for IScriptOnlineApplication. Since CoDeSys V3.5,
all IScriptOnlineApplications are extended with this interface.

`Dispose`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IDisposable.Dispose](https://social.msdn.microsoft.com/Search/?query=System.IDisposable.Dispose) for more information!

`application`

:   Gets the application object for this online application.

`application_state`

:   Gets the application state.

`create_boot_application`()

:   Creates a boot application for this application on the device.

```
:::
Note

If the current application is not online, a file dialog asks the
user for a path to write the boot file for. You may want to use
[IScriptApplication.create_boot_application]instead.
:::
```

`force_prepared_values`()

:   Forces the prepared values.

```
**Exception**: ValuesFailedException
:   If the force of some values fails.
```

`get_forced_expressions`()

:   Gets all expressions for values currently forced for this
application (including those prepared by other scripts, editors
etc.).

```
**Returns**: (list)
:   The forced expressions.
```

`get_online_device`()

:   Gets the online device for this application.

```
**Returns**: (IScriptOnlineDevice)
```

`get_prepared_expressions`()

:   Gets all expressions for values currently prepared for this
application (including those prepared by other scripts, editors
etc.).

```
**Returns**: (list)
:   The prepared expressions.
```

`get_prepared_value`(*expression*)

:   Gets the prepared value for a given expression.

```
**Parameter**: expression (str)
:   The expression.

**Returns**: (str)
:   The prepared value, or None if nothing is prepared.
```

`is_logged_in`

:   Gets a value indicating whether this
[IScriptOnlineApplication](#iscriptonlineapplication) is
logged in.

`login`(*change_option*, *delete_foreign_apps*)

:   Performs the application login. If the application was logged in
before, it will be logged out and a fresh login will be performed.

```
**Parameter**: change_option (OnlineChangeOption)
:   The change_option.

**Parameter**: delete_foreign_apps (bool)
:   If set to **True**, delete foreign applications.
```

`logout`()

:   Logs this application out. If the application is not logged in,
nothing happens.

`operation_state`

:   Gets the operation state.

`read_value`(*expression*)

:   Gets the current value for a given expression.

```
:::
Note

Monitoring must be enabled.
:::

**Parameter**: expression (str)
:   The expression.

**Returns**: (str)
:   The value.
```

`read_values`(*expressions*)

:

`read_values`(*expressions*)

:   Gets the current values for a list of expressions.

```
:::
Note

Monitoring must be enabled.
:::

**Parameter**: expressions (String\[\])
:   The expressions.

**Returns**: (list)
:   The values.
```

`reset`(*reset_option*, *force_kill*)

:   Resets the online application. This also clears all breakpoints on
the application (if any).

```
**Parameter**: reset_option (ResetOption)
:   The reset_option. This parameter is optional, the default
    value is [ResetOption.Warm].

**Parameter**: force_kill (bool)
:   Force the immediate kill of the application without finishing
    of the current cycle. This parameter is optional, the default
    value is false.

:::
Note

If the application is currently halted on a breakpoint, and the
device supports to kill a task during the execution cycle
([TargetProperties.TaskKillable]), you can
use the **force_kill** parameter to force the reset without
running the current cycle to an end. If the device does not
support [TargetProperties.TaskKillable], this
parameter will be ignored, and the current cycle will always be
finished.
:::
```

`set_prepared_value`(*expression*, *value*)

:   Prepares values the specified expression. Use None or the empty
string to unprepare the value.

```
**Parameter**: expression (str)
:   The expression.

**Parameter**: value (str)
:   The value.
```

`set_unforce_value`(*expression*, *restore*)

:   Prepares the specified forced expression for unforcing.

```
**Parameter**: expression (str)
:   The expression.

**Parameter**: restore (bool)
:   If set to **True**, the value is reset to the value before
    forcing. (This parameter is optional.)
```

`source_download`()

:   Downloads the source archive to the device.

`start`()

:   Starts this application.

```
**Exception**: TimeoutException
:   In case of the operation taking to long.
```

`stop`()

:   Stops this application.

```
**Exception**: TimeoutException
:   In case of the operation taking to long.
```

`timeout`

:   Gets or sets the timeout for some operations. Some operations like
start() have to wait for defined application states. If those
operations take longer than this timeout, a
[TimeoutException](#timeoutexception) is thrown. The default timeout is 60 seconds.

`unforce_all_values`()

:   Unforces all forced values for the current application.

```
**Exception**: ValuesFailedException
:   If the unforce of some values fails.
```

`write_prepared_values`()

:   Writes the prepared values.

```
**Exception**: ValuesFailedException
:   If the write of some values fails.
```

## IScriptOnlineDevice

Base: object

Extension interface for IScriptOnlineDevice4 since V3.5.10.0

`Dispose`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IDisposable.Dispose](https://social.msdn.microsoft.com/Search/?query=System.IDisposable.Dispose) for more information!

`activate_license`(*ticket*, *url*, *license_names*)

:   Performs a license activation on a remote device. The first
container returned be the device will be used for activation.

```
**Parameter**: ticket (str)
:   The ticket which contains the licenses.

**Parameter**: url (str)
:   The license server. If **None** the default license server
    will be used.

**Parameter**: license_names (String\[\])
:   The licenses which should be activated. If **None** or if no
    license is specified, every kind of license will be activated
    by default.
```

`connect`()

:   Connects this instance. (The connection is a shared connection to
the device.) Please note that other actions like reset_origin may
implicitly connect to the device.

`connected`

:   Gets a value indicating whether this [IScriptOnlineDevice](#iscriptonlinedevice) is
connected.

`create_directory`(*remote_directory*)

:   Create a directory on the PLC.

```
**Parameter**: remote_directory (str)
:   Path of the new directory.
```

`create_user_management`(*load_from_project*)

:   Creates a new user management instance for this device.

```
**Parameter**: load_from_project (bool)
:   By default, the instance is initialized with the information
    stored in the device object in the current project. By setting
    this parameter to false, you can suppress this loading, e. G.
    if you want to load the user management via the
    [IScriptDeviceUserManagement.upload],
    [IScriptDeviceUserManagement.load] or
    [IScriptDeviceUserManagement.load]
    methods.

**Returns**: (IScriptDeviceUserManagement)
:   The created user management instance.
```

`current_logged_on_username`

:   Gets the name of the user who is currently logged on in the
device. If **None** or an empty string is returned, nobody is
logged on.

`delete_directory`(*remote_directory*, *recursive*)

:   Delete a directory on the PLC.

```
**Parameter**: remote_directory (str)
:   Path of the remote directory.

**Parameter**: recursive (bool)
:   True, delete the directory resursively.
```

`delete_file`(*remote_file*)

:   Delete a file on the PLC.

```
**Parameter**: remote_file (str)
:   Path of the remote file.
```

`device`

:   Gets the underlying device object for this online device.

`disconnect`()

:   Disconnects this instance. (As the connection is shared, the
underlying connection may actually stay open, for example when an
application is still online.)

`download_file`(*local_file*, *remote_file*, *force_overwrite*)

:   Download a file to the PLC.

```
**Parameter**: local_file (str)
:   Path of the local file.

**Parameter**: remote_file (str)
:   Path of the remote file.

**Parameter**: force_overwrite (bool)
:   Force the overwrite if the remote file already exists.
```

`download_source`(*additional_items*)

:   Downloads the source archive to the device (non-compact download).

```
**Parameter**: additional_items (IEnumerable\`1)
:   The additional items to include in the project archive.

:::
Note

This method will throw various Exceptions on errors.
:::

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_items**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`download_source`(*additional_items*)

:   Downloads the source archive to the device (non-compact download).

```
**Parameter**: additional_items (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.IScriptProjectArchiveCategory\[\])
:   The additional items to include in the project archive.

:::
Note

This method will throw various Exceptions on errors.
:::

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_items**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`download_source`(*bCompact*, *additional_items*)

:   Downloads the source archive to the device.

```
**Parameter**: bCompact (bool)
:   If TRUE, the source archive will only contain the PLC and
    applications of the current device. If FALSE, the source
    archive will contain all PLCs and all applications in the
    project. This parameter is optional, the default is false.

**Parameter**: additional_items (IEnumerable\`1)
:   The additional items to include in the project archive.

**Exception**: Exception
:   This method will throw various implementation-dependent
    subclasses of [Exception] on errors.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_items**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`download_source`(*bCompact*, *additional_items*)

:   Downloads the source archive to the device.

```
**Parameter**: bCompact (bool)
:   If TRUE, the source archive will only contain the PLC and
    applications of the current device. If FALSE, the source
    archive will contain all PLCs and all applications in the
    project. This parameter is optional, the default is false.

**Parameter**: additional_items (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.IScriptProjectArchiveCategory\[\])
:   The additional items to include in the project archive.

**Exception**: Exception
:   This method will throw various implementation-dependent
    subclasses of [Exception] on errors.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_items**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`forced_disconnect`()

:   Forcibly disconnects all shared connections to the device
(connections via online applications, as well as other
connections), and resets the current login and session
information.

`get_file_list_of_directory`(*remote_directory*)

:   Read a directory on the PLC.

```
**Parameter**: remote_directory (str)
:   Path of the directory.

**Returns**: (IScriptDirectoryInfo\[\])
:   List of info elements which descript the files and directories
    inside the given remote directory.
```

`rename_directory`(*old_name*, *new_name*)

:   Rename a directory on the PLC.

```
**Parameter**: old_name (str)
:   Path of the remote directory with the old name.

**Parameter**: new_name (str)
:   Path of the remote directory with the new name.
```

`rename_file`(*old_name*, *new_name*)

:   Rename a file on the PLC.

```
**Parameter**: old_name (str)
:   Path of the remote file with the old name.

**Parameter**: new_name (str)
:   Path of the remote file with the new name.
```

`reset_origin`()

:   Reset the device to the origin (shipping) state. For example, all
plc applications, boot applications, and retain and persistent
variables are deleted.

`shared_connected`

:   Gets a value indicating whether this IScriptOnlineDevice or
anything else has a shared connection to the device.

`upload_file`(*remote_file*, *local_file*, *force_overwrite*)

:   Upload a file from the PLC.

```
**Parameter**: remote_file (str)
:   Path of the remote file.

**Parameter**: local_file (str)
:   Path of the local file.

**Parameter**: force_overwrite (bool)
:   Force the overwrite if the local file already exists.
```

`upload_source`(*archive_path*)

:   Uploads the source from the device, and saves it under the
specified output path.

```
**Parameter**: archive_path (str)
:   The local path where to save the project archive. (Usually
    ending with the extension .prj).

:::
Note

This method will throw various Exceptions on errors.
:::
```

## IScriptPouObjectCollection

Base: object

A collection of POUs which are executed by a task.

This interface is exported to python, and thus adheres to python
naming standards.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`__len__`()

:   Gets the length.

```
**Returns**: (int)
:   The number of POUs.
```

`add`(*pou_name*, *comment*)

:   Add a POU to the list.

```
**Parameter**: pou_name (str)
:   Name of the POU

**Parameter**: comment (str)
:   Optional comment about this entry
```

`insert`(*index*, *pou_name*, *comment*)

:   Insert a POU to the list at the specified index.

```
**Parameter**: index (int)
:   Index of a POU at which a new POU should be insert.

**Parameter**: pou_name (str)
:   Name of the POU

**Parameter**: comment (str)
:   Optional coment about this entry
```

`remove`(*index*)

:   Remove a POU from the list at the specified index.

```
**Parameter**: index (int)
:   Index of a POU which should be removed.
```

`remove`(*pou_name*)

:   Remove the first POU with the specified name from the list.

```
**Parameter**: pou_name (str)
:   Name of the POU
```

`replace`(*index*, *pou_name*, *comment*)

:   Replace the POU in the list at the specified index.

```
**Parameter**: index (int)
:   Index of a POU which should be replaced.

**Parameter**: pou_name (str)
:   Name of the POU

**Parameter**: comment (str)
:   Optional comment about this entry
```

## IScriptProject

Base: object

Extension interface for IScriptProject7 since V3.5.5.0

`Equals`(*other*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System](https://social.msdn.microsoft.com/Search/?query=System).IEquatable\`1.Equals for more information!

`Extender`

:   Gets the Extender instance for the current object.

`active_application`

:   Gets or sets the active application.

```
:::
Note

This is a property. You can read or assing a IScriptObjekt for the
application you want to be the active application.
:::
```

`check_all_pool_objects`()

:   Checks all pool objects. This command only works reliable for
libraries, and when called on primary projects.

```
:::
Note

You can use the [ISystem.get_messages] and
[ISystem.get_message_objects] calls to check
whether any messages were added.
:::
```

`clean_all`()

:   Performs a "Clean All".

`close`()

:   Closes this project. The corresponding Object Manager project will
also be closed. If this project has got unsaved changes, these
changes will be discarded.

`create_folder`(*foldername*)

:   Creates a folder with the specified foldername in the POU view.

```
**Parameter**: foldername (str)
:   The foldername.
```

`create_folder`(*foldername*, *structured_view*)

:   Creates a folder with the specified foldername.

```
**Parameter**: foldername (str)
:   The foldername.

**Parameter**: structured_view (Guid)
:   The structured view. This parameter is optional, if you pass
    Guid.Empty or omit the parameter, the "POU" view is used.

:::
Note

There are three predefined structured views, and the guids are
provided as constants:

-   *SV_DEV*: The device view, The device view,:: SV_DEV =
    Guid("{D9B2B2CC-EA99-4c3b-AA42-1E5C49E65B84}")
-   *SV_POU*: The POU view, The POU view,:: SV_POU =
    Guid("{21AF5390-2942-461a-BF89-951AAF6999F1}")

The Modules View currently does not support folders, so no GUID is
provided.
:::
```

`dirty`

:   Gets a boolean value indicating whether this project has been
changed since the last call to save().

`document`(*objects*)

:

`document`(*objects*)

:

`export_doc`(*path*, *ext_path*, *formatting*)

:   Exports the documentation for primary project in JSON format into
a string, or a file at the given path.

```
**Parameter**: path (str)
:   The path of the file we export into. If omitted, we export
    into a string and return that string. (This parameter is
    optional.)

**Parameter**: ext_path (str)
:   The path where external documentation files should be
    exported. If ommited, the same path as in **path** is used. If
    both ommited, the external documentation media is ignored.

**Parameter**: formatting (\_3S.CoDeSys.DocExport.Formatting)
:   [Formatting] of the export file.

**Returns**: (str)
:   The exported JSON as string, or null if a filepath is given.
```

`export_native`(*objects*, *destination*, *recursive*, *one_file_per_subtree*, *profile_name*, *reporter*)

:

`export_xml`(*reporter*, *objects*, *path*, *recursive*)

:

`export_xml`(*reporter*, *objects*, *path*, *recursive*, *export_folder_structure*)

:

`export_xml`(*reporter*, *objects*, *path*, *recursive*, *export_folder_structure*, *declarations_as_plaintext*)

:

`export_xml`(*objects*, *path*, *recursive*, *export_folder_structure*, *declarations_as_plaintext*)

:

`find`(*names*)

:   Finds objects matching the given path.

```
:::
Note

Names are not unique in the tree, so several Objects can be
delivered. The search is against the nonlocalized name and
non-recursive.
:::

**Parameter**: names (String\[\])
:   The path of names to follow.

**Returns**: (list)
:   The collection of objects.
```

`find`(*name*, *recursive*)

:   Finds objects matching the given name.

```
:::
Note

Names are not unique in the tree, so several Objects can be
delivered. The search is against the nonlocalized name.
:::

**Parameter**: name (str)
:   The name.

**Parameter**: recursive (bool)
:   Whether we search recursively (This parameter is optional,
    default = false).

**Returns**: (list)
:   The collection of objects.
```

`generate_runtime_system_files`(*destination_directory*, *generate_m4*, *generate_c*)

:   Generate_runtime_system_fileses the specified
destination_directory.

```
**Parameter**: destination_directory (str)
:   The destination_directory. Relative pathes are interpreted
    relative to the project location. If you pass None or the
    empty string, the project directory is used.

**Parameter**: generate_m4 (bool)
:   if set to **True**, M4 code is generated.

**Parameter**: generate_c (bool)
:   if set to **True**, C Code is generated.

:::
Note

At least one of **generate_m4** and **generate_c**must be set.
:::
```

`get_children`(*recursive*)

:   Gets the children of our object.

```
**Parameter**: recursive (bool)
:   If set to **True**, we work recursive (This parameter is
    optional, default = false).

**Returns**: (list)
:   All child objects.
```

`get_project_info`()

:   Gets the project information object, implicitly creating one if
not existing yet.

```
**Returns**: (IScriptObject)
:   The project information object.
```

`handle`

:   Gets the internal Automation Platform handle of the Project.

```
:::
Note

This handle is primarily useful for other Atomation Platform
plugins which provide functionality for scripts via IScriptDriver.
When they consume IScriptProjects as their parameters, they can
use the handle to gain access to the underlying Automation
Platform object.
:::
```

`has_project_info`

:   Gets a value indicating whether this [IScriptProject](#iscriptproject) already has a
project information object.

`import_native`(*filenames*, *filter*, *handler*)

:

`import_native`(*filename*, *filter*, *handler*)

:   Imports the specified files in the native xml format in the top
level of this project.

```
**Parameter**: filename (str)
:   The filename.

**Parameter**: filter (NativeImportFilter)
:   The filter - if null is passed, all files are imported.

**Parameter**: handler (NativeImportHandler)
:   The handler - if null passed, the default handler is used.
```

`import_xml`(*conflictResolve*, *dataOrPath*, *import_folder_structure*)

:   Imports the contents of the specified PLCopenXML file into the top
level of the project.

```
**Parameter**: conflictResolve (ConflictResolve)
:   The conflict resolution strategy.

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Parameter**: import_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also imported.

:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML file. (On other common platforms like unix and OSX,
\< is uncommon and discouraged in file names.) This heuristics may
be replaced by a more sophisticated heuristics in the future. This
method will report the progress as script messages.
:::
```

`import_xml`(*reporter*, *dataOrPath*)

:   Imports the contents of the specified PLCopenXML file into the top
level of the project.

```
:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML file. (On other common platforms like unix and OSX,
\< is uncommon and discouraged in file names.) This heuristics may
be replaced by a more sophisticated heuristics in the future.
:::

**Parameter**: reporter (ImportReporter)
:   The import reporter.

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.
```

`import_xml`(*reporter*, *dataOrPath*, *import_folder_structure*)

:   Imports the contents of the specified PLCopenXML file into the top
level of the project.

```
:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML file. (On other common platforms like unix and OSX,
\< is uncommon and discouraged in file names.) This heuristics may
be replaced by a more sophisticated heuristics in the future.
:::

**Parameter**: reporter (ImportReporter)
:   The import reporter.

**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Parameter**: import_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also imported.
```

`import_xml`(*dataOrPath*, *import_folder_structure*)

:   Imports the contents of the specified PLCopenXML file into the top
level of the project.

```
**Parameter**: dataOrPath (str)
:   The PLCopenXML file path, or the PLCOpenXML as string.

**Parameter**: import_folder_structure (bool)
:   if set to **True**, the folder structure of the objects is
    also imported.

:::
Note

The heuristics to find out whether the content is a file or
directly an XML string currently is as follows: if it contains the
'\<' character, it is regarded as an XML file. Rationale: On
windows, \< is an invalid char in path names, and it is contained
in every XML file. (On other common platforms like unix and OSX,
\< is uncommon and discouraged in file names.) This heuristics may
be replaced by a more sophisticated heuristics in the future. This
method will apply [ConflictResolve.Copy] as
strategy.
:::
```

`is_root`

:   Gets a value indicating whether this instance is the root of the
object tree. This returns true for all ScriptProject instances,
and false for all ScriptObject instances.

`library`

:   Gets a boolean value indicating whether the project is a
background library project. Those projects represent a library
which was loaded because it is referenced by the primary project
(directly or indirectly). It will automatically be closed when the
primary project is closed.

```
:::
Note

If you want to check whether the primary project is a library or
not, check whether the [IScriptProject.path]
ends with ".library" or ".project".
:::
```

`login`(*username*, *password*)

:   Log into the project using the specified credentials.

```
**Parameter**: username (str)
:   The username.

**Parameter**: password (str)
:   The password.
```

`logout`()

:   Log out from the project (back to the user "nobody").

`path`

:   Gets the absolute path where this project is physically stored.

```
:::
Note

To change that path, use save_as().
:::
```

`primary`

:   Gets a boolean value indicating whether the primary attribute has
been set for this project. The primary project is the one the user
is currently working with.

```
:::
Note

The other, non-primary projects (aka background projects) can
serve several purposes, for example:

-   Libraries referenced by the primary project.
-   Projects opened for comparison by the "Compare Project"
    command.
-   Temporary projects created for various purposes, e. G. by the
    V2.3 import converter, or the CODESYS SVN add-on.

Those projects are not directly user visible, and you should not
modify or close them from within your scripts.
:::
```

`project`

:   Gets the project.

```
:::
Note

This returns "this" rsp. "self" if called on Projects.
:::
```

`save`()

:   Saves this project at its physical location (see path).

```
:::
Note

The encryption settings are not changed.
:::
```

`save_archive`(*path*)

:   Saves the project as an archive. All additional categories which
are selected by default are included, but no extra files.

```
**Parameter**: path (str)
:   The path to save the archive.
```

`save_archive`(*path*, *additional_categories*)

:   Save_archives the specified path.

```
**Parameter**: path (str)
:   The path to save the archive.

**Parameter**: additional_categories (IEnumerable\`1)
:   The categories of additional items to include in the project
    archive.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_categories**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`save_archive`(*path*, *additional_files*, *additional_categories*)

:

`save_archive`(*path*, *additional_files*, *additional_categories*)

:   Save_archives the specified path.

```
**Parameter**: path (str)
:   The path to save the archive.

**Parameter**: additional_files (String\[\])
:   The additional (external) files to include into the archive.

**Parameter**: additional_categories (IEnumerable\`1)
:   The additional categories of items to include into the
    archive.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_categories**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`save_archive`(*path*, *additional_categories*)

:   Save_archives the specified path.

```
**Parameter**: path (str)
:   The path where to save the project archive.

**Parameter**: additional_categories (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.IScriptProjectArchiveCategory\[\])
:   The additional_categories.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_categories**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`save_archive`(*path*, *comment*, *additional_files*, *additional_categories*)

:

`save_archive`(*path*, *comment*, *additional_files*, *additional_categories*)

:

`save_archive`(*path*, *comment*, *additional_files*, *additional_categories*)

:   Save_archives the specified path.

```
**Parameter**: path (str)
:   The path to save the archive.

**Parameter**: comment (str)
:   The comment.

**Parameter**: additional_files (String\[\])
:   The additional_files.

**Parameter**: additional_categories (IEnumerable\`1)
:   The categories of additional items to include in the project
    archive.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_categories**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`save_archive`(*path*, *comment*, *additional_categories*)

:   Saves the project as an archive. All additional categories which
are selected by default are included, but no extra files.

```
**Parameter**: path (str)
:   The path to save the archive.

**Parameter**: comment (str)
:   The commend to set for the archive.

**Parameter**: additional_categories (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.IScriptProjectArchiveCategory\[\])
:   The categories of additional items to include in the project
    archive.

:::
Note

For a definition of the additional items, see
[IScriptProjectArchiveCategories]. If you
don't pass any **additional_categories**,
[IScriptProjectArchiveCategories.default] is
used. To exclude all additional items, explixitly pass None.
:::
```

`save_as`(*path*, *password*)

:   Saves the project under a new filename and with different
encryption.

```
:::
Note

If no password is given (null / None is passed), encryption stays
as it is. If the password given, but an empty string, encryption
is disabled. Otherwise, the password is used as new password to
encrypt the project. If you want to change password without
changing the path, use proj.save_as(proj.path, "myPassword");
:::

**Parameter**: path (str)
:   The new path to save the project.

**Parameter**: password (str)
:   The password. (This parameter is optional.)
```

`save_as_compiled_library`(*destination_name*)

:   Save the current project as a compiled library. (This command
currently only works for the primary project.)

```
**Parameter**: destination_name (str)
:   The destination_name.

:::
Note

The **destination_name** has the following semantics: If it is
omitted or the empty string, the full project path will be used,
with the extension changed to ".compiled_library". If the name of
an existing directory is given, the library will be saved there,
using the project base name and the extension changed to
".compiled_library". Otherwise, the destination name will be
interpreted as the path relative to where the current project re.
:::
```

`user_management`

:   Returns the user management object for this project.

```
**Exception**: Exception
:   If no user management is available.
```

## IScriptProjectArchiveCategory

Base: object

Represents a category of items which can be included into a project
archive.

`description`

:   Gets a description for this project category. This string should
be localized.

`guid`

:   Gets the Guid for this category.

`name`

:   Gets a display name for this project category, e.g. "Referenced
libraries". This string should be localized.

`selected_by_default`

:   Gets a boolean value indicating whether this category should be
selected for project archive inclusion per default. This is a hint
for the presentation layer.

## IScriptProjectDeviceExtension

Base: object

Functionality to add top-level devices (e. G. SPS) to projects.
IScriptProject instances are amended with this objects.

:::
Note

This interface is exported to python, and thus adheres to python
naming standards.
:::

`add`(*name*, *device*, *module*)

:   Adds the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: device (IDeviceId)
:   The device id.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

`add`(*name*, *type*, *id*, *version*, *module*)

:   Adds the specified device.

```
**Parameter**: name (str)
:   Name of the device.

**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device identification.

**Parameter**: version (str)
:   The device version.

**Parameter**: module (str)
:   The module ID. (This parameter is optional.)
```

## IScriptProjectInfoMarker

Base: object

The all objects are extended with this interface, since CoDeSys V3.5
SP2

`is_project_info`

:   Gets a value indicating whether this
[IScriptProjectInfoMarker](#iscriptprojectinfomarker) is the
project info object.

## IScriptProjectInfoObject

Base: object

The project information objects are extended with this interface,
since CoDeSys V3.5 SP2

`author`

:   Gets or sets the author.

`categories`

:   If the project is used as a library, it appears under the
following categories.

`change_accessor_generation`(*generate_accessors*)

:   Changes the generate_accessor flag.

```
**Parameter**: generate_accessors (bool)
:   if set to **True**, the accessors are generated.

:::
Note

As changing this flag is potentially expensive (genrating several
POUs), it is an explicit function and no property setter.
:::
```

`company`

:   Gets or sets the company.

```
:::
Note

Libraries are uniquely identified by the tuple
([IScriptProjectInfoObject.company],
[IScriptProjectInfoObject.title],
[IScriptProjectInfoObject.version]).
:::
```

`default_namespace`

:   Gets or sets the default namespace when the project is used as a
library.

`description`

:   Gets or sets the description.

```
:::
Note

This string may be multiline.
:::
```

`dongle_licencing_active`

:   Gets or sets a value indicating whether this library has dongle
license protection.

```
:::
Note

If dongle licensing is activated, the user needs to connect a
dongle containing the appropriate license in order to use this
library. For the licensing to work correctly, bot firm_code and
product_code MUST be specified. Please note that only compiled
libraries will be protected!
:::

**Exception**: InvalidOperationException
:   When setting to True, but
    [IScriptProjectInfoObject.dongle_licensing_firm_code]or
    [IScriptProjectInfoObject.dongle_licensing_product_code] are not set.
```

`dongle_licensing_activation_mail`

:   Gets or sets the dongle licensing activation email address.

`dongle_licensing_activation_url`

:   Gets or sets the dongle licensing activation url.

`dongle_licensing_firm_code`

:   Gets or sets the dongle licensing firm code.

```
:::
Note

If dongle licensing is activated, the user needs to connect a
dongle containing the appropriate license in order to use this
library. For the licensing to work correctly, bot firm_code and
product_code MUST be specified. Please note that only compiled
libraries will be protected!
:::

**Exception**: InvalidOperationException
:   When trying to unset this value while
    [IScriptProjectInfoObject.dongle_licencing_active] is set.

**Exception**: ArgumentOutOfRangeException
:   When trying to set this to a negative value.
```

`dongle_licensing_product_code`

:   Gets or sets the dongle licensing product code.

```
:::
Note

If dongle licensing is activated, the user needs to connect a
dongle containing the appropriate license in order to use this
library. For the licensing to work correctly, bot firm_code and
product_code MUST be specified. Please note that only compiled
libraries will be protected!
:::

**Exception**: InvalidOperationException
:   When trying to unset this value while
    [IScriptProjectInfoObject.dongle_licencing_active] is set.

**Exception**: ArgumentOutOfRangeException
:   When trying to set this to a negative value.
```

`generate_accessors`

:   Gets a value indicating whether this
[IScriptProjectInfoObject](#iscriptprojectinfoobject)
generates property accessor POU objects or not.

`is_project_info`

:   Gets a value indicating whether this
[IScriptProjectInfoMarker](#iscriptprojectinfomarker) is the
project info object.

`released`

:   Gets or sets a value indicating whether the project containing
this [IScriptProjectInfoObject](#iscriptprojectinfoobject) is
released.

```
:::
Note

Released library projects should not be modified any more. Unsed
the released flag and change the version if you want to modify a
released library.
:::
```

`title`

:   Gets or sets the title.

```
:::
Note

Libraries are uniquely identified by the tuple
([IScriptProjectInfoObject.company],
[IScriptProjectInfoObject.title],
[IScriptProjectInfoObject.version]).
:::
```

`values`

:   Gets the custom property dictionary.

```
:::
Note

The following types are allowed:

  ------------------------------------------------------------------------------------------------
  Type                               Description
  ---------------------------------- -------------------------------------------------------------
  [String]      Textual properties.

  [[DateTime]{.std                   Date / time properties.
  .std-ref}](#datetime)

  [Int32]       Numerical properties.

  [Boolean]     Boolean properties.

  [Version]     Version properties, they may also be passed as [String] or tuple / sequence of integers.
  ------------------------------------------------------------------------------------------------

You're responsible yourself to set the correct type. Any
inconsistencies or problems introduced by fiddling with this
dictionary are your own responsibility.

Some properties are defined in the online help: See the section
"Libraries -\> Guidelines for creating Libraries -\> Library
Development Summary -\> CODESYS LibDevSummary V3.5.4.0 -\>
Concepts and Elements -\> Library Properties": The following types
are allowed:

  ------------------------------------------------------------------------------------------------
  Type                               Description
  ---------------------------------- -------------------------------------------------------------
  [String]      Textual properties.

  [[DateTime]{.std                   Date / time properties.
  .std-ref}](#datetime)

  [Int32]       Numerical properties.

  [Boolean]     Boolean properties.

  [Version]     Version properties, they may also be passed as [String] or tuple / sequence of integers.
  ------------------------------------------------------------------------------------------------

You're responsible yourself to set the correct type. Any
inconsistencies or problems introduced by fiddling with this
dictionary are your own responsibility.

Some properties are defined in the online help: See the section
"Libraries -\> Guidelines for creating Libraries -\> Library
Development Summary -\> CODESYS LibDevSummary V3.5.4.0 -\>
Concepts and Elements -\> Library Properties":

Name Type Description Required Company Text Serves for structuring
(filter) in the "Add Library" dialog Required Title Text Name of
the library Required Version Version Library verison Released Bool
A library should not be modified after having been released Author
Text Author of the current library version DefaultNamespace Text
World-wide unique prefix, for defining the scope of the symbols of
the library Description Text Short description of the purpose of
the library Placeholder Text which Placeholder should be used for
referencing the library IsContainerLibrary Bool This library
follwos the rules for a Container Library IsInterfaceLibrary Bool
This library follows the rules for a Interface Library
LanguageModelAttribute Text The access on symbols of the library
is only possible via Namespace/Prefix IsEndUserLibrary Bool This
Library is especially designed for the needs of end users
:::
```

`version`

:   Gets or sets the version.

```
:::
Note

Libraries are uniquely identified by the tuple
([IScriptProjectInfoObject.company],
[IScriptProjectInfoObject.title],
[IScriptProjectInfoObject.version]).
:::
```

## IScriptRepositorySource

Base: object

Repository source.

`is_internal`

:   Is the repository source internal?

```
:::
Note

If true, then this repository source is an implicit source (like
the project internal repository or the installation specific
repository). Therefore its properties like name and location are
readonly and may not be changed.
:::
```

`location_url`

:   Get or set the location URL.

`name`

:   Get or set the name of the repository source.

## IScriptRepositorySourceList

Base: object

A collection of [IScriptRepositorySource](#iscriptrepositorysource) objects.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`__len__`()

:   Gets the length (number of sources).

```
**Returns**: (int)
:   The number of sources.
```

`add`(*name*, *location_url*)

:   Add a new repository source with the specified name.

```
**Parameter**: name (str)
:   Name for the new source.

**Parameter**: location_url (str)
:   Optional,

**Returns**: (IScriptRepositorySource)
:   The added repository source.
```

`move`(*source*, *index*)

:   Move an existing repository source to the specified location in
the collection.

```
**Parameter**: source (IScriptRepositorySource)
:   Existing repository source.

**Parameter**: index (int)
:   New index of the repository source.
```

`remove`(*source*)

:   Remove an existing repository source.

```
**Parameter**: source (IScriptRepositorySource)
:   The repository source to remove.

:::
Note

Internal sources cannot be removed.
:::
```

## IScriptScanTargetDescription

Base: object

Description of a scan target found during a device scan.

`address`

:   Gets the router address for this device. An hierarchical
addressing scheme is used. Example: "123.5". Each component of the
router address corresponds to an array element of the return
value.

`block_driver`

:   Property to access the type of block driver used for this target

`block_driver_address`

:   Property to store and retrieve the driver-specific address for
this target.

`device_id`

:   Gets the ID of the type to be matched with the installed device
types (target descriptions).

`device_name`

:   Gets the name of the device. Example: "PLCFeeder". If no name has
been explicitly assigned to the device, it is derived from the
corresponding router address, e.g. "@127.5".

`locked_in_cache`

:   If set to true, the devicedescription will stay in the gateways
device cache, even during rebuild. So this is not a property of
the device itself but a property of the device description object
and may be changed by plugins.

`parent_address`

:   Get the router address of the parent node of this device. Usually
this will be the device address without the last address
component. Is null if the parentAddress is unknown.

`type_name`

:   Gets a string indicating the device type. Example: "Beckhoff
CX1000-100" or "BRC Motion Logic Controller".

`vendor_name`

:   Gets a string indicating the device vendor. Example: "Beckhoff" or
"BRC".

## IScriptSymbolConfigObject

Base: object

Functionality for manipulating symbol configuration objects.

This interface is exported to python, and thus adheres to python
naming standards.

`available_client_side_layout_calculators`

:   Gets all currently known layout calculators.

`check_effective_direct_io_access`()

:   Checks whether and why the direct Access to the I/O Area is
effectively enabled / disabled.

```
**Returns**: (DirectIoAccessObstacles)
:   The [DirectIoAccessObstacles](#directioaccessobstacles)
    flag describing which reasons prevent the Direct IO Access
    from being enabled.

:::
Note

Enabling direct access to the I/O area is supported for debugging
purposes, e. G. testing the cables and connections. It is not
meant for productive operation. It is only available under certain
conditions, e. G. the compiler version must be \>= V3.5.8.0 and
the symbol config must not be generated as a child application.
:::
```

`client_side_layout_calculator`

:   Gets or sets the calculator object denoting the currently
configured client side layout calculator.

```
:::
Note

Currently, two different values are allowed: [Guid.Empty] to use the Compatibility Offset Calculator which is
always available. And "{0141eb75-141b-4ea1-9a8c-75f952b22a6c}" to
use the OptimizedOutputOffsetCalculator which is new with V3.5.7.0
and also requires the compiler version 3.5.7.0 (see
[http://jira.3s-software.com/browse/CDS-41816](http://jira.3s-software.com/browse/CDS-41816)). This scheme may be extended to allow more or even
arbitrary offset calculators in the future.
:::
```

`client_side_layout_calculator_guid`

:   Gets or sets the Guid denoting the currently configured client
side layout calculator.

```
:::
Note

Currently, two different values are allowed: [Guid.Empty] to use the Compatibility Offset Calculator which is
always available. And "{0141eb75-141b-4ea1-9a8c-75f952b22a6c}" to
use the OptimizedOutputOffsetCalculator which is new with V3.5.7.0
and also requires the compiler version 3.5.7.0 (see
[http://jira.3s-software.com/browse/CDS-41816](http://jira.3s-software.com/browse/CDS-41816)). This scheme may be extended to allow more or even
arbitrary offset calculators in the future.
:::
```

`content_feature_flags`

:   The configured content feature flags. This is partially redundant
with \[ISymbolConfigObject5.ExportCommentsInXML\]and \[ISymbolConfigObject6.SupportOPCUA\].

`effective_content_feature_flags`

:   The effective content feature flags, considering the
\[IScriptSymbolConfigObject.content_feature_flags\]and the compiler version setting.

`effective_symbol_attribute_filter_type`

:   The effective filter type, considering compiler version and other
side conditions.

`effective_symbol_comment_filter_type`

:   The effective comment filter type, considering compiler version
and other side conditions.

`enable_direct_io_access`

:   Gets or sets a boolean whether direct Access to the I/O Area is
configured.

```
:::
Note

Enabling direct access to the I/O area is supported for debugging
purposes, e. G. testing the cables and connections. It is not
meant for productive operation. It is only available under certain
conditions, e. G. the compiler version must be \>= V3.5.8.0 and
the symbol config must not be generated as a child application.
:::
```

`get_all_datatypes`(*compile*)

:   Get all data types (compiler and configured).

```
**Parameter**: compile (bool)
:   If True, build the application before generating the list. If
    the application was not build before, the returned list is
    empty.

**Returns**: (IScriptSymbolConfigSignatureCollection)
:   Collection of data types.
```

`get_all_signatures`(*compile*)

:   Get all signatures (compiler and configured).

```
**Parameter**: compile (bool)
:   If True, build the application before generating the list. If
    the application was not build before, the returned list is
    empty.

**Returns**: (IScriptSymbolConfigSignatureCollection)
:   Collection of signatures.
```

`get_direct_io_obstacle_explanations`(*obstacles*)

:   Gets user readable, localized messages / explanations of the
obstacles.

```
**Parameter**: obstacles (DirectIoAccessObstacles)
:   The obstacles.

**Returns**: (list)
:   A list of strings with one entry for each obstacle, or an "is
    enabled" message when **obstacles** ==
    [DirectIoAccessObstacles.None].
```

`get_only_configured_datatypes`()

:   Get only the configured data types.

```
**Returns**: (IScriptSymbolConfigSignatureCollection)
:   Collection of signatures.
```

`get_only_configured_signatures`()

:   Get only the configured signatures.

```
**Returns**: (IScriptSymbolConfigSignatureCollection)
:   Collection of signatures.
```

`get_symbol_configuration_xsd`()

:   Gets the current symbol configuration XML schema, as appropriate
for the current symbol config object.

```
**Returns**: (Byte\[\])
:   The current symbol configuration XML schema as byte array.

:::
Note

The schema is delivered as a byte array, containing the UTF-8
encoded XSD file as it is also published in the
[http://www.3s-software.com/schemas/Symbolconfiguration.xsd](http://www.3s-software.com/schemas/Symbolconfiguration.xsd).
:::
```

`is_symbol_config`

:   Gets a value indicating whether this instance is a symbol config
object.

`symbol_attribute_filter_data`

:   Describes the filter data for
\[SymbolAttributeFilterTypes.Prefix\] and
\[SymbolAttributeFilterTypes.Regex\].

`symbol_attribute_filter_type`

:   The configured filter type for the attributes.

`symbol_comment_filter_type`

:   The configured comment filter type.

## IScriptSymbolConfigObjectMarker

Base: object

Every IScriptObject instance will be extended with this method.

This interface is exported to python, and thus adheres to python
naming standards.

`is_symbol_config`

:   Gets a value indicating whether this instance is a symbol config
object.

## IScriptSymbolConfigSignature

Base: object

Signature element of the symbol configuration.

`full_qualified_name`

:   The full qualified name of this element. For example:

`library_id`

:   The identification of the library where this signature is
declared.

`name`

:   The name of this element.

`namespace_path`

:   Namespace path of the library where this signature is declared.

`variables`

:   The variables of the signature.

## IScriptSymbolConfigSignatureCollection

Base: object

Collection of symbol configuration signatures.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`__len__`()

:   Gets the length (number of signatures).

```
**Returns**: (int)
:   The number of signatures.
```

`find`(*name*, *library_id*)

:   Get the first [IScriptSymbolConfigSignature](#iscriptsymbolconfigsignature)
with the specified name and libarary ID which should be fully
qualified.

```
**Parameter**: name (str)
:   Name of a signature.

**Parameter**: library_id (str)
:   Library ID.

**Returns**: (IScriptSymbolConfigSignature)
:   Signature of the symbol configuration. Otherwise None.
```

## IScriptSymbolConfigVariable

Base: object

Variable element of the symbol configuration.

`alias_type`

:   The name of the alias type.

```
:::
Note

For variables with aliased types, the [Type],
[ISymbolConfigVariable.VariableType]and
[ISymbolConfigVariable2.FullQualifiedBaseType] properties point to the effective, resolved type. Use
this member in the UI to display the alias type used in the
source. This member is only valid for objects parsed from the
compiler, not for configured symbol config instances.
:::
```

`attribute_access`

:   Gets the attribute access. When
\[IScriptSymbolConfigVariable.attribute_access\] is false, the result of this member is undefined.

`comment`

:   Gets the comment of the signature or variable, or an empty string
if no comment is available.

```
:::
Note

This member is only valid for objects parsed from the compiler,
not for configured symbol config instances.
:::
```

`configured_access`

:   The allowed symbolic access to this variable

`effective_access`

:   The effective symbolic access to this variable.

`exported_via_attribute`

:   Gets a value indicating whether this variable is configured via
compiler attribute.

`full_qualified_base_type`

:   Gets the full qualified base type of the member.

```
:::
Note

This is currently only set for supported data types (userdef and
array).
:::
```

`maximal_access`

:   The maximal access that is allowed for this variable, decided by
the given attributes

`name`

:   The name of this variable

`type`

:   The type of this variable, as the user declared it.

`type_library_id`

:   Gets the library id, when the type of the member is from a
library.

```
:::
Note

This is currently only set for supported data types (userdef and
array).
:::
```

## IScriptSymbolConfigVariableCollection

Base: object

Collection of symbol configuration variables.

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`__len__`()

:   Gets the length (number of signatures).

```
**Returns**: (int)
:   The number of signatures.
```

## IScriptTaskConfigObject

Base: object

Functionality for manipulating task configuration objects.

This interface is exported to python, and thus adheres to python
naming standards.

`create_task`(*name*)

:   Add a task object to a task configuration.

```
**Returns**: (IScriptObject)
:   Script object of the task object
```

`is_task_configuration`

:   Gets a value indicating whether this instance is a task
configuration object.

## IScriptTaskConfigObjectMarker

Base: object

Every IScriptObject instance will be extended with this method.

This interface is exported to python, and thus adheres to python
naming standards.

`is_task_configuration`

:   Gets a value indicating whether this instance is a task
configuration object.

## IScriptTaskObject

Base: object

Functionality for manipulating task objects.

This interface is exported to python, and thus adheres to python
naming standards.

`core_binding`

:   Core binding. On multicore deivce each task can have an optional
core binding.

`event`

:   Use event to trigger the task.

```
Requires the property [IScriptTaskObject.kind_of_task] to be set to [KindOfTask.Event] or
[KindOfTask.Status].
```

`event_pou_guid`

:   Guid of POU for event.

`external_event`

:   Use external event to trigger the task.

```
Requires the property [IScriptTaskObject.kind_of_task] to be set to [KindOfTask.ExternalEvent].
```

`interval`

:   Interval of the task.

```
Requires the property [IScriptTaskObject.kind_of_task] to be set to [KindOfTask.Cyclic]or
[KindOfTask.ExternalEvent] if the device
supports it.
```

`interval_unit`

:   Unit used for the \[IScriptTaskObject.interval\].

```
Requires the property [IScriptTaskObject.kind_of_task] to be set to [KindOfTask.Cyclic]or
[KindOfTask.ExternalEvent] if the device
supports it.
```

`is_task`

:   Gets a value indicating whether this instance is a task object.

`kind_of_task`

:   Kind of task.

`name`

:   Name of the task.

`parent_synchron_task`

:   Task of the device application which allows synchronous calls to
child application in bus cycle.

```
Requires the property [IScriptTaskObject.kind_of_task] to be set to [KindOfTask.ParentSynchron].
```

`pous`

:   Collection of POUs which are executed by the task.

`priority`

:   Priority of the task.

`watchdog`

:   Settings for the watchdog of the task.

## IScriptTaskObjectMarker

Base: object

Every IScriptObject instance will be extended with this method.

This interface is exported to python, and thus adheres to python
naming standards.

`is_task`

:   Gets a value indicating whether this instance is a task object.

## IScriptTextListItemsCollection

Base: object

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic](https://social.msdn.microsoft.com/Search/?query=System.Collections.Generic).IEnumerable\`1.GetEnumerator for more information!

`Item`

:

`__len__`()

:

`add`(*id*, *defaulttext*)

:

`remove`(*id*)

:

## IScriptTextListMarker

Base: object

`is_textlist`

:

## IScriptTextListObject

Base: object

`addlanguage`(*language*)

:

`checkids`()

:

`export`(*exportfile*)

:

`exportonlydifference`(*importfile*, *exportfile*)

:

`getlanguage`(*index*)

:

`importfile`(*importfile*)

:

`importreplacementfile`(*importfile*)

:

`is_textlist`

:

`languagecount`()

:

`removelanguage`(*language*)

:

`removeunusedids`()

:

`rows`

:

`updatetextids`()

:

## IScriptTextListObjectContainer

Base: object

`create_textlist`(*name*)

:

`get_global_textlist`()

:

`has_global_textlist`

:

## IScriptTextListRow

Base: object

`defaulttext`

:

`id`

:

`languagetext`(*index*)

:

`languagetextcount`()

:

`setdefaulttext`(*defaulttext*)

:

`setlanguagetext`(*language*, *text*)

:

## IScriptTreeObject

Base: object

Common base functionality for IScriptObject and IScriptProject.

This interface is exported to python, and thus adheres to python
naming standards.

`find`(*names*)

:   Finds objects matching the given path.

```
:::
Note

Names are not unique in the tree, so several Objects can be
delivered. The search is against the nonlocalized name and
non-recursive.
:::

**Parameter**: names (String\[\])
:   The path of names to follow.

**Returns**: (list)
:   The collection of objects.
```

`find`(*name*, *recursive*)

:   Finds objects matching the given name.

```
:::
Note

Names are not unique in the tree, so several Objects can be
delivered. The search is against the nonlocalized name.
:::

**Parameter**: name (str)
:   The name.

**Parameter**: recursive (bool)
:   Whether we search recursively (This parameter is optional,
    default = false).

**Returns**: (list)
:   The collection of objects.
```

`get_children`(*recursive*)

:   Gets the children of our object.

```
**Parameter**: recursive (bool)
:   If set to **True**, we work recursive (This parameter is
    optional, default = false).

**Returns**: (list)
:   All child objects.
```

`handle`

:   Gets the internal Automation Platform handle of the Project.

```
:::
Note

This handle is primarily useful for other Atomation Platform
plugins which provide functionality for scripts via IScriptDriver.
When they consume IScriptProjects as their parameters, they can
use the handle to gain access to the underlying Automation
Platform object.
:::
```

`is_root`

:   Gets a value indicating whether this instance is the root of the
object tree. This returns true for all ScriptProject instances,
and false for all ScriptObject instances.

`project`

:   Gets the project.

```
:::
Note

This returns "this" rsp. "self" if called on Projects.
:::
```

## IScriptUI

Base: object

The script can interact with the user via this instance.

:::
Note

Please note that some of the functionalities depend on the currently
installed MessageService instance.

In --noUI-Mode (console-only mode), a basic, somehow restricted
implementation querying the user via text input is provided instead.
Especially multi-line input is not user friendly, and store_key or
predefined values for text input do not work. But as --noUI-Mode is
primarily meant for unattended batch execution, it is a bad idea to
ask the user in general.
:::

`browse_directory_dialog`(*message*, *path*, *root_folder*, *new_folder_button*)

:

`choose`(*message*, *options*, *initial_selection*, *cancellable*, *message_key*, *arguments*)

:

`error`(*message*, *message_key*, *arguments*)

:   Reports an error message to the user. This method blocks until the
user has acknowledged this message.

```
**Parameter**: message (str)
:   The message to display the user.

**Parameter**: message_key (str)
:   The message key, for automated filtering / handling by
    prompt_answers or similar mechanism by other plugins (e. G.
    automated test tools). Most users can leave the default here.

**Parameter**: arguments (Object\[\])
:   Optional objects which build the variable part of the message.
    In other words, if **message** is build via a string
    formatting operation, the arguments of that formatting
    operation should be passed as **arguments** here. This is for
    advanced usages via automated test tools, most users can
    ignore it.
```

`info`(*message*, *message_key*, *arguments*)

:   Reports an informational message to the user. This method blocks
until the user has acknowledged this message.

```
**Parameter**: message (str)
:   The message to display the user.

**Parameter**: message_key (str)
:   The message key, for automated filtering / handling by
    prompt_answers or similar mechanism by other plugins (e. G.
    automated test tools). Most users can leave the default here.

**Parameter**: arguments (Object\[\])
:   Optional objects which build the variable part of the message.
    In other words, if **message** is build via a string
    formatting operation, the arguments of that formatting
    operation should be passed as **arguments** here. This is for
    advanced usages via automated test tools, most users can
    ignore it.
```

`open_file_dialog`(*title*, *filename*, *directory*, *filter*, *filter_index*, *default_extension*, *stateguid*, *multiselect*, *check_file_exists*, *check_path_exists*)

:

`prompt`(*message*, *choice*, *default_result*, *store_description*, *store_key*, *message_key*, *arguments*)

:   Prompts the user. This method blocks until the user has answered
the question. This method allows the user to store his/her answer.
The next time the same question is prompted to the user by this
method, the method immediately returns with the stored result.
**See also:** \[IScriptUI.reset_stored_result\]

```
**Parameter**: message (str)
:   The message to display.

**Parameter**: choice (PromptChoice)
:   Which answers the user can chose from.

**Parameter**: default_result (PromptResult)
:   The default answer which is displayed to the user in a
    highlighted manner.

**Parameter**: store_description (str)
:   The text which is displayed next to the control where the user
    can decide that (s)he does not want to see that question again
    (e.g. "Do not show this message again", or "Apply for all
    objects"). This is optional, but you must supply either both
    **store_description** and **store_key** or none of them.

**Parameter**: store_key (str)
:   A non-null caller-specific key with which the prompt can be
    identified. This is optional, but you must supply either both
    **store_description** and **store_key** or none of them.

**Parameter**: message_key (str)
:   The message key, for automated filtering / handling by
    [ISystem.prompt_answers] or similar
    mechanism by other plugins (e. G. automated test tools). Most
    users can leave the default here.

**Parameter**: arguments (Object\[\])
:   Optional objects which build the variable part of the message.
    In other words, if **message** is build via a string
    formatting operation, the arguments of that formatting
    operation should be passed as **arguments** here. This is for
    advanced usages via automated test tools, most users can
    ignore it.

**Returns**: (PromptResult)
:   The answer provided by the user.
```

`query_credentials`(*message*, *username*, *password*, *cancellable*)

:   Queries the user to input a username and password. The password is
masked ("\\\*\\\*\\\*\\\*") during input.

```
**Parameter**: message (str)
:   The message to display for the user.

**Parameter**: username (str)
:   The username to be prefilled in the textbox.

**Parameter**: password (str)
:   The password to be prefilled in the textbox.

**Parameter**: cancellable (bool)
:   if set to **True**, the user can cancel / abort the dialog,
    the default is false.

**Returns**: (list)
:   A tuple containing the username and password, or None if the
    user did cancel the dialog.

:::
Note

This method is currently not processed by
[ISystem.prompt_answers].
:::
```

`query_password`(*message*, *password*, *cancellable*)

:   Queries the user to input a password. The text is masked
("\\\*\\\*\\\*\\\*") during input.

```
**Parameter**: message (str)
:   The message to display for the user.

**Parameter**: password (str)
:   The password to be prefilled in the textbox.

**Parameter**: cancellable (bool)
:   if set to **True**, the user can cancel / abort the dialog,
    the default is false.

**Returns**: (str)
:   The entered password, or None if the user did cancel the
    dialog.

:::
Note

This method is currently not processed by
[ISystem.prompt_answers].
:::
```

`query_string`(*message*, *text*, *multi_line*, *cancellable*)

:   Queries the user to input or edit a text string.

```
**Parameter**: message (str)
:   The message to display for the user.

**Parameter**: text (str)
:   The text to be prefilled in the textbox.

**Parameter**: multi_line (bool)
:   if set to **True**, the user can enter a multiline text.

**Parameter**: cancellable (bool)
:   if set to **True**, the user can cancel / abort the dialog,
    the default is false.

**Returns**: (str)
:   The entered string, or None if the user did cancel the dialog.

:::
Note

This method is currently not processed by
[ISystem.prompt_answers].
:::
```

`reset_stored_result`(*store_key*)

:   Resets any prompt results stored by \[IScriptUI.prompt\] or \[IScriptUI.select_many\].

```
**Parameter**: store_key (str)
:   A non-null caller-specific key with which the prompt can be
    identified.
```

`save_file_dialog`(*title*, *filename*, *directory*, *filter*, *filter_index*, *default_extension*, *stateguid*, *check_file_exists*, *check_path_exists*, *check_overwrite*, *check_create*)

:

`select_many`(*message*, *choice*, *result*, *items*, *message_key*, *arguments*)

:

`warning`(*message*, *message_key*, *arguments*)

:   Reports a warning message to the user. This method blocks until
the user has acknowledged this message.

```
**Parameter**: message (str)
:   The message to display the user.

**Parameter**: message_key (str)
:   The message key, for automated filtering / handling by
    prompt_answers or similar mechanism by other plugins (e. G.
    automated test tools). Most users can leave the default here.

**Parameter**: arguments (Object\[\])
:   Optional objects which build the variable part of the message.
    In other words, if **message** is build via a string
    formatting operation, the arguments of that formatting
    operation should be passed as **arguments** here. This is for
    advanced usages via automated test tools, most users can
    ignore it.
```

## IScriptVendorDescription

Base: object

Vendor descriptiong.

`families`

:   Get all families of the vendor.

`get_family`(*family_id*)

:   Get the family with the specified family Id.

```
**Parameter**: family_id (int)
:   Family Id.

**Returns**: (IScriptDeviceFamily)
:   Device family object or **None** if there is no matching
    family.
```

`vendor_id`

:   Id of the vendor.

`vendor_info`

:   Vendor information.

`version`

:   Version.

## IScriptVendorInfo

Base: object

Vendor information.

`addresses`

:   Address of the vendor.

`faxes`

:   Fax number(s).

`mail_addresses`

:   eMail address(es).

`name`

:   Vendor name.

`phones`

:   Phone number(s).

`web_addresses`

:   Web address(es).

## IScriptWatchdog

Base: object

A configuration for a watchdog.

This interface is exported to python, and thus adheres to python
naming standards.

`enabled`

:   Enable the watchdog for a task.

`sensitivity`

:   Sensitivity of the watchdog.

`time`

:   Time monitoring for a task.

`time_unit`

:   Unit used for the \[IScriptWatchdog.time\].

## ImportReporter

Base: object

python classes can implement their own export_xml reporter here. This
interface is exposed under the name ImportReporter.

`aborting`

:   Gets a boolean value indicating whether importing should be
aborted or not.

`added`(*obj*)

:   This method is called whenever an object has been successfully
added during import.

```
**Parameter**: obj (IScriptObject)
:   The the newly added object.
```

`error`(*message*)

:   This method is called when an error has occurred during
export_xml.

```
**Parameter**: message (str)
:   The message describing the problem.
```

`replaced`(*obj*)

:   This method is called whenever an object has been successfully
replaced during import.

```
**Parameter**: obj (IScriptObject)
:   The the replacing object.
```

`resolve_conflict`(*obj*)

:   This method is called when an object to import is already
existing.

```
**Parameter**: obj (IScriptObject)
:   The the already existing object.

**Returns**: (ConflictResolve)
:   How to resolve the conflict: rename the new object, replace
    the existing object, or skip the new object.
```

`skipped`(*objectname*)

:   This method is called whenever an object has been skipped during
import.

```
**Parameter**: objectname (str)
:   The name of the skipped object.
```

`warning`(*message*)

:   This method is called when an warning has occurred during
export_xml.

```
**Parameter**: message (str)
:   The message describing the problem.
```

## NativeExportReporter

Base: object

This reporter is used for the native XML export. This interface is
exposed under the name NativeExportReporter.

`cancel`(*message*)

:   This method is called when an error occurs during serialization or
deserialization. The code that triggered the serialization should
discard the resulting stream because it will not be correctly
formatted in this case. The code that triggered the
deserialization should discard the resulting object because it
might be inconsistent.

```
**Parameter**: message (str)
:   A message describing the reason of the warning.
```

`skipped`(*type_name*, *serializable_value_name*)

:   This method is called when data has been effectively skipped
during serialization or deserialization.

```
**Parameter**: type_name (str)
:   The typename of the object that was not stored or restored
    completely.

**Parameter**: serializable_value_name (str)
:   The serializable value name of the member or property that has
    been skipped.
```

`warn`(*message*)

:   This method is called when a warning occurs during serialization
or deserialization.

```
**Parameter**: message (str)
:   A message describing the reason of the warning.
```

## NativeImportHandler

Base: object

Handler callback for the native XML import. This interface is exposed
under the name NativeImportHandler.

`conflict`(*name*, *existingObject*, *newguid*)

:   Queries how to resolve a conflict.

```
**Parameter**: name (str)
:   The name.

**Parameter**: existingObject (IScriptObject)
:   The existing object.

**Parameter**: newguid (Guid)
:   The newguid.

**Returns**: (NativeImportResolve)
:   The resolution for this conflict.
```

`progress`(*name*, *pastedObject*, *exception*)

:   Reports progress of import.

```
**Parameter**: name (str)
:   The name.

**Parameter**: pastedObject (IScriptObject)
:   The pasted object.

**Parameter**: exception (Exception)
:   The exception.
```

`skipped`(*name*)

:

# Classes

## ApplicationException

Base: object

This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException) for more information! .. data:: Data

> This is a .NET framework type, see
> [https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.Data](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.Data){.reference
> .external} for more information!

`GetBaseException`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.GetBaseException](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.GetBaseException) for more information!

`GetObjectData`(*info*, *context*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.GetObjectData](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.GetObjectData) for more information!

`HResult`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.HResult](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.HResult) for more information!

`HelpLink`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.HelpLink](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.HelpLink) for more information!

`InnerException`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.InnerException](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.InnerException) for more information!

`Message`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.Message](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.Message) for more information!

`Source`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.Source](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.Source) for more information!

`StackTrace`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.StackTrace](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.StackTrace) for more information!

`TargetSite`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.TargetSite](https://social.msdn.microsoft.com/Search/?query=System.ApplicationException.TargetSite) for more information!

## DateTime

Base: object

This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime](https://social.msdn.microsoft.com/Search/?query=System.DateTime) for more information! .. method:: Add(value)

> This is a .NET framework type, see
> [https://social.msdn.microsoft.com/Search/?query=System.DateTime.Add](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Add){.reference
> .external} for more information!

`AddDays`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddDays](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddDays) for more information!

`AddHours`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddHours](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddHours) for more information!

`AddMilliseconds`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddMilliseconds](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddMilliseconds) for more information!

`AddMinutes`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddMinutes](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddMinutes) for more information!

`AddMonths`(*months*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddMonths](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddMonths) for more information!

`AddSeconds`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddSeconds](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddSeconds) for more information!

`AddTicks`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddTicks](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddTicks) for more information!

`AddYears`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddYears](https://social.msdn.microsoft.com/Search/?query=System.DateTime.AddYears) for more information!

`Compare`(*t1*, *t2*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Compare](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Compare) for more information!

`CompareTo`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.CompareTo](https://social.msdn.microsoft.com/Search/?query=System.DateTime.CompareTo) for more information!

`CompareTo`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.CompareTo](https://social.msdn.microsoft.com/Search/?query=System.DateTime.CompareTo) for more information!

`Date`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Date](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Date) for more information!

`Day`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Day](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Day) for more information!

`DayOfWeek`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.DayOfWeek](https://social.msdn.microsoft.com/Search/?query=System.DateTime.DayOfWeek) for more information!

`DayOfYear`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.DayOfYear](https://social.msdn.microsoft.com/Search/?query=System.DateTime.DayOfYear) for more information!

`DaysInMonth`(*year*, *month*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.DaysInMonth](https://social.msdn.microsoft.com/Search/?query=System.DateTime.DaysInMonth) for more information!

`Equals`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Equals](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Equals) for more information!

`Equals`(*t1*, *t2*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Equals](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Equals) for more information!

`FromBinary`(*dateData*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromBinary](https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromBinary) for more information!

`FromFileTime`(*fileTime*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromFileTime](https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromFileTime) for more information!

`FromFileTimeUtc`(*fileTime*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromFileTimeUtc](https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromFileTimeUtc) for more information!

`FromOADate`(*d*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromOADate](https://social.msdn.microsoft.com/Search/?query=System.DateTime.FromOADate) for more information!

`GetDateTimeFormats`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats](https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats) for more information!

`GetDateTimeFormats`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats](https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats) for more information!

`GetDateTimeFormats`(*format*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats](https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats) for more information!

`GetDateTimeFormats`(*format*, *provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats](https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetDateTimeFormats) for more information!

`GetObjectData`(*info*, *context*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Runtime.Serialization.ISerializable.GetObjectData](https://social.msdn.microsoft.com/Search/?query=System.Runtime.Serialization.ISerializable.GetObjectData) for more information!

`GetTypeCode`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetTypeCode](https://social.msdn.microsoft.com/Search/?query=System.DateTime.GetTypeCode) for more information!

`Hour`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Hour](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Hour) for more information!

`IsDaylightSavingTime`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.IsDaylightSavingTime](https://social.msdn.microsoft.com/Search/?query=System.DateTime.IsDaylightSavingTime) for more information!

`IsLeapYear`(*year*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.IsLeapYear](https://social.msdn.microsoft.com/Search/?query=System.DateTime.IsLeapYear) for more information!

`Kind`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Kind](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Kind) for more information!

`MaxValue`

:   Value: None

```
This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.MaxValue](https://social.msdn.microsoft.com/Search/?query=System.DateTime.MaxValue) for more information!
```

`Millisecond`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Millisecond](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Millisecond) for more information!

`MinValue`

:   Value: None

```
This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.MinValue](https://social.msdn.microsoft.com/Search/?query=System.DateTime.MinValue) for more information!
```

`Minute`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Minute](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Minute) for more information!

`Month`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Month](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Month) for more information!

`Now`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Now](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Now) for more information!

`Parse`(*s*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Parse](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Parse) for more information!

`Parse`(*s*, *provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Parse](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Parse) for more information!

`Parse`(*s*, *provider*, *styles*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Parse](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Parse) for more information!

`ParseExact`(*s*, *formats*, *provider*, *style*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ParseExact](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ParseExact) for more information!

`ParseExact`(*s*, *format*, *provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ParseExact](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ParseExact) for more information!

`ParseExact`(*s*, *format*, *provider*, *style*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ParseExact](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ParseExact) for more information!

`Second`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Second](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Second) for more information!

`SpecifyKind`(*value*, *kind*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.SpecifyKind](https://social.msdn.microsoft.com/Search/?query=System.DateTime.SpecifyKind) for more information!

`Subtract`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Subtract](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Subtract) for more information!

`Subtract`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Subtract](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Subtract) for more information!

`Ticks`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Ticks](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Ticks) for more information!

`TimeOfDay`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.TimeOfDay](https://social.msdn.microsoft.com/Search/?query=System.DateTime.TimeOfDay) for more information!

`ToBinary`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToBinary](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToBinary) for more information!

`ToBoolean`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToBoolean](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToBoolean) for more information!

`ToByte`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToByte](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToByte) for more information!

`ToChar`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToChar](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToChar) for more information!

`ToDateTime`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToDateTime](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToDateTime) for more information!

`ToDecimal`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToDecimal](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToDecimal) for more information!

`ToDouble`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToDouble](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToDouble) for more information!

`ToFileTime`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToFileTime](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToFileTime) for more information!

`ToFileTimeUtc`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToFileTimeUtc](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToFileTimeUtc) for more information!

`ToInt16`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToInt16](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToInt16) for more information!

`ToInt32`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToInt32](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToInt32) for more information!

`ToInt64`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToInt64](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToInt64) for more information!

`ToLocalTime`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToLocalTime](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToLocalTime) for more information!

`ToLongDateString`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToLongDateString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToLongDateString) for more information!

`ToLongTimeString`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToLongTimeString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToLongTimeString) for more information!

`ToOADate`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToOADate](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToOADate) for more information!

`ToSByte`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToSByte](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToSByte) for more information!

`ToShortDateString`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToShortDateString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToShortDateString) for more information!

`ToShortTimeString`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToShortTimeString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToShortTimeString) for more information!

`ToSingle`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToSingle](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToSingle) for more information!

`ToString`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToString) for more information!

`ToString`(*format*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToString) for more information!

`ToString`(*format*, *provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToString](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToString) for more information!

`ToType`(*conversionType*, *provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToType](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToType) for more information!

`ToUInt16`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToUInt16](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToUInt16) for more information!

`ToUInt32`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToUInt32](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToUInt32) for more information!

`ToUInt64`(*provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToUInt64](https://social.msdn.microsoft.com/Search/?query=System.IConvertible.ToUInt64) for more information!

`ToUniversalTime`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToUniversalTime](https://social.msdn.microsoft.com/Search/?query=System.DateTime.ToUniversalTime) for more information!

`Today`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Today](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Today) for more information!

`TryParse`(*s*, *provider*, *styles*, *result*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParse](https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParse) for more information!

`TryParse`(*s*, *result*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParse](https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParse) for more information!

`TryParseExact`(*s*, *formats*, *provider*, *style*, *result*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParseExact](https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParseExact) for more information!

`TryParseExact`(*s*, *format*, *provider*, *style*, *result*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParseExact](https://social.msdn.microsoft.com/Search/?query=System.DateTime.TryParseExact) for more information!

`UtcNow`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.UtcNow](https://social.msdn.microsoft.com/Search/?query=System.DateTime.UtcNow) for more information!

`Year`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.DateTime.Year](https://social.msdn.microsoft.com/Search/?query=System.DateTime.Year) for more information!

## DeviceId

Base: object

Represents a Device ID.

:::
Note

An implementation class of this interface is injected under the name
"DeviceID" into the python scope, so python code can create device IDs
without the need to subclass that interface. The constructor signature
is: DeviceID(int iType, string stId, string stVersion) This interface
is exported to python, and thus adheres to python naming standards.
:::

`id`

:   Id of the device. The format for this id is specified for each
type. The id is unique within the class of devices of one type.

`type`

:   Type of the device.

`version`

:   The version of the device. The format for the version string is
specified for each type.

## Guid

Base: object

This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid](https://social.msdn.microsoft.com/Search/?query=System.Guid) for more information! .. method:: CompareTo(value)

> This is a .NET framework type, see
> [https://social.msdn.microsoft.com/Search/?query=System.Guid.CompareTo](https://social.msdn.microsoft.com/Search/?query=System.Guid.CompareTo){.reference
> .external} for more information!

`CompareTo`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.CompareTo](https://social.msdn.microsoft.com/Search/?query=System.Guid.CompareTo) for more information!

`Empty`

:   Value: None

```
This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.Empty](https://social.msdn.microsoft.com/Search/?query=System.Guid.Empty) for more information!
```

`Equals`(*g*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.Equals](https://social.msdn.microsoft.com/Search/?query=System.Guid.Equals) for more information!

`NewGuid`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.NewGuid](https://social.msdn.microsoft.com/Search/?query=System.Guid.NewGuid) for more information!

`Parse`(*input*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.Parse](https://social.msdn.microsoft.com/Search/?query=System.Guid.Parse) for more information!

`ParseExact`(*input*, *format*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.ParseExact](https://social.msdn.microsoft.com/Search/?query=System.Guid.ParseExact) for more information!

`ToByteArray`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.ToByteArray](https://social.msdn.microsoft.com/Search/?query=System.Guid.ToByteArray) for more information!

`ToString`(*format*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.ToString](https://social.msdn.microsoft.com/Search/?query=System.Guid.ToString) for more information!

`ToString`(*format*, *provider*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.ToString](https://social.msdn.microsoft.com/Search/?query=System.Guid.ToString) for more information!

`TryParse`(*input*, *result*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.TryParse](https://social.msdn.microsoft.com/Search/?query=System.Guid.TryParse) for more information!

`TryParseExact`(*input*, *format*, *result*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Guid.TryParseExact](https://social.msdn.microsoft.com/Search/?query=System.Guid.TryParseExact) for more information!

## LibManager

Base: object

An instance implementing this interface is injected into the
scriptengine scope under the name librarymanager.

`categories`

:   Gets the all known library categories.

`find_library`(*displayName*)

:   Finds the library with the specified display_name.

```
**Parameter**: display_name
:   The display name to search for.

**Returns**: (list)
:   A python tuple containing the IManagedLib and the
    ILibRepository, or None if nothing found.
```

`get_all_libraries`(*repository*)

:   Gets all libraries.

```
**Parameter**: repository (ILibRepository)
:   The repository.

**Returns**: (list)
```

`get_all_libraries`(*excludeShadowedLibs*)

:   Gets all libraries.

```
**Parameter**: exclude_shadowed_libs
:   if set to **True**, shadowed libs are excluded. This parameter
    is optional, the default is True.

**Returns**: (list)
```

`get_category`(*guid*)

:   Gets the category with the specified GUID.

```
**Parameter**: guid (Guid)
:   The GUID.

**Returns**: (ILibCategory)
:   The library category.
```

`get_file_path`(*library*)

:   Gets the file path of the specified library in the library
repository.

```
**Parameter**: library (IManagedLib)
:   The library.

**Returns**: (str)
:   The file path of the library.
```

`get_library`(*name*, *repository*)

:   Gets all libraries with the specified name.

```
**Parameter**: name (str)
:   The name of the library.

**Parameter**: repository (ILibRepository)
:   The repository. This parameter is optional. If you pass None,
    all repositories are searched in order.

**Returns**: (IManagedLib)
:   The found library.
```

`insert_repository`(*rootfolder*, *name*, *index*)

:   Creates a new library repository.

```
**Parameter**: rootfolder (str)
:   The rootfolder for the repository (this must be the full path
    to an existing directory on disk).

**Parameter**: name (str)
:   The name of the repository.

**Parameter**: index (int)
:   The index of the repository in the list. -1 means the
    repository is added to the end of the list. This parameter is
    optional, the default value is -1 (end of list).

**Returns**: (ILibRepository)
:   The newly created repository.
```

`install_library`(*filepath*, *repository*, *overwrite*)

:   Installs the library with the specified filepath.

```
**Parameter**: filepath (str)
:   The filepath of the library to install.

**Parameter**: repository (ILibRepository)
:   The repository. This parameter is optional, if omitted, the
    first repository in the list is used.

**Parameter**: overwrite (bool)
:   if set to **True**, existing libraries are replaced. This
    parameter is optional, the default value is false.

**Returns**: (IManagedLib)
:   The installed library.
```

`move_repository`(*repository*, *iNewIndex*)

:   Move_repositories the specified repository to a new position in
the list. Use this to manipulate the search order.

```
**Parameter**: repository (ILibRepository)
:   The repository.

**Parameter**: new_index
:   The new index. You can pass -1 to move it to the end of the
    list.
```

`remove_repository`(*repository*, *bDeleteOnDisk*)

:   Removes the specified repository.

```
**Parameter**: repository (ILibRepository)
:   The repository.

**Parameter**: delete_on_disk
:   If set to **True**, the on-disk directory is also deleted.
```

`repositories`

:   Gets the list of available library repositories. The order of
those repositories is configurable by the user in the dialog and
the script.

```
:::
Note

This list is a snapshot of the current state. When repositories
are created, removed or moved, those changes are not reflected
"live" in the list, and you need to get a fresh copy..
:::
```

`top_level_categories`

:   Gets the all known top level library categories.

`uninstall_library`(*repository*, *library*)

:   Uninstalls a library from the specified repository.

```
**Parameter**: repository (ILibRepository)
:   The repository.

**Parameter**: library (IManagedLib)
:   The library.
```

`update_repository`(*repository*, *newName*, *newLocation*, *copyLibraries*)

:   Update the specified repository.

```
**Parameter**: repository (ILibRepository)
:   The repository.

**Parameter**: new_name
:   The new name.

**Parameter**: new_location
:   The new location.

**Parameter**: copy_libraries
:   if set to **True**, the libraries from the old location are
    installed at the new location, if they don't exist.
```

## MultipleChoiceSelector

Base: object

Delegate for selecting one of multiple choices for simulating
interactive user input via system.promt_answers. Script authors have
to cast their delegates to this type by wrapping them via a call to
MultipleChoiceSelector().

Example:

:   :::
::: highlight
def MyFilter(choices):
return choices.IndexOf("MyWantedItem")

```
                system.prompt_answers["my message key"] = MultipleChoiceSelector(MyFilter)
:::
:::
```

**Parameter**: choices
:   The choices.

**Returns**:
:   The index of the accepted choice.

`Invoke`(*choices*)

:

## NativeImportFilter

Base: object

This method can be used to filter the imported objects.

**Parameter**: name
:   The name.

**Parameter**: guid
:   The GUID.

**Parameter**: type
:   The type.

**Parameter**: path
:   A python tuple containing the object path.

**Returns**:
:   true if the item is to be imported.

`Invoke`(*name*, *guid*, *type*, *path*)

:

## PromptChoiceFilter

Base: object

Delegating for accepting one of a list of given choices for simulating
interactive user input via system.promt_answers. Script authors have
to cast their delegates to this type by wrapping them via a call to
PromptChoiceFilter(). Example:

def MyFilter(choice): return choice in ("erste", "zweite", "dritte")

system.prompt_answers\["my message key"\] =
PromptChoiceFilter(MyFilter)

**Parameter**: choice
:   The choice.

**Returns**:
:   True if the given item is to be accepted.

`Invoke`(*choice*)

:

## ScriptDeviceRepository

Base: object

Extension interface for device objects since V3.5.10.0

`create_device_identification`(*type*, *id*, *version*)

:   Factory method for an \[IDeviceId\] object.

```
**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device Id.

**Parameter**: version (str)
:   Version.

**Returns**: (IDeviceId)
:   A new [IDeviceId] object with the
    provided values.
```

`create_module_identification`(*type*, *id*, *version*, *module_id*)

:   Factory method for an [IModuleId](#imoduleid) object.

```
**Parameter**: type (int)
:   The device type.

**Parameter**: id (str)
:   The device Id.

**Parameter**: version (str)
:   Version.

**Parameter**: module_id (str)
:   The module Id.

**Returns**: (IModuleId)
:   A new [IModuleId](#imoduleid) object with the provided values.
```

`get_all_devices`()

:   Get a collection containing all devices in the repository. Devices
which are installed in more than one repository source are
returned only once.

```
**Returns**: (IScriptDeviceCollection)
:   A device collection containing the current result of the
    query.
```

`get_all_devices`(*device_id*)

:   Get a collection containing all devices in the repository,
including local modules of **device_id**

```
**Parameter**: device_id (IDeviceId)
:   The id of the device that provides the context for the local
    modules.

**Returns**: (IScriptDeviceCollection)
:   A device collection containing the current result of the
    query.
```

`get_all_devices`(*device_id*, *source*)

:   Get a collection containing all devices in the specified
repository source.

```
**Parameter**: source (IScriptRepositorySource)
:   The repository source to enumerate.

**Parameter**: device_id (IDeviceId)
:   The id of the device that provides the context for the local
    modules.

**Returns**: (IScriptDeviceCollection)
:   A device collection containing the current result of the
    query.
```

`get_all_devices`(*source*)

:   Get a collection containing all devices in the specified
repository source.

```
**Parameter**: source (IScriptRepositorySource)
:   The repository source to enumerate.

**Returns**: (IScriptDeviceCollection)
:   A device collection containing the current result of the
    query.
```

`get_all_devices`(*name*, *source*)

:   Get all device which contain the specified name.

```
**Parameter**: name (str)
:   Text which the name of the device has to contain.

**Parameter**: source (IScriptRepositorySource)
:   Optional, search only in the repository source.

**Returns**: (list)
:   A device tuple containing the current result of the query.
```

`get_all_vendor_descriptions`()

:   Get a collection of all vendor descriptions in the repository.

```
**Returns**: (list)
:   A collection of vendor descriptions.
```

`get_all_vendor_descriptions`(*source*)

:   Get a collection of all vendor descriptions in the specified
repository source.

```
**Parameter**: source (IScriptRepositorySource)
:   Repository source.

**Returns**: (list)
:   A collection of vendor descriptions containing the current
    result of the query.
```

`get_device`(*device_id*)

:   Get the device description with the specified device
identification.

```
**Parameter**: device_id (IDeviceId)
:   Device identification.

**Returns**: (IScriptDeviceDescription)
:   The requested device description, or **None** if the device
    description does not exist.
```

`get_device_category`(*category*)

:   Get the device category with the specified type GUID.

```
**Parameter**: category (Guid)
:   The type GUID of the device category implementation.

**Returns**: (IScriptDeviceCategory)
:   The requested device category, or **None** if the device
    category does not exist.
```

`get_device_category`(*category_id*)

:   Get the device category with the specified device category ID.

```
**Parameter**: category_id (int)
:   The device category ID of the device category implementation.
    This value corresponds to the
    **DeviceDescription/DeviceInfo/Category** tags of the device
    description file.

**Returns**: (IScriptDeviceCategory)
:   The requested device category, or **None** if the device
    category does not exist.
```

`get_device_family`(*family*)

:

```
**Parameter**: family (str)
:   **VendorID:FamilyID**.

**Returns**: (IScriptDeviceFamily)
```

`get_vendor_description`(*vendor_id*)

:   Get the vendor description with the specified vendor Id.

```
**Parameter**: vendor_id (int)
:   Vendor Id.

**Returns**: (IScriptVendorDescription)
:   The requested vendor description, or **None** if the vendor
    description does not exist.
```

`import_device`(*stream*, *source*, *source_path*, *save_device_cache*)

:   Import a device description file into a repository.

```
**Parameter**: stream (Stream)
:   The stream that contains the device description. This must be
    a valid device description file. Other types of device
    descriptions must be imported by special plug-ins.

**Parameter**: source (IScriptRepositorySource)
:   The repository source where the device should be stored. This
    parameter may be **None**, in which case the default
    repository source is used. The repository source must be one
    of the sources defined in
    [IScriptDeviceRepository.sources].

**Parameter**: source_path (str)
:   Sourcepath for the import. Relative file references inside the
    device description are resolved relative to this source path.
    May be empty, if the device description contains only absolute
    file references.

**Parameter**: save_device_cache (bool)
:   True: after removing the device the device cache is also
    written False: The device cache is not written. If many
    devices are removed then this is much faster

**Returns**: (IDeviceId)
:   The ID of the imported device description.
```

`import_device`(*path*, *source*, *converter_factory_guid*, *save_device_cache*)

:   Convert a foreign device description file and import the result
into a repository.

```
**Parameter**: path (str)
:   The file that contains the device description. This must be a
    valid device description file. Other types of device
    descriptions must be imported by special plug-ins.

**Parameter**: source (IScriptRepositorySource)
:   The repository source where the device should be stored. This
    parameter may be **None**, in which case the default
    repository source is used. The repository source must be one
    of the sources defined in
    [IScriptDeviceRepository.sources].

**Parameter**: converter_factory_guid (Guid)
:   The guid of the converter to import a foreign device
    description. For example CANopen EDS files.

**Parameter**: save_device_cache (bool)
:   True: after removing the device the device cache is also
    written False: The device cache is not written. If many
    devices are removed then this is much faster

**Returns**: (IDeviceId)
:   The ID of the imported device description.

:::
Note

List of known converter factories: -
{C633F245-876F-45E8-AAB4-3FBD994C08B8} - Use as default because
all available converters are tried -
{3992C588-7BDB-4A7C-908D-F444808D8CD2} - XML files of EtherCAT -
{6066AEF4-F19A-41ac-A249-721BDAE32D40} - GSDML files of Profinet
IO - {CDDE0374-9EFD-401e-93C8-F19443FB60ED} - XML files of
Sercos3 - {1ce4a9c1-37d3-496c-9e80-cd99ad3807ee} - EDS files of
CANbus
:::
```

`import_device`(*path*, *source*, *save_device_cache*)

:   Import a device description file into a repository.

```
**Parameter**: path (str)
:   The file that contains the device description. This must be a
    valid device description file. Other types of device
    descriptions must be imported by special plug-ins.

**Parameter**: source (IScriptRepositorySource)
:   The repository source where the device should be stored. This
    parameter may be **None**, in which case the default
    repository source is used. The repository source must be one
    of the sources defined in
    [IScriptDeviceRepository.sources].

**Parameter**: save_device_cache (bool)
:   True: after removing the device the device cache is also
    written False: The device cache is not written. If many
    devices are removed then this is much faster

**Returns**: (IDeviceId)
:   The ID of the imported device description.
```

`import_vendor_description`(*stream*, *source*, *source_path*)

:   Import a vendor description file into a repository.

```
**Parameter**: stream (Stream)
:   The stream that contains the vendor description. This must be
    a valid vendor description file. Other types of vendor
    descriptions must be imported by special plug-ins.

**Parameter**: source (IScriptRepositorySource)
:   The repository source where the device should be stored. This
    parameter may be **None**, in which case the default
    repository source is used. The repository source must be one
    of the sources defined in
    [IScriptDeviceRepository.sources].

**Parameter**: source_path (str)
:   Source path for the import. Relative file references inside
    the vendor description are resolved relative to this source
    path. May be empty, if the vendor description contains only
    absolute file references.

**Returns**: (IScriptVendorDescription)
:   The imported vendor description.
```

`import_vendor_description`(*path*, *source*)

:   Import a vendor description file into a repository.

```
**Parameter**: path (str)
:   The file that contains the vendor description. This must be a
    valid vendor description file.

**Parameter**: source (IScriptRepositorySource)
:   The repository source where the device should be stored. This
    parameter may be **None**, in which case the default
    repository source is used. The repository source must be one
    of the sources defined in
    [IScriptDeviceRepository.sources].

**Returns**: (IScriptVendorDescription)
:   The imported vendor description.
```

`rebuild_device_cache`()

:   Rebuild the device cache.

```
:::
Note

The device cache is deleted, initialized and saved.
:::
```

`remove_device`(*device_id*, *source*, *save_device_cache*)

:   Remove a device from the specified repository source.

```
**Parameter**: device_id (IDeviceId)
:   Defines the device to remove.

**Parameter**: source (IScriptRepositorySource)
:   Remove the device from this repository source. If **None** the
    device is removed from the default repository source.

**Parameter**: save_device_cache (bool)
:   Optional,
```

`remove_vendor_description`(*vendor_id*, *source*)

:   Remove a vender description from the specified repository source.

```
**Parameter**: vendor_id (int)
:   The vendor id.

**Parameter**: source (IScriptRepositorySource)
:   Remove the device from this repository source. If **None** the
    device is removed from the default repository source.
```

`save_device_cache`()

:   Saves the current devices in the device cache. Could be used to
force it after adding or removing many devices.

`sources`

:   Get the repository sources of the device repository.

## ScriptImplementationLanguages

Base: object

Defines the Guids for the standard IEC 61131-3 languages and those
available as CODESYS extensions. An instance of this interface will be
injected with the name "ImplementationLanguages".

:::
Note

This interface is available since V3.5.9.0.
:::

`cfc`

:   Gets the language guid for CFC / Continous Flow Chart (free layout
FUP).

`fbd`

:   Gets the language guid for FBD / Function Block Diagram (FBS).

`instruction_list`

:   Gets the language guid for IL / Instruction List (AWL).

`ladder`

:   Gets the language guid for LD / Ladder Diagram (KOP).

`page_oriented_cfc`

:   Gets the language guid for Page oriented CFC / Continous Flow
Chart (free layout FUP).

`sfc`

:   Gets the language guid for SFC / Secuential Function Chart (AS).

```
:::
Note

Currently, SFC cannot be used for
[IScriptIecLanguageObjectContainer.create_pou] with [PouType.Function],
[IScriptIecLanguageMemberContainer.create_method],
[IScriptIecLanguageMemberContainer.create_property]and
[IScriptIecLanguageMemberContainer.create_transition].
:::
```

`st`

:   Gets the language guid for ST / Structured Text.

`uml_statechart`

:   Gets the language guid for the uml statechart.

```
:::
Note

The UML AddOn needs to be installed for this language.
:::
```

## ScriptModuleRepository

Base: object

Extension of IScriptModuleRepository2, supplying additional access for
creating module declaration objects.

`ScanIfNecessary`()

:

`add_reference_instance`(*scriptObj*, *scriptSlot*, *index*)

:   Adds a reference instance to the module tree under the specified
slot. The slot has to have an ownership of type reference,
otherwise the operation will return null.

```
**Parameter**: scriptObj (IScriptObject)
:   The IScriptObject-Object of the module instance which shall be
    reference by the created reference instance.

**Parameter**: scriptSlot (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.IScriptModuleSlotInstance)
:   The IScriptModuleSlot-Object under which the new reference
    instance shall be created.

**Parameter**: index (int)
:   The index defining the position of the created reference
    instance under the slot.

**Returns**: (IScriptObject)
:   Returns the added reference instance as IScriptObject-Object
    or null if the operation failed.
```

`add_submodule_instance`(*stInstanceName*, *scriptMd*, *scriptSlot*, *index*)

:   Adds a submodule instance to the module tree under the specified
slot. The slot has to have an ownership of type submodule,
otherwise the operation will return null.

```
**Parameter**: stInstanceName (str)
:   The desired name of the submodule instance.

**Parameter**: scriptMd (IScriptModule)
:   The IScriptModule-Object describing the desired module type.

**Parameter**: scriptSlot (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.IScriptModuleSlotInstance)
:   The IScriptModuleSlot-Object under which the new submodule
    instance shall be created.

**Parameter**: index (int)
:   The index defining the position of the created submodule
    instance under the slot.

**Returns**: (IScriptObject)
:   Returns the added submodule instance as IScriptObject-Object
    or null if the operation failed.
```

`add_toplevel_instance`(*stInstanceName*, *scriptMd*)

:   Adds a toplevel instance to the module tree.

```
**Parameter**: stInstanceName (str)
:   The desired name for the toplevel instance.

**Parameter**: scriptMd (IScriptModule)
:   The IScriptModule-Object describing the desired module type.

**Returns**: (IScriptObject)
:   Returns the added toplevel instance IScriptObject-Object or
    null if the operation failed.
```

`create_module_declaration_object`(*stDeclObjectName*, *stDeclObjectText*)

:   Adds a module declaration object to the POU-Pool.

```
**Parameter**: stDeclObjectName (str)
:   The name of the module declaration object.

**Parameter**: stDeclObjectText (str)
:   The declaration text in the module declaration object. This
    text can be changed using the module declaration object
    afterwards.

**Returns**: (IScriptObject)
:   Returns the module declaration object as IScriptObject-Object
    or null if the operation failed.
```

`find_module`(*stQualifiedName*)

:   Finds the module with its declaration at the given qualified path
(namespace.modulename).

```
**Parameter**: stQualifiedName (str)
:   The qualified path of the module description.

**Returns**: (IScriptModule)
:   The module defined by the module description at the qualified
    path.
```

`generate`()

:

`generate_and_login`()

:

`get_all_instances`()

:   Gets all Module-Instances of the primary project.

```
**Returns**: (list)
:   Returns all Module-Instances of the primary project.
```

`get_all_modules`()

:   Gets all Modules available in the primary project.

```
**Returns**: (list)
:   Returns all Modules available in the primary project
```

`get_compatible_modules`(*slot*)

:   Gets all modules which are compatible to a specified slot

```
**Parameter**: slot (IScriptModuleSlot)
:   The slot for which comaptible modules shall be searched.

**Returns**: (list)
:   Returns a list of all compatible modules as
    IScriptModule-Objects.
```

`get_toplevel_instances`()

:   Gets all Toplevel-Module-Instances of the primary project.

```
**Returns**: (list)
:   Returns all Toplevel-Module-Instances of the primary project.
```

`get_toplevel_modules`()

:   Gets all Toplevel-Modules available in the primary project.

```
**Returns**: (list)
:   Returns all Toplevel-Modules available in the primary project.
```

`load_wildcard_setting`(*stFileName*)

:   Loads s specific xml file into the wildcard options dialog

```
**Parameter**: stFileName (str)
:   The file to be loaded into the wildcard dialogs settings. If
    null the current filename or last used filename is used.

**Returns**: (bool)
:   Returns true if loading succeeded.
```

`scan_all_modules`()

:

`set_generator`(*stGenGuid*, *bEnable*)

:   Enables generators in the generator settings

```
**Parameter**: stGenGuid (str)
:   The string representation of Guid of the generator, which
    shall be enabled.

**Parameter**: bEnable (bool)
:   Whether the generator shall be enabled or not.

**Returns**: (bool)
:   Returns true if enablilng succeeded.
```

`update_all_module_instances`()

:

## ScriptOnline

Base: object

Extension for \[IScriptOnline\] since CODESYS
V3.5.8.0.

`PermittedSourceKindsForFallback`

:   Gets the permitted source kinds. If
\[ITemporaryLoginCredentialsContext.QueryForCredentials\] returns false, and at least one of the bits here is set,
the code will fall back to the default
\[ProvideCredentialsHandler\] set via
\[IOnlineManager4.SetProvideCredentialsHandler\], passing him an \[IProvideCredentialsArgs2\] instance whose
\[IProvideCredentialsArgs2.PermittedSourceKinds\] member resembles the CredentialSourceKind flags set
here. (However, for older or OEM \[ProvideCredentialsHandler\] implementations, it is not guaranteed that those
flags are honored.)

`QueryForCredentials`(*sender*, *args*)

:   Queries for credentials.

```
**Parameter**: sender (object)
:   The sender.

**Parameter**: args (\_3S.CoDeSys.Core.Online.IProvideCredentialsArgs)
:   The args.

**Returns**: (bool)
:   True if we found credentials which should be tried, false if
    we did not find any credentials.

:::
Note

If this function returns false, and
[ITemporaryLoginCredentialsContext.PermittedSourceKindsForFallback] returns [CredentialSourceKind.None], the login fails.
:::
```

`UNFORCE`

:   Special value for unforcing a variable - it is returned by
\[IScriptOnlineApplication.get_prepared_value\]and can be fed to
\[IScriptOnlineApplication.set_prepared_value\]. See also
\[IScriptOnlineApplication.set_unforce_value\].

`UNFORCE_RESTORE`

:   Special value for unforcing and restoring a variable - it is
returned by \[IScriptOnlineApplication.get_prepared_value\]and can be fed to
\[IScriptOnlineApplication.set_prepared_value\]. See also
\[IScriptOnlineApplication.set_unforce_value\].

`auth_fallback_modes`

:   Gets or sets the setting how authentication credentials are
acquired when no default credentials are set, and no specific
credentials match the target.

```
:::
Note

This setting is in effect until the end of the current script
execution. By default, this is set to
[CredentialSourceKind.All]. You can modify
this value to disable interactive login.
:::
```

`clear_all_credentials`()

:   Clears all credentials which were set by this script.

```
:::
Note

This only clears the cretentials at the level of the script. The
online manager and other components may cache credentials
internally, those caches are currently not cleared by this method.
:::
```

`create_online_application`(*application*)

:   Creates an online application.

```
:::
Note

To prevent resource leaks, script writers should wrap the usage of
the online application in a with: block when they use var refs.
:::

**Parameter**: application (IScriptObject)
:   The application object to use. If this parameter is omitted,
    the active application is used. (This parameter is optional.)

**Returns**: (IScriptOnlineApplication)
:   The online application object.
```

`create_online_device`(*device*)

:   Creates an online device.

```
:::
Note

To prevent resource leaks, script writers should wrap the usage of
the online device in a with: block.
:::

**Parameter**: device (IScriptObject)
:   The application object to use. If this parameter is omitted,
    the device of the active application is used. (This parameter
    is optional.)

**Returns**: (IScriptOnlineDevice)
:   The online application object.
```

`gateway_drivers`

:   Gets the gateway drivers.

`gateways`

:   Gets all currently known gateways.

`set_default_credentials`(*username*, *password*)

:   Sets the default credentials for login to devices.

```
**Parameter**: username (str)
:   The username.

**Parameter**: password (str)
:   The password.

:::
Note

This setting is in effect until the end of the current script
execution. Use None for the username and omit the password to
delete the default credentials.
:::
```

`set_specific_credentials`(*target*, *username*, *password*)

:   Sets the default credentials for login to a specific device.

```
**Parameter**: target (object)
:   The target. You can pass a device object, an online device
    object, an application, or an online application. If you pass
    an application or online application, the setting will take
    effect for all applications in the corresponding device
    object.

**Parameter**: username (str)
:   The username.

**Parameter**: password (str)
:   The password.

:::
Note

This setting is in effect until the end of the current script
execution. Use None for the username and omit the password to
delete specific credentials.
:::
```

## ScriptProjectArchiveCategories

Base: object

The list of available archive categories. Enumerating this object will
give all categories available in the current installation. Some often
used categories are defined here, but may be unavailable (throw
exceptions) in customized environments. An instance of this object is
injected into the scriptengine module with the name
"ArchiveCategories".

`Add`(*item*)

:

`Clear`()

:

`Contains`(*item*)

:

`CopyTo`(*array*, *arrayIndex*)

:

`Count`

:

`GetEnumerator`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator](https://social.msdn.microsoft.com/Search/?query=System.Collections.IEnumerable.GetEnumerator) for more information!

`GetEnumerator`()

:

`IndexOf`(*item*)

:

`Insert`(*index*, *item*)

:

`IsReadOnly`

:

`Item`

:

`Remove`(*item*)

:

`RemoveAt`(*index*)

:

`all`

:   A collection of all categories (returns self).

`bootproject`

:   Gets the category for the files containing offline boot
applications, that were generated for the current project.

`compileinfo`

:   Gets the category for the compileinfo. This is needed for logins
and online changes into an existing application without download.

`default`

:   The default selection of archive categories.

`devices`

:   Gets the category for the device descriptions of the devices used
in the project.

`fdt`

:   Gets the category for the FDT Bulk Data.

`images`

:   Gets the category for the imagepool images of the project.

`libraries`

:   Gets the category for the libraries referenced by the project.

`libraryprofile`

:   Gets the category for the library profile that is currently in use
with this project.

`none`

:   No categories (empty set).

```
:::
Note

This is a special sentinel value, different from passing an
arbitrary empty list.
:::
```

`options`

:   Gets the category for the project, user, and machine specific
preferences.

`visualprofile`

:   Gets the category for the active visualization profile.

`visualstyles`

:   Gets the category for the visualization styles which are currently
referenced by this project.

`visuextensions`

:   Gets the category for the active visualization extensions.

## ScriptProjects

Base: object

Extension interface for \[IScriptProjects\] since
V3.5.8.0

`all`

:   Gets a (possibly empty) List of all currently opened projects.

```
**Returns**:
:   The list of all projects.
```

`convert`(*stPath*, *stOutputPath*, *converterGuid*, *bPrimary*)

:   Converts the specified project.

```
**Parameter**: path
:   The path of the project to convert.

**Parameter**: output_path
:   The output path. This parameter is optional, if it is omitted,
    the output path will be auto-generated from the project path
    by changing the file extension.

**Parameter**: converter
:   The GUID of the CoDeSys converter factory as Guid object.

**Parameter**: primary
:   If set to **True**, open as primary project. (This parameter
    is optional, the default is true.) See
    [IScriptProject.primary] for more
    information.

**Returns**: (IScriptProject)
:   The converted project.

:::
Note

Currently, password and device conversion prompts cannot be caught
by the script.

Some converter guids are:

Guid: Description \* *{E3BC006A-5E3E-4f8f-AEE7-27FD1E0F2A3F}*:
CoDeSys for Automation Alliance project files (bevore V3.0,
\\\*.pro) \* *{941937BF-9A12-4174-814E-63D1523C94CC}*: CoDeSys for
Automation Alliance library files (before V3.0, \\\*.lib)
:::
```

`convert`(*stPath*, *stOutputPath*, *converter*, *bPrimary*)

:   Converts the specified project.

```
**Parameter**: path
:   The path of the project to convert.

**Parameter**: output_path
:   The output path. This parameter is optional, if it is omitted,
    the output path will be auto-generated from the project path
    by changing the file extension.

**Parameter**: converter (str)
:   The GUID of the CoDeSys converter factory as string object.
    This parameter is optional, if omitted, the script engine will
    try to guess using the extension of the file name.

**Parameter**: primary
:   if set to **True**, open as primary project. (This parameter
    is optional, the default is true.) See
    [IScriptProject.primary] for more
    information.

**Returns**: (IScriptProject)
:   The converted project.

:::
Note

Currently, password and device conversion prompts cannot be caught
by the script.

Some converter guids are:

Guid: Description \* *{E3BC006A-5E3E-4f8f-AEE7-27FD1E0F2A3F}*:
CoDeSys for Automation Alliance project files (bevore V3.0,
\\\*.pro) \* *{941937BF-9A12-4174-814E-63D1523C94CC}*: CoDeSys for
Automation Alliance library files (before V3.0, \\\*.lib)
:::
```

`create`(*stPath*, *bPrimary*)

:   Creates a new project.

```
**Parameter**: path
:   The location where the project content is to be stored.

**Parameter**: primary
:   if set to **True** the project will be the new primary project
    (This parameter is optional, default = true). See
    [IScriptProject.primary] for more
    information.

**Returns**: (IScriptProject)
:   The created IProject instance.
```

`get_by_path`(*stPath*)

:   Gets a Project by the absolute path where the project is
physically stored.

```
**Parameter**: path
:   The path to the project.

**Returns**: (IScriptProject)
:   The project instance.
```

`open`(*stPath*, *stPassword*, *bPrimary*)

:   Opens the specified project.

```
:::
Note

If a password is given, SystemInstances.ObjectManager must
implement IObjectManager9, or a InvalidOperationException will be
thrown (even if the project is not actually password protected).
If the password is omitted, null or empty string, opening a
password protected archive will prompt the user for a password.
:::

**Parameter**: path
:   The path of the project file to open.

**Parameter**: password
:   The password for the project encryption. (This parameter is
    optional.)

**Parameter**: primary
:   if set to **True**, open as primary project. (This parameter
    is optional, the default is true)

**Returns**: (IScriptProject)
:   The opened project.
```

`open`(*stPath*, *encryption_password*, *session_user*, *session_password*, *bPrimary*)

:   Opens the specified project.

```
**Parameter**: path
:   The path of the project file to open.

**Parameter**: encryption_password (str)
:   The project encryption password. (This parameter is optional.)

**Parameter**: session_user (str)
:   The project session user (project usermanagement, this
    parameter is optional).

**Parameter**: session_password (str)
:   The project session password (project usermanagement, this
    parameter is optional).

**Parameter**: primary
:   if set to **True**, open as primary project. (This parameter
    is optional, the default is true)

**Returns**: (IScriptProject)
:   The opened project.

:::
Note

If a password is given, SystemInstances.ObjectManager must
implement IObjectManager9, or a InvalidOperationException will be
thrown (even if the project is not actually password protected).
If the password is omitted, null or empty string, opening a
password protected archive will prompt the user for a password.
:::
```

`open`(*stPath*, *encryption_password*, *session_user*, *session_password*, *bPrimary*, *update_flags*, *allow_readonly*)

:   Opens the specified project.

```
**Parameter**: path
:   The path of the project file to open.

**Parameter**: encryption_password (str)
:   The project encryption password. (This parameter is optional.)

**Parameter**: session_user (str)
:   The project session user (project usermanagement, this
    parameter is optional).

**Parameter**: session_password (str)
:   The project session password (project usermanagement, this
    parameter is optional).

**Parameter**: primary
:   if set to **True**, open as primary project. (This parameter
    is optional, the default is true)

**Parameter**: update_flags (VersionUpdateFlags)
:   The flags telling whether some aspects (libraries, compiler
    version) ought to be updated when the project is loaded. The
    default is to silently update nothing.

**Parameter**: allow_readonly (bool)
:   if set to **True**, allow the project to be opened as
    read-only. (This parameter is optional, the default is false)

**Returns**: (IScriptProject)
:   The opened project.

:::
Note

If a password is given, SystemInstances.ObjectManager must
implement IObjectManager9, or a InvalidOperationException will be
thrown (even if the project is not actually password protected).
If the password is omitted, null or empty string, opening a
password protected archive will prompt the user for a password.

For the **update_flags** parameter, the
[VersionUpdateFlags.SilentMode]is usually
combined with one or more of the **Update\...** flags defined in
the [VersionUpdateFlags](#versionupdateflags)enum. If you
only pass some **Update\...** flags without the
[VersionUpdateFlags.SilentMode]flag, they
will be used as initial values when the update dialog pops up. To
silently update everything, you can pass the combination
**:ref:\`VersionUpdateFlags.SilentMode**[\|](#id139)[VersionUpdateFlags.UpdateAll\`].
:::
```

`open_archive`(*stArchiveFile*, *stProjectPath*, *bOverwrite*, *stPassword*)

:   Opens a project archive.

```
**Parameter**: archivefile
:   The path of the project archive.

**Parameter**: projectpath
:   The path for the extracted project.

**Parameter**: overwrite
:   if set to **True**, overwrite existing objects and project
    files (This parameter is optional, default is false).

**Parameter**: password
:   The password. (This parameter is optional.)

**Returns**: (IScriptProject)
:   The opened project.

:::
Note

The parameter **projectpath** will be evaluated using the
following algorithm:

1.  If it's the path of an existing file, and **overwrite** is
    true, it will be overwritten.
2.  If it's the path to an existing file, and **overwrite** is
    false, an [IOException] will be thrown.
3.  *None*
4.  *None*
5.  *None*
6.  *None*
7.  In all other cases, a [DirectoryNotFoundException] will be thrown.

This method will return null when the archive extraction was
cancelled tue to an error or overwriting of files. If a password
is given, SystemInstances.ObjectManager must implement
IObjectManager9, or a MissingMethodException will be thrown (even
if the project is not actually password protected). If the
password is omitted, null or empty string, opening a password
protected archive will prompt the user for a password.
:::
```

`open_archive`(*stArchiveFile*, *stProjectPath*, *bOverwrite*, *encryption_password*, *session_user*, *session_password*)

:   Opens a project archive.

```
**Parameter**: archivefile
:   The path of the project archive.

**Parameter**: projectpath
:   The path for the extracted project.

**Parameter**: overwrite
:   If set to **True**, overwrite existing objects and project
    files (This parameter is optional, default is false).

**Parameter**: encryption_password (str)
:   The project encryption password. (This parameter is optional.)

**Parameter**: session_user (str)
:   The project session user (project usermanagement, this
    parameter is optional).

**Parameter**: session_password (str)
:   The project session password (project usermanagement, this
    parameter is optional).

**Returns**: (IScriptProject)
:   The opened project.

:::
Note

The parameter **projectpath** will be evaluated using the
following algorithm:

1.  If it's the path of an existing file, and **overwrite** is
    true, it will be overwritten.
2.  If it's the path to an existing file, and **overwrite** is
    false, an [IOException] will be thrown.
3.  *None*
4.  *None*
5.  *None*
6.  *None*
7.  In all other cases, a [DirectoryNotFoundException] will be thrown.

This method will return null when the archive extraction was
cancelled tue to an error or overwriting of files. If a password
is given, SystemInstances.ObjectManager must implement
IObjectManager9, or a MissingMethodException will be thrown (even
if the project is not actually password protected). If the
password is omitted, null or empty string, opening a password
protected archive will prompt the user for a password.
:::
```

`open_archive`(*stArchiveFile*, *projectpath*, *bOverwrite*, *encryption_password*, *session_user*, *session_password*, *update_flags*)

:   Opens a project archive.

```
**Parameter**: archivefile
:   The path of the project archive.

**Parameter**: projectpath (str)
:   The path for the extracted project.

**Parameter**: overwrite
:   If set to **True**, overwrite existing objects and project
    files (This parameter is optional, default is false).

**Parameter**: encryption_password (str)
:   The project encryption password. (This parameter is optional.)

**Parameter**: session_user (str)
:   The project session user (project usermanagement, this
    parameter is optional).

**Parameter**: session_password (str)
:   The project session password (project usermanagement, this
    parameter is optional).

**Parameter**: update_flags (VersionUpdateFlags)
:   The flags telling whether some aspects (libraries, compiler
    version) ought to be updated when the project is loaded. The
    default is to silently update nothing.

**Returns**: (IScriptProject)
:   The opened project.

:::
Note

The parameter **projectpath** will be evaluated using the
following algorithm:

1.  If it's the path of an existing file, and **overwrite** is
    true, it will be overwritten.
2.  If it's the path to an existing file, and **overwrite** is
    false, an [IOException] will be thrown.
3.  *None*
4.  *None*
5.  *None*
6.  *None*
7.  In all other cases, a [DirectoryNotFoundException] will be thrown.

This method will return null when the archive extraction was
cancelled tue to an error or overwriting of files. If a password
is given, SystemInstances.ObjectManager must implement
IObjectManager9, or a MissingMethodException will be thrown (even
if the project is not actually password protected). If the
password is omitted, null or empty string, opening a password
protected archive will prompt the user for a password. For the
**update_flags** parameter, the
[VersionUpdateFlags.SilentMode]is usually
combined with one or more of the **Update\...** flags defined in
the [VersionUpdateFlags](#versionupdateflags)enum. If you
only pass some **Update\...** flags without the
[VersionUpdateFlags.SilentMode]flag, they
will be used as initial values when the update dialog pops up. To
silently update everything, you can pass the combination
**:ref:\`VersionUpdateFlags.SilentMode**[\|](#id141)[VersionUpdateFlags.UpdateAll\`].
:::
```

`primary`

:   Gets the primary project, or None if no primary project currently
exists.

```
**Returns**:
:   The primary project instance.

:::
Note

The primary project is the one the user usually works with. See
[IScriptProject.primary] for more
information.
:::
```

## ScriptSymbolConfigInvalidObjectException

Base: Exception

Exception which is thrown when the symbol configuration object is
modified externally and so the scripting objects are not valid
anymore.

`Data`

:

`GetBaseException`()

:

`GetObjectData`(*info*, *context*)

:

`HResult`

:

`HelpLink`

:

`InnerException`

:

`Message`

:

`Source`

:

`StackTrace`

:

`TargetSite`

:

## SystemImpl

Base: object

Extension interface for ISystem since V3.5.5.0.

`abort_autocheck`

:   Gets or sets a value indicating whether this script execution
automatically checks for aborts.

```
:::
Note

If this property is set to True (the default value), the script
engine uses the python tracing functionality to check for aborts
after every line of executed python code, and throws an
KeyboardInterruptException if aborted. You can disable this
automatic checks by setting this property to false. Certain
debuggin modes also disable this check.
:::
```

`abortable`

:   Whether the script is abortable.

```
:::
Note

Since V3.5.5.0, scripts are abortable by default. The user can
abort the script by pressing the Cancel button in the progress
display. This property controls whether this Cancel button is
enabled.
:::
```

`aborting`

:   Gets a value indicating whether this \[ISystem\] is aborting.

```
:::
Note

This property gets set to true once the user presses an enabled
"Cancel" button on the progress display, and it cannot be reset by
the script. Use this property for explicit abortion checks when
you disabled [ISystem.abort_autocheck].
:::
```

`clear_messages`(*categoryGuid*)

:   Clears the specified category.

```
**Parameter**: category
:   The category.
```

`clear_messages`(*stCategoryGuid*)

:

`commands`

:   Gets the commands.

`delay`(*nMilliSeconds*)

:   Delays the script for the specified amount of milliseconds. The
message loop is served during the wait to allow background tasks
to be processed.

```
:::
Note

The actual duration of the delay will not meet hard realtime
requirements.
:::

**Parameter**: milliseconds
:   The duration to wait.
```

`dump_scripting_api`(*output_file*, *allowed_drivers*, *allowed_objects*, *additional_entry_points*, *additional_assemblies*, *specially_prepared_executor*)

:

`dump_scripting_api`(*allowed_drivers*, *allowed_objects*, *additional_entry_points*, *additional_assemblies*, *specially_prepared_executor*)

:

`executable_filename`

:   Gets the name of the executable file (the currently running
application).

`execute_on_primary_thread`(*code*, *async*)

:   !!Experts Only!! Executes a specified piece of code in the primary
thread.

```
**Parameter**: code (\_3S.CoDeSys.ScriptEngine.BasicFunctionality.PieceOfCode)
:   The code to execute. A python function, which will be called
    without parameters, and should not return any value.

**Parameter**: async (bool)
:   If **True**, this method returns immediately, otherwise the
    this method returns after the delegate has been finished.

:::
Note

Advanced users only! Using multiple threads is neither officially
supported nor encouraged in CoDeSys python scripts, you do that
"on your own risk".

This method is safe to be called from non-primary threads.

This method relies on the primary thread processes its message
queue. (If you don't know what the message queue is, threads are
probably not the right thing for you\...)

Be careful to ensure that all your own threads are finished when
the main thread exits the script, or strange effects can occur.

You can use the .NET System.Threading or the python threading
module to create new threads.
:::
```

`exit`(*exitcode*)

:   Exits the application platform by shutting down the engine and
exiting the process.

```
:::
Note

If you just want to terminate the script execution without
exitting the platform, call sys.exit() or raise a
SystemExitException. (When running the script via --runscript
command line parameter in --noUI-Mode, this will also terminate
CoDeSys, as there's nothing else to do after the script exitted.)
:::

**Parameter**: exitcode (int)
:   The exitcode we return to the operating system. If omitted, we
    return the ExitCode 0 which normally means success.
```

`factories`

:   Gets the factories.

`get_message_categories`(*bActive*)

:   Gets all message categories.

```
**Parameter**: bActive (bool)
:   If set to **True** (the default), only the active ones (those
    which had at least one message since the current codesys
    instance was started) are returned. If set to false, all
    categories existing in the current installation are returned.

**Returns**: (list)
:   A list of guids.
```

`get_message_category_description`(*categoryGuid*)

:   Gets a description for the secified message category.

```
**Parameter**: category
:   The category.

**Returns**: (str)
:   The description of that message category.
```

`get_message_objects`(*categoryGuid*, *severities*)

:   Gets all messages of a given category and severity which are
currently in the store.

```
**Parameter**: category
:   The category Guid (defaults to the ScriptMessage category).

**Parameter**: severities (Severity)
:   The severities (This can be a combination of several severity
    flags) - by default, all messages are returned.

**Returns**: (list)
:   The list of message texts.
```

`get_message_objects`(*stCategoryGuid*, *severities*)

:   Gets all messages of a given category and severity which are
currently in the store.

```
**Parameter**: category
:   The category Guid (defaults to the ScriptMessage category).

**Parameter**: severities (Severity)
:   The severities (This can be a combination of several severity
    flags) - by default, all severities are returned.

**Returns**: (list)
:   The list of message texts.
```

`get_messages`(*categoryGuid*)

:   Gets all messages of a given category which are currently in the
store.

```
**Parameter**: category
:   The category Guid (defaults to the ScriptMessage category).

**Returns**: (list)
:   The list of message texts.
```

`get_messages`(*stCategoryGuid*)

:   Gets all messages of a given category which are currently in the
store.

```
**Parameter**: category
:   The category Guid as string representation. If the Category is
    omitted, the ScriptMessage category is used. (This parameter
    is optional.)

**Returns**: (list)
:   The list of message texts.
```

`object_produced_by_factory`(*factoryguid*)

:

`process_messageloop`()

:   Processes the Win32 message loop of the current Thread, if
present. This allows the UI to be updated during long running
processes. It should be safe to call this from python scripts
without reentrancy problems, because the ScriptExecutor calls
SystemInstances.Engine.Frame.StartLengthyOperation(); to prevent
the user from triggering more commands while the script is
running.

`progress_absolute`(*item*, *absolute_progress*)

:   Advances the progress of the current subtask.

```
**Parameter**: item (str)
:   The item which is currently completed.

**Parameter**: absolute_progress (int)
:   The total number of items completed so far.
```

`progress_start`(*description*, *items*, *unit*)

:   Starts the progress information for a specific subtask.

```
**Parameter**: description (str)
:   The description of the subtask.

**Parameter**: items (int)
:   The number of items, if known in advance. (This parameter is
    optional)

**Parameter**: unit (str)
:   The unit of items, for example objects or lines. (This
    parameter is optional)
```

`progress_step`(*item*, *completed*)

:   Advances the progress of the current subtask.

```
**Parameter**: item (str)
:   The item which is currently completed.

**Parameter**: completed (int)
:   The number of items completed in this step. (This parameter is
    optional, the default is 1 item)
```

`prompt_answers`

:   Gets the prompt answers Dictionary for simulating interactive user
input.

```
:::
Note

This dictionary is used to intercept the IMessageService
interface. Whenever a method with a stmessage_key is called, the
dictionary is searched for the message_key. If found, the
corresponding value is returned (for prompts), or the call is
ignored (for errors). All other calls are forwarded to the
original messageService. For this to work, all the keys must be
strings matching the message_key values. For Prompts, the
following possibilities exist:

If the value given does not make sense in the context of the
current prompt, an InvalidCastException is raised. For errors, the
values are not used and don't matter (may be null / None).

To give best semantics for the scripts, this dictionary is a
PythonDictionary instance, that means you can easily add values:

To give best semantics for the scripts, this dictionary is a
PythonDictionary instance, that means you can easily add values:

::: highlight-default
::: highlight
    # set a value:
:::
:::

System.prompt_answers\["OverWriteFiles"\] = PromptResult.Cancel

\# Set multiple values: System.prompt_answers.update(
{"OverWriteFiles": PromptResult.OK, "DisFullError": None})

\# Reset everything: System.prompt_answers.clear()
:::
```

`prompt_handling`

:   Gets or sets the way message service prompts are handled.

`search_command_guid`(*tokens*)

:

`search_factories_for`(*typeguid*)

:

`trace`

:   Gets or sets a value indicating whether trace \[ISystem\] is active on the current script execution.

```
:::
Note

trace is the replacement for the old "echo" functionality in the
CoDeSys V2.3 batch mode. It adds log messages (Category
ScriptMessage, Severity Info) into the IMessageStorage on the
following events: Change of source code line, entering and
exitting of python scope, exception thrown in python code. This
setting may be ignored: For example, due to internal restrictions
in the IronPython Engine, script tracing is disabled in debugging
mode.
:::
```

`ui`

:   Gets the script ui instance.

`ui_present`

:   Gets a value indicating whether we have an UI. If this is false,
we're running in a console application or background service.

`write_message`(*severity*, *stMessage*, *obj*, *position*, *length*)

:   Writes the message to the Message Store.

```
:::
Note

Position and length are only meaningfull if obj is a ScriptObject
and are ignored otherwise.
:::

**Parameter**: severity (Severity)
:   The severity.

**Parameter**: stMessage (str)
:   The message text.

**Parameter**: obj (IScriptObject)
:   The ScriptObject the message belongs to.

**Parameter**: position (int)
:   The position including offset in the data for the message.
    (This parameter is optional.)

**Parameter**: length (int)
:   The length in the data for the message. (This parameter is
    optional.)
```

`write_message`(*severity*, *stMessage*, *obj*)

:   Writes the message to the Message Store.

```
:::
Note

Position and length are only meaningfull if obj is a ScriptObject
and are ignored otherwise.
:::

**Parameter**: severity (Severity)
:   The severity.

**Parameter**: stMessage (str)
:   The message text.

**Parameter**: obj (IScriptProject)
:   The ScriptProject the message belongs to.
```

`write_message`(*severity*, *stMessage*, *obj*, *position*, *length*)

:   Writes the message to the Message Store.

```
:::
Note

Position and length are only meaningfull if obj is a ScriptObject
and are ignored otherwise.
:::

**Parameter**: severity (Severity)
:   The severity.

**Parameter**: stMessage (str)
:   The message text.

**Parameter**: obj (IScriptTreeObject)
:   The ScriptObject or ScriptProject the message belongs to.
    (This parameter is optional.)

**Parameter**: position (int)
:   The position including offset in the data for the message.
    (This parameter is optional.)

**Parameter**: length (int)
:   The length in the data for the message. (This parameter is
    optional.)
```

## TimeoutException

Base: object

This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException) for more information! .. data:: Data

> This is a .NET framework type, see
> [https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.Data](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.Data){.reference
> .external} for more information!

`GetBaseException`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.GetBaseException](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.GetBaseException) for more information!

`GetObjectData`(*info*, *context*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.GetObjectData](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.GetObjectData) for more information!

`HResult`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.HResult](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.HResult) for more information!

`HelpLink`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.HelpLink](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.HelpLink) for more information!

`InnerException`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.InnerException](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.InnerException) for more information!

`Message`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.Message](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.Message) for more information!

`Source`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.Source](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.Source) for more information!

`StackTrace`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.StackTrace](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.StackTrace) for more information!

`TargetSite`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.TargetSite](https://social.msdn.microsoft.com/Search/?query=System.TimeoutException.TargetSite) for more information!

## ValuesFailedException

Base: ApplicationException

This exception is thrown by write_prepared_values and
force_prepared_values.

This class is exported to python, and thus adheres to python naming
standards.

`Data`

:

`GetBaseException`()

:

`GetObjectData`(*info*, *context*)

:

`HResult`

:

`HelpLink`

:

`InnerException`

:

`Message`

:

`Source`

:

`StackTrace`

:

`TargetSite`

:

`failed_expressions`

:   Gets the list of the failedexpressions.

## Version

Base: object

This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version](https://social.msdn.microsoft.com/Search/?query=System.Version) for more information! .. data:: Build

> This is a .NET framework type, see
> [https://social.msdn.microsoft.com/Search/?query=System.Version.Build](https://social.msdn.microsoft.com/Search/?query=System.Version.Build){.reference
> .external} for more information!

`Clone`()

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.Clone](https://social.msdn.microsoft.com/Search/?query=System.Version.Clone) for more information!

`CompareTo`(*value*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.CompareTo](https://social.msdn.microsoft.com/Search/?query=System.Version.CompareTo) for more information!

`CompareTo`(*version*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.CompareTo](https://social.msdn.microsoft.com/Search/?query=System.Version.CompareTo) for more information!

`Equals`(*obj*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.Equals](https://social.msdn.microsoft.com/Search/?query=System.Version.Equals) for more information!

`Major`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.Major](https://social.msdn.microsoft.com/Search/?query=System.Version.Major) for more information!

`MajorRevision`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.MajorRevision](https://social.msdn.microsoft.com/Search/?query=System.Version.MajorRevision) for more information!

`Minor`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.Minor](https://social.msdn.microsoft.com/Search/?query=System.Version.Minor) for more information!

`MinorRevision`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.MinorRevision](https://social.msdn.microsoft.com/Search/?query=System.Version.MinorRevision) for more information!

`Revision`

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.Revision](https://social.msdn.microsoft.com/Search/?query=System.Version.Revision) for more information!

`ToString`(*fieldCount*)

:   This is a .NET framework type, see
[https://social.msdn.microsoft.com/Search/?query=System.Version.ToString](https://social.msdn.microsoft.com/Search/?query=System.Version.ToString) for more information!
