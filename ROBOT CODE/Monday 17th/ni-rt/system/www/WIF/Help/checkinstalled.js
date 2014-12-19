/*************************************************************
*
*     Registers files as clients for dynamic content. To register a file as a dynamic content client, 
*		add the name of your CHM file to the alldynamicclients array on a new line, followed by a comma.
*		However, the last file in the list should NOT be followed by a comma.
*				  
*************************************************************/
var alldynamicclients = new Array(
	"addonlicensing",
	"criodevicehelp",
	"DataFinderTK",
	"daqmxio",
	"daqmxtutorial",
	"dspdesignblocks",
	"dspdesignhelp",
	"embserial",
	"embsharedvi",
	"expresswb",
	"glang",
	"gmath",
	"gswoict",
	"frc",
	"frcdialog",
	"ftc",
	"IMAQVision",
	"inlinecnode",
	"lvaft",
	"lvaftconcepts",
	"lvarmdialog",
	"lvarmhelp",
	"lvasptconcepts",
	"lvbioconcepts",
	"lvbiomed",
	"lvcdsimshrd",
	"lvcdtextmath",
	"lvcgenhelp",
	"lvconcepts",
	"lvctrldsgn",
	"lvdaqmx",
	"lvdatabase",
	"lvdettmerge",
	"lvdfdtconcepts",
	"lvdigfiltdestk",
	"lvdscconcepts",
	"lvdsc",
	"lvdschelp",
	"lvdscprop",
	"lvept",
	"lveptconcepts",
	"lvfbhelp",
	"lvfpga",
	"lvfpgacompile",
	"lvfpgaconcepts",
	"lvfpgadialog",
	"lvfpgahelp",
	"lvfpgahost",
	"lvfpgahosthelp",
	"lvfpgamain",
	"lvhyperdev",
	"lvhyperref",
	"lvioscan",
	"lvipbuilder",
	"lvipbuilderref",
	"lvjitterphtk",
	"lvmasmt",
	"lvmasmtref",
	"lvmve",
	"lvnxt",
	"lvoffice",
	"lvpdadialog",
	"lvpdagsm",
	"lvpid",
	"lvpidmain",
	"lvrgthelp",
	"lvrobodialog",
	"lvrobogsm",
	"lvroboprop",
	"lvrobovi",
	"lvrtbestpractices",
	"lvrtdialog",
	"lvrtconcepts",
	"lvrthowto",
	"lvrthelp",
	"lvrtvihelp",
	"lvsc",
	"lvscconcepts",
	"lvschowto",
	"lvsim",
	"lvsimconcepts",
	"lvsimemi",
	"lvsimesi",
	"lvsimhowto",
	"lvsimtkconcepts",
	"lvsitconcepts",
	"lvsysid",
	"lvsysidconcepts",
	"lvtextmath",
	"lvtextmathmain",
	"lvtimefreqtk",
	"lvtimeseriestk",
	"lvtpcdialog",
	"lvtpcgsm",
	"lvtrace",
	"lvtracehelp",
	"lvutfconcepts",
	"lvutf",
	"lvwavelettk",
	"lvwsnhelp",
	"lvvianalyzer",
	"lvxpe",
	"msureasstvi",
	"mxcncpts",
	"nimclvfb",
	"nisyscfg",	
	"oictref",
	"optsenmain",
	"optsenref",
	"p2pstreamhelp",
	"riohelprt",
	"robocrio",
	"robocriodialog",
	"rthyperhelp",
	"rtlinux",
	"sndvibtk",
	"sndvibasst",
	"svamain",
	"svmain",
	"target2devicehelp",
	"veristand",
	"veristandmerge",
	"veristandsdapi",
	"vsexecapi",
	"vsmithelp",
	"vsmitref"
	);

//Registers files as clients for single-sourced dynamic content
//(typically, this content is sourced in XML and displayed in database-generated topics)
var ss_dynamic_clients = new Array ("lvrthelp","lvfpga","lvpdagsm","lvtpcgsm","lvipbuilderref");

for (i = 0; i < alldynamicclients.length; i++) {
	var client = alldynamicclients[i];
	var chm_js = "ms-its:" + client + ".chm::/" + client + ".js";
	include_js(chm_js);
}


