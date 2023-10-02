frappe.ui.form.on("Item",{
	onload : function(frm){
		if (frm.doc.__islocal){
			auto_populate_fields(frm)
		}
	},
});




function auto_populate_fields(frm){

	var childTableRows = cur_frm.doc.attributes || [];
	for (var i = 0; i < childTableRows.length; i++){
		var row = childTableRows[i];
		if (row.attribute == 'Height'){
				cur_frm.doc.height = row.attribute_value
		}
		if (row.attribute == 'Width'){
			cur_frm.doc.width = row.attribute_value
		}
		if (row.attribute == 'Yield'){
			cur_frm.doc.yield = row.attribute_value
		}
		frm.refresh_fields();
	}
}

