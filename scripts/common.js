window.onload = function() {
	document.getElementById("reset").onclick = resetSelect;
	
	var typesList = new Array(document.getElementsByName('nor')[0], 
		document.getElementsByName('fir')[0], 
		document.getElementsByName('wat')[0], 
		document.getElementsByName('ele')[0], 
		document.getElementsByName('gra')[0], 
		document.getElementsByName('ice')[0], 
		document.getElementsByName('fig')[0], 
		document.getElementsByName('poi')[0], 
		document.getElementsByName('gro')[0], 
		document.getElementsByName('fly')[0], 
		document.getElementsByName('psy')[0], 
		document.getElementsByName('bug')[0], 
		document.getElementsByName('roc')[0], 
		document.getElementsByName('gho')[0], 
		document.getElementsByName('dra')[0], 
		document.getElementsByName('dar')[0], 
		document.getElementsByName('ste')[0]);
	var compList = new Array(document.getElementsByName('norc')[0], 
		document.getElementsByName('firc')[0], 
		document.getElementsByName('watc')[0], 
		document.getElementsByName('elec')[0], 
		document.getElementsByName('grac')[0], 
		document.getElementsByName('icec')[0], 
		document.getElementsByName('figc')[0], 
		document.getElementsByName('poic')[0], 
		document.getElementsByName('groc')[0], 
		document.getElementsByName('flyc')[0], 
		document.getElementsByName('psyc')[0], 
		document.getElementsByName('bugc')[0], 
		document.getElementsByName('rocc')[0], 
		document.getElementsByName('ghoc')[0], 
		document.getElementsByName('drac')[0], 
		document.getElementsByName('darc')[0], 
		document.getElementsByName('stec')[0]);
	
	function resetSelect() {
		for (var i=0; i<17; i++) {
			typesList[i].selectedIndex = 0;
			compList[i].selectedIndex = 2;
		}
	}
}