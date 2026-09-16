PROGRAM Standard_ST
VAR
	xDoYouWork: BOOL;
	xYayyyy: BOOL;
END_VAR

// --- BEGIN IMPLEMENTATION ---

xDoYouWork := TRUE;

// some random comment
(* Some 
random
 multi 

line 
comment

*)
IF xDoYouWork THEN
	xYayyyy := TRUE;
	
ELSE
	xYayyyy := FALSE;
END_IF