{attribute 'qualified_only'}
VAR_GLOBAL PERSISTENT RETAIN

wEngineOnCount		:WORD;	//Count OF times Engine is turned ON
wGpsOnCount			:WORD;	//Count OF times GPS Activated
wAutoOnCount		:WORD;	//Count OF times Auto Harvest Activated
wFlightOnCount		:WORD;	//Count OF times Flight Converyor is turned ON
wTotalMaintCount	:WORD;	//Count of times Maintenance Mode Activated
wTotalFilterCount	:WORD;	//Count of Filter Bypass Alarms
wTotalPressCount	:WORD;	//Count of Pressure Alarms
wTotalTempCount		:WORD;	//Count OF Temperature Alarms
wTotalEstopCount	:WORD;	//Count of times E-Stop is Activated
wTotalStallCount	:WORD;	//Count of Machine Stalls
wTotalDerateCount	:WORD;	//Count of De-rate Events
wTotalVoltageCount	:WORD;	//Count of Voltage Alarms

wHarvPlcVoltCount  : WORD;    // Total count of Trailer PLC Voltage Alarms
wHarvDispVoltCount : WORD;    // Total count of Trailer Display Voltage Alarms
wTracDispVoltCount : WORD;    // Total count of Prime Mover Display Voltage Alarms

wNode20VoltCount   : WORD;    // Total count of IO module Node 20 Module Voltage Alarm
wNode0VoltCount   : WORD;    // Total count of Engine Node 50 Voltage Alarm

	
END_VAR
